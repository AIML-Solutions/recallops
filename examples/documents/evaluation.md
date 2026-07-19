# Retrieval Evaluation Notes

Retrieval quality should be measured with repeatable query fixtures. Recall@k measures whether any expected document appears in the top results. Mean reciprocal rank rewards systems that place the first relevant result earlier.

For ML and RAG workflows, retrieval evaluation should include both semantic ranking and metadata filter behavior. A system can have a strong embedding model and still fail if it ignores dataset tags, experiment metrics, source dates, or document provenance.

RecallOps includes evaluation utilities so retrieval behavior can be checked during development and regression testing.
