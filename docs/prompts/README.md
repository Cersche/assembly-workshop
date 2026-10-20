# My prompt shortcuts

The saved prompts live in [.claude/commands/](../../.claude/commands/), one `.md` file each. Type `/` followed by its name in the Claude chat box (for example `/fix-bug`), then a space and your details, and press Enter. Whatever you type after the name gets inserted into the prompt.

To change a prompt, edit its file. To add a new one, copy any file in `.claude/commands/`, rename it, and edit the text. The filename becomes the command name, so keep only prompt files in that folder. New or changed prompts show up in the next session you start. Avoid names that Claude Code already uses, such as `review`, `init` or `plan`.

## Which one to use

| When you want to… | Type | Example |
|---|---|---|
| Start a work session | `/resume-work` | `/resume-work I want to add a new tray size` |
| Understand some code | `/explain-code` | `/explain-code how Save works in the GUI` |
| Learn a concept | `/teach-me` | `/teach-me what a git branch is` |
| Think before building | `/plan-first` | `/plan-first add a delete button to slots` |
| Build something small | `/add-feature` | `/add-feature show slot numbers on the rack` |
| Fix something broken | `/fix-bug` | `/fix-bug Save button does nothing after renaming a slot` |
| Get unstuck on an error | `/stuck` | `/stuck` then paste the error |
| Check the work before accepting it | `/check-work` | `/check-work` |
| Tidy code without changing behavior | `/refactor-safely` | `/refactor-safely the color preset code` |
| Prepare a git commit | `/commit-message` | `/commit-message` |
| Run several sessions at once | `/parallel-plan` | `/parallel-plan 1) tray wizard fix 2) new docs` |
| Finish for the day | `/wrap-session` | `/wrap-session` |

## A good everyday flow

1. `/resume-work`: get caught up
2. `/plan-first`: agree on the plan
3. `/add-feature` or `/fix-bug`: do the work
4. `/check-work`: catch mistakes
5. `/wrap-session`: summary, handoff notes, backup reminder

## Tips for working with Claude

- **Be specific.** Say what you see, what you expected, and where it happens. "The Save button on the Setup tab does nothing after I rename a slot" beats "Save is broken."
- **Plan before big changes.** For anything bigger than a small fix, use `/plan-first` and let Claude ask questions.
- **One task per session.** Long sessions that mix several unrelated tasks get confusing. Start a new session for new work.
- **Ask "how do you know?"** If Claude says something works, ask how it checked. Real verification beats claims.
- **Paste screenshots and errors.** Claude can read images and the full error text.
- **It's fine to say "stop."** You can interrupt, redirect, or say "undo that" at any time.
- **Back up often.** Most of this project isn't in git. Copy it to `D:\Backups` after important changes.

## Codex prompts

Every paste-ready prompt for Codex is also saved in [codex/](codex/), one dated file each, so it can always be found again.
