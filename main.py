
from preprocessing.text_cleaner import TextCleaner
from embedding.embedder import Embedder
from extraction.skill_extractor import SkillExtractor
from extraction.experience_extractor import ExperienceExtractor
from scoring.similarity import SimilarityEngine
from scoring.weighted_scorer import compute_final_score
from utils.config import  (
    EMBEDDING_MODEL,
    SKILL_SIM_THRESHOLD
)
from routes import recruiter_routes


from fastapi import FastAPI
from routes import ats_routes, review_routes, eligibility_routes
app = FastAPI(title="ATS Engine")
app.include_router(ats_routes.router, prefix="/api")
app.include_router(review_routes.router, prefix="/api")
app.include_router(eligibility_routes.router, prefix="/api")
app.include_router(recruiter_routes.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "ATS Engine Running"}

class ATS:

    def __init__(self):
        self.model = Embedder.load_model(EMBEDDING_MODEL)

    @staticmethod
    def generate_explanation(skill_score, semantic_score, experience_score):

        explanation = []

        if skill_score >= 0.6:
            explanation.append("Strong skill alignment detected.")
        elif skill_score >= 0.3:
            explanation.append("Partial skill match detected.")
        else:
            explanation.append("Significant skill gap detected.")

        if semantic_score >= 0.75:
            explanation.append("High contextual similarity with job description.")

        if experience_score < 1:
            explanation.append("Experience slightly below requirement.")

        return " ".join(explanation)

    def run(self, resume_path, jd_text):

        # -----------------------------
        # Parse Resume
        # -----------------------------
        resume_raw = resume_text
        jd_raw = jd_text

        resume_clean = TextCleaner.clean(resume_raw)
        jd_clean = TextCleaner.clean(jd_text)

        # -----------------------------
        # Extract JD Skills
        # -----------------------------
        jd_skills = SkillExtractor.extract_from_jd(jd_text)

        # -----------------------------
        # Resume Chunking
        # -----------------------------
        resume_chunks = [
            chunk.strip()
            for chunk in resume_raw.split("\n")
            if len(chunk.strip()) > 20
        ]

        if not resume_chunks:
            resume_chunks = [resume_clean]

        resume_embeddings = self.model.encode(resume_chunks)

        # -----------------------------
        # Skill Matching
        # -----------------------------
        matched_skills = []
        missing_skills = []
        skill_match_count = 0

        for skill in jd_skills:

            skill_embedding = self.model.encode([skill])[0]

            similarity_score = SimilarityEngine.max_similarity(
                skill_embedding,
                resume_embeddings
            )

            if similarity_score >= SKILL_SIM_THRESHOLD:
                skill_match_count += 1
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

        skill_score = skill_match_count / max(len(jd_skills), 1)

        # -----------------------------
        # Overall Semantic Similarity
        # -----------------------------
        resume_embedding = self.model.encode([resume_clean])[0]
        jd_embedding = self.model.encode([jd_clean])[0]

        semantic_score = SimilarityEngine.similarity(
            resume_embedding,
            jd_embedding
        )

        # -----------------------------
        # Experience Score
        # -----------------------------
        resume_exp = ExperienceExtractor.extract_years(resume_raw)
        jd_exp = ExperienceExtractor.extract_years(jd_text)

        if jd_exp == 0:
            experience_score = 1
        else:
            experience_score = min(resume_exp / jd_exp, 1)

        # -----------------------------
        # Final Score
        # -----------------------------
        raw_score = WeightedScorer.compute(
            skill_score,
            semantic_score,
            experience_score
        )

        normalized_score = WeightedScorer.normalize(raw_score)
        category = WeightedScorer.categorize(normalized_score)
        confidence = WeightedScorer.confidence(
            skill_score,
            semantic_score
        )

        # -----------------------------
        # Return Output
        # -----------------------------
        return {
            "fit_score": normalized_score,
            "category": category,
            "confidence": confidence,
            "skill_score": round(skill_score, 4),
            "semantic_score": round(semantic_score, 4),
            "experience_score": round(experience_score, 4),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "explanation": ATS.generate_explanation(
                skill_score,
                semantic_score,
                experience_score
            )
        }