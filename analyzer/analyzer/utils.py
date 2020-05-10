import re

import numpy as np
from fasttext.FastText import _FastText as FastTextModel


def convert_bin_to_vec(model: FastTextModel) -> np.ndarray:
    """Convert binary fastText model to word vectors model."""
    word_vectors = np.zeros((len(model.words), model.get_dimension() + 1), dtype=object)

    for idx, word in enumerate(model.words):
        vector = model.get_word_vector(word)
        word_vectors[idx][0] = word
        word_vectors[idx][1:] = vector

    return word_vectors


def save_vec_model(model: FastTextModel, path: str) -> None:
    """Save vector fastText model.

    Binary fastText model is covnerted to vecotr model and saved to PATH.vec
    file in the following format:

    n d
    word_1 w_1 w_2 w_3 ... w_d
    word_2 w_1 w_2 w_3 ... w_d
    .
    .
    .
    word_n w_1 w_2 w_3 ... w_d

    """
    num_words = len(model.words)
    dim = model.get_dimension()

    vec_model = convert_bin_to_vec(model)

    np.savetxt(
        path,
        vec_model,
        header=f"{num_words} {dim}",
        fmt=["%s"] + ["%.12e"] * dim,
        delimiter=" ",
        comments="",
    )


def remove_non_text_chars(text: str) -> str:
    return re.sub("\\W", " ", text)


def remove_redundant_whitespaces(text: str) -> str:
    return re.sub("\\s+", " ", text).strip()
