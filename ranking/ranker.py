class Ranker:

    @staticmethod
    def rank(results):
        return sorted(results, key=lambda x: x["final_score"], reverse=True)