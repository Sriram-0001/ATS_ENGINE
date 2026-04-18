def summarize_review(review: str, requirements: str):

    review_lower = review.lower()
    req_skills = [r.strip().lower() for r in requirements.split("\n") if r.strip()]

    matched = []
    missing = []

    for skill in req_skills:

    # 🔥 find where skill appears
        if skill in review_lower:

            # get small context around skill
            idx = review_lower.find(skill)
            context = review_lower[max(0, idx-30): idx+30]

            # 🔥 check negation ONLY in local context
            if "lack" in context or "missing" in context:
                missing.append(skill)
            else:
                matched.append(skill)

        else:
            missing.append(skill)

    # simple alignment score
    if len(req_skills) == 0:
        alignment_score = 0
    else:
        alignment_score = int((len(matched) / len(req_skills)) * 100)

    # summary (basic for now)
    if alignment_score > 75:
        summary = "Candidate shows strong alignment with required skills."
    elif alignment_score > 50:
        summary = "Candidate meets several requirements but has noticeable gaps."
    else:
        summary = "Candidate lacks key skills required for the role."
    
    print("API KEY:", os.getenv("GROQ_API_KEY"))

    return {
        "summary": summary,
        "alignment_score": alignment_score,
        "matched_skills": matched,
        "missing_skills": missing
    }