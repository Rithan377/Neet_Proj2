#services/embeding_service.py
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight for testing

def get_embeddings(chunks):
    for chunk in chunks:
        chunk["embedding"] = model.encode(chunk["text"]).tolist()

    # Debug: print first 3 chunks keys and embedding length
    for i, c in enumerate(chunks[:3]):
        print(f"Chunk {i+1} keys: {c.keys()}")
        print(f"Embedding length: {len(c['embedding'])}")
        print(f"First 5 embedding values: {c['embedding'][:5]}")

    return chunks
