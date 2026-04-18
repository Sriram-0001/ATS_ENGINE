import numpy as np


class Evaluator:

    @staticmethod
    def evaluate(results, ground_truth_scores):
        predicted = [r["final_score"] for r in results]
        correlation = np.corrcoef(predicted, ground_truth_scores)[0, 1]
        return correlation