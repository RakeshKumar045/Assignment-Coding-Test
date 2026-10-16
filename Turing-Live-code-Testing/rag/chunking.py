"""Splits document text into retrievable chunks."""


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list:
    """Splits `text` into overlapping fixed-size character chunks.

    Args:
        text: the full document text.
        chunk_size: max characters per chunk.
        overlap: number of characters each chunk repeats from the end of
            the previous chunk, so content that straddles a chunk boundary
            still appears intact in at least one chunk.

    Returns:
        A list of chunk strings, in document order. Never returns empty
        chunks. `overlap` must be smaller than `chunk_size`.

    TODO(candidate): implement this. Think about:
    - what happens if `overlap >= chunk_size` (should not silently misbehave)
    - empty or whitespace-only input
    - making sure content that straddles a chunk boundary still appears
      intact in at least one chunk
    """



    if not text:
        return []

    text = """Our refund policy allows a full refund within 14 days of purchase if the customer has not
        exceeded 100 API calls. After 14 days, refunds are issued as account credit instead of cash,
        and the credit can be applied to any future invoice. Refund requests are processed within
        3 business days of approval."""

    #suppose size= 100 , overlap = 20

    chunks = []
    start = 0

    text_length = len(text)

    while start < text_length:
        end = min(text_length, start + overlap)
        chunks.append(text[start:end])
        if end == text_length:
            break
        start = start + chunk_size - overlap

    print("text : ", text)
    print("text len : ", len(text))
    print("#"*100)
    print("chunks : ", chunks)
    return chunks


# if __name__ == "__main__":
#     text = """Billing and Refunds
#
# Customers are billed monthly on the anniversary of their signup date. Invoices are emailed
# automatically and can also be downloaded from the billing dashboard at any time.
#
# Our refund policy allows a full refund within 14 days of purchase if the customer has not
# exceeded 100 API calls. After 14 days, refunds are issued as account credit instead of cash,
# and the credit can be applied to any future invoice. Refund requests are processed within
# 3 business days of approval.
#
# Failed payments are retried automatically three times over five days before the account is
# downgraded to the free tier. Customers can update their card on file from account settings.
# """
#     chunk_text(text,100,  50)
#     print("chunk completed")
#     # raise NotImplementedError("chunk_text is not implemented yet")
