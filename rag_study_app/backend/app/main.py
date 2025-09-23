from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import book_router, chapter_router, subtopic_router, qa_router

app = FastAPI(title="RAG Study App", version="1.0")

# Enable CORS for Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(book_router.router, prefix="/books")
app.include_router(chapter_router.router, prefix="/chapters")
app.include_router(subtopic_router.router, prefix="/subtopics")
app.include_router(qa_router.router, prefix="/ask")

@app.get("/")
def root():
    return {"message": "RAG Study App Backend Running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
