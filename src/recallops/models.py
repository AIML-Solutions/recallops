from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

Metadata = dict[str, Any]


class Document(BaseModel):
    document_id: str
    text: str
    metadata: Metadata = Field(default_factory=dict)


class Chunk(BaseModel):
    chunk_id: str
    document_id: str
    text: str
    ordinal: int
    metadata: Metadata = Field(default_factory=dict)


class IngestLocalRequest(BaseModel):
    path: str
    collection: str = "research_ops"
    metadata: Metadata = Field(default_factory=dict)
    chunk_size: int | None = None
    chunk_overlap: int | None = None


class IngestResponse(BaseModel):
    collection: str
    documents: int
    chunks: int
    status: Literal["indexed", "empty"]


class SearchRequest(BaseModel):
    query: str
    collection: str = "research_ops"
    top_k: int = Field(default=5, ge=1, le=100)
    filters: Metadata = Field(default_factory=dict)

    @field_validator("query")
    @classmethod
    def query_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("query must not be empty")
        return value


class SearchResult(BaseModel):
    chunk_id: str
    document_id: str
    score: float
    text: str
    metadata: Metadata = Field(default_factory=dict)


class SearchResponse(BaseModel):
    query: str
    collection: str
    results: list[SearchResult]


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    service: str = "recallops"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class CollectionStats(BaseModel):
    collection: str
    documents: int
    chunks: int
