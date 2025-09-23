# app/scripts/ingest.py
from pathlib import Path
import faiss
from app.services.parser import parse_pdf
from app.services.embedding_service import get_embeddings
from app.db.vector_db_instance import vector_db  # <-- use global instance
import os

# Path to save FAISS index
INDEX_PATH = "faiss.index"

# ------------------------------
# Absolute path to PDF file
# ------------------------------
pdf_path = Path(__file__).resolve().parent.parent.parent.parent / "data" / "med-test-rag.pdf"

# ------------------------------
# 1. Parse PDF into chunks
# ------------------------------
chunks = parse_pdf(str(pdf_path), chunk_size=500)
print(f"Number of chunks: {len(chunks)}")
print("First 3 chunks:", chunks[:3])

# ------------------------------
# 2. Generate embeddings for chunks
# ------------------------------
chunks = get_embeddings(chunks)  # Must attach 'embedding' key to each chunk
print("Embeddings added. Example:", chunks[0].get("embedding")[:5] if chunks else "No chunks")

# ------------------------------
# 3. Add chunks to global VectorDB
# ------------------------------
if vector_db.dim != len(chunks[0]["embedding"]):
    vector_db.dim = len(chunks[0]["embedding"])
    vector_db.index = faiss.IndexFlatL2(vector_db.dim)  # Re-create FAISS index with correct dimension

# Add chunks to vector DB
vector_db.add_chunks(chunks)

# ------------------------------
# 4. Save index to disk
# ------------------------------
vector_db.save_index(INDEX_PATH)
print(f"✅ Ingestion completed! {len(chunks)} chunks added and index saved to '{INDEX_PATH}'.")

