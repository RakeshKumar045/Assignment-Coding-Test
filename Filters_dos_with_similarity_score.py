# Filters documents with a similarity score below min score

search_results = [
    {
        "id": "doc1",
        "text": "Pump maintenance procedure",
        "score": 0.91,
        "department": "maintenance"
    },
    {
        "id": "doc2",
        "text": "Employee leave policy",
        "score": 0.85,
        "department": "hr"
    },
    {
        "id": "doc3",
        "text": "Water treatment troubleshooting guide",
        "score": 0.95,
        "department": "maintenance"
    },
    {
        "id": "doc4",
        "text": "Old equipment document",
        "score": 0.60,
        "department": "maintenance"
    }
]


def retrieve_top_documents(
        search_results,
        top_k=2,
        min_score=0.80,
        department=None
):
    filter_doc = []
    for d in search_results:
        if d["score"] >= min_score and (department is None or d.get("department") == department):
            filter_doc.append(d)

    result = sorted(filter_doc, key=lambda a: a["score"], reverse=True)

    return result[:top_k]


res = retrieve_top_documents(
    search_results,
    top_k=2,
    min_score=0.80,
    department=None
)

print(res)













