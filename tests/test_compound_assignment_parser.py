import pytest

from sloperator.errors import SlopSyntaxError
from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Assign, Binary


def test_plus_equal_is_a_token_and_parses_as_assignment():
    tokens = tokenize("score += 1 + 2✨")
    assert [token.type for token in tokens] == [
        TokenType.IDENTIFIER,
        TokenType.PLUS_EQUAL,
        TokenType.NUMBER,
        TokenType.PLUS,
        TokenType.NUMBER,
        TokenType.SPARKLES,
        TokenType.EOF,
    ]

    (statement,) = parse(tokens)
    assert isinstance(statement, Assign)
    assert statement.name.lexeme == "score"
    assert statement.operator.type is TokenType.PLUS_EQUAL
    assert isinstance(statement.value, Binary)
    assert statement.value.operator.type is TokenType.PLUS


def test_plus_equal_is_not_an_expression_operator():
    with pytest.raises(SlopSyntaxError) as info:
        parse(tokenize("hallucinate(score += 1)✨"))

    assert info.value.message == "expected ')' after arguments, found '+='"
