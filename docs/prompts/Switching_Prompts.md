# Switching prompts — copy, paste, go

For moving between Brian's two Claude accounts, the Codex account and four devices (PC, laptop, iPad, iPhone).
Repo: https://github.com/Cersche/assembly-workshop (private, branch `main`). Rules: AGENTS.md → "Cloud repo and account switching".

**Golden rule:** one worker at a time. Whoever finishes hands off (prompt 2) before the next one starts (prompt 1).
**Uploads:** every push asks Brian first. Say yes, or run `git push` yourself.

---

## 1. Start — Claude, any account, any device

```
Pick up Assembly Workshop. First get the latest from GitHub (git pull on the PC; cloud sessions already have it). Read AGENTS.md, HANDOFF.md and ROADMAP.md. Tell me in a few plain lines: where things stand, what the last worker (Claude account or Codex) finished, anything left half-done, and what you suggest next. Don't change anything yet.
```

## 2. Hand off — Claude, before switching away

```
Wrap up so another account or Codex can take over. Update HANDOFF.md with what we did, what's unfinished and the exact next step. Commit everything with a clear message. Then ask me before pushing to GitHub. After the push, tell me in one line that it's safe to switch.
```

## 3. Emergency hand off — running out of usage

```
Usage is almost out. Quickest safe stop: add 3–5 lines to the top of HANDOFF.md (what you were doing, what's done, what's broken or half-done, next step), commit, and ask me to push. No other work.
```

## 4. Send a job to Codex — Claude writes the prompt

```
Write a Codex task for: <describe the job>. Save it in docs/prompts/codex/ with today's date, and put the full prompt in your final message so I can paste it. Codex should: git pull, read AGENTS.md and HANDOFF.md, work on a branch named codex/<short-name>, run the checks, write a report in work/codex-tasks/, commit, and ask me before pushing. Then commit the prompt file and ask me to push, so Codex can see it.
```

## 5. Start — Codex (paste into Codex)

```
Assembly Workshop, repo Cersche/assembly-workshop (private). git pull, then read AGENTS.md and HANDOFF.md and follow them exactly. Your task is in docs/prompts/codex/<file name>. Work on branch codex/<short-name>, never directly on main. Run the checks listed in HANDOFF.md and report real results, failures included. Write your report to work/codex-tasks/<task>-REPORT.md, commit, and ask before pushing. Don't print, publish, make the repo public or touch data/normal-use.
```

## 6. Review Codex's work — Claude

```
Codex finished branch codex/<short-name>. git pull / fetch it, read its report in work/codex-tasks/, check the diff against the task prompt and AGENTS.md, and run the checks. Tell me plainly: did it do the job, anything wrong or risky? Don't merge into main until I say so; then merge, update HANDOFF.md and ask before pushing.
```

## 7. Quick check from the phone — read only

```
Read-only check on Assembly Workshop: read HANDOFF.md from GitHub and tell me in 3 lines where things stand and what's next. Don't change, commit or push anything.
```

---

**If something goes sideways:** "A push was rejected" → `Pull, merge carefully, show me any conflicts, never force-push.` "Two workers overlapped" → `Compare both versions, tell me what differs, change nothing until I pick.`
