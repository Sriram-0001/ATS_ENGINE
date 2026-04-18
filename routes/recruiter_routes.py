from fastapi import APIRouter
from pydantic import BaseModel
from services.recruiter_service import generate_recruiter_decision

router = APIRouter()


class RecruiterRequest(BaseModel):
    ats_score: float
    strengths: list
    improvements: list
    missing_keywords: list
    experience_level: str

    alignment_score: float
    matched_skills: list
    missing_skills: list

    eligibility: dict


@router.post("/recruiter-decision")
def recruiter_decision(request: RecruiterRequest):

    return generate_recruiter_decision(
        ats_score=request.ats_score,
        strengths=request.strengths,
        improvements=request.improvements,
        missing_keywords=request.missing_keywords,
        experience_level=request.experience_level,
        alignment_score=request.alignment_score,
        matched_skills=request.matched_skills,
        missing_skills=request.missing_skills,
        eligibility=request.eligibility
    )