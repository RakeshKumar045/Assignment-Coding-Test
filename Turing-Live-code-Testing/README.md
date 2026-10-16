# Coding Exercise — Build a Mini RAG Pipeline

## Context

Your team wants a small internal knowledge base search over a handful of product docs
(`data/*.txt`) before wiring it up to a real LLM. You've been asked to build the retrieval
half from scratch: chunk the docs, embed the chunks, **save the index**, retrieve the most
relevant ones for a query, and assemble a cited answer.

That split matches a real RAG service: an ingest job writes the vector index once; query
time loads it instead of re-embedding every document. `rag/store.py` already implements
`save_index` / `load_index` (a JSON file standing in for FAISS/Chroma/Pinecone) — call them,
don't reimplement them. `main.py` already wires ingest → save → load → answer.

There's no real embedding model or LLM here — `rag/embeddings.py` gives you a deterministic,
hash-based stand-in for an embedding API call (feature hashing: texts that share more words
land closer together in cosine similarity, the way a real embedding model would, but with no
network call and no API key). `rag/documents.py` reads the `.txt` files in `data/`.
`rag/store.py` saves and loads the index. Those three are plumbing — the pipeline logic is
what we're evaluating.

## Your task

Implement the pipeline in `rag/`:

- `rag/chunking.py::chunk_text` — split a document into overlapping fixed-size chunks.
- `rag/retriever.py::build_index` — chunk and embed every document into a flat in-memory index
  (`list` of `IndexedChunk`). `main.py` then calls `save_index` / `load_index` for you.
- `rag/retriever.py::cosine_similarity` — cosine similarity between two vectors.
- `rag/retriever.py::retrieve` — return the top-k chunks for a query, best first, using the
  **loaded** index (same shape as `build_index`'s return value).
- `rag/answer.py::assemble_answer` — format the retrieved chunks into a cited answer string.

All the function/class signatures and docstrings are already in place as a starter skeleton
with `TODO`s — fill in the logic.

## How to run

```
pip install -r requirements.txt
python main.py "What is the refund policy after 14 days?"
pytest
```

Both will fail with `NotImplementedError` / red tests until you've implemented the pipeline —
that's expected for a build-from-scratch exercise, not a sign anything is broken.

## What we're looking for

Not just "does it run" — how you reason about a retrieval system:

- Do you understand *why* cosine similarity is the right comparison for these vectors (and
  what would go wrong if query and index chunks were embedded with different `model` values)?
- Do you handle the boundary cases in chunking deliberately (empty docs, overlap ≥ chunk size)
  rather than by accident?
- Is your code structured so each stage (chunk → embed → index → retrieve → assemble) is
  independently testable, or is it one tangled function?
- How do you validate correctness beyond "the tests are green" — did you look at what's
  actually being retrieved for a real query?

## Suggested time budget

30–45 minutes for Ask 1. Asks 2+ if time allows.

---

## Ask 1 — Make the pipeline work

Implement chunking, embedding-backed indexing, top-k cosine retrieval, and cited answer assembly as described above. `pytest` should pass and `python main.py` should return a sensible, cited answer for the default query.

---

## Ask 2 — Near-duplicates and no-match queries

1. Run `python main.py "What is the refund policy after 14 days?"` — `billing.txt` and `support.txt` both contain a near-duplicate refund paragraph (reworded, not identical), so the top-2 results are redundant. Add near-duplicate detection at index-build or retrieval time. Exact string matching is not enough — the wording differs.
2. Handle a query with nothing relevant in the index (try `"zebra giraffe volcano tectonic plates"`). Return a clear “nothing relevant found” instead of padding with irrelevant chunks just because `top_k` wants 3 results.

---

## If you finish early

Keep going from the code you already have. You do not have to implement these fully.

1. The index grows without bound as documents are added. Add a hard cap on indexed chunks with an eviction policy (for example LRU or FIFO), and persist the result with `save_index` so the cap survives process restart. Then: `retrieve` is a linear scan — at what index size does that miss an interactive budget (say under 200ms), and what would you change first? Use real numbers, not just “use a vector database.” The JSON file is the toy version of a vector store — what would have to change if this were FAISS/Chroma instead?
2. Pure vector similarity is weak on exact terms (product codes, error strings). Design or sketch a simple hybrid (keyword/BM25 plus cosine). When is that complexity worth it, and how would you know it broke in production before customers told you?

