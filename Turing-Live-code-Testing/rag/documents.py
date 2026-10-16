"""Loads the source documents that make up the knowledge base."""

import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def load_documents(data_dir: str = DATA_DIR) -> dict:
    """Returns {filename: full_text} for every .txt file in data_dir."""
    docs = {}
    for name in sorted(os.listdir(data_dir)):
        path = os.path.join(data_dir, name)
        if os.path.isfile(path) and name.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as fh:
                docs[name] = fh.read()
    return docs
