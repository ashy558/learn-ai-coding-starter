# Sloperator

A tree-walking interpreter for [SlopLang](docs/spec.md), written in Python.

```bash
uv run sloperator.py examples/fib.slop
uv run sloperator.py --check examples/fib.slop   # parse only; exits 1 on error
```

## Validation

```bash
uv run pytest              # tests
uv run ruff format --check # formatting
uv run ruff check          # linting
uv run ty check            # type checking
```

Run all four before submitting changes.

The language — slop words, tokens, values, scoping, and control flow — is
specified in [`docs/spec.md`](docs/spec.md); `examples/` has running programs.

## Layout

| Path | What it is |
| --- | --- |
| `sloperator.py` | Command-line entrypoint |
| `sloperator/lexer/` | Source text to tokens |
| `sloperator/parser/` | Tokens to AST (`ast.py` holds the nodes) |
| `sloperator/evaluator/` | Walks the AST: values, environments, interpreter |
| `sloperator/runner.py` | Runs source through all three stages |
| `docs/spec.md` | Language specification |
| `examples/` | Example programs |
| `tests/` | Pytest suite |
| `playground/` | Web server and editor for running programs |

## Playground and sandbox

```bash
uv run playground/server.py            # http://localhost:8080
docker compose up -d --build           # rebuild after Docker changes
```

`Dockerfile` extends the OpenCode image with `uv`, `python3`, and `git`.
`docker-compose.yml` keeps `.venv` and uv caches in named volumes: a host-built
venv has absolute host paths and cannot run in the container. The entrypoint runs
`uv sync --frozen` (or `uv sync` without a lockfile) before launching OpenCode.
