"""Embedding function. Stands in for a real embedding API call.

Deterministic and hash-based so the exercise needs no network access or a
real model. This uses the "hashing trick" (feature hashing, as in
scikit-learn's HashingVectorizer): every token in the text is hashed into
one of `dims` buckets with a deterministic +1/-1 sign, and the resulting
sparse count vector is the embedding. Two texts that share more words end
up with higher cosine similarity -- the property real semantic embeddings
have, without needing a real model. Vectors built with two different
`model` values live in unrelated spaces (the hash salt is mixed into every
token digest), exactly like two real embedding models would.
"""

import hashlib
import re

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> list:
    return _TOKEN_RE.findall(text.lower())


def embed(text: str, model: str = "fake-embed-v1", dims: int = 64) -> list:
    """Returns a `dims`-length embedding vector for `text`.

    Deterministic: calling this twice with the same (text, model, dims)
    always returns the same vector.
    """
    vec = [0.0] * dims
    for tok in _tokenize(text):
        h = hashlib.sha256(f"{model}:{tok}".encode()).hexdigest()
        idx = int(h[:8], 16) % dims
        sign = 1.0 if int(h[8], 16) % 2 == 0 else -1.0
        vec[idx] += sign
    return vec
