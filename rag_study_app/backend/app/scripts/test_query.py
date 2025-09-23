# test_query.py
"""
from app.services.embedding_service import get_embeddings
from app.db.vector_db_instance import vector_db

# ------------------------------
# Query text
# ------------------------------
query = "what are polysaccharides"

# ------------------------------
# 1. Generate embedding for the query
# ------------------------------
query_emb = get_embeddings([{"text": query}])[0]["embedding"]

# ------------------------------
# 2. Search in VectorDB
# ------------------------------
results = vector_db.query(query_emb, top_k=3)

# ------------------------------
# 3. Print results
# ------------------------------
print("Query:", query)
print("Top results:", results)
"""
# app/scripts/test_query.py
from app.services.embedding_service import get_embeddings
from app.db.vector_db_instance import vector_db  # Make sure it's the shared instance

# Check FAISS index
print("FAISS index ntotal:", vector_db.index.ntotal)

# Your query
query = "what are polysaccharides"
query_emb = get_embeddings([{"text": query}])[0]["embedding"]
results = vector_db.query(query_emb, top_k=3)

print("Query:", query)
print("Top results:", results)
