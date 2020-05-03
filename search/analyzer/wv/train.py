import logging
import multiprocessing as mp
from functools import partial

import click
import fasttext

import paths
from analyzer.utils import save_vec_model


click.option = partial(click.option, show_default=True)

logger = logging.getLogger("analyzer.wv.train")


EMBEDDING_DIM = 128
EPOCHS = 30
LEARNING_RATE = 0.1
LOSS = "ns"
MIN_WORD_COUNT = 2
MODEL = "skipgram"
NEGATIVE_SAMPLES = 5
WINDOW_SIZE = 5


def _save_model(model) -> None:
    dim = model.get_dimension()

    bin_model_file = paths.fasttext_model_file(module="wv", dim=dim, extension="bin")
    model.save_model(bin_model_file)
    logger.info(f"Ads word vector binary model saved to '{bin_model_file}'")

    vec_model_file = paths.fasttext_model_file(module="wv", dim=dim, extension="vec")
    save_vec_model(model, path=vec_model_file)
    logger.info(f"Ads word vector vector model saved to '{vec_model_file}'")


@click.command()
@click.option(
    "--model", type=str, default=MODEL, help="Type of model: 'cbow' or 'skipgram'"
)
@click.option(
    "--loss", type=str, default=LOSS, help="Loss function: 'ns', 'softmax', 'hs'"
)
@click.option("--dim", type=int, default=EMBEDDING_DIM, help="Word vector dimension.")
@click.option("--epochs", type=int, default=EPOCHS, help="Number of training epochs.")
@click.option(
    "--min_word_count",
    type=int,
    default=MIN_WORD_COUNT,
    help="Minimal number of word occurrences.",
)
@click.option(
    "--window_size", type=int, default=WINDOW_SIZE, help="Size of the context window.",
)
@click.option(
    "--negative_samples",
    type=int,
    default=NEGATIVE_SAMPLES,
    help="Number of negative samples.",
)
@click.option(
    "--lr",
    type=float,
    default=LEARNING_RATE,
    help="Learning rate. It should be in [0.01, 1.0].",
)
@click.option(
    "--threads",
    type=int,
    default=mp.cpu_count(),
    help="Number of threads used in training. Defaults to number of cores.",
)
def train(
    model: str,
    loss: str,
    dim: int,
    epochs: int,
    min_word_count: int,
    window_size: int,
    negative_samples: int,
    lr: float,
    threads: int,
) -> None:
    """Train word vectors on ads data.

    Word vectors are trained with fastText library. Trained word vectors are
    saved to 'models/ads.wv.{dim}.vec' and binary model to 'models/ads.wv.{dim}.bin'.

    """

    kwargs = {
        "model": model,
        "loss": loss,
        "dim": dim,
        "epoch": epochs,
        "min_count": min_word_count,
        "lr": lr,
        "thread": threads,
        "ws": 10,
        "neg": negative_samples,
    }

    logger.info(f"Starting fastText training on '{paths.PROCESSED_ADS_PATH}'")
    logger.info(f"Training args: {kwargs}")

    print()

    model = fasttext.train_unsupervised(paths.PROCESSED_ADS_PATH, **kwargs)

    print()

    _save_model(model)


if __name__ == "__main__":
    train()
