# Parser conventions

`docs/spec.md` (Grammar section) is the source of truth for the language; the
implementation lives in `sloperator/parser/parser.py` with AST nodes in
`sloperator/parser/ast.py`. Follow the two conventions below when changing it.

## One method per grammar rule

- Every rule in the spec's grammar is handled by exactly one method, with a
  `snake_case` name (`functionDecl` -> `function_decl`, `expressionStmt` ->
  `expression_stmt`).
- Methods form the precedence ladder and call only the next-lower rule
  (`expression` -> `logic_or` -> `logic_and` -> ... -> `primary`). Do not skip
  levels or parse a tighter construct directly from a looser method.
- Do not merge two rules into one method. If a rule needs a helper, keep the
  rule's own method and give the helper a name that describes what it does
  (for example a `_tail` helper for a left-associative loop).
- A new rule requires a method here, an AST node if it produces one, spec
  coverage, and tests.

`parameters` and `arguments` are currently parsed inline inside their callers
rather than as their own methods; treat that as an existing deviation, not a
pattern to copy.

## Syntax errors describe the found token

- Raise syntax errors through `self.error(token, message)` (directly, or via
  `expect`/`terminator`). It appends `, found '<lexeme>'`, or
  `, but reached end of file` when the token is EOF, so a diagnostic always
  says what was actually there.
- The message says what was expected, not what was found: for example
  `expected '(' after clanker name`. `error` supplies the found token; do not
  repeat it in the message or end the message with a period.
- Use `expect` for a required token (`expect(TokenType.RIGHT_PAREN, "...")`).
  For an unexpected token that cannot start the construct, report the token
  that was consumed, as `primary` does with `expected an expression`.
- Messages are part of the public diagnostics asserted in
  `tests/test_errors.py`; update that test and `docs/spec.md` when a message
  changes.
- Restrictions that are not simple token mismatches (`duplicate parameter name
  'x'`, `ship is only allowed inside a clanker`) may raise `SlopSyntaxError`
  directly, but the message must still identify the offending token or
  construct.
