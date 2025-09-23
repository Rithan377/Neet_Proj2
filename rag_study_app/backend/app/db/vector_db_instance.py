from app.db.vector_db import VectorDB
import os

# Path to FAISS index
INDEX_PATH = "faiss.index"

# Create global VectorDB instance
vector_db = VectorDB(dim=384)

# Load saved index if exists
vector_db.load_index(INDEX_PATH)
