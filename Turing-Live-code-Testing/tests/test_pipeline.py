"""Baseline correctness tests for the mini RAG pipeline (Ask 1).

Run: pytest (from inside 01-mini-rag-pipeline/)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from rag.answer import assemble_answer  # noqa: E402
from rag.chunking import chunk_text  # noqa: E402
from rag.documents import load_documents  # noqa: E402
from rag.retriever import IndexedChunk, build_index, retrieve  # noqa: E402
from rag.service import answer_query  # noqa: E402
from rag.store import load_index, save_index  # noqa: E402


def test_chunk_text_respects_chunk_size():
    text = "word " * 500
    chunks = chunk_text(text, chunk_size=100, overlap=20)
    assert chunks, "expected at least one chunk"
    assert all(len(c) <= 100 for c in chunks)


def test_chunk_text_rejects_overlap_not_smaller_than_chunk_size():
    import pytest

    with pytest.raises(ValueError):
        chunk_text("some text", chunk_size=50, overlap=50)


def test_chunk_text_empty_input_returns_no_chunks():
    assert chunk_text("") == []
    assert chunk_text("   ") == []


def test_overlap_preserves_content_that_spans_a_boundary():
    # With overlap=0 this exact marker would be split across two chunks
    # and would not appear intact anywhere. Overlap must prevent that.
    text = "A" * 35 + "MARKERPHRASE" + "B" * 35
    chunks = chunk_text(text, chunk_size=40, overlap=10)
    assert any("MARKERPHRASE" in c for c in chunks), (
        "a phrase spanning a chunk boundary should still appear intact in "
        "at least one chunk when overlap > 0"
    )


def test_build_index_creates_one_entry_per_chunk_with_a_vector():
    docs = {"doc1.txt": "alpha beta gamma. " * 40}
    index = build_index(docs, chunk_size=50, overlap=10)
    assert len(index) == len(chunk_text(docs["doc1.txt"], 50, 10))
    for entry in index:
        assert entry.doc_id == "doc1.txt"
        assert isinstance(entry.vector, list)
        assert len(entry.vector) > 0
        assert any(v != 0 for v in entry.vector)


def test_retrieve_ranks_the_relevant_document_highest():
    index = build_index(load_documents())
    hits = retrieve("How do I enable SSO for my workspace?", index, top_k=3)
    assert hits, "expected at least one hit"
    top_chunk, top_score = hits[0]
    assert top_chunk.doc_id == "security.txt"
    # Scores must be sorted descending.
    scores = [score for _, score in hits]
    assert scores == sorted(scores, reverse=True)


def test_retrieve_respects_top_k():
    index = build_index(load_documents())
    hits = retrieve("refund", index, top_k=2)
    assert len(hits) <= 2


def test_retrieve_on_empty_index_returns_empty():
    assert retrieve("anything", []) == []


def test_answer_query_cites_the_retrieved_chunk():
    index = build_index(load_documents())
    result = answer_query("What happens to my refund after 14 days?", index, top_k=2)
    assert "billing.txt" in result or "support.txt" in result
    assert "credit" in result.lower()


def test_assemble_answer_on_no_hits_does_not_crash():
    result = assemble_answer("anything", [])
    assert isinstance(result, str)
    assert "anything" in result


def test_save_and_load_index_roundtrip(tmp_path):
    index = build_index({"doc1.txt": "refund window is fourteen days. " * 20}, chunk_size=80, overlap=10)
    path = tmp_path / "index.json"
    save_index(index, str(path))
    loaded = load_index(str(path))
    assert len(loaded) == len(index)
    assert all(isinstance(row, IndexedChunk) for row in loaded)
    assert loaded[0].doc_id == index[0].doc_id
    assert loaded[0].text == index[0].text
    assert loaded[0].vector == index[0].vector
    hits = retrieve("fourteen day refund", loaded, top_k=1)
    assert hits
