from sloperator.runner import run_source


def test_ralph_checks_its_condition_before_the_first_iteration():
    source = """ralph ❌ {
    hallucinate(“never”)✨
}"""
    result = run_source(source)
    assert result.stdout == ""
    assert result.stderr == ""
    assert result.exit_code == 0
