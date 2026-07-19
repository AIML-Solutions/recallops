# Ingestion

The local ingestion path supports Markdown and text files.

```bash
python -m recallops.ingest.pipeline \
  --input examples/documents \
  --collection research_ops \
  --chunk-size 700 \
  --chunk-overlap 120
```

Ingestion steps:

1. Load supported files.
2. Normalize source metadata.
3. Create deterministic document IDs.
4. Split text into overlapping chunks.
5. Generate embeddings.
6. Upsert chunks into the retrieval index.

The reference chunker is character-based for deterministic tests. Production deployments can replace it with tokenizer-aware or structure-aware chunking while preserving the retrieval API.
