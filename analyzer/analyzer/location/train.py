import logging
import os
import pickle
from typing import Tuple

import click
from sklearn.feature_extraction.text import CountVectorizer

from .. import paths
from .processing import read_location_tokens


logger = logging.getLogger("analyzer.location.train")

current_dir = os.path.dirname(os.path.abspath(__file__))
LOCATIONS_PATH = os.path.join(current_dir, "locations")


@click.command()
@click.option(
    "--ngram-range",
    type=(int, int),
    default=(2, 3),
    help="The lower and upper boundary of the range of n-values for word or char n-grams.",
    show_default=True,
)
@click.option(
    "--analyzer",
    type=str,
    default="char_wb",
    help="Whether the feature should be made of word n-gram or character n-grams.",
    show_default=True,
)
@click.option(
    "--strip-accents",
    type=str,
    default="ascii",
    help="Remove accents and perform other character normalization.",
    show_default=True,
)
@click.option(
    "--locations-path",
    type=str,
    default=LOCATIONS_PATH,
    help="Path to file with locations. Each line corresponds to one location variants.",
    show_default=True,
)
def train(
    ngram_range: Tuple[int, int], analyzer: str, strip_accents: str, locations_path: str
) -> None:
    """Train n-gram vectorizer on location data."""
    kwargs = {
        "ngram_range": ngram_range,
        "analyzer": analyzer,
        "strip_accents": strip_accents,
    }

    logger.info(f"Starting locations n-gram vectorizer training on '{locations_path}'")
    logger.info(f"Training args: {kwargs}")

    vectorizer = CountVectorizer(**kwargs)

    location_tokens, _ = read_location_tokens(locations_path)
    vectorizer.fit(location_tokens)

    with open(paths.LOCATIONS_VECTORIZER_PATH, "wb") as fp:
        pickle.dump(vectorizer, fp, protocol=pickle.HIGHEST_PROTOCOL)

    logger.info(
        f"Locations n-gram vectorizer saved to '{paths.LOCATIONS_VECTORIZER_PATH}'"
    )


if __name__ == "__main__":
    train()
