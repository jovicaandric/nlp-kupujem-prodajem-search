import logging
import multiprocessing as mp

import click
import fasttext

from .. import paths


logger = logging.getLogger("analyzer.category.train")

EMBEDDING_DIM = 100
WORD_NGRAMS = 2
EPOCHS = 30
LEARNING_RATE = 0.1


@click.command()
@click.option(
    "--dim",
    type=int,
    default=EMBEDDING_DIM,
    help="Word vector dimension.",
    show_default=True,
)
@click.option(
    "--word_ngrams",
    type=int,
    default=WORD_NGRAMS,
    help="Max length of word ngrams.",
    show_default=True,
)
@click.option(
    "--epochs",
    type=int,
    default=EPOCHS,
    help="Number of training epochs.",
    show_default=True,
)
@click.option(
    "--lr",
    type=float,
    default=LEARNING_RATE,
    help="Learning rate. It should be in [0.01, 1.0].",
    show_default=True,
)
@click.option(
    "--threads",
    type=int,
    default=mp.cpu_count(),
    help="Number of threads used in training. Defaults to number of cores.",
    show_default=True,
)
def train(dim: int, word_ngrams: int, epochs: int, lr: float, threads: int) -> None:
    pretrained_vectors_path = paths.fasttext_model_file(
        module="wv", dim=dim, extension="vec"
    )

    kwargs = {
        "dim": dim,
        "epoch": epochs,
        "word_ngrams": word_ngrams,
        "lr": lr,
        "thread": threads,
        "pretrained_vectors": pretrained_vectors_path,
    }

    logger.info(f"Starting fastText training on '{paths.FASTTEXT_CATEGORY_TRAIN_PATH}'")
    logger.info(f"Training args: {kwargs}")

    print()

    model = fasttext.train_supervised(paths.FASTTEXT_CATEGORY_TRAIN_PATH, **kwargs)

    print()

    [test_samples, precision, recall] = model.test(paths.FASTTEXT_CATEGORY_TEST_PATH)

    print()

    logger.info(f"Tested on {test_samples} samples")
    logger.info(f"Precision@1 = {precision:.4f}")
    logger.info(f"Recall@1    = {recall:.4f}")

    dim = model.get_dimension()
    model_file = paths.fasttext_model_file(module="category", dim=dim, extension="bin")
    model.save_model(model_file)

    logger.info(f"Ads category classification model saved to '{model_file}'")


if __name__ == "__main__":
    train()
