import pytest

from recallops.ingest.chunking import chunk_text


def test_chunk_overlap_preserves_context() -> None:
    text = "abcdefghijklmnopqrstuvwxyz" * 4
    chunks = chunk_text(text, document_id="doc_1", chunk_size=40, chunk_overlap=10)

    assert len(chunks) > 1
    assert chunks[0].text[-10:] == chunks[1].text[:10]
    assert chunks[0].metadata["chunk_ordinal"] == 0


def test_empty_text_returns_no_chunks() -> None:
    assert chunk_text("  ", document_id="doc_1", chunk_size=10, chunk_overlap=2) == []


def test_invalid_overlap_is_rejected() -> None:
    with pytest.raises(ValueError, match="smaller than chunk_size"):
        chunk_text("hello", document_id="doc_1", chunk_size=10, chunk_overlap=10)
