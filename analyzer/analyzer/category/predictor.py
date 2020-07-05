import logging
from typing import Optional

import fasttext
from fasttext.FastText import _FastText as FastTextModel

from ..predictor import BasePredictor


logger = logging.getLogger("analyzer.category.predictor")


class AdCategoryPredictor(BasePredictor):
    def __init__(self, model: FastTextModel, confidence_threshold: float = 0.75):
        self._model = model
        self._confidence_threshold = confidence_threshold
        self._label_tag = "__label__"

    @classmethod
    def from_path(cls, path: str) -> "AdCategoryPredictor":
        model = fasttext.load_model(path)

        logger.info("Ad category predictor initialized")

        return cls(model)

    def predict(self, user_query: str) -> Optional[str]:
        predictions = self._model.predict(user_query)
        category = predictions[0][0].replace(self._label_tag, "")
        confidence = predictions[1][0]
        prediction = category if confidence > self._confidence_threshold else None
        return prediction
