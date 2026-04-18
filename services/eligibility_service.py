import re


def extract_cgpa(text):
    match = re.search(r'(\d\.\d)', text)
    return float(match.group(1)) if match else 0


def extract_branch(text):
    text = text.lower()
    if "computer science" in text or "cse" in text:
        return "cse"
    return "other"


def evaluate_candidate(resume_text: str, drive_requirements: str):

    resume_lower = resume_text.lower()
    req_lower = drive_requirements.lower()

    cgpa_required = 7.0 if "7.0" in req_lower else 0
    branch_required = "cse" if "cse" in req_lower else None

    candidate_cgpa = extract_cgpa(resume_text)
    candidate_branch = extract_branch(resume_text)

    reasons = []

    # ❌ NOT ELIGIBLE
    if candidate_cgpa < cgpa_required:
        reasons.append("GPA requirement not satisfied.")

    if branch_required and candidate_branch != branch_required:
        reasons.append("Branch requirement not satisfied.")

    if reasons:
        return {
            "eligible": False,
            "percentage": 0,
            "analysis": {
                "reasons": reasons,
                "conclusion": "The candidate does not meet mandatory eligibility criteria."
            }
        }

    # ✅ ELIGIBLE
    strengths = []
    weaknesses = []
    improvements = []

    if candidate_cgpa >= cgpa_required:
        strengths.append(f"Meets GPA requirement ({candidate_cgpa}).")

    if branch_required:
        strengths.append("Belongs to required branch.")

    # basic skill scoring
    skills = ["java", "spring boot", "microservices", "docker"]

    matched = [s for s in skills if s in resume_lower]
    missing = [s for s in skills if s not in resume_lower]

    percentage = int((len(matched) / len(skills)) * 100)

    if missing:
        weaknesses.append(f"Missing skills: {', '.join(missing)}")
        improvements.append("Improve missing technical skills.")

    return {
        "eligible": True,
        "percentage": percentage,
        "analysis": {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "improvements": improvements,
            "conclusion": f"The candidate shows a suitability score of {percentage}%."
        }
    }