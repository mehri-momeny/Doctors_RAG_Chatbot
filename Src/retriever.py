from Src.Embedding_And_vector_store import embed_texts, COLLECTION_NAME

def retrieve(client, query, top_k=5):
    query_vector = embed_texts([query])[0]

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True
    )
    points = results.points

    return [p.payload["text"] for p in points]

