
from sklearn.metrics.pairwise import cosine_similarity
from Src.Embedding_And_vector_store import embed_texts

def rerank(query, chunks, top_n=3):
    query_emb = embed_texts([query])
    chunk_embs = embed_texts(chunks)

    scores = cosine_similarity(query_emb, chunk_embs)[0]
    ranked = sorted(zip(chunks, scores), key=lambda x: x[1], reverse=True)

    #return ranked
    return [text for text, _ in ranked[:top_n]]
