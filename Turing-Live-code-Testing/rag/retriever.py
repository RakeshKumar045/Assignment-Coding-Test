"""Builds a vector index over chunked documents and retrieves top-k matches."""

from dataclasses import dataclass, field

# from aws_lambda_api.qna_flask import embeddings
from chunking import chunk_text
from embeddings import embed


@dataclass
class IndexedChunk:
    doc_id: str
    chunk_id: int
    text: str
    vector: list = field(default_factory=list)


def cosine_similarity(a: list, b: list) -> float:
    """Returns cosine similarity between two equal-length vectors.

    TODO(candidate): implement this. Guard against a zero vector (an
    empty chunk, or a query that tokenizes to nothing) -- don't let that
    raise a ZeroDivisionError.
    """
    raise NotImplementedError("cosine_similarity is not implemented yet")


def build_index(documents: dict, chunk_size: int = 300, overlap: int = 50) -> list:
    """Chunks and embeds every document.

    Args:
        documents: {doc_id: full_text}.

    Returns:
        A flat list of IndexedChunk, in (doc_id, chunk_id) order.

    After this returns, `main.py` persists the list with `save_index`
    (given in `rag/store.py`) and reloads it with `load_index` before
    calling `retrieve`. You implement the in-memory list; the disk
    round-trip is already wired.

    TODO(candidate): implement this using `chunk_text` and `embed`.
    """


    index = []
    for doc in documents:
        chunks = chunk_text(documents[doc], chunk_size)

        for k, v in enumerate(chunks):
            embeddings = embed(v)
            res_index = {"doc_id": doc, "chunk_id": k, "text": v, "embeddings": embeddings}

            index.append(res_index)


    return index
    # raise NotImplementedError("build_index is not implemented yet")



def retrieve(query: str, index: list, top_k: int = 3):
    """Returns up to `top_k` (IndexedChunk, score) pairs, best first.

    TODO(candidate): implement this. Embed the query with the *same*
    function/parameters used to build the index, score every entry, and
    return the top `top_k` sorted by score descending.
    """

    if not query or not index:
        raise NotImplementedError("retrieve is not implemented yet")

    score_chunks = []
    query_embeddings = "testing our model"
    query_embeddings = embed(query)
    for i in index:
        score = cosine_similarity(query_embeddings, i["embeddings"])
        score_chunks.append((i, score))

    res = []
    for s, i in sorted(score_chunks, key=lambda x: x[1], reverse=True):
        res.append(i)
    return res




if __name__ == "__main__":
    text = """Billing and Refunds

        Customers are billed monthly on the anniversary of their signup date. Invoices are emailed
        automatically and can also be downloaded from the billing dashboard at any time.
        
        Our refund policy allows a full refund within 14 days of purchase if the customer has not
        exceeded 100 API calls. After 14 days, refunds are issued as account credit instead of cash,
        and the credit can be applied to any future invoice. Refund requests are processed within
        3 business days of approval.
        
        Failed payments are retried automatically three times over five days before the account is
        downgraded to the free tier. Customers can update their card on file from account settings.
        """

    documents_dic = {}

    documents_dic["text"] = text

    build_index(documents_dic, 300, 50)
    # chunk_text(text,100,  50)
    print("building retrieved")
    # raise NotImplementedError("chunk_text is not implemented yet")
