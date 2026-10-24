---
name: create-and-validate
description: Add a SlopLang example program with an exact-output test, then run the full check suite. Use when asked to create a test program and validate it end to end, or to add spec-backed example coverage and confirm tests, formatting, linting, and types all pass.
---

# Create And Validate

This skill chains two existing skills. Do not repeat their instructions here;
load each one with the `skill` tool and follow it as written.

## Workflow

1. Load the `create-test-program` skill and complete its workflow: add the
   `examples/<name>.slop` program and its exact-output test.
2. Only after the example and test are in place, load the `validate` skill and
   run every check it lists from the project root.
3. Report the example path, its exact output, the test name, and which checks
   passed or failed.

## Guardrails

- Load both skills rather than working from memory; their steps are the source
  of truth. If either skill changes, this skill follows the change.
- Keep the order. Validation runs against the finished example and test, so
  running it first only checks unrelated code.
- If `create-test-program` stops on a spec gap or an interpreter mismatch,
  report that and do not continue to validation as though the work succeeded.
- Report failures before proposing fixes, as `validate` directs.
