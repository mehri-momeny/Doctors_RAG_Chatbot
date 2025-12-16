from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

_model = None
COLLECTION_NAME = "doctors"

def chunk_documents(texts):
    chunks = []
    for i, text in enumerate(texts):
        chunks.append({
            "id": i,
            "text": text
        })
    return chunks

def get_embedding_model():
    global _model
    if _model is None:
        #_model = SentenceTransformer("all-MiniLM-L6-v2")
        _model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    return _model

def embed_texts(texts):
    model = get_embedding_model()
    return model.encode(texts)

def get_client():
   return QdrantClient(":memory:")
   #return QdrantClient( url="http://localhost:8501")

def create_collection(client, vector_size):
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={
            "size": vector_size,
            "distance": "Cosine"
        }
    )

def store_chunks(client, chunks, embeddings):
    points = [
        PointStruct(
            id=chunk["id"],
            vector=embeddings[i],
            payload={"text": chunk["text"]}
        )
        for i, chunk in enumerate(chunks)
    ]
    client.upsert(collection_name=COLLECTION_NAME, points=points)
