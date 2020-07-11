import logging
import os
import pickle
from collections import defaultdict
from typing import Optional, List, Tuple

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

    def predict(self, user_query: str) -> Tuple[Optional[str], str]:
        clean_query = utils.remove_non_text_chars(text=user_query.lower())

        query_word_ngrams = []
        for n in [1, 2, 3]:
            ngrams = make_word_ngrams(text=clean_query, n=n)
            query_word_ngrams.extend(ngrams)

        query_ngram_vectors = self._vectorizer.transform(query_word_ngrams)
        similarities = cosine_similarity(query_ngram_vectors, self._location_vectors)

        max_indices = similarities.argmax(axis=1)
        max_similarities = similarities[range(len(query_word_ngrams)), max_indices]

        location_similarity_scores = defaultdict(list)
        location_token_to_ngram_indices = defaultdict(list)
        for ngram_index, (index, similarity) in enumerate(
            zip(max_indices, max_similarities)
        ):
            if similarity > self._confidence_threshold:
                location_token = self._location_tokens[index]
                location_similarity_scores[location_token].append(similarity)

                # Store ngram indices to track which part of input query
                # corresponds to predicted location.
                location_token_to_ngram_indices[location_token].append(ngram_index)

        location: Optional[str] = None
        location_query_words: Optional[str] = None
        if location_similarity_scores:
            best_location_token, _ = max(
                location_similarity_scores.items(), key=lambda pair: sum(pair[1])
            )
            location = self._location_reverse_index.get(best_location_token)
            location_query_words = self._get_location_query_words(
                location_token_to_ngram_indices[best_location_token], query_word_ngrams
            )

        if location_query_words:
            new_query = user_query.replace(location_query_words, "")
        else:
            new_query = user_query

        return location, new_query

    def _get_location_query_words(
        self, ngram_indices: List[int], ngrams: List[str]
    ) -> str:
        words = max(
            [ngrams[idx] for idx in ngram_indices], key=lambda ngram: len(ngram.split())
        )
        return words
