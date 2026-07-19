from recallops.models import SearchResult
from recallops.rag.context import build_context


def test_build_context_includes_sources_and_scores() -> None:
    context = build_context(
        [
            SearchResult(
                chunk_id="chunk_1",
                document_id="doc_1",
                score=0.9,
                text="Metadata matters.",
                metadata={"source": "architecture.md"},
            )
        ]
    )

    assert "architecture.md" in context
    assert "0.900" in context
    assert "Metadata matters." in context
