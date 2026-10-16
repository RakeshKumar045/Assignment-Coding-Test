"""CLI entrypoint: python main.py "your question here".

Ingest (chunk + embed) is separate from query time, the same way a real RAG
service writes a vector index once and then loads it for retrieval.
"""

import sys

from rag.documents import load_documents
from rag.retriever import build_index
from rag.service import answer_query
from rag.store import DEFAULT_INDEX_PATH, load_index, save_index

DEFAULT_QUERY = "What is the refund policy after 14 days?"

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) or DEFAULT_QUERY

    index = build_index(load_documents())
    save_index(index, DEFAULT_INDEX_PATH)
    index = load_index(DEFAULT_INDEX_PATH)

    print(f"Indexed {len(index)} chunks (saved to {DEFAULT_INDEX_PATH}).\n")
    print(answer_query(query, index))
