import logging
import os
import pickle
from functools import partial
from typing import Tuple, Dict, Iterable

import click
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

import paths


click.option = partial(click.option, show_default=True)


logger = logging.getLogger("analyzer.category.train_tf")

TrainTestSplit = Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]

MAX_NUM_WORDS = 64_000
MAX_SEQUENCE_LEN = 35
EMBEDDING_DIM = 256


class CategoryLabelEncoder:
    """Encodes string ad categories into int labels.

    String category lables are encoded into ints in rage [0, num_categories].
    This encoding is suitable for sparse categorical crossentropy loss.

    """

    def __init__(self):
        self._cat_to_label: Dict[str, int] = {}
        self._label_to_cat: Dict[int, str] = {}

    def fit(self, categories: Iterable[str]) -> None:
        unique_categories = set(categories)
        for index, category in enumerate(unique_categories):
            if category not in self._cat_to_label:
                self._cat_to_label[category] = index
                self._label_to_cat[index] = category

    def transform(self, categories: Iterable[str]) -> np.ndarray:
        labels = np.array(
            [self._cat_to_label[category] for category in categories], dtype=np.uint8
        )
        return labels

    def fit_transform(self, categories: Iterable[str]) -> np.ndarray:
        self.fit(categories)
        return self.transform(categories)

    def num_classes(self) -> int:
        return len(self._cat_to_label)


def tokenize_texts(
    texts: np.ndarray, max_num_words: int, max_sequence_len: int
) -> Tuple[Tokenizer, np.ndarray]:
    tokenizer = Tokenizer(num_words=max_num_words)
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    padded_sequences = pad_sequences(sequences, maxlen=max_sequence_len)
    return tokenizer, padded_sequences


def split_dataset(data: np.ndarray, test_size: float = 0.25) -> TrainTestSplit:
    test_data_index = int(data.shape[0] * test_size)
    test_data = data[:test_data_index, :]
    train_data = data[test_data_index:, :]

    x_train = train_data["sample"].values
    y_train = train_data["label"].values

    x_test = test_data["sample"].values
    y_test = test_data["label"].values

    return x_train, y_train, x_test, y_test


def load_embedding_index(embedding_dim: int) -> Dict[str, np.ndarray]:
    embeddings_index = {}

    with open(paths.fasttext_model_file(embedding_dim, "vec"), "r") as fp:
        for line in fp:
            values = line.split()

            # First line is in form (num_words, embedding_dim).
            if len(values) == 2:
                continue

            word = values[0]
            vector = np.asarray(values[1:], dtype="float32")
            embeddings_index[word] = vector

    return embeddings_index


def load_word_vectors(
    word_index: Dict[str, int],
    embeddings_index: Dict[str, np.ndarray],
    embedding_dim: int,
    max_num_words: int,
) -> np.ndarray:
    embedding_matrix = np.zeros((max_num_words + 1, embedding_dim))

    for word, i in word_index.items():
        if i >= max_num_words:
            continue

        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

    return embedding_matrix


def create_model(
    target_size: int,
    embedding_weights: np.ndarray,
    sequence_length: int,
    vocab_size: int,
    embedding_dim: int,
    recurrent_units: int = 256,
    dense_units: int = 512,
):
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Embedding(
                vocab_size,
                embedding_dim,
                weights=embedding_weights,
                input_length=sequence_length,
                trainable=False,
            ),
            tf.keras.layers.Bidirectional(tf.keras.layers.GRU(recurrent_units)),
            tf.keras.layers.Dense(dense_units, activation="relu"),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(target_size, activation="softmax"),
        ]
    )

    model.compile(
        loss=tf.keras.losses.SparseCategoricalCrossentropy(),
        optimizer=tf.keras.optimizers.Adam(),
        metrics=["sparse_categorical_accuracy"],
    )

    return model


@click.command()
@click.option(
    "--embedding_dim", type=int, default=EMBEDDING_DIM, help="Size of word vectors."
)
@click.option(
    "--max_num_words",
    type=int,
    default=MAX_NUM_WORDS,
    help="Number of words considered by tokenizer.",
)
@click.option(
    "--max_sequence_len",
    type=int,
    default=MAX_SEQUENCE_LEN,
    help="Length of tokenized text sequences.",
)
def train(embedding_dim: int, max_num_words: int, max_sequence_len: int) -> None:
    """Train RNN ad classification model with tensorflow.

    Note that training is in the experimental setup, where goal is to check if
    various recurrent models perform better than baseline fastText models.

    """
    cat_df = pd.read_csv(paths.CATEGORY_CLASSIFIER_DATASET_FILE)
    cat_df.dropna(inplace=True)
    cat_df = cat_df.sample(frac=1)

    label_encoder = CategoryLabelEncoder()
    label_encoder.fit(categories=cat_df.label.values)

    tokenizer, data = tokenize_texts(
        texts=cat_df["sample"].values,
        max_num_words=max_num_words,
        max_sequence_len=max_sequence_len,
    )

    with open(paths.TOKENIZER_PATH, "wb") as fp:
        pickle.dump(tokenizer, fp, protocol=pickle.HIGHEST_PROTOCOL)
        logger.info(f"Tokenizer saved to '{paths.TOKENIZER_PATH}'")

    test_data_index = int(data.shape[0] * 0.25)

    x_test = data[:test_data_index, :]
    x_train = data[test_data_index:, :]

    y_test = cat_df["label"].iloc[:test_data_index].values
    y_test = label_encoder.transform(y_test)

    y_train = cat_df["label"].iloc[test_data_index:].values
    y_train = label_encoder.transform(y_train)

    embeddings_index = load_embedding_index(embedding_dim)
    embedding_weights = load_word_vectors(
        tokenizer.word_index, embeddings_index, embedding_dim, max_num_words
    )

    target_size = label_encoder.num_classes()
    vocab_size = max_num_words + 1  # +1 for OOV token.

    model = create_model(
        target_size=target_size,
        vocab_size=vocab_size,
        embedding_weights=[embedding_weights],
        sequence_length=max_sequence_len,
        embedding_dim=embedding_dim,
    )

    model.summary()

    model.fit(
        x_train,
        y_train,
        validation_split=0.05,
        epochs=10,
        batch_size=128,
        callbacks=[
            tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=1),
            tf.keras.callbacks.ModelCheckpoint(
                os.path.join(paths.MODELS_DIR, "category_classifier.{epoch:02d}.hdf5")
            ),
        ],
    )

    [loss, accuracy] = model.evaluate(x_test, y_test)

    logger.info(f"Training done: model checkpoints are saved to '{paths.MODELS_DIR}/'")
    logger.info(f"Evaluation loss: {loss}")
    logger.info(f"Evaluation accuracy: {accuracy}")


if __name__ == "__main__":
    train()
