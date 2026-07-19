from __future__ import annotations

import math

from recallops.models import Chunk, SearchResult
from recallops.search.filters import metadata_matches


class InMemoryIndex:
    def __init__(self) -> None:
        self._collections: dict[str, list[tuple[Chunk, list[float]]]] = {}

    def upsert(self, collection: str, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        existing = {
            chunk.chunk_id: (chunk, vector)
            for chunk, vector in self._collections.get(collection, [])
        }
        for chunk, vector in zip(chunks, vectors, strict=True):
            existing[chunk.chunk_id] = (chunk, vector)
        self._collections[collection] = list(existing.values())

    def search(
        self,
        collection: str,
        query_vector: list[float],
        *,
        top_k: int,
        filters: dict[str, object] | None = None,
    ) -> list[SearchResult]:
        candidates = self._collections.get(collection, [])
        results: list[SearchResult] = []
        for chunk, vector in candidates:
            if filters and not metadata_matches(chunk.metadata, filters):
                continue
            score = _cosine(query_vector, vector)
            results.append(
                SearchResult(
                    chunk_id=chunk.chunk_id,
                    document_id=chunk.document_id,
                    score=score,
                    text=chunk.text,
                    metadata=chunk.metadata,
                )
            )
        results.sort(key=lambda item: item.score, reverse=True)
        return results[:top_k]

    def stats(self, collection: str) -> tuple[int, int]:
        rows = self._collections.get(collection, [])
        documents = {chunk.document_id for chunk, _ in rows}
        return len(documents), len(rows)


def _cosine(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right, strict=False))
    left_norm = math.sqrt(sum(a * a for a in left)) or 1.0
    right_norm = math.sqrt(sum(b * b for b in right)) or 1.0
    return dot / (left_norm * right_norm)
