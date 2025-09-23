# db/vector_db.py
import faiss
import numpy as np

class VectorDB:
    def __init__(self, dim):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.chunks = []

    def add_chunks(self, chunks):
        embeddings = np.array([c["embedding"] for c in chunks]).astype("float32")
        self.index.add(embeddings)
        self.chunks.extend(chunks)

    def query(self, query_embedding, top_k=2):
        D, I = self.index.search(np.array([query_embedding]).astype("float32"), top_k)
        return [self.chunks[i] for i in I[0]]
