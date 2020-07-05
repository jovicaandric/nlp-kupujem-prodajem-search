import logging
import os
import pickle
from collections import defaultdict
from typing import Optional

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .. import utils
from ..predictor import BasePredictor
from .processing import make_word_ngrams, read_location_tokens


logger = logging.getLogger("analyzer.location.predictor")


class AdLocationPredictor(BasePredictor):
    def __init__(self, vectorizer: CountVectorizer, confidence_threshold: float = 0.65):
        self._confidence_threshold = confidence_threshold

        current_dir = os.path.dirname(os.path.abspath(__file__))
        locations_path = os.path.join(current_dir, "locations")
        self._location_tokens, self._location_reverse_index = read_location_tokens(
            locations_path
        )

        self._vectorizer = vectorizer
        self._location_vectors = self._vectorizer.fit_transform(self._location_tokens)

    @classmethod
    def from_path(cls, path: str) -> "AdLocationPredictor":
        with open(path, "rb") as fp:
            vectorizer = pickle.load(fp)

        logger.info("Ad location predictor initialized")

        return cls(vectorizer)

    def predict(self, user_query: str) -> Optional[str]:
        clean_query = utils.remove_non_text_chars(text=user_query.lower())

        query_word_ngrams = []
        for n in [1, 2, 3]:
            ngrams = make_word_ngrams(text=clean_query, n=n)
            query_word_ngrams.extend(ngrams)

        query_ngram_vectors = self._vectorizer.transform(query_word_ngrams)
        similarities = cosine_similarity(query_ngram_vectors, self._location_vectors)

        max_indices = similarities.argmax(axis=1)
        max_similarities = similarities[range(len(query_word_ngrams)), max_indices]

        location_scores = defaultdict(list)
        for index, similarity in zip(max_indices, max_similarities):
            if similarity > self._confidence_threshold:
                location_token = self._location_tokens[index]
                location_scores[location_token].append(similarity)

        prediction: Optional[str]
        if location_scores:
            best_location_token, _ = max(
                location_scores.items(), key=lambda pair: sum(pair[1])
            )
            prediction = self._location_reverse_index.get(best_location_token)
        else:
            prediction = None

        logger.debug(f"Predicted '{prediction}' as location for query: '{user_query}'")

        return prediction
