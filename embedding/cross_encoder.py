from sentence_transformers import CrossEncoder
import numpy as np

class ATSCrossEncoder:

    def __init__(self):
        self.model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

    def score(self, resume, jd):

        score = self.model.predict([(resume, jd)])[0]

        # 🔥 normalize
        semantic_score = 1 / (1 + np.exp(-score))

        # ✅ NOW this is valid
        print("SEMANTIC SCORE:", semantic_score)

        return float(semantic_score)