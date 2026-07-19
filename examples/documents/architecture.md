# Metadata-Aware Retrieval Architecture

Metadata-aware retrieval combines vector similarity with structured constraints. In RAG systems this is useful because relevant context is rarely defined by semantic similarity alone. Source, date, document type, experiment identifier, dataset, model family, and evaluation metrics can all change whether a chunk should be eligible for retrieval.

RecallOps keeps metadata attached to retrieval-optimized vectors and uses deterministic document and chunk identifiers. The local reference implementation uses an in-memory index for repeatable tests; durable deployments can back the same service boundary with Postgres metadata records and Qdrant ANN search.

This architecture makes retrieval easier to test. Engineers can validate whether filters narrow the candidate set, whether ranking returns expected documents, and whether metadata survives the ingestion path.
