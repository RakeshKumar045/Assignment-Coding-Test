"""Assembles a final answer from retrieved chunks.

Stands in for an LLM generation call: instead of a real model, it
deterministically formats the retrieved chunks with citations. The point
of this exercise is the retrieval pipeline, not generation quality.
"""


def assemble_answer(query: str, hits: list) -> str:
    """Formats retrieved (IndexedChunk, score) pairs into a cited answer.

    Args:
        query: the original user query.
        hits: output of `retriever.retrieve` -- a list of
            (IndexedChunk, score) pairs, best first.

    Returns:
        A deterministic string citing each retrieved chunk by
        "[doc_id#chunk_id]", or a message saying nothing relevant was
        found when `hits` is empty.

    TODO(candidate): implement this. Must not crash on an empty `hits`.
    """
    raise NotImplementedError("assemble_answer is not implemented yet")
