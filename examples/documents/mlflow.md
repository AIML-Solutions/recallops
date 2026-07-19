# MLflow Experiment Discovery

MLflow runs contain operational knowledge about experiments: parameters, metrics, datasets, model versions, tags, artifact locations, and evaluation outputs. Indexing this metadata makes it possible to retrieve prior experiments by intent, not only by run identifier.

Example retrieval questions include which runs used a reranker, which embedding model performed best on a dataset, and which experiments exceeded a target Recall@5 threshold.

RecallOps models experiment runs as searchable technical documents with nested metadata for metrics and parameters.
