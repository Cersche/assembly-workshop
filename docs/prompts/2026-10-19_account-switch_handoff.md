You're picking up Assembly Workshop (local Python 3.10 app in outputs/Mechanical_Design_App; it designs equipment trays and faceplates for a Lab Rax mini rack and exports STLs). Read AGENTS.md, HANDOFF.md and ROADMAP.md first. ROADMAP Now/Next/Later is the only plan: no phase numbers.

Where we are: Option 1 of the equipment wizard rework (work/equipment-wizard-options/Options.html), which Brian chose.
- Step 1 (tray offset/rotation in equipment_tray.scad) is committed as 129b482.
- Steps 2–4 are built, checked and NOT committed: per-slot tray data, the shorter wizard (Device → Holes → Ports) and the new "Place on tray" window (tray-placement.js). The follow-up makes cable ports and clearance screening use each slot's tray settings. The rack view still shows the library mesh, with a "Placement not rendered yet" note (Brian's choice).
- Checks: run_checks.ps1 passes (86 Python + 141 JS). Details are in HANDOFF.md.
- A "rendering quality" side session also ran. Check what it left before building on it.

Next:
1. Review the uncommitted diff (`git status`), run run_checks.ps1, then ask Brian before committing. Commit only these app files and tests, never data/ or outputs/ assets.
2. Then continue ROADMAP "Now", then "Next": the cable inventory / parts order.

Offload to Codex whenever possible. Write each piece as a tight Codex task in work/codex-tasks/ (spec + REPORT pattern). Put the combined Codex prompt in docs/prompts/codex/ and in your final message. Claude reviews Codex's results and does UI and integration work only.

Rules:
- Never use data/normal-use for testing. Use disposable data folders.
- No exports, printing, purchases, pushes or commits without Brian's OK.
- Fit, retention and strength stay UNKNOWN.
- The Pi 4 is sample equipment only.
- Keep reports short and in plain language.
