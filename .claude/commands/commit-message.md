---
description: Look at the changes and draft a commit, then ask before committing
argument-hint: (optional) what the change was for
---
Prepare a git commit for the current changes. $ARGUMENTS

1. Run `git status` and `git diff` and tell me, briefly, what's in there.
2. Point out anything that shouldn't be committed (secrets, user data, large generated files, scratch files, anything from outputs/ or data/).
3. Draft a clear commit message: a short summary line, then a few lines on what and why.
4. Show me exactly which files you'd include, and wait for my OK.

Never push.
