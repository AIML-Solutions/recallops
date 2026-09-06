# RecallOps

**Retrieve the right context before it costs you time.**

RecallOps is an open-stack reference service for aggregating, indexing, and retrieving technical knowledge with metadata-aware vector search.

It is designed for ML and RAG workflows where teams need to search across research papers, experiment metadata, model notes, evaluation reports, and technical documentation without losing the metadata that makes results useful.

## Why RecallOps

RAG systems fail when retrieval loses operational context. A vector hit is not enough; teams also need source, date, model, dataset, experiment, metric, tag, provenance, and access-boundary metadata. RecallOps keeps that metadata attached to every chunk and makes it usable at query time.

```text
Sources -> Ingestion -> Summarization -> Metadata Store -> ANN Index -> Retrieval API -> RAG Context
```

## What It Includes

- Metadata-aware vector search with an in-memory reference index
- Docker Compose scaffolding for Postgres and Qdrant-backed deployments
- FastAPI service for health, ingestion, search, and collection stats
- Deterministic chunk/document identifiers for repeatable ingestion
- Local document ingestion for Markdown and text files
- arXiv ingestion interface for research snapshots
- MLflow indexing interface for experiment discovery
- RAG context builder for downstream applications
- Retrieval evaluation with Recall@k and MRR
- Docker Compose local stack
- Unit, API, integration, evaluation, and smoke-test flows

## Architecture

```text
                 +-------------------+
                 |  Local Docs       |
                 |  arXiv Papers     |
                 |  MLflow Runs      |
                 |  Model Cards      |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 |  Ingestion        |
                 |  chunk + normalize|
                 +---------+---------+
                           |
              +------------+-------------+
              |                          |
              v                          v
      +---------------+          +----------------+
      | Metadata      |          | Vector Index   |
      | records       |          | embeddings     |
      +-------+-------+          +--------+-------+
              |                           |
              +------------+--------------+
                           |
                           v
                 +-------------------+
                 | FastAPI Retrieval |
                 | filters + context |
                 +-------------------+
```

The verified local reference path uses an in-memory index so ingestion, filtering, ranking, API behavior, and evaluation can be tested without external services. The Docker Compose stack includes Postgres and Qdrant as deployment targets for durable metadata and ANN indexing adapters.

## Quick Start

```bash
git clone https://github.com/AIML-Solutions/recallops.git
cd recallops
cp .env.example .env
docker compose up --build
```

The API starts on:

```text
http://localhost:8000
```

Check health:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "recallops"
}
```

## Ingest Example Documents

```bash
python -m recallops.ingest.pipeline \
  --input examples/documents \
  --collection research_ops \
  --chunk-size 700 \
  --chunk-overlap 120
```

Or use the API:

```bash
curl -X POST http://localhost:8000/ingest/local \
  -H "Content-Type: application/json" \
  -d '{
    "path": "examples/documents",
    "collection": "research_ops",
    "metadata": {
      "source_type": "docs",
      "project": "retrieval-reference",
      "tags": ["rag", "metadata", "ann"]
    }
  }'
```

## Search With Metadata Filters

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How do metadata filters improve RAG retrieval?",
    "collection": "research_ops",
    "top_k": 5,
    "filters": {
      "source_type": "docs",
      "tags": ["retrieval", "architecture"]
    }
  }'
```

Example response:

```json
{
  "query": "How do metadata filters improve RAG retrieval?",
  "collection": "research_ops",
  "results": [
    {
      "chunk_id": "chunk_c3d0a5...",
      "document_id": "doc_f5d1b8...",
      "score": 0.84,
      "text": "Metadata filters reduce retrieval noise by constraining vector search...",
      "metadata": {
        "source": "architecture.md",
        "source_type": "docs",
        "tags": ["retrieval", "architecture"]
      }
    }
  ]
}
```

## ML Experiment Search

RecallOps can index MLflow experiment metadata so retrieval can answer questions about prior model runs, evaluation scores, datasets, parameters, and artifacts.

```bash
python -m recallops.ingest.mlflow \
  --tracking-uri ./mlruns \
  --collection research_ops
```

Search experiment metadata:

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "retrieval experiments that used reranking",
    "collection": "research_ops",
    "top_k": 10,
    "filters": {
      "doc_type": "experiment_run",
      "tags": ["rag", "reranking"],
      "metrics.recall_at_5": { "gte": 0.8 }
    }
  }'
```

## arXiv Research Snapshots

Use the arXiv connector to create a searchable research snapshot for retrieval, RAG, ANN indexing, model evaluation, or related ML topics.

```bash
python -m recallops.ingest.arxiv \
  --query 'cat:cs.IR AND (RAG OR retrieval OR embeddings OR reranking)' \
  --max-results 25 \
  --collection research_ops
```

Network-backed ingestion is intentionally opt-in for tests and automation.

## Configuration

Key settings are environment-driven:

| Variable | Default | Purpose |
| --- | --- | --- |
| `RECALLOPS_API_HOST` | `0.0.0.0` | FastAPI bind host |
| `RECALLOPS_API_PORT` | `8000` | FastAPI port |
| `POSTGRES_DSN` | `postgresql://recallops:recallops@postgres:5432/recallops` | Metadata store |
| `QDRANT_URL` | `http://qdrant:6333` | Vector index service |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Embedding model |
| `VECTOR_SIZE` | `384` | Embedding vector size |
| `DEFAULT_COLLECTION` | `research_ops` | Default retrieval collection |
| `CHUNK_SIZE` | `700` | Default chunk size |
| `CHUNK_OVERLAP` | `120` | Default chunk overlap |
| `SEARCH_TOP_K` | `5` | Default result count |
| `SEARCH_EF` | `64` | ANN search ef parameter for Qdrant-backed deployments |

## Testing

RecallOps treats retrieval quality as a testable system property: filters, ingestion, ranking, and evaluation are covered by automated tests rather than left as manual notebook checks.

Run the full local suite:

```bash
make test
```

Run focused suites:

```bash
make test-unit
make test-api
make test-eval
```

Run integration tests against Docker Compose services:

```bash
make compose-up
make test-integration
```

Run the end-to-end smoke test:

```bash
make smoke
```

Network-dependent tests are opt-in:

```bash
ENABLE_NETWORK_TESTS=1 make test-network
```

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
make lint
make test
```

## Design Principles

- Keep source metadata attached to every chunk.
- Treat the vector index as a retrieval index, not the source of truth.
- Make retrieval behavior measurable.
- Keep connectors optional and testable with fixtures.
- Prefer explicit filters over implicit prompt-only constraints.
- Keep secrets and environment-specific access control outside the repository.

## Production Notes

RecallOps is structured as a service that can be attached to internal systems. Organization-specific deployments should add authentication, authorization, retention policy, audit logging, and access enforcement before indexing restricted content into shared collections.

## Related

- [triage-mesh](https://github.com/AIML-Solutions/triage-mesh) — security-first multi-agent system over MCP + A2A; the kind of agentic consumer RecallOps feeds context to
- [multiclaw-harness](https://github.com/AIML-Solutions/multiclaw-harness) — regression harnesses for the agent workflows built on retrieval like this

## License

MIT
