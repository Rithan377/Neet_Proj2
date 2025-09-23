from fastapi import APIRouter

router = APIRouter()

@router.get("/{book_id}")
def get_chapters(book_id: str):
    return ["Chapter 1: Human Anatomy", "Chapter 2: Plant Physiology"]

