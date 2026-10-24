---
name: run-bootdev-lesson
description: Run a Boot.dev lesson dry-run from the project root, compare its raw expected and observed output, propose a fix when an expectation fails, and submit only after a clean preflight. Use when asked to run, check, or submit a `bootdev` lesson, or when given a `bootdev run <uuid>` command.
---

# Run Boot.dev Lesson

Run lessons from the project root (the directory containing `AGENTS.md`). Use the
shell tool's working directory rather than changing directories in the command.

## Workflow

1. Determine the lesson ID:
   - If the user supplied a UUID, use it.
   - Otherwise omit the UUID to run the next lesson with `bootdev run`.
2. Preflight without submitting:

   ```bash
   bootdev run <uuid>
   ```

   Run from the project root. Do not add `-s` for this step.

3. Interpret the dry run (`bootdev run`):
   - The current CLI (verified with v1.32.6) does not grade a dry run. Expect
     `?` markers, no `✓`/`X` verdict, and no `All tests passed!` summary; those
     absences are normal, not failures.
   - Exit code `0` only means the command completed without a fatal error
     (auth, update, network, unsupported lesson, and so on). It does not mean
     the lesson would pass.
   - A dry run is **successful** only when all of these hold:
     - the process exits `0` and every step runs, with no skipped step,
       dependency failure, unsupported OS/lesson type, or API/HTTP error;
     - every printed `Expect ...` line is satisfied by the printed
       observation, compared manually:
       - `Expect exit code N` against `> Command exit code: M`;
       - each jq expectation against the values under `> jq output:` →
         `Results:`;
       - stdout contains/excludes/line-count expectations against
         `> Command stdout:`;
       - HTTP status, body, header, and JSON expectations against the HTTP
         response section;
     - no expectation is contradicted or impossible to check from the output.
   - Otherwise the dry run **failed**. A `?` marker by itself is not a
     failure; an unmatched expectation is.
4. If the dry run fails:
   - Do not submit.
   - Do not edit files unless the user asked for the fix to be applied.
   - Report each failing expectation with its command and observed output.
   - Propose a specific fix: files to change, the intended change, and the
     command to re-run. Ask for approval before editing.
   - After an approved fix, re-run the same check command from step 2.
5. If the dry run is clean, submit the same lesson:

   ```bash
   bootdev submit <uuid>
   ```

   The dry run is only a preflight: the server grades on submission. If no UUID
   was supplied, `bootdev submit` does not silently pick a lesson: it announces
   `Submitting next lesson: <n> - <title>` and stops at an interactive
   `Continue? [y/N]:` prompt. Check that the announced title is the lesson just
   checked in step 3; if it is not, answer `n` and ask the user for the lesson
   ID. Only answer `y` after the user has approved submitting that lesson.

   A non-interactive shell cannot answer the prompt: stdin reads end-of-file,
   the command prints `Error: submission canceled`, and it exits `1`. Once the
   user has approved, feed the answer in for that run:

   ```bash
   printf 'y\n' | bootdev submit <uuid>
   ```

   `bootdev submit` exits `0` when the lesson passes or fails, but `1` when the
   prompt is canceled or for fatal/API/auth errors. Read the submitted verdict
   (`Tests failed!`, `All tests passed! 🎉`, XP, and the website) rather than the
   exit code.
6. Report each dry-run expectation and whether it matched, then the submission
   verdict and XP when Boot.dev prints it.

## Guardrails

- Never submit when any dry-run expectation is contradicted, missing, or cannot
  be checked from the printed output.
- Do not claim a dry run passed because the exit code is `0` or because no
  error appeared; only a complete manual expectation check counts.
- Never answer the `Continue? [y/N]:` prompt before the user approves, and only
  for the lesson named in it. `bootdev submit` does not pick a lesson silently.
- Do not claim submission success without `All tests passed! 🎉` in the submit
  output or equivalent confirmation on the website.
- Keep proposed fixes separate from applied changes; wait for approval.
- Preserve unrelated user work and do not commit on the user's behalf.
