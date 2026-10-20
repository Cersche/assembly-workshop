# Equipment wizard: last two fixes (2026-10-19)

Both open wizard problems are fixed. Nothing is committed yet. No exports, prints or pushes were run.

## 1. Keystone faceplate was rejected as non-manifold

**What was wrong.** It was a real geometry defect, not the mesh check. OpenSCAD 2021 snaps 2D points to a 1/65536 mm grid. The golden keystone block is built from 2D outlines with depths 0.08 and 4.08 mm. Neither value is on that grid, so the block's front and back faces landed 0.0000134 mm off the plate's faces. Its top and bottom faces also landed a hair off the plate opening after the 3D move. That left a hair-thin sliver. In the STL, one edge was shared by four triangles instead of two, so the check was right to reject it.

**Fix (`equipment_tray.scad`, `ks_golden()` only):**
- The outline depths are shifted by −0.08 before `polygon()`, and the 0.08 is added back in the 3D move. The plate-flush faces now sit at exactly 0 and 4.0 mm, which are on the grid.
- The block is cut 0.1 mm oversize in height, then trimmed in rack coordinates by the same box that cuts the plate opening, so the faces match exactly.
- The mesh check is unchanged. The `KS_GOLD` table (golden opening dimensions) and `ks_tight=0.2` are byte-for-byte unchanged. In an old-vs-new comparison of the keystone block, all straight edges and the opening are identical. 11 points on the curved latch fillets moved by at most 0.0005 mm (rounding).

**Checked:** 1U faceplates with a keystone at −100, −75, +75 and +100 mm now pass `read_mesh` with no repair nudge. Before the fix, all four failed. A 2U plate with a keystone at +95 mm also passed through the app's own Render exact preview (`nudge_mm` 0). Old file: `docs/archive/pre_keystone_manifold_20261019/equipment_tray.scad`.

**Not checked:** other export qualities (Draft/Fine), the single-piece joint and 3U–5U plates. These are Codex task 16. Printed fit is still UNKNOWN. This change does not alter the printed v5 golden coupon files.

## 2. Rack view now draws each slot's own tray

Before, the rack view always drew the library item's mesh and showed "Placement not rendered yet". Now each wizard slot shows its own settings:

- **No slot tray settings:** the library item's build, as before.
- **Slot tray settings, exact render already exists** (from Render exact preview or Generate in Place on tray): that exact mesh. The new `POST /api/equipment-placement-mesh` route (`equipment.cached_allocation_render`) only checks whether the render exists. It never renders.
- **Slot tray settings, no exact render yet:** a box sketch of the same settings (`TrayPlacement.rackSketch` in `tray-placement.js`). It shows plate height (U), tray size, offset and rotation, rear support and bracket, and dark blocks where keystones and ports are cut. The inspector says it is a sketch and how to get the exact shape.

The old note is gone. Faceplate images and the selection outline now use the slot's own openings. After Render exact preview or Generate, the slot switches from the sketch to the exact mesh. Small fix found on the way: the wizard's "please redraw" signal had no listener. Library meshes only appeared on the next unrelated redraw. `workspace.js` now listens for it.

**Browser-checked** on a disposable copy (port 8789, `disposable-rackview-8789`): Test Switch in U03 was set to 90°, −30 mm offset, 2U and a keystone at +95. The rack showed the 2U sketch over U03–U04 with the keystone and LAN openings, and the keystone's cable port marker lined up in Rear view. After Render exact preview and a reload, the exact mesh loaded and the sketch note was gone. data/normal-use was not touched.

## Tests

`run_checks.ps1`: **102 Python (1 skipped) + 153 JS, all pass**. Before: 95 + 152.
- `test_keystone_mesh.py`: static checks run in run_checks (golden table hash, ks_tight, grid-safe depths, matching clip box). A real-render test runs only with `AW_RENDER_TESTS=1`, because run_checks starts no OpenSCAD. It was run by hand and passed.
- `test_tray_placement.py`: render lookup finds existing renders, never renders, and rejects invalid settings. The JS sketch tray size matches the Python/SCAD formulas.
- `js-tests/tray-placement.js`: sketch geometry, no render calls in the rack-view code, and the redraw wiring.
- `js-tests/equipment-rebuild.js`: updated one call for the new `partsFor(placement)` signature.

Archived originals: `docs/archive/pre_rack_tray_view_20261019/`. Fit, retention and strength stay UNKNOWN.
