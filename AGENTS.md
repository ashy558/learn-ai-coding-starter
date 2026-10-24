# AGENTS.md

Sloperator is a tree-walking interpreter for SlopLang, a Python 3.13 project
managed with `uv`. Language behavior is defined in
[`docs/spec.md`](docs/spec.md); treat it as authoritative and do not infer
semantics from examples alone.

## Project layout

| Path | Role |
| --- | --- |
| `sloperator.py` | CLI entrypoint and exit codes |
| `sloperator/lexer/` | Source text to tokens |
| `sloperator/parser/` | Tokens to AST (`ast.py` holds the nodes) |
| `sloperator/evaluator/` | AST walking: values, environments, interpreter |
| `sloperator/runner.py` | Runs source through all three stages |
| `docs/spec.md` | Language specification |
| `examples/` | Runnable `.slop` programs |
| `tests/` | Pytest suite |
| `playground/` | Web server and editor |

`sloperator/parser/AGENTS.md` adds conventions for parser changes.

`.slop` files use non-ASCII syntax (`✨`, `“…”`, `—`, `✅`, `❌`); preserve
those characters when editing examples, tests, and docs.

## Validation

Run all four before committing; there is no CI:

```bash
uv run pytest               # tests
uv run ruff format --check  # formatting
uv run ruff check           # linting
uv run ty check             # type checking
```

Comparison and equality tests live in `tests/test_comparisons.py`; run those
alone with `uv run pytest tests/test_comparisons.py`.

The `validate` skill runs only pytest and ruff, so it does not cover `ty`.

## Formatting

Run `uv run ruff format` after any code change. Make formatting changes only
as a last step, once all the logic changes are done, so formatting diffs stay
separate from behavioral ones.

## When to add regression tests

Add a regression test whenever you fix a bug or correct behavior that could
silently return. The test should fail on the old code and pass on the new code.

- Put focused regression tests in a clearly named file, such as
  `tests/test_lexer_regression.py`, `tests/test_unary_minus.py`, or
  `tests/test_nested_calls.py`.
- Change or add a diagnostic: update `tests/test_errors.py`, which asserts
  complete messages (`SlopLang <kind> error at line N: ...`), and update
  `docs/spec.md`.
- Add or change syntax or semantics: add lexer, parser, and evaluator tests as
  applicable, and update `docs/spec.md`.
- Keep invariants covered, especially the ones Python would otherwise blur:
  booleans are not numbers (`✅ == 1` is false), integer division truncates
  toward zero, and runtime errors stay `SlopError` subclasses rather than
  escaping as tracebacks.
- Test through `sloperator.runner.run_source` to assert `stdout`, `stderr`, and
  `exit_code`; `tests/test_evaluator.py` has `run`/`fails` helpers. CLI tests
  invoke `sloperator.py` with `sys.executable`, not `uv`.
- `tests/test_examples.py` auto-discovers every `examples/*.slop`, so adding an
  example also adds a test. Do not rely on an example as the only regression
  coverage.

Two known code/spec mismatches must not be encoded in new examples or tests
unless deliberately preserving them: `ralph` executes its body once before
checking the condition, and a bare nested `{ ... }` block inside a `clanker`
uses the globals as its parent. See `docs/spec.md` for the intended behavior.
