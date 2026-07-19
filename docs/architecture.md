# Architecture

RecallOps is organized around a simple premise: semantic similarity is useful, but operational retrieval needs metadata.

The verified local reference implementation uses an in-memory vector index so the ingestion, filtering, ranking, API, and evaluation paths can be tested without external services.

For durable deployments, the service boundaries target two stores:

- **Postgres** for durable document, chunk, source, and ingestion metadata.
- **Qdrant** for approximate nearest neighbor search over embedding vectors.

The service boundaries are designed so persistence adapters can be added without changing the API contract.

## Flow

```text
Documents -> Loader -> Chunker -> Embedder -> Metadata Store + Vector Index -> Search API
```

## Design Decisions

- Deterministic identifiers make ingestion repeatable.
- Metadata is attached to every chunk, not only the parent document.
- Filters are explicit query parameters, not prompt-only instructions.
- Retrieval metrics are part of the project, not an external notebook.
- Network-backed connectors are opt-in for tests and automation.
