# 14 — Cable inventory / parts order (pure JavaScript module)

**Goal:** a pure, Node-testable module `outputs/Mechanical_Design_App/cable-inventory.js` that turns a **saved** rack's cable plan into a grouped parts list and CSV. Claude builds the Review card against the API below, so keep names and shapes exactly. Decisions (defaults): [work/cable-management/Parts_Order_Decisions.md](../cable-management/Parts_Order_Decisions.md). Data shape: Step 3 `cabling` block ([Step3_Decisions.md](../cable-management/Step3_Decisions.md)). Planning only: lengths are estimates; nothing claims a cable, jack or guide fits.

**Module pattern:** copy `cable-sheet.js` (IIFE, `root.LabRaxCableInventory = api`, `module.exports = api` under Node). No DOM, fetch, `window` or `Date`. **Never mutate `rack`.** Context `ctx = {ports: LabRaxPorts, cables: LabRaxCables, library: [items]}` exactly as cable-sheet.js uses it. Use `ctx.cables.estimate` for lengths and `ctx.ports.portsFor(rack, placement, item)` / `ctx.ports.TYPES` for ports and type labels. Do not change any other module.

## Frozen API (exact export list)

```
LIMITS          'Lengths are planning estimates. Jack type, guide capacity, cable fit and strength are UNKNOWN. No prices or purchases.'
STOCK_LENGTHS_M [0.15, 0.3, 0.5, 1, 1.5, 2, 3, 5]
CSV_COLUMNS     ['Section','Item','Quantity','Buy or print','Cables','Notes']
stockLength(m)          → number from STOCK_LENGTHS_M (smallest ≥ m), or null when m > 5 or not finite
items(rack, ctx)        → [row]
csv(rack, ctx, meta)    → string (meta = {savedAt?: string})
```

**row** (all keys always present): `{section: 'cables'|'keystones'|'guides', key, item, quantity, source: 'buy'|'print', cables: [numbers], notes: [strings]}`

- **cables:** group by `cable.type` and `stockLength(estimate.length_m)`. `key = 'cable:' + type + ':' + (stock ?? 'custom')`. `item = '<type label> · <stock> m'` (label from `ctx.ports.TYPES[type]?.label`, else the raw type, else `'Unknown type'`), or `'<label> · custom length (≥ <length_m> m)'` with the largest length in the group when stock is null. `cables` = the cable numbers in numeric order (same sort as `cable-sheet.sortCables`). Notes: `'check: incomplete'` once if any cable in the group has `estimate.complete === false` or an end whose placement/port/endpoint no longer exists. Every cable is counted, including incomplete ones.
- **keystones:** one row, `key = 'keystones'`, `item = 'Keystone jack'`, quantity = number of distinct `ks-N` pass-throughs across all placements (count each `ks-N-front`/`ks-N-rear` pair once per placement). `source:'buy'`, note `'Jack type UNKNOWN'`. Omit the row when the quantity is 0.
- **guides:** one row, `key = 'guides'`, `item = 'Lab Rax Cable Guide'`, quantity = `rack.cabling.guides.length`, `source:'print'`, note `'Local model only; not in PRINT THE RACK; never redistributed'`. Omit when 0.
- Order: cables (by type label, then stock length ascending, custom last), keystones, guides.

**csv:** UTF-8 BOM, CRLF record endings, every field quoted and formula-guarded the same way as `cable-sheet.csv`. Header row `CSV_COLUMNS`; `Cables` joined with `' '`, `Notes` with `'; '`. Final two lines: a row with `LIMITS` in Notes, and `Saved <savedAt>` when given.

## Tests and checks

Add `outputs/Mechanical_Design_App/js-tests/cable-inventory.js` (node:test, fixtures built in code): stock rounding at boundaries (0.15, 0.16, 5, 5.01, NaN); grouping across types; custom length row; incomplete flag (unconnected end and removed port); keystone pair counted once; guides row; empty rack → `[]`; CSV quoting/guarding/BOM/CRLF; rack is not mutated (deep-compare before/after). Register it in `run_checks.ps1` the same way task 13 did. Run `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1`; it must pass.

**May change:** `cable-inventory.js` (new), `js-tests/cable-inventory.js` (new), `run_checks.ps1` (registration only; archive copy first). Then write `14-cable-inventory-logic-REPORT.md` per the standing rules.
