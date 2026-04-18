import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class SimilarityEngine:

    @staticmethod
    def similarity(vec_a, vec_b):
        return cosine_similarity([vec_a], [vec_b])[0][0]

    @staticmethod
    def max_similarity(vec, matrix):
        sims = cosine_similarity([vec], matrix)
        return float(np.max(sims))