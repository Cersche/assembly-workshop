---
description: Clean up code without changing what it does
argument-hint: <file or area to clean up>
---
Clean up $ARGUMENTS without changing its behavior.

- First, tell me what you'd change and why, and wait for my OK.
- Behavior must stay exactly the same: same outputs, same files, same STL results.
- Don't touch immutable revisions, historical evidence, or the mechanical baseline.
- Make changes in small steps and run the existing checks after them.
- If you find an actual bug while doing this, tell me — don't silently fix it as part of the cleanup.

At the end, show what changed and confirm the checks still pass.
