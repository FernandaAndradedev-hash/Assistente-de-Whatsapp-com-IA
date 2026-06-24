"""
Camada de segurança para o atendente de WhatsApp.

Proteções:
1. Sanitização de mensagens (HTML, injection, tamanho)
2. Rate limiting por número de telefone (via Redis)
3. Verificação de assinatura HMAC do webhook
4. Validação do payload do webhook
"""
import hashlib
import hmac
import logging
import re
import time

import bleach

import config

logger = logging.getLogger(__name__)


# Padrões de Prompt Injection ─────────────────────────────────────────────────

_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions?",
    r"disregard\s+(all\s+)?(previous|prior)\s+instructions?",
    r"forget\s+(everything|all|your)",
    r"you\s+are\s+now\s+(a|an)\s+\w+",
    r"act\s+as\s+(if\s+you\s+are|a|an)\s+",
    r"pretend\s+(you\s+are|to\s+be)\s+",
    r"new\s+(system\s+)?instructions?\s*:",
    r"system\s+prompt\s*:",
    r"\[INST\]",
    r"\[SYSTEM\]",
    r"###\s*instruction",
    r"jailbreak",
    r"do\s+anything\s+now",
    r"developer\s+mode",
    r"(show|reveal|print)\s+(your\s+)?(system\s+prompt|instructions?)",
]

_INJECTION_RE = re.compile(
    "|".join(_INJECTION_PATTERNS),
    re.IGNORECASE | re.DOTALL,
)


# ─────────────────────────────────────────────────────────────────────────────
# Rate Limiting (sem Redis — usando dict em memória)
# Para produção com múltiplos workers, use Redis como backend.
# ─────────────────────────────────────────────────────────────────────────────

# Estrutura: { "5511999999999": [timestamp1, timestamp2, ...] }
_rate_limit_store: dict[str, list[float]] = {}


def check_rate_limit(phone_number: str) -> bool:
    """
    Verifica se o número excedeu o limite de mensagens.

    Algoritmo: sliding window
    - Mantém timestamps das últimas mensagens
    - Remove timestamps fora da janela de tempo
    - Verifica se o count está abaixo do limite

    Args:
        phone_number: Número do remetente (ex: "5511999999999")

    Returns:
        True se dentro do limite, False se excedeu.
    """
    now = time.time()
    window = config.RATE_LIMIT_WINDOW_SECONDS
    max_msgs = config.RATE_LIMIT_MAX_MESSAGES

    # Inicializa se primeira mensagem do número
    if phone_number not in _rate_limit_store:
        _rate_limit_store[phone_number] = []

    # Remove timestamps fora da janela deslizante
    _rate_limit_store[phone_number] = [
        ts for ts in _rate_limit_store[phone_number]
        if now - ts < window
    ]

    # Verifica limite
    if len(_rate_limit_store[phone_number]) >= max_msgs:
        logger.warning(
            "Rate limit excedido | número: %s | msgs na janela: %d",
            phone_number[-4:],  # log apenas últimos 4 dígitos por privacidade
            len(_rate_limit_store[phone_number]),
        )
        return False

    # Registra nova mensagem
    _rate_limit_store[phone_number].append(now)
    return True


# Sanitização de Mensagens ────────────────────────────────────────────────────

def sanitize_message(text: str) -> str:
    """
    Sanitiza mensagem recebida do WhatsApp.

    Etapas:
    1. Verifica tipo
    2. Remove HTML
    3. Normaliza espaços
    4. Verifica tamanho
    5. Detecta prompt injection

    Args:
        text: Texto da mensagem recebida.

    Returns:
        Texto sanitizado.

    Raises:
        ValueError: Se mensagem for inválida ou suspeita.
    """
    if not isinstance(text, str):
        raise ValueError("Mensagem deve ser texto.")

    # Remove HTML — WhatsApp pode enviar texto formatado
    clean = bleach.clean(text, tags=[], strip=True)

    # Normaliza espaços
    clean = re.sub(r"\s+", " ", clean).strip()

    if not clean:
        raise ValueError("Mensagem vazia.")

    if len(clean) > config.MAX_MESSAGE_LENGTH:
        raise ValueError(
            f"Mensagem muito longa ({len(clean)} chars). "
            f"Máximo: {config.MAX_MESSAGE_LENGTH} caracteres."
        )

    # Detecta prompt injection
    match = _INJECTION_RE.search(clean)
    if match:
        logger.warning(
            "Prompt injection detectado | padrão: %r | número caracteres: %d",
            match.group()[:30],
            len(clean),
        )
        raise ValueError("Mensagem com conteúdo inválido.")

    return clean


# Verificação HMAC do Webhook ─────────────────────────────────────────────────

def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """
    Verifica se o webhook veio realmente da Evolution API.

    Se o secret não estiver configurado, a verificação é pulada
    (útil para desenvolvimento local).

    Args:
        payload: Body bruto da requisição (bytes).
        signature: Header 'x-webhook-signature' da requisição.

    Returns:
        True se assinatura válida ou se secret não configurado.
    """
    if not config.WEBHOOK_SECRET:
        # Em desenvolvimento, sem secret configurado, aceita tudo
        logger.debug("WEBHOOK_SECRET não configurado — verificação HMAC desabilitada.")
        return True

    expected = hmac.new(
        config.WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()

    # compare_digest previne timing attacks
    return hmac.compare_digest(expected, signature)


# Validação do Payload do Webhook ─────────────────────────────────────────────

def extract_message_from_webhook(payload: dict) -> dict | None:
    """
    Extrai os dados relevantes do payload da Evolution API.

    O payload da Evolution tem uma estrutura específica.
    Esta função normaliza para o formato que o restante do sistema usa.

    Args:
        payload: Payload JSON do webhook.

    Returns:
        Dict com {phone, message, instance} ou None se não for mensagem de texto.
    """
    try:
        event = payload.get("event", "")

        # Só processa eventos de mensagem recebida
        if event != "messages.upsert":
            return None

        data = payload.get("data", {})
        key = data.get("key", {})
        message = data.get("message", {})

        # Ignora mensagens enviadas pelo próprio bot
        if key.get("fromMe", False):
            return None

        # Extrai número do remetente
        remote_jid = key.get("remoteJid", "")
        phone = remote_jid.replace("@s.whatsapp.net", "").replace("@g.us", "")

        if not phone:
            return None

        # Extrai texto da mensagem
        # WhatsApp tem vários tipos de mensagem — só processamos texto
        text = (
            message.get("conversation")                          # mensagem simples
            or message.get("extendedTextMessage", {}).get("text")  # mensagem com preview de link
        )

        if not text:
            # Mensagem de áudio, imagem, sticker, etc. — ignora por enquanto
            logger.debug("Mensagem não-texto recebida de %s. Ignorando.", phone[-4:])
            return None

        return {
            "phone": phone,
            "message": text,
            "instance": payload.get("instance", ""),
        }

    except (KeyError, AttributeError, TypeError) as exc:
        logger.error("Erro ao extrair mensagem do webhook: %s", exc)
        return None


def validate_response_safety(response: str) -> str:
    """
    Verifica se a resposta do LLM não vaza informações do sistema.
    """
    leak_patterns = [
        r"system\s+prompt",
        r"minhas\s+instru[cç][oõ]es",
        r"fui\s+instru[ií]do",
        r"NUNCA\s+revele",
    ]
    for pattern in leak_patterns:
        if re.search(pattern, response, re.IGNORECASE):
            logger.warning("Possível vazamento de system prompt na resposta.")
            return (
                "Desculpe, não consegui processar sua mensagem. "
                "Por favor, tente novamente."
            )
    return response