import fasttext

import paths


class AdCategoryClassifier:
    def __init__(self, dim: int = 100, confidence_threshold: float = 0.8):
        self.confidence_threshold = confidence_threshold

        model_path = paths.fasttext_model_file("category", dim=dim, extension="bin")
        self._model = fasttext.load_model(model_path)
        self._label_tag = "__label__"

    def predict(self, query: str) -> str:
        predictions = self._model.predict(query)
        category = predictions[0][0].replace(self._label_tag, "")
        confidence = predictions[1][0]
        return category, confidence
