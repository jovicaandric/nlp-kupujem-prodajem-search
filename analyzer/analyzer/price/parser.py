import re
from collections import Counter
from typing import Set, List, Tuple, Optional

import stanza
from price_parser import Price


_NUM_PATTERNS: Set[str] = set(["ADP NUM", "ADP NUM ADP NUM"])
_ADJ_PATTERNS: Set[str] = set(
    ["ADP ADJ", "ADP ADJ ADP ADJ", "ADP NUM ADP ADJ", "ADP ADJ ADP NUM"]
)
PATTERNS: Set[str] = _NUM_PATTERNS.union(_ADJ_PATTERNS)

NLP = stanza.Pipeline(lang="sr", processors="tokenize,pos", logging_level="WARN")

WordPosList = List[Tuple[str, str]]
PriceQuery = List[Tuple[str, Optional[float]]]


class Modifier:
    NONE: str = ""
    LESS_OR_EQUAL: str = "lte"
    GREATER_OR_EQUAL: str = "gte"


class Currency:
    EUR: str = "EUR"
    RSD: str = "RSD"

    DEFAULT: str = EUR

    RSD_TOKENS: Set[str] = set(["rsd", "dinara", "dinar", "din"])
    EUR_TOKENS: Set[str] = set(["eur", "eura", "evra", "euro", "€"])


class PriceRangeParser:
    DEFAULT_FILTER = (Modifier.GREATER_OR_EQUAL, 0.0)

    def parse(self, query: str) -> Tuple[PriceQuery, Optional[str]]:
        price_range = self._parse_price_range(query)

        if not price_range:
            return [], None

        price_query, currency = self._parse_price_query(price_range)

        if all(price_filter == self.DEFAULT_FILTER for price_filter in price_query):
            return [], None

        if currency is None:
            currency = self._parse_currency(query)

        return price_query, currency

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
            pattern_len = len(pattern.split())
            tokens = []
            if pattern_len == 2:
                _, (token, _) = candidate
                tokens.append(token)

            elif pattern_len == 4:
                _, (from_token, _), _, (to_token, _) = candidate
                tokens.append(from_token)
                tokens.append(to_token)

            is_num = len(tokens) > 0 and all(
                re.sub("\\D+", "", token).isdigit() for token in tokens
            )
            return is_num

        return False

    def _get_pos_tags(self, word_pos_list: WordPosList) -> str:
        pos_tags = " ".join([upos for _, upos in word_pos_list])
        return pos_tags

    def _parse_price_query(
        self, price_range: WordPosList
    ) -> Tuple[PriceQuery, Optional[str]]:
        is_between_query = len(price_range) == 4

        currencies: List[str] = []

        query: PriceQuery
        if is_between_query:
            raw_first_mod, raw_first_price, raw_second_mod, raw_second_price = [
                word for word, _ in price_range
            ]

            first_price = Price.fromstring(raw_first_price.upper())
            if first_price.currency:
                currencies.append(first_price.currency)

            first_mod = self._parse_modifier(raw_first_mod)

            first_filter: Tuple[str, Optional[float]]
            if first_mod == Modifier.NONE or first_price.amount is None:
                first_filter = self.DEFAULT_FILTER
            else:
                first_filter = (first_mod, first_price.amount_float)

            second_price = Price.fromstring(raw_second_price.upper())
            if second_price.currency:
                currencies.append(second_price.currency)

            second_mod = self._parse_modifier(raw_second_mod)

            second_filter: Tuple[str, Optional[float]]
            if second_mod == Modifier.NONE or second_price.amount is None:
                second_filter = self.DEFAULT_FILTER
            else:
                second_filter = (second_mod, second_price.amount_float)

            query = [first_filter, second_filter]
        else:
            mod, raw_price = [word for word, _ in price_range]

            price = Price.fromstring(raw_price.upper())
            if price.currency:
                if price.currency in Currency.EUR_TOKENS:
                    currencies.append(Currency.EUR)
                if price.currency in Currency.RSD_TOKENS:
                    currencies.append(Currency.RSD)

            modifier = self._parse_modifier(mod)

            if modifier == Modifier.NONE or price.amount is None:
                query = [self.DEFAULT_FILTER]
            else:
                query = [
                    (modifier, price.amount_float),
                ]

        currency = None
        if currencies:
            [(currency, _)] = Counter(currencies).most_common(n=1)

        return query, currency

    def _parse_modifier(self, modifier: str) -> str:
        return {
            "od": Modifier.GREATER_OR_EQUAL,
            "iznad": Modifier.GREATER_OR_EQUAL,
            "do": Modifier.LESS_OR_EQUAL,
            "ispod": Modifier.LESS_OR_EQUAL,
        }.get(modifier, Modifier.NONE)

    def _parse_currency(self, query: str) -> str:
        query_lower = query.lower()
        for rsd_token in Currency.RSD_TOKENS:
            if rsd_token in query_lower:
                return Currency.RSD

        for eur_token in Currency.EUR_TOKENS:
            if eur_token in query_lower:
                return Currency.EUR

        return Currency.DEFAULT


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
