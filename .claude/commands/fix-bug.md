---
description: Find the real cause of a bug, fix it, and prove the fix works
argument-hint: <what's wrong, error message, steps to reproduce>
---
There's a bug: $ARGUMENTS

Work through it like this:

1. Reproduce it, or explain exactly why you can't. Use disposable test data, never data/normal-use/.
2. Find the root cause, not just the symptom. Tell me what it is and point to file:line.
3. Make the smallest fix that solves the root cause. Don't refactor or "improve" unrelated code.
4. Show that it's fixed: rerun the reproduction, and run any existing checks that cover this area.
5. Tell me what you changed, what you verified, and anything you couldn't verify.

If the fix needs a decision from me, or would touch a lot of files, stop and ask first.
