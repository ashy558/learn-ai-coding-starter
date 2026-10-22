"""Coverage: a call used directly as an argument to another call."""

from sloperator.runner import run_source


def test_call_as_argument_is_evaluated_before_the_outer_call():
    source = """clanker announce(label) {
    hallucinate(label)✨
    ship label✨
}
clanker wrap(value) {
    hallucinate(“wrapped”, value)✨
    ship value✨
}
hallucinate(wrap(announce(“inner”)))✨"""
    result = run_source(source)

    assert result.stdout == "inner\nwrapped inner\ninner\n"
    assert result.stderr == ""
    assert result.exit_code == 0
