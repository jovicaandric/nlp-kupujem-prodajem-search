import logging
import re
from typing import List, Tuple

import click
import numpy as np
import pandas as pd
from pandarallel import pandarallel

from .. import paths, utils


logger = logging.getLogger("analyzer.data.transform")

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
    "iz",
    "kod",
    "lokacija",
    "mesto",
    "okolina",
    "pored",
    "u okolini",
    "u",
    "unutar",
]


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
    line = utils.remove_redundant_whitespaces(line)
    line = line.lower()

    return line


def _make_ad_text_lines(ads_df: pd.DataFrame) -> List[str]:
    lines = ads_df.parallel_apply(_convert_ad_to_text_line, axis=1)
    return lines


def _transform_ads_to_text_lines(ads_df: pd.DataFrame) -> None:
    lines = _make_ad_text_lines(ads_df)

    with open(paths.PROCESSED_ADS_PATH, "w") as fp:
        fp.writelines("\n".join(lines))

    logger.info(f"Transformed ads saved to '{paths.PROCESSED_ADS_PATH}'")


def _convert_ad_to_category_classification_sample(ad: pd.Series,) -> Tuple[str, str]:
    name = utils.remove_non_text_chars(ad["name"])
    description = utils.remove_non_text_chars(ad["description"])

    sample = f"{name} {description}"
    sample = utils.remove_redundant_whitespaces(sample)
    sample = sample.lower()
    label = ad.category.lower()

    return sample, label


def _make_category_classification_samples(ads_df: pd.DataFrame) -> pd.DataFrame:
    ad_samples = ads_df.parallel_apply(
        _convert_ad_to_category_classification_sample, axis=1
    )

    # Make (sub_category, category) dataset pairs.
    sub_category_samples = (
        ads_df[["sub_category", "category"]]
        .drop_duplicates()
        .parallel_apply(
            lambda row: (
                utils.remove_non_text_chars(row.sub_category).lower(),
                row.category.lower(),
            ),
            axis=1,
        )
    )

    samples = ad_samples.append(sub_category_samples, ignore_index=True)
    ad_category_df = pd.DataFrame.from_records(samples, columns=["sample", "label"])
    ad_category_df = ad_category_df.sample(frac=1)
    return ad_category_df


def _transform_ads_to_category_classification_samples(ads_df: pd.DataFrame) -> None:
    ad_category_df = _make_category_classification_samples(ads_df)
    ad_category_df.to_csv(paths.CATEGORY_DATA_PATH, index=False)

    logger.info(
        f"Ad category classification dataset saved to '{paths.CATEGORY_DATA_PATH}'"
    )


def _make_locations(ads_df: pd.DataFrame) -> List[str]:
    unique_locations = ads_df.location.dropna().unique()

    locations = []
    for location in sorted(unique_locations):
        clean_location = utils.remove_non_text_chars(location)
        clean_location = utils.remove_redundant_whitespaces(clean_location)

        if clean_location:
            locations.append(clean_location)

    return locations


def _transform_ads_to_locations(ads_df: pd.DataFrame) -> None:
    locations = _make_locations(ads_df)

    with open(paths.LOCATIONS_PATH, "w") as fp:
        fp.writelines("\n".join(locations))

    logger.info(f"Ads locations saved to '{paths.LOCATIONS_PATH}'")


@click.command()
def transform() -> None:
    """Transforms raw ads to text lines.

    Raw ad rows from CSV file are converted into text lien suitable for fastText
    unsupervised model training. Output text lines are used to train distributed
    word vectors.

    Transformed, processed ad lines are saved to 'data/processed/ads.txt'.
    Ads category classification samples are saved to 'data/interim/categories.csv'.
    Ads locations are saved to 'data/processed/locations.txt'.

    """
    ads_df = pd.read_csv(paths.RAW_ADS_PATH)
    ads_df.fillna("", inplace=True)

    logger.info(f"Loaded {ads_df.shape[0]} ads")

    _transform_ads_to_text_lines(ads_df)
    _transform_ads_to_category_classification_samples(ads_df)
    _transform_ads_to_locations(ads_df)


if __name__ == "__main__":
    transform()
