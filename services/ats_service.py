from extraction.skill_extractor import SkillExtractor
from extraction.experience_extractor import ExperienceExtractor
from scoring.weighted_scorer import compute_final_score
from embedding.cross_encoder import ATSCrossEncoder
from extraction.semantic_skill_matcher import SemanticSkillMatcher


def process_ats(resume_text: str, jd_text: str):

    # 🔹 1. Clean (skip for now)
    resume_clean = resume_text
    jd_clean = jd_text

    # 🔹 2. Extract skills
    skill_extractor = SkillExtractor()
    resume_skills = skill_extractor.extract(resume_clean, source="resume")
    jd_skills = skill_extractor.extract(jd_clean, source="jd")

    # 🔹 3. Extract experience
    exp_extractor = ExperienceExtractor()
    resume_exp = exp_extractor.extract(resume_clean)

    
    # 🔹 semantic scoring
    cross_encoder = ATSCrossEncoder()
    semantic_score = cross_encoder.score(resume_clean, jd_clean)

    # 🔹 cap it
    semantic_score = min(semantic_score, 0.85)

    # 🔹 5. Skill matching
    matcher = SemanticSkillMatcher()

    matched_skills, missing_skills = matcher.match_skills(
    resume_skills, jd_skills
    )

    if len(jd_skills) == 0:
        skill_score = 0
    else:
        skill_score = len(matched_skills) / len(jd_skills)
    

    # 🔹 6. Final scoring
    result = compute_final_score(
        skill_score=skill_score,
        semantic_score=semantic_score,
        experience_score=resume_exp,
        missing_skills=missing_skills
    )
    print("RESUME SKILLS:", resume_skills)
    print("JD SKILLS:", jd_skills)
    print("MATCHED:", matched_skills)
    print("MISSING:", missing_skills)

    # 🔹 7. Response
    return {
        "ats_score": round(result["fit_score"], 2),
        "match_percentage": round(result["fit_score"], 2),
        "strengths": result["strengths"],
        "improvements": result["improvements"],
        "missing_keywords": missing_skills,
        "experience_level": result["experience_level"]
    }
    