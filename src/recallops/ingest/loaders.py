from __future__ import annotations

from pathlib import Path

from recallops.ids import stable_id
from recallops.models import Document, Metadata

SUPPORTED_SUFFIXES = {".md", ".markdown", ".txt"}


def load_local_documents(path: str | Path, metadata: Metadata | None = None) -> list[Document]:
    root = Path(path)
    if not root.exists():
        raise FileNotFoundError(f"input path does not exist: {root}")

    files = [root] if root.is_file() else sorted(p for p in root.rglob("*") if p.is_file())
    documents: list[Document] = []
    base_metadata = metadata or {}

    for file_path in files:
        if file_path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        text = file_path.read_text(encoding="utf-8")
        if not text.strip():
            continue
        relative = str(file_path.relative_to(root)) if root.is_dir() else file_path.name
        doc_metadata = {
            **base_metadata,
            "source": relative,
            "source_path": str(file_path),
            "source_type": base_metadata.get("source_type", "local_file"),
            "doc_type": base_metadata.get("doc_type", "technical_doc"),
        }
        documents.append(
            Document(
                document_id=stable_id("doc", relative, text),
                text=text,
                metadata=doc_metadata,
            )
        )

    return documents
