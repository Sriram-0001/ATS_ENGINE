from sentence_transformers import SentenceTransformer
import torch


class Embedder:
    _model = None

    @classmethod
    def load_model(cls, model_name):
        if cls._model is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            cls._model = SentenceTransformer(model_name, device=device)
        return cls._model

    @classmethod
    def encode(cls, texts):
        if isinstance(texts, str):
            texts = [texts]

        return cls._model.encode(
            texts,
            convert_to_numpy=True,
            batch_size=16,
            show_progress_bar=False
        )