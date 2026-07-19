import pytest

from recallops.search.filters import metadata_matches, to_qdrant_filter


def test_metadata_exact_and_tag_filters() -> None:
    metadata = {"source_type": "docs", "tags": ["rag", "retrieval"]}

    assert metadata_matches(metadata, {"source_type": "docs", "tags": ["rag"]})
    assert not metadata_matches(metadata, {"tags": ["mlflow"]})


def test_nested_numeric_filters() -> None:
    metadata = {"metrics": {"recall_at_5": 0.84}}

    assert metadata_matches(metadata, {"metrics.recall_at_5": {"gte": 0.8}})
    assert not metadata_matches(metadata, {"metrics.recall_at_5": {"lt": 0.8}})


def test_unsupported_operator_is_rejected() -> None:
    with pytest.raises(ValueError, match="unsupported filter operator"):
        metadata_matches({"score": 1}, {"score": {"between": [0, 2]}})


def test_qdrant_filter_shape() -> None:
    qdrant_filter = to_qdrant_filter(
        {"doc_type": "experiment_run", "metrics.recall_at_5": {"gte": 0.8}, "tags": ["rag"]}
    )

    assert qdrant_filter == {
        "must": [
            {"key": "doc_type", "match": {"value": "experiment_run"}},
            {"key": "metrics.recall_at_5", "range": {"gte": 0.8}},
            {"key": "tags", "match": {"value": "rag"}},
        ]
    }
