import logging
import re
from typing import List, Tuple

import click
import numpy as np
import pandas as pd
from pandarallel import pandarallel

import paths


logger = logging.getLogger(__name__)

pandarallel.initialize()


SEARCH_PHRASES = [
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


def _remove_non_text_chars(text: str) -> str:
    return re.sub("\\W", " ", text)


def _remove_redundant_whitespaces(text: str) -> str:
    return re.sub("\\s+", " ", text).strip()


def _convert_ad_to_text_line(ad: pd.Series) -> str:
    category = re.sub("-", " ", ad["category"])
    sub_category = re.sub("-", " ", ad["sub_category"])
    name = re.sub("\\W", " ", ad["name"])
    description = re.sub("\\W", " ", ad["description"])
    location = re.sub("\\W", " ", ad["location"])

    prob = np.random.random()
    search_phrase = np.random.choice(SEARCH_PHRASES) if prob > 0.7 else ""
    location_phrase = np.random.choice(LOCATION_PHRASES) if prob > 0.2 else ""

    line = (
        f"{search_phrase} {name} {category} {sub_category} "
        f"{description} {location_phrase} {location}"
    )
    line = _remove_redundant_whitespaces(line)
    line = line.lower()

    return line


def _make_ad_text_lines(ads_df: pd.DataFrame) -> None:
    lines = ads_df.parallel_apply(_convert_ad_to_text_line, axis=1)

    with open(paths.PROCESSED_ADS_FILE, "w") as fp:
        fp.writelines("\n".join(lines))

    logger.info(f"Transformed ads saved to '{paths.PROCESSED_ADS_FILE}'")


def _convert_ad_to_category_classification_sample(
    ad: pd.Series,
) -> List[Tuple[str, str]]:
    name = _remove_non_text_chars(ad["name"])
    description = _remove_non_text_chars(ad["description"])
    sub_category = _remove_non_text_chars(ad["sub_category"])

    sample = f"{name} {sub_category} {description}"
    sample = _remove_redundant_whitespaces(sample)
    sample = sample.lower()
    label = ad.category.lower()

    return sample, label


def _make_category_classification_samples(ads_df: pd.DataFrame) -> None:
    samples = ads_df.parallel_apply(
        _convert_ad_to_category_classification_sample, axis=1
    )

    ad_category_df = pd.DataFrame.from_records(samples, columns=["sample", "label"])
    ad_category_df.to_csv(paths.CATEGORY_CLASSIFICATION_FILE, index=False)

    logger.info(
        f"Ad category classification dataset saved to '{paths.CATEGORY_CLASSIFICATION_FILE}'"
    )


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

    _make_ad_text_lines(ads_df)
    _make_category_classification_samples(ads_df)


if __name__ == "__main__":
    transform()
