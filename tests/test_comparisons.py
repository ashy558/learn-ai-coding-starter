from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Binary, ExprStmt
from sloperator.runner import run_source


def only_expression(source: str):
    (statement,) = parse(tokenize(source))
    assert isinstance(statement, ExprStmt)
    return statement.expression


def test_comparison_binds_tighter_than_equality():
    expr = only_expression("1 < 2 == ✅✨")
    assert isinstance(expr, Binary) and expr.operator.type is TokenType.EQUAL_EQUAL
    assert isinstance(expr.left, Binary) and expr.left.operator.type is TokenType.LESS
    result = run_source("hallucinate(1 < 2 == ✅)✨")
    assert result.stderr == ""
    assert result.stdout == "✅\n"
