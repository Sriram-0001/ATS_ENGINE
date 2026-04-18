def compute_final_score(skill_score, semantic_score, experience_score, missing_skills):

    experience_score = min(experience_score / 5, 1)

    fit_score = (
        0.4 * semantic_score +
        0.4 * skill_score +
        0.2 * experience_score
    ) * 100

    # 🔥 penalty
    penalty = min(len(missing_skills) * 5, 30)
    fit_score -= penalty

    # 🔥 clamp AFTER penalty
    fit_score = max(fit_score, 10)   # floor
    fit_score = min(fit_score, 100)  # cap
    if fit_score > 80:
        category = "Excellent Fit"
    elif fit_score > 65:
        category = "Good Fit"
    elif fit_score > 45:
        category = "Moderate Fit"
    else:
        category = "Poor Fit"
    if len(missing_skills) > 0:
        fit_score = min(fit_score, 90)

    strengths = []
    improvements = []

    if semantic_score > 0.7:
        strengths.append("Strong overall alignment with job role")
    else:
        improvements.append("Resume content not strongly aligned")

    if skill_score > 0.6:
        strengths.append("Good overlap with required technical skills")
    else:
        improvements.append("Missing key required skills")

    if experience_score < 0.5:
        improvements.append("Insufficient experience")

    return {
        "fit_score": fit_score,
        "category": category,
        "strengths": strengths,
        "improvements": improvements,
        "experience_level": (
            "Fresher" if experience_score < 0.3 else
            "Intermediate" if experience_score < 0.7 else
            "Experienced"
        )
    }