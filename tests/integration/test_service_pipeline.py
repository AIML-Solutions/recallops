from pathlib import Path

from recallops.config import Settings
from recallops.models import IngestLocalRequest, SearchRequest
from recallops.service import RecallOpsService


def test_service_pipeline_indexes_and_filters(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "mlflow.md").write_text(
        "MLflow metrics and parameters support experiment discovery for RAG pipelines.",
        encoding="utf-8",
    )
    service = RecallOpsService(Settings())

    ingest = service.ingest_local(
        IngestLocalRequest(
            path=str(docs),
            collection="integration",
            metadata={"source_type": "docs", "doc_type": "experiment_note", "tags": ["mlflow"]},
        )
    )
    search = service.search(
        SearchRequest(
            query="experiment metrics",
            collection="integration",
            filters={"doc_type": "experiment_note", "tags": ["mlflow"]},
        )
    )

    assert ingest.status == "indexed"
    assert search.results
    assert search.results[0].metadata["doc_type"] == "experiment_note"
