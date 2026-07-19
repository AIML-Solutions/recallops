# Retrieval Evaluation

RecallOps includes basic retrieval metrics to keep quality testable.

## Metrics

- **Recall@k**: fraction of relevant documents found in the top `k` results.
- **MRR**: mean reciprocal rank of the first relevant result.

Example fixture:

```yaml
- query: "How should retrieval quality be measured?"
  relevant_docs:
    - evaluation.md
  filters:
    source_type: docs
```

Evaluation should be run against stable fixtures during development and against representative corpora before operational use.
