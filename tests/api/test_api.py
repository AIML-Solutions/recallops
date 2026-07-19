from pathlib import Path

from fastapi.testclient import TestClient

from recallops.api.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["service"] == "recallops"


def test_ingest_search_and_stats(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "architecture.md").write_text(
        "Metadata filters improve retrieval by reducing noisy vector candidates.",
        encoding="utf-8",
    )

    ingest = client.post(
        "/ingest/local",
        json={
            "path": str(docs),
            "collection": "api_test",
            "metadata": {"source_type": "docs", "tags": ["retrieval"]},
            "chunk_size": 80,
            "chunk_overlap": 10,
        },
    )
    assert ingest.status_code == 200
    assert ingest.json()["chunks"] == 1

    search = client.post(
        "/search",
        json={
            "query": "metadata retrieval",
            "collection": "api_test",
            "top_k": 3,
            "filters": {"tags": ["retrieval"]},
        },
    )
    assert search.status_code == 200
    assert search.json()["results"][0]["metadata"]["source"] == "architecture.md"

    stats = client.get("/collections/api_test/stats")
    assert stats.status_code == 200
    assert stats.json()["documents"] == 1
    assert stats.json()["chunks"] == 1


def test_search_rejects_empty_query() -> None:
    response = client.post("/search", json={"query": "", "collection": "api_test"})

    assert response.status_code == 422
