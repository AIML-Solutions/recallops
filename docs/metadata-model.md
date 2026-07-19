# Metadata Model

RecallOps metadata is intentionally flexible. Common fields include:

| Field | Purpose |
| --- | --- |
| `source` | Human-readable source name |
| `source_path` | Local path or source URI |
| `source_type` | `docs`, `paper`, `experiment`, `model_card`, etc. |
| `doc_type` | More specific document classification |
| `tags` | Retrieval and governance tags |
| `project` | Project or corpus grouping |
| `dataset` | Dataset reference for ML records |
| `model_name` | Model family or registered model |
| `metrics.*` | Nested metrics for experiment search |
| `params.*` | Nested parameters for experiment search |

Nested metadata can be filtered with dotted keys, for example:

```json
{
  "metrics.recall_at_5": { "gte": 0.8 },
  "params.embedding_model": "bge-small",
  "tags": ["reranking"]
}
```
