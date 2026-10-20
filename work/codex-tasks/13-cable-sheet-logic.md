# 13 — Cable management Step 5: schedule, CSV and label text (pure JavaScript module)

**Goal:** a pure, Node-testable module `outputs/Mechanical_Design_App/cable-sheet.js` that turns a **saved** rack's cable plan into the cable schedule rows, the CSV text, the wrap-label texts and the sheet notes. Claude is building the drawing, the printable pages and the Review card against the API below **in parallel**, so keep the names and return shapes exactly as written. Decisions: [work/cable-management/Step5_Decisions.md](../cable-management/Step5_Decisions.md) (read all 11 and the defaults). Data shape: Step 3's `cabling` block ([Step3_Decisions.md](../cable-management/Step3_Decisions.md)) plus the Step 4 additions. These are planning documents: lengths are estimates and nothing here claims a real cable or guide fits.

**Module pattern:** copy `cable-routes.js` (IIFE, `root.LabRaxCableSheet = api`, `module.exports = api` under Node). No DOM, no fetch, no `window`, no `Date` (the caller passes the save time). **Never mutate `rack` or its contents** (no `upkeep` call). Context: `ctx = {ports: LabRaxPorts, cables: LabRaxCables, suggest: LabRaxCableSuggest | undefined, library: [items]}`. Use `ctx.cables` for `estimate`, `warnings`, `linkedCable`, `endFace`, `cableColor`, `EXIT_POSITIONS`. Use `ctx.ports.portsFor(rack, placement, item)` (item = `ctx.library.find(i => i.id === placement.equipment)`) and `ctx.ports.TYPES`. Do not change `cable-routes.js`, `cable-ports.js` or `cable-suggest.js`.

**Shared helpers (internal):** `pad = n => String(n).padStart(2, '0')`; equipment name = `placement.assembly?.name || item?.name || 'Equipment'`; a keystone port is one with `type === 'keystone'` whose id matches `/^ks-(\d+)-(front|rear)$/`, and its short name is `'K' + n`; guide label = `post + ' U' + pad(slot)` (e.g. `RR U03`); exit label = `EXIT_POSITIONS[position]`, plus `' U' + pad(slot)` for `left` / `right` (e.g. `Bottom rear`, `Left side U04`).

## Frozen API (exact export list)

```
LIMITS        'Lengths are planning estimates. Guide capacity, cable fit, bend tolerance and strength are UNKNOWN.'
CSV_COLUMNS   ['Number','From','To','Type','Carries','Colour','Route','Exit','Length estimate (m)','Service loop (m)','Linked to','Warnings','Note']
sortCables(rack)                → new array of rack.cabling.cables, sorted by number with
                                   String(a.number).localeCompare(String(b.number), undefined, {numeric: true}), ties by id
endName(rack, end, ctx)         → string (long form, for the schedule)
shortName(rack, end, ctx)       → string (short form, for labels)
faceOf(rack, cable, ctx)        → 'front' | 'rear'
schedule(rack, ctx)             → [row]   (sortCables order)
csv(rack, ctx, meta)            → string  (meta = {savedAt?: string})
labels(rack, ctx)               → [label]
notes(rack, ctx)                → [{number, text}]
```

**`endName`:**
- `null` → `Unconnected`.
- An endpoint → `<name> (outside)`. A missing endpoint → `Removed endpoint`.
- A port → `<equipment> · <port.label> (U<pad slot><face>)`, where slot is `placement.slot`. `<face>` is `''` for a keystone port, because its label already says front or rear. Otherwise it is `' front'` or `' rear'` when `ctx.cables.endFace` is known, else `', face UNKNOWN'`. Examples: `Raspberry Pi 4 · Ethernet (U01 rear)`, `Keystones · Keystone 1 · rear (U02)`, `Box · USB (U05, face UNKNOWN)`.
- A missing placement → `Removed equipment`. A missing port → `<equipment> · removed port`.

**`shortName`:**
- A keystone port → `K<n>`.
- Another port → the equipment name.
- An endpoint → its name.
- `null` → `unconnected`.
- A missing placement, port or endpoint → `removed`.

**`faceOf`:** `'front'` only when both ends are ports and `ctx.cables.endFace` is `'front'` for both. Otherwise `'rear'`.

**`schedule` row** (all keys always present):
```
{id, number, face,                          // face = faceOf
 from, to,                                  // endName
 type,                                      // ctx.ports.TYPES[type]?.label || type
 carries,                                   // ctx.suggest ? ctx.suggest.carries(rack, cable, ctx) : (cable.carries || '')
 colour,                                    // ctx.cables.cableColor(cable)
 route,                                     // guide labels in route order joined ' → ', or 'direct' when none; + ' (manual)' when route.mode === 'manual'; guide ids not in the rack are skipped
 exit,                                      // exit label of route.exit, '' when none or missing
 length_m,                                  // estimate.length_m when estimate.complete, else null
 to_exit,                                   // estimate.to_exit
 length,                                    // '' when length_m is null, else length_m.toFixed(1) + (to_exit ? ' to exit' : '')
 service_loop_m,                            // cable.service_loop_m ?? settings.service_loop_m ?? 0.15
 linked,                                    // '' or '<other number> via K<n>' (see below)
 warnings,                                  // ctx.cables.warnings(rack, cable, ctx) (array of strings)
 note}                                      // cable.note || ''
```
`linked`: take `ctx.cables.linkedCable(rack, cable, ctx)`. If it names a cable that exists, the text is `<that cable's number> via <shortName of this cable's keystone end>`. Otherwise it is `''`.

**`csv`:**
- The text starts with `'﻿'`. Every line ends with `\r\n`, including the last.
- Line 1 is one field: `# <rack.name || 'Rack'> cable schedule · saved <meta.savedAt || 'time unknown'> · lengths are planning estimates; fit and capacity UNKNOWN`.
- Line 2 is `CSV_COLUMNS`. Then one line per schedule row, in this order: number, from, to, type, carries, colour, route, exit, length, `String(service_loop_m)`, linked, warnings joined with `' '`, note.
- Field rules, in order:
  - If the value starts with `=`, `+`, `-`, `@`, a tab or CR, prefix `'`.
  - Then quote the field (wrap in `"` and double any `"`) if it contains `,`, `"`, CR or LF, or has leading or trailing spaces.

**`labels`:** for each cable in `sortCables` order, and for each of `from` then `to` that is not `null`, one label:
```
{cable: id, number, end: 'from' | 'to',
 text: '<number> · <shortName this end> → <shortName other end>',   // e.g. 'C7 · K1 → Modem', 'C8 · Pi 4 → unconnected'
 sub:  '<type label> · this end: <detail>'}                         // e.g. 'RJ45 (Ethernet) · this end: K1 rear'
```
`<detail>` depends on the end:
- a keystone port → `K<n> front` or `K<n> rear`;
- another port → `<equipment> <port.label>`;
- an endpoint → its name;
- anything missing → `removed`.

**`notes`:** for each cable in `sortCables` order, one `{number, text}` per string in `ctx.cables.warnings(rack, cable, ctx)`. The caller adds `LIMITS` itself.

## Tests

Add a new `js-tests/cable-sheet.js` and register it in `run_checks.ps1` the same way as `cable-suggest.js`. Build the fixtures in code, in the `js-tests/cable-routes.js` style: a 6U rack named with a comma and a quote, a pi4 placement, and a fake wizard item with rear ports, an IEC port and `keystones: [0]`. Give the wizard placement an `assembly.name`, add endpoints and a bottom-rear exit, and use real `cable-ports.js`, `cable-routes.js` and `cable-suggest.js`.

Cover:
- the exact export list, and loading in `vm` without window, DOM or fetch;
- numeric sort (C2 before C10, ties by id);
- every `endName` and `shortName` case;
- `faceOf` for front/front, front/rear and endpoint cables;
- every schedule field: manual suffix, skipped missing guide, `direct`, left/right exit labels, `to exit`, an incomplete cable giving `''` and `null`, `linked` both ways on a keystone pair;
- `carries` with and without `ctx.suggest`;
- CSV: BOM, CRLF, header, quoting of comma, quote and newline, the formula guard, field order and row count;
- labels: both ends, an unconnected end, keystone detail;
- notes;
- no mutation (a deep-equal of the rack before and after every call).

**May change:** new `outputs/Mechanical_Design_App/cable-sheet.js`, new `outputs/Mechanical_Design_App/js-tests/cable-sheet.js`, `outputs/Mechanical_Design_App/run_checks.ps1` (registration only), and this task's REPORT file. **Keep LF line endings** in all of them. Do not touch:
- `workspace.js`, `rack-studio.js`, `index.html`, `app.py` or the asset manifest;
- `cable-routes.js`, `cable-ports.js`, `cable-view.js` or `cable-suggest.js`;
- `cable-sheet-view.js` or `js-tests/cable-sheet-view.js` (Claude's, in progress);
- `data/`.

Claude wires the module into the page.

**Done when:** `run_checks.ps1` passes and the report lists the API as built (any deviation called out), the files with before/after SHA-256, and the commands run with their results.
