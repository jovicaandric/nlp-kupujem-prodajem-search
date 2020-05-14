import os

import numpy as np
import pytest

from analyzer import utils


def test_convert_bin_to_vec(mock_fasttext_model):
    vec_model = utils.convert_bin_to_vec(mock_fasttext_model)

    # dim + 1 because word is in the first place of one row.
    expected_shape = (len(mock_fasttext_model.words), mock_fasttext_model.dim + 1)
    assert vec_model.shape == expected_shape

    for row in vec_model:
        word = row[0]
        vector = row[1:]
        assert (mock_fasttext_model.get_word_vector(word) == vector).all()


def test_save_vec_model(mock_fasttext_model, tmpdir):
    model_path = os.path.join(tmpdir, "test_model.vec")
    utils.save_vec_model(mock_fasttext_model, path=model_path)

    assert os.path.exists(model_path)

    with open(model_path, "r") as fp:
        saved_model_lines = fp.read().splitlines()

    header = saved_model_lines[0]
    expected_header = f"{len(mock_fasttext_model.words)} {mock_fasttext_model.dim}"
    assert header == expected_header

    for line in saved_model_lines[1:]:
        tokens = line.split()
        word = tokens[0]
        vector = np.around(np.array(tokens[1:], dtype=np.float), 12)
        expected_vector = np.around(mock_fasttext_model.get_word_vector(word), 12)
        np.testing.assert_allclose(vector, expected_vector)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("", ""),
        (" ", " "),
        ("+a", " a"),
        (".a", " a"),
        ("0a", "0a"),
        ("a", "a"),
        ("1", "1"),
    ],
)
def test_remove_non_text_chars(text, expected):
    assert utils.remove_non_text_chars(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("", ""),
        (" ", ""),
        ("\t", ""),
        ("\t\t", ""),
        ("\n", ""),
        (" a ", "a"),
        (" a\t\tb\t\tc ", "a b c"),
    ],
)
def test_remove_redundant_whitespaces(text, expected):
    assert utils.remove_redundant_whitespaces(text) == expected
