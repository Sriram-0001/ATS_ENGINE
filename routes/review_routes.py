from fastapi import APIRouter
from pydantic import BaseModel
from services.review_service import summarize_review

router = APIRouter()

class ReviewRequest(BaseModel):
    review: str
    requirements: str


@router.post("/summarize-review")
def summarize(data: ReviewRequest):
    return summarize_review(data.review, data.requirements)