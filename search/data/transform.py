import logging
import re

import click
import numpy as np
import pandas as pd

import paths


logger = logging.getLogger(__name__)


SEARCH_PHRASES = [
    "",
    "daj mi",
    "daj",
    "hocu",
    "kupi",
    "kupujem",
    "nadji mi",
    "nadji",
    "pronadji",
    "trazi",
    "trazim",
]

LOCATION_PHRASES = [
    "",
    "blizu",
    "grad",
    "kod",
    "lokacija",
    "mesto",
    "okolina",
    "pored",
    "u okolini",
    "u",
    "unutar",
]


def _ad_to_line(ad) -> str:
    category = re.sub("-", " ", ad["category"])
    sub_category = re.sub("-", " ", ad["sub_category"])
    name = re.sub("\\W", " ", ad["name"])
    description = re.sub("\\W", " ", ad["description"])
    location = re.sub("\\W", " ", ad["location"])

    search_phrase = np.random.choice(SEARCH_PHRASES)
    location_phrase = np.random.choice(LOCATION_PHRASES)

    line = (
        f"{search_phrase} {name} {category} {sub_category} "
        f"{description} {location_phrase} {location}"
    )
    line = re.sub("\\s+", " ", line).strip().lower()
    return line


@click.command()
def transform() -> None:
    """Transforms raw ads to text lines.

    Raw ad rows from CSV file are converted into text lien suitable for fastText
    unsupervised model training. Output text lines are used to train distributed
    word vectors.

    Transformed, processed lines are saved to 'data/processed/ads.txt'.

    """
    ads_df = pd.read_csv(paths.RAW_ADS_FILE)
    ads_df.fillna("", inplace=True)

    logger.info(f"Loaded {ads_df.shape[0]} ads")

    lines = ads_df.apply(_ad_to_line, axis=1)

    with open(paths.PROCESSED_ADS_FILE, "w") as fp:
        fp.writelines("\n".join(lines))

    logger.info(f"Transformed ads saved to '{paths.PROCESSED_ADS_FILE}'")


if __name__ == "__main__":
    transform()
