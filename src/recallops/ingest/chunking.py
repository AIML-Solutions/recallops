from __future__ import annotations

from recallops.ids import stable_id
from recallops.models import Chunk, Metadata


def chunk_text(
    text: str,
    *,
    document_id: str,
    chunk_size: int,
    chunk_overlap: int,
    metadata: Metadata | None = None,
) -> list[Chunk]:
    """Split text into deterministic overlapping character chunks.

    Character chunking is intentionally simple and predictable for the reference
    service. Production deployments can replace this with tokenizer-aware or
    structure-aware chunkers without changing the retrieval API.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must be non-negative")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    normalized = text.strip()
    if not normalized:
        return []

    chunks: list[Chunk] = []
    start = 0
    ordinal = 0
    step = chunk_size - chunk_overlap
    base_metadata = metadata or {}

    while start < len(normalized):
        end = min(start + chunk_size, len(normalized))
        chunk_body = normalized[start:end]
        chunk_id = stable_id("chunk", document_id, ordinal, chunk_body)
        chunks.append(
            Chunk(
                chunk_id=chunk_id,
                document_id=document_id,
                text=chunk_body,
                ordinal=ordinal,
                metadata={**base_metadata, "chunk_ordinal": ordinal},
            )
        )
        if end == len(normalized):
            break
        start += step
        ordinal += 1

    return chunks
