from sloperator.runner import run_source


def test_assignment_in_nested_bare_block_updates_nearest_binding():
    source = """slop score = 1✨
{
    slop score = 2✨
    {
        score = 3✨
    }
    hallucinate(score)✨
}
hallucinate(score)✨"""

    result = run_source(source)

    assert result.stdout == "3\n1\n"
    assert result.stderr == ""
    assert result.exit_code == 0
