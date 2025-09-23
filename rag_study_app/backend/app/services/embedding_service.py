# services/embedding_service.py
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight for testing

def get_embeddings(chunks):
    for chunk in chunks:
        chunk["embedding"] = model.encode(chunk["text"]).tolist()
    return chunks
