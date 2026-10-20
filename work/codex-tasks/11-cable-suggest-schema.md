# 11 — Cable management Step 4: schema for suggestions (Python)

**Goal:** Save accepts the four new optional fields that Step 4 needs. Decisions: [work/cable-management/Step4_Decisions.md](../cable-management/Step4_Decisions.md) (read it, especially "Data shape additions"). Planning data only: no geometry, STLs or pins.

**Fields (all optional; output a field only when it was supplied, so legacy racks and the existing `{'settings': {}}` round-trip test are unchanged):**
- `cabling.cables[i].carries`: exactly `'power'` or `'data'`. Error: `Cable carries is power or data.`
- `cabling.cables[i].unplug_often`: a real bool (`type(x) is bool`). Error: `Cable unplugged often must be true or false.`
- `cabling.settings.power_post`: exactly `'RR'` or `'RL'`. Error: `The power post is RR or RL.`
- `cabling.settings.ignored_suggestions`: a list of at most 500 objects with exactly the keys `id` and `sig`; `id` a non-empty string of at most 120 characters, `sig` a non-empty string of at most 32 characters, ids unique. Errors in plain words (for example `Ignored suggestions are a list of at most 500 {id, sig} entries.`). Ids are not checked against current suggestions (they are computed in the page).

Unknown keys stay rejected everywhere as today.

**Tests:** extend `test_cable_plan.py`: round trip of each field through `cable_plan.validate` and through `rack_workspace` save/read on temporary data (follow the existing helpers), absence stays absent, and rejections for: wrong `carries`, non-bool `unplug_often` (including `1`), wrong `power_post` (including `'rr'`, `'FL'`), `ignored_suggestions` not a list, too long (501), entry with an extra key, missing `sig`, empty or over-long `id`/`sig`, duplicate ids.

**May change:** `outputs/Mechanical_Design_App/cable_plan.py`, `outputs/Mechanical_Design_App/test_cable_plan.py`. No existing test should become obsolete; if one does, stop and write it in the report instead of changing it. **Keep LF line endings** (check the file's current endings first and keep them). Do not touch `rack_workspace.py`, `workspace.js`, `rack-studio.js`, `index.html`, `app.py`, `cable-routes.js`, the asset manifest or `data/`.

**Done when:** `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1` passes, and the report lists the files with before/after SHA-256 and the commands run with their results.
