# Task 09 — cable schema report

Completed 2026-10-19. Final checks PASS: 71 Python + 94 JavaScript tests (including task 10). Brian explicitly authorized one addition to the edit scope: archive `test_rack_workspace.py` and replace its obsolete `cables: []` rejection fixture with an actually unknown key. The assertion remains active; no test bypass was added.

## Changes and verification

Added `cable_plan.validate(value, slots, allocations, guide_ids)` and integrated it into `rack_workspace._cabling`. It returns only supplied new fields, validates references, uniqueness, bounds, finite numeric values, known fields and one cable per port end, and allows unconnected ends and outside endpoints without an exit. Settings defaults apply only when settings is supplied. Existing guides/ports-only documents and racks without cabling retain their prior shape. Unknown guide fields are now rejected as required by the task's unknown-keys rule.

Four new Python tests cover full temporary save/read and legacy round trips, valid boundary/default cases, unknown guide fields and more than 80 rejection subcases. These include duplicate port use, guide/exit/endpoint/allocation references, invalid colour, bool slot, non-finite numbers, oversized integers, too-long notes and unknown nested keys.

Commands actually run:
- Targeted `Get-Content`, `rg`, `Get-Item` and `Get-FileHash` inspections; `Copy-Item` archives; Python stdin scripts for LF normalization, SHA-256 verification and reports.
- `powershell -NoProfile -ExecutionPolicy Bypass -File outputs/Mechanical_Design_App/run_checks.ps1`: initial run failed solely on the obsolete cables rejection (69/70 Python passed; 76/76 JS passed).
- `& 'C:/Program Files/Python310/python.exe' -B work/gui-refinement/check_python.py`: confirmed the same sole obsolete assertion; all new tests passed.
- After Brian authorized the assertion correction, `run_checks.ps1`: PASS, 70 Python + 76 JS at the end of the initial task 09 implementation.
- Final schema review added the unknown-guide-field test and oversized-number case. Final `run_checks.ps1`: PASS, 71 Python + 94 JS with task 10 registered. Output was summarized using `Select-String`; the script explicitly reported `RESULT: all checks passed`.

Assumptions: identities are preserved exactly; endpoint names and cable numbers are trimmed before validation/uniqueness checks. Hex colours accept either case and normalize to lowercase. Port existence deliberately remains a client/library concern. No open decisions remain for task 09. The README queue update was explicitly requested by Brian.

Existing changed files were copied byte-for-byte before editing to `docs/archive/codex/2026-10-19/cable-tasks-09-10/`. Edited and new source, test, queue and report files use UTF-8/LF; archive copies preserve original bytes (including original line endings).

Nothing in `data/normal-use` or other user data was read or written. Tests use newly created temporary data or in-memory fixtures. No server was started/restarted, no desktop session was opened, and no builds, exports, printing, installs, commits or pushes were performed. Physical fit, strength and guide capacity remain UNKNOWN. No prohibited front-end file or asset manifest was edited.

## File hashes

| File | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| outputs/Mechanical_Design_App/rack_workspace.py | 27e4f3701f839f99c09665ba34ed114bb9f8c5aab775c3b10b73175d2ac8edf2 | bae3ed6b9356979431c0f791f1613d1c3f256efbe414c10dbe2c78cb95d95538 |
| outputs/Mechanical_Design_App/cable_plan.py | new | d57f7423e04048d4dfdc7e6d3245ce6e576b550c151b780acf7efbd503710b5b |
| outputs/Mechanical_Design_App/test_cable_plan.py | new | 42fdde368bbc4eb1321558a3736fa23d6e5e9590fc7648cb33ad147885801817 |
| work/gui-refinement/check_python.py | d796351edb7ce215acf170ac5d50b7fe1407c48a15ba372d066ca53ee3c3fbca | d7f242eda8ee15b7be8b21853f9e4a21fdfb203826563971238de964c1ed305e |
| outputs/Mechanical_Design_App/test_rack_workspace.py | ffa927a3ef2b7579ab4d4ccfe9a0eeb74b4f378959f9d5951ffb68febb8bbada | 92feaa6024a6b37447d74743813ed58c4111400bd120f5a3affbd6a11c415f7d |
| work/codex-tasks/README.md | e79474eaf84c82407ed58518a28e3496210c21a5939df33dba07f65a83f9e3c1 | 62b4f51339156ff738216fbb78569c4707c286175e827891a9a7abba234295bd |
