from __future__ import annotations

from recallops.config import Settings
from recallops.embeddings.model import Embedder, HashingEmbedder
from recallops.ingest.chunking import chunk_text
from recallops.ingest.loaders import load_local_documents
from recallops.models import (
    CollectionStats,
    IngestLocalRequest,
    IngestResponse,
    SearchRequest,
    SearchResponse,
)
from recallops.search.memory import InMemoryIndex


class RecallOpsService:
    def __init__(self, settings: Settings, embedder: Embedder | None = None) -> None:
        self.settings = settings
        self.embedder = embedder or HashingEmbedder(settings.vector_size)
        self.index = InMemoryIndex()

    def ingest_local(self, request: IngestLocalRequest) -> IngestResponse:
        chunk_size = request.chunk_size or self.settings.chunk_size
        chunk_overlap = request.chunk_overlap or self.settings.chunk_overlap
        documents = load_local_documents(request.path, request.metadata)
        chunks = [
            chunk
            for document in documents
            for chunk in chunk_text(
                document.text,
                document_id=document.document_id,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                metadata=document.metadata,
            )
        ]
        if chunks:
            vectors = self.embedder.embed_texts(chunk.text for chunk in chunks)
            self.index.upsert(request.collection, chunks, vectors)
        return IngestResponse(
            collection=request.collection,
            documents=len(documents),
            chunks=len(chunks),
            status="indexed" if chunks else "empty",
        )

    def search(self, request: SearchRequest) -> SearchResponse:
        vector = self.embedder.embed_query(request.query)
        results = self.index.search(
            request.collection,
            vector,
            top_k=request.top_k,
            filters=request.filters,
        )
        return SearchResponse(query=request.query, collection=request.collection, results=results)

    def stats(self, collection: str) -> CollectionStats:
        documents, chunks = self.index.stats(collection)
        return CollectionStats(collection=collection, documents=documents, chunks=chunks)
