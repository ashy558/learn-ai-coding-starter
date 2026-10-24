"""Tests for joining strings with `+`."""

import pytest

from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


def test_adding_an_empty_string_leaves_a_variable_unchanged():
    source = """slop word = “slop”✨
word = word + “”✨
hallucinate(word)✨"""
    assert run(source) == "slop\n"


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("“slop” + “”", "slop"),
        ("“” + “slop”", "slop"),
        ("“” + “slop” + “”", "slop"),
        ("“” + “”", ""),
    ],
)
def test_empty_string_is_the_identity_for_concatenation(expression: str, expected: str):
    assert run(f"hallucinate({expression})✨") == f"{expected}\n"


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("“slop” + “✨”", "slop✨"),
        ("“✨” + “slop”", "✨slop"),
        ("“🚀” + “🛸”", "🚀🛸"),
        ("“✨” + “”", "✨"),
        ("“” + “✨”", "✨"),
    ],
)
def test_adding_strings_containing_emoji(expression: str, expected: str):
    assert run(f"hallucinate({expression})✨") == f"{expected}\n"


def test_emoji_inside_a_string_is_text_not_syntax():
    assert run("hallucinate(“✨ ✅ ❌”)✨") == "✨ ✅ ❌\n"
