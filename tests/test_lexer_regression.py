"""Regression tests for lexer error paths not covered by test_lexer.py."""

import pytest

from sloperator.errors import LexicalError
from sloperator.lexer import tokenize


@pytest.mark.parametrize("ch", ["?", "@", "~", "$"])
def test_unexpected_character_reports_generic_error(ch: str):
    # These characters fall through every specific branch in scan_token, so they
    # must be caught by the generic fallback rather than silently ignored.
    with pytest.raises(LexicalError) as info:
        tokenize(f"a {ch} b")

    assert info.value.line == 1
    assert info.value.message == f"unexpected character '{ch}'"
    assert str(info.value) == f"SlopLang lexical error at line 1: unexpected character '{ch}'"


def test_unexpected_character_reports_current_line():
    with pytest.raises(LexicalError) as info:
        tokenize("slop x = 1✨\nslop y = 2 ? 3✨")

    assert info.value.line == 2
    assert info.value.message == "unexpected character '?'"
