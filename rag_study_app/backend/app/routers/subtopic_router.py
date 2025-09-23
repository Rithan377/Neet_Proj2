from fastapi import APIRouter

router = APIRouter()

@router.get("/{chapter_id}")
def get_subtopics(chapter_id: str):
    return ["9.1 Heart", "9.2 Brain", "9.3 Lungs"]
