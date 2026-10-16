"""Public entrypoint tying chunking -> embedding -> retrieval -> answer together."""

from .answer import assemble_answer
from .retriever import build_index, retrieve


def answer_query(query: str, index: list, top_k: int = 3) -> str:
    """Retrieves the top-k chunks for `query` and assembles a cited answer."""
    hits = retrieve(query, index, top_k=top_k)
    return assemble_answer(query, hits)
