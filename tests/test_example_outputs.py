"""Exact stdout for programs in examples/."""

from pathlib import Path

from sloperator.runner import run_source

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def assert_example_output(name: str, expected: str) -> None:
    source = (EXAMPLES / f"{name}.slop").read_text(encoding="utf-8")
    result = run_source(source)
    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.stdout == expected


def test_equality_output():
    assert_example_output(
        "equality",
        "✅\n❌\n❌\n",
    )
