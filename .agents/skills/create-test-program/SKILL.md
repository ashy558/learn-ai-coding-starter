---
name: create-test-program
description: Create a SlopLang example program and an exact-output test for a language feature. Use when asked to add an example to examples/, pin an example's stdout in tests/test_example_outputs.py, or build a test program that demonstrates behavior from docs/spec.md.
---

# Create Test Program

Given a language feature, add a runnable example in `examples/` and a test in
`tests/test_example_outputs.py` that pins the example's complete stdout.
`docs/spec.md` is authoritative; the current interpreter is not.

## Workflow

1. Read the feature's section in `docs/spec.md`, including the grammar and
   operator tables when relevant. Note the exact syntax, accepted value types,
   and edge cases. Do not infer semantics from existing examples.
2. Check `examples/` and `tests/test_example_outputs.py` for existing coverage.
   Extend an existing example only when the feature clearly belongs with it;
   otherwise choose a new descriptive lowercase kebab-case name, such as
   `unary-not.slop`.
3. Write `examples/<name>.slop`. It must:
   - use spec syntax exactly: `“ ”` strings, `—` comments, `✨` terminators,
     and no `;`, `//`, `"`, or `for`;
   - exercise the feature with one or two revealing edge cases;
   - print deterministic output with `hallucinate`, with no unbounded `ralph`;
   - begin with a `—` comment naming the feature.
4. Predict the output from the spec before running anything. If the spec is
   silent or contradictory, stop and report the gap instead of guessing.
5. Run the example with the `run_slop` tool, passing `examples/<name>.slop`.
   Its stdout must match your prediction, with empty stderr and exit code 0.
   If it does not, stop and report the spec/interpreter mismatch. Never bless
   current behavior into the test.
6. Create `tests/test_example_outputs.py` if it does not exist, using the
   harness below. Add one test for the new example at the end.
7. Run `uv run pytest tests/test_example_outputs.py tests/test_examples.py`.
   If you changed Python, also run `uv run ruff format --check` and
   `uv run ruff check`.
8. Report the example path, its exact output, the test name, and the commands
   that passed.

## Test harness

Pinned output includes every newline. Do not use `.strip()`, `.splitlines()`,
or a loop that hides formatting differences. If the file is missing, create it
with this harness and replace the placeholder test with the first real one:

```python
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


def test_<snake_case_name>_output():
    assert_example_output(
        "<name>",
        "<first line>\n"
        "<second line>\n",
    )
```

Add later tests the same way: one `test_<snake_case_name>_output` function that
calls `assert_example_output`. Reuse the helper rather than duplicating the
read-and-run logic, and name the test after the example file. Every
`hallucinate` adds a newline, so expected strings normally end in `\n`; a blank
line is `"\n"`.

## Guardrails

- Keep the example and test paired: one new example normally gets one new
  exact-output test. `tests/test_examples.py` already checks that every example
  runs cleanly, so this file adds the exact-text assertion, not a second smoke
  test.
- This skill adds coverage, not language behavior. Do not edit `docs/spec.md`
  or the interpreter to make an example pass. If the feature is missing or
  wrong, report it and stop.
- Examples must succeed. Error-diagnostic coverage belongs in
  `tests/test_errors.py`, not here.
- Preserve the non-ASCII syntax in every edited file.
- If the feature is a bug fix, also add a focused regression test outside this
  module, as required by `AGENTS.md`.
