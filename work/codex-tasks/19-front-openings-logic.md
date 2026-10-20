# 19 — Front openings follow the device + starting opening sizes (pure logic, JS + Python)

**Goal:** Brian decided (2026-10-19, [E2E report](../equipment-wizard-options/E2E_Acceptance_Report.md) questions 1 and 5): when the Place on tray window moves a wizard device, the faceplate openings for its **front ports move with it**; when the device is turned, the openings are **not guessed** (left where entered) and a plain warning says so. Each port type also gets an **editable starting opening size**. Write two small pure modules with the same behaviour, plus tests. Claude wires them into equipment.py, tray-placement.js, cable-ports.js and the wizard, so keep names and shapes exactly.

Background frames (read, do not change): `outputs/Mechanical_Design_App/equipment_tray.scad` (ports are `[x,z,w,h,r]`, X from plate centre, Z from plate bottom; plate_h = u·44.45 − 2.45; keystone block 21 × 33.5 mm from plate_h/2 − 15 to plate_h/2 + 18.5 around each keystone X), `equipment.py` `clean()` (port bounds), `tray-placement.js` `DEFAULTS`/`values()`.

## Frozen API — JavaScript `outputs/Mechanical_Design_App/port-openings.js`

Module pattern: copy `cable-inventory.js` (IIFE, `root.LabRaxPortOpenings = api`, `module.exports = api` under Node). No DOM, fetch, `window`, `Date`. **Never mutate inputs.**

```
DEFAULT_SIZES   {rj45:{w:17,h:14,r:1}, 'usb-a':{w:15,h:8,r:1}, 'usb-c':{w:12,h:7,r:3}, hdmi:{w:17,h:8,r:1},
                 'micro-hdmi':{w:11,h:7,r:2}, 'dc-barrel':{w:11,h:11,r:5.5}, iec:{w:28,h:20,r:1}, other:{w:15,h:8,r:1}}
SIZE_NOTE       'Starting size for this connector type: a guess, not a measured size. Edit it to match your device.'
defaultSize(type)          → copy of DEFAULT_SIZES[type], or of DEFAULT_SIZES.other for unknown/missing types
lift(spec)                 → 0 when spec.device_mount === 'straps', else +spec.standoff (missing standoff → 6, missing mount → 'inserts')
frontOpenings(libSpec, tray) → {ports, dx, dz, follows, rotation, message}
problems(ports, u, keystones) → [plain-language strings]
```

**frontOpenings:** `libSpec` = the library item's spec (ports as entered); `tray` = the slot's `placement.tray` (may be null/undefined/{}; only these keys count: dev_off_x, dev_rot, device_mount, standoff — tray keys win over libSpec keys, as `equipment.allocation_spec()`).
- `rotation` = effective `dev_rot` (number, default 0).
- If `rotation === 0`: `dx = eff.dev_off_x − (libSpec.dev_off_x || 0)`, `dz = lift(eff) − lift(libSpec)` (missing offsets = 0), `follows = true`, every port gets `x + dx`, `z + dz` (other keys copied unchanged; round x/z to 3 decimals like `equipment.num()`), `message = null`.
- If rotation is 90, 180 or 270: `dx = dz = 0`, `follows = false`, ports are copies as entered, and `message` is exactly:
  - 90/270: `'The device is turned <rotation>°, so its front ports now face the side of the tray. The front openings no longer line up with them. The faceplate STL keeps the openings where they were entered in the library (not moved). Check them, or remove them in Edit library item.'`
  - 180: same text with `'now face the rear of the tray'` instead of `'now face the side of the tray'`.
- No ports → `ports: []` (still return dx/dz/follows/rotation/message as above; message only when rotated **and** at least one front port exists, else null).

**problems(ports, u, keystones):** one message per broken opening, in port order, label = `p.label || 'Port ' + (index+1)`. plate_h = u·44.45 − 2.45, PLATE_HALF = 126. Checks (same limits as `equipment.clean()`, plus the keystone block):
- `|x| + w/2 > 126` → `'<label> opening would run past the faceplate edge. Move the device back toward the centre or edit the port.'`
- `z − h/2 < 2` or `z + h/2 > plate_h − 2` → `'<label> opening would run off the top or bottom of the faceplate. Change the standoff or faceplate height, or edit the port.'`
- overlaps any keystone block (`|x − k| < 10.5 + w/2` and the Z ranges `[z−h/2, z+h/2]` and `[plate_h/2 − 15, plate_h/2 + 18.5]` overlap) → `'<label> opening would cut into keystone <n> (at X = <k> mm). Move the device or the keystone.'` (n = 1-based keystone index; k as given).
- At most one message per port (first failing check in the order above). Non-finite x/z/w/h → skip the port.

## Frozen API — Python `outputs/Mechanical_Design_App/port_openings.py`

Same rules and identical strings, stdlib only:
```
DEFAULT_SIZES, SIZE_NOTE
default_size(type) -> dict
lift(spec) -> float
front_openings(lib_spec, tray) -> dict with keys 'ports','dx','dz','follows','rotation','message'
problems(ports, u, keystones) -> list[str]
```
Python degree sign is `°` (U+00B0), same as JS. Numbers: format k in messages with `:g` in Python and the plain JS number in JS (fixtures use values where they print the same, e.g. 60, -60, 72.5).

## Tests

- `outputs/Mechanical_Design_App/js-tests/port-openings.js` (node:test) and `outputs/Mechanical_Design_App/test_port_openings.py` (unittest), sharing the same fixtures written in each file: no tray → unchanged; offset +11 → x+11; tray standoff 10 vs library 6 → z+4; straps vs inserts(6) → z−6; library already offset 5, tray 5 → unchanged; rotation 90/180/270 → as entered, exact messages; rotation with no ports → message null; unknown type → other size; defaultSize returns a copy (mutating it does not change the table); problems: edge, top/bottom, keystone overlap (and a just-clear case), one message per port, non-finite skipped; inputs not mutated (deep compare).
- Register the JS test in `run_checks.ps1` like `js-tests/tray-placement.js`; add `'test_port_openings'` to the module tuple in `work/gui-refinement/check_python.py`.
- Run `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1`; it must pass.

**May change:** `port-openings.js`, `port_openings.py`, `js-tests/port-openings.js`, `test_port_openings.py` (all new); `run_checks.ps1` and `work/gui-refinement/check_python.py` (registration only; archive copies first). Do **not** touch equipment.py, equipment_tray.scad, tray-placement.js, cable-ports.js, equipment-wizard.js or index.html (Claude integrates). No renders, no server. Then write `19-front-openings-logic-REPORT.md` per the standing rules.
