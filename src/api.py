"""
Webhook que recebe mensagens da Evolution API e retorna respostas.

Fluxo:
  Evolution API → POST /webhook → validações → agent → resposta → Evolution API
"""
import logging
import sys

import httpx
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware

import config
from agent import process_message
from validators import (
    check_rate_limit,
    extract_message_from_webhook,
    sanitize_message,
    verify_webhook_signature,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Clínica Vida+ — Atendente WhatsApp",
    description="Webhook para atendimento automático via WhatsApp.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


# Envio de mensagem via Evolution API ─────────────────────────────────────────

async def send_whatsapp_message(phone: str, message: str) -> bool:
    """
    Envia uma mensagem via Evolution API.

    Args:
        phone: Número do destinatário (formato: 5511999999999)
        message: Texto a enviar

    Returns:
        True se enviou com sucesso, False caso contrário.
    """
    url = (
        f"{config.EVOLUTION_API_URL}/message/sendText/"
        f"{config.EVOLUTION_INSTANCE}"
    )
    headers = {
        "apikey": config.EVOLUTION_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "number": phone,
        "text": message,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return True
    except httpx.HTTPStatusError as exc:
        logger.error(
            "Erro ao enviar mensagem para %s: %s",
            phone[-4:],
            exc.response.text,
        )
        return False
    except httpx.RequestError as exc:
        logger.error("Erro de conexão com Evolution API: %s", exc)
        return False


# Endpoints ───────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    """Health check."""
    return {"status": "ok", "service": "Clínica Vida+ WhatsApp Bot"}


@app.post("/webhook", status_code=status.HTTP_200_OK)
async def webhook(request: Request):
    """
    Recebe eventos da Evolution API.

    A Evolution API envia um POST para este endpoint a cada mensagem recebida.
    Respondemos 200 imediatamente e processamos de forma assíncrona.
    """
    # Lê o body bruto para verificação HMAC
    raw_body = await request.body()

    # Verificação de assinatura (desativada se WEBHOOK_SECRET não configurado)
    signature = request.headers.get("x-webhook-signature", "")
    if not verify_webhook_signature(raw_body, signature):
        logger.warning("Webhook com assinatura inválida recebido.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Assinatura inválida.",
        )

    # Parse do JSON
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payload inválido.",
        )

    # Extrai dados da mensagem
    message_data = extract_message_from_webhook(payload)

    if message_data is None:
        # Evento não é mensagem de texto — ignora silenciosamente
        return {"status": "ignored"}

    phone = message_data["phone"]
    raw_message = message_data["message"]

    logger.info("Mensagem recebida de %s (len: %d)", phone[-4:], len(raw_message))

    # Rate limiting
    if not check_rate_limit(phone):
        await send_whatsapp_message(
            phone,
            "Você enviou muitas mensagens em pouco tempo. "
            "Por favor, aguarde um momento antes de continuar. 🙏",
        )
        return {"status": "rate_limited"}

    # Sanitização
    try:
        clean_message = sanitize_message(raw_message)
    except ValueError as exc:
        logger.info("Mensagem inválida de %s: %s", phone[-4:], exc)
        await send_whatsapp_message(
            phone,
            "Não consegui entender sua mensagem. "
            "Por favor, tente novamente com texto simples.",
        )
        return {"status": "invalid_message"}

    # Processa e responde
    try:
        response = process_message(phone, clean_message)
        await send_whatsapp_message(phone, response)
        return {"status": "ok"}

    except Exception as exc:
        logger.error(
            "Erro ao processar mensagem de %s: %s",
            phone[-4:],
            exc,
            exc_info=True,
        )
        await send_whatsapp_message(
            phone,
            "Desculpe, tive um problema técnico. "
            "Por favor, tente novamente em instantes ou ligue: (11) 3456-7890",
        )
        return {"status": "error"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)