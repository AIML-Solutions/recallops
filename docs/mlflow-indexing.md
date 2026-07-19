# MLflow Indexing

MLflow indexing turns experiment runs into searchable metadata-rich records.

```bash
python -m recallops.ingest.mlflow \
  --tracking-uri ./mlruns \
  --collection research_ops
```

Useful fields include:

- experiment name
- run ID and status
- params
- metrics
- tags
- artifact URI
- dataset names
- model versions

This supports experiment discovery through both semantic search and explicit metadata filters.
