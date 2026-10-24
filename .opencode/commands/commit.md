---
description: Review changes, commit them with the given message, then rebase on origin/main
---

Current changes:

!`git status --short`
!`git diff --stat`

Commit message:

$ARGUMENTS

## Steps

1. Review the changes. Run `git diff` for tracked files and read any new files
   in full. Check for stray debug output, secrets, unintended deletions, and
   edits unrelated to the stated message. If the diff touches code or behavior,
   make sure the checks in `AGENTS.md` pass before committing.
2. Stage everything with `git add -A`. If there is nothing to commit, say so and
   skip to step 4.
3. Commit with the provided message verbatim: `git commit -m "<message>"`. Pass
   each paragraph or bullet of a multi-line message as a separate `-m`. Do not
   invent a subject, add a signature, or amend an existing commit. If the
   message is empty, ask the user for one and stop.
4. Run `git pull --rebase origin main`. If it fails or hits conflicts, stop,
   report the conflicting files, and leave the working tree as it is — do not
   abort the rebase, force-push, or resolve conflicts on your own.

Finish with a short summary of the commit hash and subject, plus the result of
the rebase.
