import hashlib
import numpy as np


class EmbeddingCache:
    def __init__(self):
        self.cache = {}

    def _hash(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    def get(self, text):
        return self.cache.get(self._hash(text))

    def set(self, text, embedding):
        self.cache[self._hash(text)] = embedding