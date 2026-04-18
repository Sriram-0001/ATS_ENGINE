EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"

# Similarity thresholds
SKILL_SIM_THRESHOLD = 0.60
SEMANTIC_SIM_THRESHOLD = 0.65

# Score Weights (balanced & realistic)
WEIGHTS = {
    "skill": 0.45,
    "semantic": 0.35,
    "experience": 0.20
}