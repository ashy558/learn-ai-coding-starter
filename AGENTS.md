# AGENTS.md

Sloperator is a tree-walking interpreter for SlopLang, a Python 3.13 project
managed with `uv`. `docs/spec.md` is the source of truth for language behavior;
`README.md` has the layout table.

## Commands

- Run: `uv run sloperator.py examples/fib.slop`
- Parse only: `uv run sloperator.py --check examples/fib.slop` (silent on
  success; exit 1 on a lexical or syntax error)
- Tests: `uv run pytest`; focus with `uv run pytest tests/test_errors.py -q` or
  `uv run pytest -k <pattern>`
- Format: `uv run ruff format --check`
- Lint: `uv run ruff check`
- Types: `uv run ty check`

Run all four checks before committing; there is no CI. The `validate` skill only
runs pytest and ruff, so it does not cover `ty`.

The `run_slop` tool (`.opencode/plugins/run-slop.ts`) runs a `.slop` file from
the repo root with a 30-second timeout. Prefer it for quick runs and
experiments.

## Language and tests

- `.slop` is UTF-8 with non-ASCII syntax: `✨` ends statements, `“…”` are
  strings, `—` starts comments, and `✅`/`❌` are booleans. Straight quotes,
  `;`, and `//` are lexical errors. Preserve these characters when editing
  examples, tests, and docs.
- `tests/test_errors.py` asserts complete diagnostics
  (`SlopLang <kind> error at line N: ...`). Update that test and `docs/spec.md`
  when changing an error message.
- `tests/test_examples.py` auto-discovers every `examples/*.slop`; each must
  exit 0, produce non-empty stdout, and write nothing to stderr. Adding an
  example adds a test.
- `tests/test_cli.py` invokes the CLI with `sys.executable`, not `uv`.
- Test through `sloperator.runner.run_source` to get `stdout`, `stderr`, and
  `exit_code`; `tests/test_evaluator.py` has `run`/`fails` helpers.
- Python's `bool` is an `int`, but SlopLang must not coerce: `✅ == 1` is false
  and `is_number` excludes booleans. Tests enforce this.
- Integer division truncates toward zero (`-7 / 2` is `-3`); do not use Python
  `//` directly.
- Errors must stay `SlopError` subclasses formatted by `SlopError.__str__`.
  Anything else escapes as a traceback, which the CLI tests forbid.

## Wiring

Pipeline: `tokenize` (`lexer/scanner.py`) -> `parse` (`parser/parser.py`, nodes
in `parser/ast.py`) -> `Interpreter.run` (`evaluator/interpreter.py`).
`runner.py` joins the stages and converts errors to `RunResult`; `sloperator.py`
owns argv and exit codes (0 success, 1 Slop error, 2 usage or unreadable file).

- The interpreter pattern-matches AST dataclasses. A new statement or expression
  needs the node, parser support, interpreter handling, docs, and tests.
- Scopes are `Environment` parent chains: `slop` is mutable, `loadbearing` and
  `clanker` bindings are immutable, and assignment updates the nearest binding.
  `clanker` declarations are top-level only; `ship` uses the `ShipSignal`
  exception.
- Call depth is capped at 500 and the Python recursion limit is raised to
  20,000, so runtime errors stay traceback-free.
- No runtime dependencies are declared; the interpreter uses only the standard
  library. Dev tools are pytest, ruff, and ty.

## Known spec gaps

`docs/spec.md` is authoritative. Current code disagrees in two places:

- `ralph` executes its body once before checking the condition
  (`Interpreter.execute`).
- A bare nested `{ ... }` block inside a `clanker` runs with the globals as its
  parent, so assigning an enclosing local from it fails. Top-level nested blocks
  work.

Do not encode either behavior in new examples or tests unless you are
deliberately preserving it.

## Playground and sandbox

- `uv run playground/server.py [port]` serves the playground at
  `http://localhost:8080`; each POST `/run` has a 5-second timeout and appends
  to `logs/runs.log` (gitignored and watcher-ignored).
- `docker compose up -d --build` builds an OpenCode sandbox, not the playground.
  Its entrypoint clones the GitHub repo and runs `opencode serve`, so only
  pushed commits are present; the host `.venv` is never used by the container.
- `opencode.jsonc` is JSONC (trailing commas are valid); it denies reading
  `.env` and the `explore` subagent. Don't bypass those. A user-level shell
  guard also rejects commands containing `.env`, including `self.environment`;
  use the `grep`/`read` tools for that text.
