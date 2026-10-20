# Task 21 · Pi 4 deep clean

Brian (2026-10-19): the Raspberry Pi 4 was only an early fit-test item. Later fit tests of other parts also went fine, so the Pi is history and nothing in the design depends on it. He wants the Pi references gone from the app ("deep clean", all three levels). AGENTS.md section "Raspberry Pi 4 is history" has the current rule.

Standing rules in [README.md](README.md) apply, with ONE exception for this task: the files listed under "Move to archive" may be moved (copy byte-for-byte to the archive folder, verify SHA-256 matches, then remove the original). Nothing else is deleted.

## Starting count (Claude, 2026-10-19)

About 105 matches for `pi ?_?4|raspberry` (case-insensitive) in outputs/Mechanical_Design_App across 31 files (workspace.js 19, app.py 11, cable-ports.js 8, index.html 7, js-tests/run.js 6, test_app.py 5, mesh_revision.py 5, …). Re-run that count before and after and put both in the report.

## Level 1 · what the user sees

- Equipment panel: remove the "Raspberry Pi 4 · supported baseline" card (`pi4Card` in workspace.js / index.html). The library ("My Equipment") and the wizard are the way in.
- Create assembly: the "Make space for a Pi4" flow (`startWizard` in workspace.js) becomes the generic flow: pick a library item, then slot span. No Pi default.
- Fallback names: `'Raspberry Pi 4'` used when a slot/assembly has no name becomes `'Untitled assembly'`.
- Assembly view: "PI4 ASSEMBLY INSPECTION" / "Pi 4 assembly" become "ASSEMBLY INSPECTION" / "Assembly".
- equipment-wizard.js: "Screw joint (current Pi 4 style)" becomes "Screw joint".
- Artwork help text, ports text, reset button text, clearance.js notes: drop Pi wording.

## Level 2 · code and data

- Saved placements use `equipment:'pi4'` and `geometry:'pi4-clearance-v2-reference'`. New placements must never write these.
- Migration: when a rack document loads, a legacy `pi4` placement is converted to point at the library example item from Level 3 (keep its saved assembly, hardware snapshot, inputs, revisions, ports overrides, artwork and appearance). Write the old document to `rack-history/` before converting (the existing history mechanism). The draft is not saved automatically: Save stays explicit.
- Pi 4 Ports preset (cable-ports.js `PI4_*`): becomes the ports of the example library item. No Pi-specific branch in cable-ports.js / cable_ports.py.
- clearance.js / pi_validation.py / mesh_revision.py / rack_workspace.py / app.py / assembly_records.py / equipment.py: remove `pi4` special cases. If a Pi-only endpoint exists only for the old path, move it with Level 3.
- Print in color (faceplate_color.py, `/api/faceplate-colors/*`): remove the "Pi 4 faceplates only" restriction if the code only gates on the equipment id and the color slicing already works on a generic faceplate outline. If it really depends on Pi geometry, leave it gated, change the wording to "not available for this faceplate yet", and explain in the report. Still opt-in, saved settings only, PROPOSED — UNVALIDATED.
- Rename Pi-specific identifiers (`isPi`, `PI4_NOTE`, `legacyTemplate` naming etc.) to generic names. Keep API compatibility for the legacy ids ONLY inside the migration.

## Level 3 · the separate Pi 4 build path

- Add the Pi 4 as ONE saved example in the equipment library: "Raspberry Pi 4 (example)", built by the generic wizard / equipment_tray.scad path, using the dimensions, hole positions and ports from pi_reference.json / pi4_baseline.scad / the ports preset. It is an example only, not a default and not selected on start. It must pass the existing placement checks and mesh check (do not run exports; renders only inside tests with disposable data).
- Move to archive: `pi4_baseline.scad`, `pi_validation.py`, `test_pi_validation.py`, and any other file whose only purpose is the old Pi path (list each in the report with why). Destination: `docs/archive/pi4-retired-20261019/` with a README saying what each file was and that the printed specimen evidence lives unchanged in `outputs/Lab_Rax_Pi4_*`.
- Do NOT move or edit: `outputs/Lab_Rax_Pi4_*` folders and zips (specimen evidence), `pi_reference.json` (rights unresolved, stays local), data/, rack-references/, catalog-packs/.
- Tests that only tested the old path move with it. Other tests get updated to the generic path. Add tests: migration of a legacy `pi4` placement (disposable fixture, built from a COPY of the shape in data/normal-use, never reading/writing the real folder), no `pi4` written by new placements, no Pi text in the first-run UI (static check on workspace.js/index.html strings).
- Update asset-manifest.json hashes for every changed front-end file (a test checks this).

## Checks

Run before and after, report exact results:

```
powershell -ExecutionPolicy Bypass -File outputs/Mechanical_Design_App/run_checks.ps1
node outputs/Mechanical_Design_App/js-tests/run.js
```

Last known: 111 Python + 164 JS pass.

## May change

outputs/Mechanical_Design_App/ source, tests, index.html, asset-manifest.json, equipment_tray.scad (only if the example needs it, without changing other outputs); docs/archive/pi4-retired-20261019/ (new). Not AGENTS.md / HANDOFF.md / ROADMAP.md / PROJECT.md (Claude does those).

## Report

work/codex-tasks/21-pi4-deep-clean-REPORT.md: before/after counts, every remaining Pi match with why it stays (migration, example item, archive), files changed/moved with SHA-256, check results, open questions. Then stop.
