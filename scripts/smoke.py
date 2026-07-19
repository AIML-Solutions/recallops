from __future__ import annotations

from pathlib import Path

from recallops.config import get_settings
from recallops.models import IngestLocalRequest, SearchRequest
from recallops.service import RecallOpsService


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    service = RecallOpsService(get_settings())
    ingest = service.ingest_local(
        IngestLocalRequest(
            path=str(root / "examples" / "documents"),
            collection="smoke",
            metadata={"source_type": "docs", "tags": ["smoke", "retrieval"]},
            chunk_size=500,
            chunk_overlap=80,
        )
    )
    search = service.search(
        SearchRequest(
            query="How does metadata improve retrieval?",
            collection="smoke",
            top_k=3,
            filters={"source_type": "docs"},
        )
    )
    if ingest.chunks <= 0:
        raise SystemExit("smoke failed: no chunks indexed")
    if not search.results:
        raise SystemExit("smoke failed: search returned no results")
    print("RecallOps smoke test passed")
    print(f"- documents ingested: {ingest.documents}")
    print(f"- chunks indexed: {ingest.chunks}")
    print(f"- search results: {len(search.results)}")
    print(f"- top source: {search.results[0].metadata.get('source')}")


if __name__ == "__main__":
    main()
