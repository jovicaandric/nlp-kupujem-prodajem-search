import logging

import click
import pandas as pd
from pandarallel import pandarallel

from .. import paths


logger = logging.getLogger("analyzer.category.transform")


@click.command()
@click.option(
    "--test_size",
    type=float,
    default=0.25,
    show_default=True,
    help="Percentage of dataset that will be used as test dataset.",
)
def transform(test_size: int) -> None:
    """Transform category classification dataset into fastText format.

    The original CSV file is split into *.train and *.test files where each file
    contains lines in form of '__label__<actual_label> sample text'.

    """
    pandarallel.initialize()

    cat_df = pd.read_csv(paths.CATEGORY_DATA_PATH)
    cat_df = cat_df.sample(frac=1)

    # Transform category dataset into fastText format.
    lines = cat_df.parallel_apply(
        lambda ad: f"__label__{ad['label']} {ad['sample']}", axis=1
    )

    test_index = int(test_size * len(lines))

    test_data = lines[:test_index]
    train_data = lines[test_index:]

    logger.info(
        f"Transformed {len(train_data)} train and {len(test_data)} test samples"
    )

    with open(paths.FASTTEXT_CATEGORY_TRAIN_PATH, "w") as fp:
        fp.writelines("\n".join(train_data))
        logger.info(f"Saved train dataset to '{paths.FASTTEXT_CATEGORY_TRAIN_PATH}'")

    with open(paths.FASTTEXT_CATEGORY_TEST_PATH, "w") as fp:
        fp.writelines("\n".join(test_data))
        logger.info(f"Saved test dataset to '{paths.FASTTEXT_CATEGORY_TEST_PATH}'")


if __name__ == "__main__":
    transform()
