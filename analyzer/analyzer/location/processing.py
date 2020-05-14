from typing import List, Dict, Tuple


LocationReverseIndex = Dict[str, str]


def make_word_ngrams(text: str, n: int) -> List[str]:
    tokens = text.split()
    ngrams = []
    for i in range(0, len(tokens) - n + 1):
        words = tokens[i : i + n]
        ngrams.append(" ".join(words))
    return ngrams


def read_location_tokens(
    locations_filepath: str, separator: str = ","
) -> Tuple[List[str], LocationReverseIndex]:
    location_tokens: List[str] = []
    reverse_index: LocationReverseIndex = {}
    with open(locations_filepath, "r") as fp:
        for line in fp.read().splitlines():
            tokens = line.split(separator)
            location_tokens.extend(tokens)
            location = tokens[0]
            for token in tokens:
                reverse_index[token] = location
    return location_tokens, reverse_index
