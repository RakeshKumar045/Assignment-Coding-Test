"""Persists the embedded index to disk.

Stands in for writing to a real vector store (FAISS, Chroma, Pinecone, …).
Ingestion writes the index once; query time loads it instead of re-embedding
every document. Given as plumbing — call these, don't reimplement them.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict

from .retriever import IndexedChunk

DEFAULT_INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "index.json")


def save_index(index: list, path: str = DEFAULT_INDEX_PATH) -> str:
    """Writes a list of IndexedChunk to `path` as JSON. Returns `path`."""
    payload = [asdict(chunk) for chunk in index]
    directory = os.path.dirname(os.path.abspath(path))
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh)
    return path


def load_index(path: str = DEFAULT_INDEX_PATH) -> list:
    """Reads a JSON index written by `save_index` back into IndexedChunk rows."""
    with open(path, "r", encoding="utf-8") as fh:
        payload = json.load(fh)
    return [IndexedChunk(**row) for row in payload]
