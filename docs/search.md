# Search

Search combines vector similarity with structured metadata filters.

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "retrieval experiments using reranking",
    "collection": "research_ops",
    "top_k": 10,
    "filters": {
      "doc_type": "experiment_run",
      "tags": ["rag", "reranking"],
      "metrics.recall_at_5": { "gte": 0.8 }
    }
  }'
```

Supported filter patterns in the reference implementation:

- Exact value match.
- List containment for tags.
- Numeric comparisons with `gt`, `gte`, `lt`, `lte`.
- Nested metadata via dotted keys.
