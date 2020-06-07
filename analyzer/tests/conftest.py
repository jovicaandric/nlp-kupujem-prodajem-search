from typing import List

import numpy as np
import pytest


class MockFastTextModel:
    def __init__(self, words: List[str], dim: int = 5) -> None:
        self.words = words
        self.dim = dim
        self._word_vectors = {word: np.random.rand(dim) for word in words}

    def get_dimension(self) -> int:
        return self.dim

    def get_word_vector(self, word: str) -> np.ndarray:
        return self._word_vectors[word]


@pytest.fixture
def mock_fasttext_model():
    model = MockFastTextModel(words=["this", "is", "a", "test", "model"])
    return model
