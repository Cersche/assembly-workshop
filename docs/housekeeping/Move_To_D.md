# Moving Assembly Workshop to the D: drive (2026-10-21)

Old home: `C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop`
New home: `D:\Projects\assembly-workshop` (change below if Brian picked another name)

Already done in the old folder:
- All pending work committed (`ce14dfa`). Not pushed yet: push only with Brian's OK.
- The merged `two-device-tray` worktree was unregistered (its branch stays).
- Live files have no hard-coded project path. `start.bat` uses relative paths; `.claude/launch.json` points only at temp folders.

## Steps (do with every Claude, Codex and app window closed, including the app server)

Run in PowerShell:

```powershell
$old = "C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop"
$new = "D:\Projects\assembly-workshop"
robocopy $old $new /E /COPY:DAT /DCOPY:DAT /R:1 /W:1
git -C $new status          # must say "nothing to commit"
```

Copy Claude's memory to the new project key (Claude names it after the path):

```powershell
$memOld = "$env:USERPROFILE\.claude\projects\C--Users-brian-Documents-Codex-2026-10-17-Assembly-Workshop\memory"
$memNew = "$env:USERPROFILE\.claude\projects\D--Projects-assembly-workshop\memory"
New-Item -ItemType Directory -Force $memNew | Out-Null
Copy-Item "$memOld\*" $memNew -Recurse
```

Then:
1. Start the app from `D:\Projects\assembly-workshop\outputs\Mechanical_Design_App\start.bat` and confirm the rack loads.
2. Open a new Claude session in the D: folder and check that it remembers things (for example, Gene).
3. Update shortcuts, the backup script destinations if needed, and the Setup facts memory to the new path.
4. Keep the old C: folder untouched for a week, then Brian decides whether to delete it. Do not delete it as part of the move.
