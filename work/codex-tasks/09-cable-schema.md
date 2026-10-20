# 09 — Cable management Step 3: save validation for cables, exits, endpoints (Python)

**Goal:** let the rack document store Step 3 cabling data and reject bad data on Save. Decisions are in [work/cable-management/Step3_Decisions.md](../cable-management/Step3_Decisions.md) (read it; decisions 2, 6, 9, 11, 12, 13, 14 matter here). Planning data only: no geometry, STL, hardware pins or Pi4 path changes.

**Do:**
- New module `outputs/Mechanical_Design_App/cable_plan.py` (stdlib only) with `validate(value, slots, allocations, guide_ids)` returning cleaned `exits`, `endpoints`, `cables`, `settings`. `allocations` maps placement id → span. Reuse `cable_ports.PORT_TYPES` and `cable_ports.PORT_ID`.
- `rack_workspace._cabling`: accept the keys `exits`, `endpoints`, `cables`, `settings` beside `guides` and `ports`, and call `cable_plan.validate`. A rack without them must load and save exactly as today (no new keys added).

**Schema (all optional lists; ids are non-empty strings ≤ 80, unique within their list):**
- `exits` (≤ 32): `{id, position: 'bottom-rear'|'top-rear'|'left'|'right', slot: int 1..slots}`. No two exits with the same position and slot.
- `endpoints` (≤ 50): `{id, kind: 'wall-outlet'|'ups'|'modem'|'wall-jack'|'desk'|'other-rack'|'other', name: 1–60 chars after trim}`.
- `cables` (≤ 200): `{id, number: 1–12 chars, unique per rack; type: one of PORT_TYPES; color?: '#rrggbb'; service_loop_m: number 0–2; from, to; face_assumed?: 'rear'; route: {mode: 'auto'|'manual', guides: [guide ids, existing, no repeats, ≤ 48], exit: existing exit id or null}; route_changed?: bool; note?: ≤ 200 chars}`.
  - An end (`from`/`to`) is `null` (unconnected, decision 14), `{allocation, port}` (allocation must be in `allocations`; port matches `PORT_ID`; port existence is NOT checked, because wizard ports live in the library), or `{endpoint}` (must be an existing endpoint id).
  - A port end (`allocation`, `port`) may appear on at most one cable end in the whole rack (decision 13). Endpoints may be used by many cables.
  - `from` and `to` must not be the same end. Both ends `null` is allowed.
  - A cable with an endpoint end and no exits in the rack is still valid (decision 6 is a UI warning, not a save error).
- `settings`: `{guide_warn_above: int 1–50 (default 6), service_loop_m: number 0–2 (default 0.15)}`; unknown keys rejected.
- Unknown keys anywhere → clear `ValueError` messages in the same plain style as `_cabling`. Numbers: reject bool, NaN, inf.

**Tests:** new `test_cable_plan.py` (temporary data only): a full round trip through `rack_workspace.save` / `read`; a rack with only guides/ports unchanged; each rejection above (at least 20 cases, including duplicate port use across two cables, unknown guide/exit/endpoint/allocation references, bad colour, bool slot, too-long note). Register it in `work/gui-refinement/check_python.py` (one line).

**May change:** `outputs/Mechanical_Design_App/rack_workspace.py`, new `cable_plan.py`, new `test_cable_plan.py`, `work/gui-refinement/check_python.py` (registration only). Archive copies of existing files first. **Keep LF line endings** (do not convert files to CRLF). Do not touch `workspace.js`, `rack-studio.js`, `cable-ports.js`, `cable-routes.js`, the asset manifest or anything in `data/`; Claude is editing the front end in parallel.

**Done when:** `run_checks.ps1` passes and the report lists files with before/after SHA-256, the commands run and their results, and says nothing in `data/normal-use` was read or written.
