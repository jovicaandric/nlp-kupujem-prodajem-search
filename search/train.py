import logging
import multiprocessing as mp

import click
import fasttext

import paths


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(module)s %(levelname)s: %(message)s"
)

logger = logging.getLogger(__name__)


EMBEDDING_DIM = 128
EPOCHS = 20
LEARNING_RATE = 0.025
LOSS = "ns"
MIN_WORD_COUNT = 3
MODEL = "skipgram"


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
    lr: float,
    threads: int,
) -> None:
    """Train word vectors on ads data.

    Word vectors are trained with fastText library. Trained word vectors are
    saved to 'models/ads.{dim}.bin'.

    """

    kwargs = {
        "model": model,
        "loss": loss,
        "dim": dim,
        "epoch": epochs,
        "min_count": min_word_count,
        "lr": lr,
        "thread": threads,
    }

    logger.info(f"Starting fastText training on '{paths.PROCESSED_ADS_FILE}'")
    logger.info(f"Training args: {kwargs}")

    print()

    model = fasttext.train_unsupervised(paths.PROCESSED_ADS_FILE, **kwargs)
    model_file = paths.fasttext_model_file(dim)
    model.save_model(model_file)

    print()

    logger.info(f"Model saved to '{model_file}'")


if __name__ == "__main__":
    train()
