import re
from typing import Set, List, Tuple

import stanza


_NUM_PATTERNS: Set[str] = set(["ADP NUM", "ADP NUM ADP NUM"])
_ADJ_PATTERNS: Set[str] = set(["ADP ADJ", "ADP ADJ ADP ADJ"])
PATTERNS: Set[str] = _NUM_PATTERNS.union(_ADJ_PATTERNS)

NLP = stanza.Pipeline(lang="sr", processors="tokenize,pos", logging_level="WARN")

WordPosList = List[Tuple[str, str]]


class PriceRangeParser:
    def __init__(self):
        pass

    def parse(self, query: str) -> dict:
        clean_query = self._preprocess(query)
        price_range = self._parse_price_range(clean_query)
        price_query = self._parse_price_query(price_range)
        return price_query

    def _preprocess(self, query: str) -> str:
        # TODO: Replace special characters.
        return query

    def _parse_price_range(self, query: str) -> WordPosList:
        word_upos: WordPosList = [
            (word.text, word.upos) for word in NLP(query).iter_words()
        ]
        pos_tags = self._get_pos_tags(word_upos)

        price_range_candidates = []
        for pattern in PATTERNS:
            try:
                idx = pos_tags.index(pattern)
                pattern_len = len(pattern.split())

                before_words_len = len(pos_tags[:idx].split())
                price_range: WordPosList = word_upos[
                    before_words_len : before_words_len + pattern_len
                ]

                if self._is_valid_price_range(candidate=price_range, pattern=pattern):
                    price_range_candidates.append(price_range)

            except ValueError:
                pass

        if not price_range_candidates:
            return []

        price_range = max(
            price_range_candidates, key=lambda price_range: len(price_range)
        )
        return price_range

    def _is_valid_price_range(self, candidate: WordPosList, pattern: str) -> bool:
        if pattern in _NUM_PATTERNS:
            return True

        if pattern in _ADJ_PATTERNS:
            tokens = []
            if pattern == "ADP ADJ":
                _, (token, _) = candidate
                tokens.append(token)

            elif pattern == "ADP ADJ ADP ADJ":
                _, (from_token, _), _, (to_token, _) = candidate
                tokens.append(from_token)
                tokens.append(to_token)

            is_num = len(tokens) > 0 and all(
                re.sub("\\D+", "", token).isdigit() for token in tokens
            )
            return is_num

        return False

    def _parse_price_query(self, price_range: WordPosList) -> dict:
        return {w: t for w, t in price_range}

    def _get_pos_tags(self, word_pos_list: WordPosList) -> str:
        pos_tags = " ".join([upos for _, upos in word_pos_list])
        return pos_tags


if __name__ == "__main__":
    from pprint import pprint

    parser = PriceRangeParser()

    while True:
        try:
            query = input("> ").strip()

            price_range_query = parser.parse(query)
            pprint(price_range_query)
        except (KeyboardInterrupt, EOFError):
            break

    print("\nExiting...")
