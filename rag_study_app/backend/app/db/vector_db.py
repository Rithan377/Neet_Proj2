import faiss
import numpy as np
import pickle
import os

class VectorDB:
    def __init__(self, dim):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.chunks = []

    def add_chunks(self, chunks):
        if not chunks:
            return
        embeddings = np.array([c["embedding"] for c in chunks]).astype("float32")
        self.index.add(embeddings)
        self.chunks.extend(chunks)

    def query(self, query_embedding, top_k=3):
        if not self.chunks or self.index.ntotal == 0:
            return []
        D, I = self.index.search(np.array([query_embedding]).astype("float32"), top_k)
        return [self.chunks[i] for i in I[0] if i < len(self.chunks)]

    # -------------------
    # Save / Load index
    # -------------------
    def save_index(self, path="faiss.index"):
        faiss.write_index(self.index, path)
        with open(path + ".chunks", "wb") as f:
            pickle.dump(self.chunks, f)
        print(f"✅ VectorDB saved. Total vectors: {self.index.ntotal}")

    def load_index(self, path="faiss.index"):
        if os.path.exists(path):
            self.index = faiss.read_index(path)
            with open(path + ".chunks", "rb") as f:
                self.chunks = pickle.load(f)
            print(f"✅ VectorDB loaded from '{path}'. Total vectors: {self.index.ntotal}")
        else:
            print(f"No FAISS index found at '{path}'. VectorDB is empty!")
