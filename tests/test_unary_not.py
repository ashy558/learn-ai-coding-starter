"""Tests for unary `!`, SlopLang's "not" operator."""

import pytest

from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Binary, ExprStmt, Literal, Unary
from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


def fails(source: str) -> str:
    result = run_source(source)
    assert result.exit_code == 1
    return result.stderr.rstrip("\n")


def only_expression(source: str):
    (statement,) = parse(tokenize(source))
    assert isinstance(statement, ExprStmt)
    return statement.expression


def test_not_flips_booleans():
    assert run("hallucinate(!✅, !❌, !!✅)✨") == "❌ ✅ ✅\n"


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("!✅", "❌"),
        ("!❌", "✅"),
        ("!!✅", "✅"),
        ("!!❌", "❌"),
        ("!!!✅", "❌"),
        ("!(1 == 1)", "❌"),
        ("!❌ || ❌", "✅"),
        ("!❌ && ✅", "✅"),
    ],
)
def test_not_results(expression: str, expected: str):
    assert run(f"hallucinate({expression})✨") == f"{expected}\n"


def test_not_applies_to_a_call_result():
    source = """clanker is_big(n) {
    ship n > 10✨
}
hallucinate(!is_big(20))✨
hallucinate(!is_big(5))✨"""
    assert run(source) == "❌\n✅\n"


def test_not_can_drive_a_condition():
    source = """slop done = ❌✨
ralph !done {
    done = ✅✨
}
hallucinate(done)✨"""
    assert run(source) == "✅\n"


def test_double_not_is_nested_unary_nodes():
    expr = only_expression("!!✅✨")
    assert isinstance(expr, Unary) and expr.operator.type is TokenType.BANG
    assert isinstance(expr.operand, Unary) and expr.operand.operator.type is TokenType.BANG
    assert isinstance(expr.operand.operand, Literal) and expr.operand.operand.value is True


def test_not_binds_tighter_than_equality():
    expr = only_expression("!✅ == ❌✨")
    assert isinstance(expr, Binary) and expr.operator.type is TokenType.EQUAL_EQUAL
    assert isinstance(expr.left, Unary) and expr.left.operator.type is TokenType.BANG
    assert isinstance(expr.left.operand, Literal) and expr.left.operand.value is True
    assert isinstance(expr.right, Literal) and expr.right.value is False


@pytest.mark.parametrize(
    ("source", "message"),
    [
        ("hallucinate(!1)✨", "operand of unary '!' must be a boolean, got number"),
        ("hallucinate(!“a”)✨", "operand of unary '!' must be a boolean, got string"),
    ],
)
def test_not_rejects_non_booleans(source: str, message: str):
    assert fails(source) == f"SlopLang runtime error at line 1: {message}"


def test_not_rejects_nil():
    assert fails("clanker nothing() {\n}\nhallucinate(!nothing())✨") == (
        "SlopLang runtime error at line 3: operand of unary '!' must be a boolean, got nil"
    )


def test_double_not_rejects_non_booleans_too():
    assert fails("hallucinate(!!1)✨") == (
        "SlopLang runtime error at line 1: operand of unary '!' must be a boolean, got number"
    )
