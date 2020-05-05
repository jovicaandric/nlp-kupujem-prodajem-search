import logging

import fasttext

import paths


logger = logging.getLogger("analyzer.category.model")


class AdCategoryClassifier:
    def __init__(self, dim: int = 100, confidence_threshold: float = 0.7):
        self.confidence_threshold = confidence_threshold
        self._label_tag = "__label__"

        model_path = paths.fasttext_model_file("category", dim=dim, extension="bin")
        self._model = fasttext.load_model(model_path)

        logger.info("Ad category classifier model loaded")

    def predict(self, query: str) -> str:
        predictions = self._model.predict(query)
        category = predictions[0][0].replace(self._label_tag, "")
        confidence = predictions[1][0]
        return category, confidence
