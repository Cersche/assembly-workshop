# 20 — "Needs an adapter cable" warning (pure JavaScript, existing cable modules)

**Goal:** Brian decided (2026-10-19, [E2E report](../equipment-wizard-options/E2E_Acceptance_Report.md) question 4): a cable that joins two **different connector types** gets a warning, **never a block**. It must appear where cable warnings already flow: the Cable panel and cable list (they call `LabRaxCables.warnings`), the wiring sheet notes and schedule CSV (`cable-sheet.js` calls the same function), the Review suggestions, and the parts order notes. Planning advice only; adapter fit is UNKNOWN.

## The rule (one helper, used everywhere)

Add to `cable-routes.js` and export as `connectorMismatch(rack, cable, ctx)`:
- Look up both ends that are ports (`{allocation, port}`) with `ctx.ports.portsFor(rack, placement, item)` (item = `ctx.library` entry whose id is `placement.equipment`, as cable-suggest.js `portInfo` does). Outside endpoints, missing ends and ports that no longer exist → no mismatch.
- Ignore type `'keystone'` (pass-through) and `'other'` and missing types.
- Mismatch when both remaining types exist and differ → return `{from: typeA, to: typeB, text}` with `text = 'Needs an adapter cable: ' + labelA + ' to ' + labelB + '.'` (labels from `ctx.ports.TYPES[type].label`, from-end first). Otherwise return `null`.
- Do not change `cable.type` or anything else in the rack. **Never mutate inputs.**

## Where it shows

1. `cable-routes.js` `warnings()`: append the mismatch `text` (after the existing warnings, same order otherwise). This automatically reaches the Cable panel, the cable list ⚠ flag, `cable-sheet.js` `schedule()`/`csv()`/`notes()`.
2. `cable-suggest.js`: new rule key `'adapter'` in `RULES` with title text `'Plan an adapter cable'`; for each mismatched cable `add('adapter', c.id, c.number + ' needs an adapter cable', 'One end is ' + labelA + ', the other ' + labelB + '. Plan an adapter cable or adapter; its fit is UNKNOWN.', {cables:[c.id], ports: portKeys(c)}, null, null, 'info')`. No apply action. It must work with Ignore/pruneIgnored like the other rules.
3. `cable-inventory.js`: a cable group whose cables include a mismatched cable gets the note `'needs adapter'` once (after `'check: incomplete'` when both apply).

## Tests

Extend `js-tests/cable-routes.js`, `js-tests/cable-suggest.js`, `js-tests/cable-sheet.js` and `js-tests/cable-inventory.js` (existing fixtures where possible): RJ45 ↔ USB-A warns with exact text; same type → none; keystone or other on one end → none; endpoint end → none; removed port → none; port type changed through a `rack.cabling.ports` override is respected; suggestion appears with level `'info'`, no apply, and can be ignored; sheet `notes()` and CSV warnings column include it; inventory note added once; nothing mutated (deep compare). Existing tests must keep passing unchanged unless a fixture really has mismatched ends (then say so in the report).

Run `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1`; it must pass.

**May change:** `cable-routes.js`, `cable-suggest.js`, `cable-inventory.js` and their four js-tests files (archive copies first). Do **not** touch `cable_plan.py` (saving must stay unblocked), workspace.js or any other file. Then write `20-adapter-cable-warning-REPORT.md` per the standing rules.
