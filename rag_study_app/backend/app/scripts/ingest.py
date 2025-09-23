from app.services.parser import parse_pdf
from app.services.embedding_service import get_embeddings
from app.db.vector_db import VectorDB

from pathlib import Path

# Absolute path relative to this script
pdf_path = Path(__file__).resolve().parent.parent.parent.parent / "data" / "med-test-rag.pdf"

# 1. Parse PDF
chunks = parse_pdf(str(pdf_path), chunk_size=500)

# 2. Get embeddings
chunks = get_embeddings(chunks)

# 3. Initialize your vector DB
db = VectorDB(dim=len(chunks[0]["embedding"]))

# 4. Add chunks to DB
db.add_chunks(chunks)

# Optional: test a query
query_text = "How do plants make food?"
query_emb = get_embeddings([{"text": query_text}])[0]["embedding"]
results = db.query(query_emb, top_k=2)
print(results)
