from fastapi import APIRouter
from pydantic import BaseModel
from services.eligibility_service import evaluate_candidate

router = APIRouter()

class EligibilityRequest(BaseModel):
    resume_text: str
    drive_requirements: str


@router.post("/check-eligibility")
def check_eligibility(data: EligibilityRequest):
    return evaluate_candidate(
        data.resume_text,
        data.drive_requirements
    )