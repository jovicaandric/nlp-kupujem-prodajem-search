import logging
import os
import re
from collections import defaultdict
from typing import List, Dict, Tuple, Optional

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


logger = logging.getLogger("analyzer.location.model")

LocationReverseIndex = Dict[str, str]


def _make_ngrams(text: str, n: int) -> List[str]:
    tokens = text.split()
    ngrams = []
    for i in range(0, len(tokens) - n + 1):
        words = tokens[i : i + n]
        ngrams.append(" ".join(words))
    return ngrams


def _read_location_tokens(
    locations_filepath: str, separator: str = ","
) -> Tuple[LocationReverseIndex, List[str]]:
    reverse_index: LocationReverseIndex = {}
    location_tokens: List[str] = []
    with open(locations_filepath, "r") as fp:
        for line in fp.read().split("\n"):
            tokens = line.split(separator)
            location_tokens.extend(tokens)
            location = tokens[0]
            for token in tokens:
                reverse_index[token] = location
    return reverse_index, location_tokens


class AdLocationClassificator:
    def __init__(self, confidence_threshold: float = 0.65):
        self.confidence_threshold = confidence_threshold

        current_dir = os.path.dirname(os.path.abspath(__file__))
        locations_path = os.path.join(current_dir, "locations")
        self._location_reverse_index, self._location_tokens = _read_location_tokens(
            locations_path
        )

        # The number of different locations is finite and relatively small (~200)
        # so vectorizer can be fit on initialization.
        self._vectorizer = CountVectorizer(
            ngram_range=(2, 3), analyzer="char_wb", strip_accents="ascii"
        )
        self._location_vectors = self._vectorizer.fit_transform(self._location_tokens)

    def predict(self, query: str) -> Optional[str]:
        if not query:
            raise ValueError("Empty query")

        clean_query = re.sub("\\W", " ", query).lower()

        query_word_ngrams = []
        for n in [1, 2, 3]:
            ngrams = _make_ngrams(text=clean_query, n=n)
            query_word_ngrams.extend(ngrams)

        query_ngram_vectors = self._vectorizer.transform(query_word_ngrams)
        similarities = cosine_similarity(query_ngram_vectors, self._location_vectors)

        max_indices = similarities.argmax(axis=1)
        max_similarities = similarities[range(len(query_word_ngrams)), max_indices]

        location_scores = defaultdict(list)
        for index, similarity in zip(max_indices, max_similarities):
            if similarity > self.confidence_threshold:
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

        logger.debug(f"Classified '{prediction}' as location for query: '{query}'")

        return prediction
