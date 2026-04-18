from sentence_transformers import SentenceTransformer, util

class SemanticSkillMatcher:

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def match_skills(self, resume_skills, jd_skills, threshold=0.6):

        matched = []
        missing = []

        for jd_skill in jd_skills:

            # ✅ FIRST: direct match (VERY IMPORTANT)
            if jd_skill in resume_skills:
                matched.append(jd_skill)
                continue

            # ✅ SECOND: semantic fallback
            jd_emb = self.model.encode(jd_skill, convert_to_tensor=True)
            resume_embs = self.model.encode(resume_skills, convert_to_tensor=True)

            scores = util.cos_sim(jd_emb, resume_embs)[0]
            max_score = scores.max().item()

            if max_score >= threshold:
                matched.append(jd_skill)
            else:
                missing.append(jd_skill)

        return matched, missing