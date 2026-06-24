"""
Busca semântica na base de conhecimento da Clínica Vida+.
"""
import logging

from openai import OpenAI
from qdrant_client import QdrantClient

import config

logger = logging.getLogger(__name__)

_openai = OpenAI(api_key=config.OPENAI_API_KEY)
_qdrant = QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)


def retrieve(query: str, category: str | None = None) -> list[dict]:
    """
    Busca chunks relevantes para a query.

    Args:
        query: Pergunta do paciente (já sanitizada).
        category: Filtro opcional por categoria
                  (ex: "agendamento", "convenios", "exames")

    Returns:
        Lista de chunks com text, title, category e score.
    """
    response = _openai.embeddings.create(
        model=config.EMBEDDING_MODEL,
        input=query,
    )
    query_vector = response.data[0].embedding

    # Filtro opcional por categoria
    search_filter = None
    if category:
        search_filter = {
            "must": [{"key": "category", "match": {"value": category}}]
        }

    results = _qdrant.search(
        collection_name=config.QDRANT_COLLECTION,
        query_vector=query_vector,
        limit=config.RETRIEVAL_TOP_K,
        with_payload=True,
        score_threshold=config.MIN_SCORE_THRESHOLD,
        query_filter=search_filter,
    )

    chunks = [
        {
            "text": hit.payload["text"],
            "title": hit.payload.get("title", ""),
            "category": hit.payload.get("category", ""),
            "score": round(hit.score, 4),
        }
        for hit in results
    ]

    logger.debug(
        "%d chunks para '%s...' | scores: %s",
        len(chunks),
        query[:40],
        [c["score"] for c in chunks],
    )

    return chunks