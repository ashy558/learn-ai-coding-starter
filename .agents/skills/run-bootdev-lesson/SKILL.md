---
name: run-bootdev-lesson
description: Run a Boot.dev lesson check from the project root, propose a fix when a check fails, and submit only when every check passes. Use when asked to run, check, or submit a `bootdev` lesson, or when given a `bootdev run <uuid>` command.
---

# Run Boot.dev Lesson

Run lessons from the project root (the directory containing `AGENTS.md`). Use the
shell tool's working directory rather than changing directories in the command.

## Workflow

1. Determine the lesson ID:
   - If the user supplied a UUID, use it.
   - Otherwise omit the UUID to run the next lesson with `bootdev run`.
2. Check without submitting:

   ```bash
   bootdev run <uuid>
   ```

   Run from the project root. Do not add `-s` for this step.
3. Interpret the result from the check output, not the shell exit code alone. A
   command can exit 0 while individual checks fail.
   - **Pass:** every check is marked `✓` and the run ends with
     `All tests passed!`.
   - **Fail:** any `✗`, failed expectation, missing file, command error, or
     absence of the final success summary.
4. If a check fails:
   - Do not submit.
   - Do not edit files unless the user asked for the fix to be applied.
   - Report each failing check with its command and the relevant output.
   - Propose a specific fix: files to change, the intended change, and the
     command to re-run. Ask for approval before editing.
   - After an approved fix, re-run the same check command from step 2.
5. If every check passes, submit the same lesson:

   ```bash
   bootdev run -s <uuid>
   ```

   If no UUID was supplied, do not guess one and do not silently let
   `bootdev run -s` pick a different lesson. Ask the user for the lesson ID, or
   confirm rerunning the next lesson with `bootdev run -s`.
6. Report the result per check and include the XP earned when Boot.dev prints it.

## Guardrails

- Never submit a failed or unverified check.
- Do not claim success without the `All tests passed!` summary.
- Keep proposed fixes separate from applied changes; wait for approval.
- Preserve unrelated user work and do not commit on the user's behalf.
