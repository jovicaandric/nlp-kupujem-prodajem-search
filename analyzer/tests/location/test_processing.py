import os

import pytest

from analyzer.location import processing


@pytest.mark.parametrize(
    "text, n, expected",
    [
        ("", 1, []),
        (" ", 1, []),
        ("abc", 1, ["abc"]),
        ("abc", 2, []),
        ("abc def", 1, ["abc", "def"]),
        ("abc def", 2, ["abc def"]),
    ],
)
def test_make_ngrams(text, n, expected):
    assert processing.make_word_ngrams(text, n) == expected


@pytest.fixture
def locations():
    return [
        "a,aa,aaa",
        "b,bb,bbb",
        "c,cc,ccc",
    ]


def test_read_location_tokens(locations, tmpdir):
    path = os.path.join(tmpdir, "locations.txt")
    with open(path, "w") as fp:
        fp.write("\n".join(locations))

    tokens, reverse_index = processing.read_location_tokens(path, separator=",")

    expected_tokens = ["a", "aa", "aaa", "b", "bb", "bbb", "c", "cc", "ccc"]
    assert tokens == expected_tokens

    expected_reverse_index = {
        "a": "a",
        "aa": "a",
        "aaa": "a",
        "b": "b",
        "bb": "b",
        "bbb": "b",
        "c": "c",
        "cc": "c",
        "ccc": "c",
    }
    assert reverse_index == expected_reverse_index
