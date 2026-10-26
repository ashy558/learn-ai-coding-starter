import pytest

from sloperator.runner import run_source


def test_plus_equal_adds_numbers_after_evaluating_the_rhs():
    source = "slop n = 2✨\nn += 3 * 4✨\nhallucinate(n)✨"
    result = run_source(source)
    assert result.stdout == "14\n"
    assert result.stderr == ""
    assert result.exit_code == 0


def test_plus_equal_concatenates_strings_on_the_nearest_binding():
    source = """slop word = “outer”✨
vibe ✅ {
    slop word = “inner”✨
    word += “!”✨
    hallucinate(word)✨
}
hallucinate(word)✨"""
    result = run_source(source)
    assert result.stdout == "inner!\nouter\n"
    assert result.stderr == ""
    assert result.exit_code == 0


def test_plus_equal_evaluates_rhs_before_checking_the_lhs():
    result = run_source("missing += hallucinate(“rhs”)✨")
    assert result.stdout == "rhs\n"
    assert result.stderr == "SlopLang runtime error at line 1: undefined variable 'missing'\n"
    assert result.exit_code == 1


@pytest.mark.parametrize(
    ("source", "line", "message"),
    [
        (
            "loadbearing LIMIT = 100✨\nLIMIT += 1✨",
            2,
            "cannot assign to loadbearing 'LIMIT'",
        ),
        (
            "clanker f() { }\nf += 1✨",
            2,
            "cannot assign to immutable binding 'f'",
        ),
        (
            "slop x = 1✨\nx += “a”✨",
            2,
            "operands of '+=' must both be numbers or both be strings, got number and string",
        ),
        (
            "slop x = ✅✨\nx += 1✨",
            2,
            "operands of '+=' must both be numbers or both be strings, got boolean and number",
        ),
        ("missing += 1✨", 1, "undefined variable 'missing'"),
    ],
)
def test_plus_equal_runtime_errors(source: str, line: int, message: str):
    result = run_source(source)
    assert result.stderr == f"SlopLang runtime error at line {line}: {message}\n"
    assert result.exit_code == 1
