from typing import Dict
from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_recruiter_decision(
    ats_score: float,
    strengths: list,
    improvements: list,
    missing_keywords: list,
    experience_level: str,
    alignment_score: float,
    matched_skills: list,
    missing_skills: list,
    eligibility: Dict
):

    # 🔥 TRY LLM FIRST
    try:

        prompt = f"""
You are a senior technical recruiter at a top tech company.

Analyze the candidate holistically and fairly.

Candidate Data:
ATS Score: {ats_score}
Strengths: {strengths}
Improvements: {improvements}
Missing Keywords: {missing_keywords}
Experience Level: {experience_level}

Alignment Score: {alignment_score}
Matched Skills: {matched_skills}
Missing Skills: {missing_skills}

Eligibility: {eligibility}

---

Return STRICT JSON:

{{
"decision": "...",
"summary": "...",
"key_strengths": [],
"key_gaps": [],
"recommendation": "..."
}}

Decision Guidelines:
- Do NOT reject candidates only for missing optional skills (e.g., Docker, Kubernetes)
- Focus on core strengths, adaptability, and learning potential
- Missing critical/core skills → Reject
- Missing secondary tools → Consider or Hold
- ATS score + alignment score should BOTH influence decision

Decision Categories:
- "Strong Hire"
- "Hire"
- "Consider"
- "Hold"
- "Reject"

- Be realistic (like a human recruiter)
- Avoid extreme decisions unless clearly justified
- Balance strengths vs gaps
- Do not repeat input text verbatim
- Convert gaps into normalized skill names (e.g., "Docker", not sentences)
- Provide a confidence score (0–1) based on overall fit
- Identify hiring risks explicitly
Behavior
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a strict recruiter."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        import json
        import re

        content = response.choices[0].message.content

        print("LLM RAW OUTPUT:", content)  # 🔥 debug

        # 🔥 extract JSON from messy output
        json_match = re.search(r"\{.*\}", content, re.DOTALL)

        if not json_match:
            raise Exception("No JSON found in LLM response")

        clean_json = json_match.group()

        return json.loads(clean_json)

    except Exception as e:

        print("LLM FAILED → fallback:", e)

        # 🔥 FALLBACK (YOUR ORIGINAL LOGIC)

        if not eligibility.get("eligible", True):
            decision = "Not Eligible"

        elif ats_score >= 75 and alignment_score >= 70:
            decision = "Strong Hire"

        elif ats_score >= 60:
            decision = "Consider"

        else:
            decision = "Not Recommended"

        summary = []

        if ats_score >= 60:
            summary.append("Candidate demonstrates good technical alignment.")
        else:
            summary.append("Candidate shows limited alignment with job requirements.")

        if missing_keywords:
            summary.append(f"Lacks key exposure to {', '.join(missing_keywords)}.")

        if experience_level == "Fresher":
            summary.append("Experience level is relatively low.")

        key_strengths = strengths + matched_skills
        key_gaps = improvements + missing_skills

        if decision == "Strong Hire":
            recommendation = "Proceed with hiring process."
        elif decision == "Consider":
            recommendation = "Candidate can be considered with some reservations."
        else:
            recommendation = "Candidate is not a strong fit for this role."
        print("API KEY:", os.getenv("GROQ_API_KEY"))
        return {
            "decision": decision,
            "summary": " ".join(summary),
            "key_strengths": list(set(key_strengths)),
            "key_gaps": list(set(key_gaps)),
            "recommendation": recommendation
        }