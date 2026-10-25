from sloperator.lexer import TokenType, tokenize
from sloperator.runner import run_source


def test_identifier_may_contain_digits_after_first_character():
    tokens = tokenize("score2 _item3 A9")

    assert [token.type for token in tokens] == [
        TokenType.IDENTIFIER,
        TokenType.IDENTIFIER,
        TokenType.IDENTIFIER,
        TokenType.EOF,
    ]
    assert [token.lexeme for token in tokens] == ["score2", "_item3", "A9", ""]


def test_variable_name_may_contain_digits():
    result = run_source("slop score2 = 40✨\nscore2 = score2 + 2✨\nhallucinate(score2)✨")

    assert result.stdout == "42\n"
    assert result.stderr == ""
    assert result.exit_code == 0


def test_function_and_parameter_names_may_contain_digits():
    result = run_source("clanker add2(value3) { ship value3 + 1✨ }\nhallucinate(add2(41))✨")

    assert result.stdout == "42\n"
    assert result.stderr == ""
    assert result.exit_code == 0


def test_identifier_cannot_start_with_a_digit():
    result = run_source("slop 2score = 40✨")

    assert result.stdout == ""
    assert result.stderr == (
        "SlopLang syntax error at line 1: expected a variable name after 'slop', found '2'\n"
    )
    assert result.exit_code == 1
