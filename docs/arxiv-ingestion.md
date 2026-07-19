# arXiv Ingestion

The arXiv connector is designed for research snapshot workflows.

```bash
python -m recallops.ingest.arxiv \
  --query 'cat:cs.IR AND (RAG OR retrieval OR embeddings OR reranking)' \
  --max-results 25 \
  --collection research_ops
```

Live network ingestion should be opt-in for tests and automation. Use fixtures for normal CI.
