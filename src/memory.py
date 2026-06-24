"""
Gerencia o histórico de conversa por número de telefone.

Usa um dicionário em memória para desenvolvimento.
Em produção com múltiplos workers, substitua por Redis:

    import redis
    _redis = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)

O histórico é limitado a MAX_HISTORY_MESSAGES para não estourar
o contexto do LLM e reduzir custos de tokens.
"""
import json
import logging
import time
from dataclasses import dataclass, field
from typing import Any

import config

logger = logging.getLogger(__name__)


@dataclass
class Session:
    """Representa uma sessão de conversa com um paciente."""
    phone: str
    messages: list[dict] = field(default_factory=list)
    last_activity: float = field(default_factory=time.time)


# Armazenamento em memória: { "5511999999999": Session }
# Para produção: substitua por Redis com TTL automático
_sessions: dict[str, Session] = {}


def _is_expired(session: Session) -> bool:
    """Verifica se a sessão expirou por inatividade."""
    return (time.time() - session.last_activity) > config.REDIS_SESSION_TTL


def get_history(phone: str) -> list[dict]:
    """
    Retorna o histórico de mensagens de um número.

    Args:
        phone: Número do paciente.

    Returns:
        Lista de mensagens no formato [{role, content}, ...]
        Retorna lista vazia se não houver histórico ou se expirou.
    """
    session = _sessions.get(phone)

    if session is None:
        return []

    if _is_expired(session):
        logger.debug("Sessão expirada para %s. Limpando.", phone[-4:])
        del _sessions[phone]
        return []

    return session.messages.copy()


def add_message(phone: str, role: str, content: str) -> None:
    """
    Adiciona uma mensagem ao histórico.

    Mantém apenas as últimas MAX_HISTORY_MESSAGES mensagens
    para controlar o tamanho do contexto enviado ao LLM.

    Args:
        phone: Número do paciente.
        role: "user" ou "assistant".
        content: Texto da mensagem.
    """
    if phone not in _sessions:
        _sessions[phone] = Session(phone=phone)

    session = _sessions[phone]
    session.messages.append({"role": role, "content": content})
    session.last_activity = time.time()

    # Mantém apenas as últimas N mensagens
    # Preserva pares (user + assistant) para manter coerência
    if len(session.messages) > config.MAX_HISTORY_MESSAGES:
        # Remove as mais antigas, mas sempre em pares
        excess = len(session.messages) - config.MAX_HISTORY_MESSAGES
        session.messages = session.messages[excess:]


def clear_session(phone: str) -> None:
    """Remove o histórico de um número (ex: quando paciente digita 'sair')."""
    _sessions.pop(phone, None)


def get_session_count() -> int:
    """Retorna o número de sessões ativas (útil para monitoramento)."""
    # Limpa sessões expiradas ao contar
    expired = [p for p, s in _sessions.items() if _is_expired(s)]
    for phone in expired:
        del _sessions[phone]
    return len(_sessions)