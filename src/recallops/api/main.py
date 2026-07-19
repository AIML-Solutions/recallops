from __future__ import annotations

import uvicorn
from fastapi import FastAPI

from recallops.config import get_settings
from recallops.models import (
    CollectionStats,
    HealthResponse,
    IngestLocalRequest,
    IngestResponse,
    SearchRequest,
    SearchResponse,
)
from recallops.service import RecallOpsService

settings = get_settings()
service = RecallOpsService(settings)

app = FastAPI(
    title="RecallOps",
    description="Metadata-aware ANN retrieval service for ML research and RAG workflows.",
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()


@app.post("/ingest/local", response_model=IngestResponse)
def ingest_local(request: IngestLocalRequest) -> IngestResponse:
    return service.ingest_local(request)


@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest) -> SearchResponse:
    return service.search(request)


@app.get("/collections/{collection}/stats", response_model=CollectionStats)
def collection_stats(collection: str) -> CollectionStats:
    return service.stats(collection)


def main() -> None:
    uvicorn.run("recallops.api.main:app", host=settings.api_host, port=settings.api_port)


if __name__ == "__main__":
    main()
