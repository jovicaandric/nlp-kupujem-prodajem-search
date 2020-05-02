import logging
import multiprocessing as mp

import click
import fasttext
import numpy as np

import paths


logger = logging.getLogger("analyzer.wv.train")


EMBEDDING_DIM = 128
EPOCHS = 20
LEARNING_RATE = 0.025
LOSS = "ns"
MIN_WORD_COUNT = 3
MODEL = "skipgram"


def _create_vec_model(model) -> np.ndarray:
    word_vectors = np.zeros((len(model.words), model.get_dimension() + 1), dtype=object)

    for idx, word in enumerate(model.words):
        vector = model.get_word_vector(word)
        word_vectors[idx][0] = word
        word_vectors[idx][1:] = vector

    return word_vectors


def _save_model(model) -> None:
    dim = model.get_dimension()

    bin_model_file = paths.fasttext_model_file(dim, extension="bin")
    model.save_model(bin_model_file)

    logger.info(f"Binary model saved to '{bin_model_file}'")

    vec_model = _create_vec_model(model)
    vec_model_file = paths.fasttext_model_file(dim, extension="vec")

    num_words = len(model.words)

    np.savetxt(
        vec_model_file,
        vec_model,
        header=f"{num_words} {dim}",
        fmt=["%s"] + ["%.12e"] * dim,
        delimiter=" ",
        comments="",
    )

    logger.info(f"Vector model saved to '{vec_model_file}'")


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

    print()

    _save_model(model)


if __name__ == "__main__":
    train()
