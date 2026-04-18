from fastapi import APIRouter
from pydantic import BaseModel
from services.ats_service import process_ats

router = APIRouter()

class ATSRequest(BaseModel):
    resume_text: str
    job_description: str


@router.post("/check-ats")
def check_ats(request: ATSRequest):
    return process_ats(request.resume_text, request.job_description)