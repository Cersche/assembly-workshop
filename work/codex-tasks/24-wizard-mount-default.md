# Task 24 · Let the wizard save a device with no mounting holes (pick the tray default mount)

Found by Claude 2026-10-20 while browser-checking task 23 with Brian's Dell OptiPlex Micro 7010 STEP. Standing rules in [README.md](README.md) apply (no commits/pushes/exports; Claude reviews, browser-checks and commits).

## Problem

The equipment wizard always saves new items with `device_mount: 'inserts'` (equipment-wizard.js `reset()`), and there is no mount choice anywhere in the wizard. equipment.py `clean()` rejects inserts/pegs without holes, so a box that should "sit flat" and has no holes cannot be saved: the Save button shows "Problem: Add at least one mounting hole for inserts or pegs." The only way through is to tick a fake hole. The step-1 hint from task 23 ("Fits 1U if it sits flat… Choose 'Sits flat' under Mounting in Place on tray") points to a choice the user can only reach after saving.

## Build

1. In the wizard's Save section (Ports step), add one "Tray default mount" choice using the existing `MOUNTS` labels (inserts / pegs / clips / straps / flat). It sets `spec.device_mount`, which is already the "Tray defaults for new slots" value shown in the summary. Default stays inserts for new items; editing an older item keeps its saved value.
2. Do NOT switch the mount automatically (Brian's direction). But if the item has no holes and the mount is inserts or pegs, show the save problem with a pointer: "…or choose another tray default mount below (e.g. Sits flat)."
3. When the mount changes, recompute `spec.u` with the shared `LabRaxPortOpenings.autoU(spec)` only if the user has not typed a U themselves (keep it simple; say in the report what you did). Front-opening Z values already entered stay as entered (the existing "Heights are for the 6 mm standoff" note must then say which lift they are for, using `deviceLift(spec)`).
4. Update the step-1 flat hint so it says to pick "Sits flat" as the tray default mount on the Ports step (or in Place on tray per slot).
5. Update asset-manifest.json sha256 for changed front-end files (CRLF normalized to LF).

## Tests

- JS: the mount choice sets `spec.device_mount`; a no-hole spec with `flat` passes the wizard's save check; inserts with no holes still shows the problem with the new pointer; hint text updated.
- Python: a no-hole `flat` spec passes `clean()` (likely already true; add the test).
- Do NOT run STL exports.

## May change

equipment-wizard.js, port-openings.js (hint text only), asset-manifest.json, test_*.py and js-tests/ (register new JS tests in js-tests/run.js). Nothing else. Never touch data/normal-use.

## Checks

Before and after, report exact results:

```
powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1
```

Do not start or stop servers.

## Report

work/codex-tasks/24-wizard-mount-default-REPORT.md: files changed with before/after SHA-256, what you did about U, check results, open questions. Fit and strength stay UNKNOWN.
