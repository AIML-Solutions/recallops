from __future__ import annotations

from recallops.models import SearchResult


def build_context(results: list[SearchResult], *, max_chars: int = 6000) -> str:
    parts: list[str] = []
    total = 0
    for result in results:
        source = result.metadata.get("source", result.document_id)
        block = f"Source: {source}\nScore: {result.score:.3f}\n{result.text.strip()}"
        if total + len(block) > max_chars:
            break
        parts.append(block)
        total += len(block)
    return "\n\n---\n\n".join(parts)
