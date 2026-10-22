from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Binary, ExprStmt, Literal
from sloperator.runner import run_source


def only_expression(source: str):
    (statement,) = parse(tokenize(source))
    assert isinstance(statement, ExprStmt)
    return statement.expression


def test_multiplication_binds_tighter_than_addition():
    expr = only_expression("1 + 2 * 3✨")
    assert isinstance(expr, Binary) and expr.operator.type is TokenType.PLUS
    assert isinstance(expr.left, Literal) and expr.left.value == 1
    assert isinstance(expr.right, Binary) and expr.right.operator.type is TokenType.STAR
    assert isinstance(expr.right.left, Literal) and expr.right.left.value == 2
    assert isinstance(expr.right.right, Literal) and expr.right.right.value == 3


def test_multiplication_before_addition_changes_the_result():
    result = run_source("hallucinate(1 + 2 * 3)✨")
    assert result.stderr == ""
    assert result.stdout == "7\n"


def test_comparison_binds_tighter_than_equality():
    expr = only_expression("1 < 2 == ✅✨")
    assert isinstance(expr, Binary) and expr.operator.type is TokenType.EQUAL_EQUAL
    assert isinstance(expr.left, Binary) and expr.left.operator.type is TokenType.LESS
    assert run_source("hallucinate(1 < 2 == ✅)✨").stdout == "✅\n"
