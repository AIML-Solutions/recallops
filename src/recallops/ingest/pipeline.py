from __future__ import annotations

import argparse

from recallops.config import get_settings
from recallops.models import IngestLocalRequest
from recallops.service import RecallOpsService


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest local documents into RecallOps.")
    parser.add_argument("--input", required=True, help="File or directory to ingest")
    parser.add_argument("--collection", default="research_ops")
    parser.add_argument("--chunk-size", type=int, default=None)
    parser.add_argument("--chunk-overlap", type=int, default=None)
    args = parser.parse_args()

    service = RecallOpsService(get_settings())
    response = service.ingest_local(
        IngestLocalRequest(
            path=args.input,
            collection=args.collection,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap,
            metadata={"source_type": "local_file"},
        )
    )
    print(response.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
