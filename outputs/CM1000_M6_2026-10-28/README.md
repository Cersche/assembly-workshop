# CM1000 bracket, M6 revision — test-print ID CM6A (2026-10-28)

PROPOSED — UNPRINTED. Fit, strength and insert retention UNKNOWN. Not printed.

Netgear CM1000 bracket for U9, redone with the rack's M6 hardware (Brian, 2026-10-28). Built on the
printed baseline `outputs/STL_Deliveries/2026-10-16_CM1000_bracket/` (`CM1000_LabRax_faceplate.3mf` +
`CM1000_LabRax_rails_v2.3mf`, which fit); those files stay untouched. Remix of noyoustupid / Jsmaz3
(CC BY-NC-SA): personal use, keep local/private, never redistribute.

## Print file

`CM6A_CM1000_M6_bracket_set.3mf`: three objects side by side.
- **CM6A-F faceplate**: front face down. Same colour parts as the baseline (5 light pipes, logo, 2 details) as parts of this object; assign filaments as before.
- **CM6A-L / CM6A-R rails**: on their outer faces (baseline orientation, without the 45° bed turn).

Single STLs (rack frame, same coordinates as the baseline 3MFs): `CM6A_faceplate.stl` (body only, no colour parts), `CM6A_rail_l.stl`, `CM6A_rail_r.stl`.
The ID (CM6A-F / -L / -R) is engraved 0.5 mm into each part's top face.

## Hardware (one item)

| Where | Baseline | CM6A |
|---|---|---|
| Faceplate → rails | 4 × M3 heat-set inserts (4 mm pocket) + 4 × M3 screws | 4 × M6 heat-set inserts (rack-post type) + 4 × **M6 × 8 button head** |
| Faceplate → rack | 4 corner slots, M6 rack screws | same 4 slots **+ 2 middle slots** (one per ear, at the U centre) = 6 × **M6 × 8 button head** into the posts' unused middle inserts |

Total: 4 inserts, 10 × M6 × 8 button heads. Hex key 4 mm.

## Changes from the baseline

- Insert pilots: Ø7.6 × 7 deep (Y9..16.5) in the faceplate's rear stubs. Walls to the modem pocket ≥ 2.0 mm (2.0–2.4 at Y12). Ø7.6 is the rack post's insert hole, which Brian says fits the inserts perfectly; insert OD/length are not measured.
- Joint screws moved from x23/231, z8.8/35.7 to **x22.6/231.4, z8.6/35.85** (toward the outer face and floor) so the Ø7.6 pilot keeps about 2 mm of wall to the pocket corner (1.8 at the old spot).
- Rails: M6 clearance Ø6.6 through the 4 mm flange (Y16..20); flange wall ≥ 2.5 mm; head/key bays 12 mm tall (head Ø10.5) and 34 mm deep (Y20..54) so a standard 4 mm L-key's short arm (~29 mm) fits. Rail floor and top under the bays are 2.6 mm (baseline 3.3). M6 × 8 through the 4 mm flange leaves about 4 mm of thread in the insert.
- Middle rack slots: copies of the lower corner slots moved up to the U centre (z22.225), x8.7 / x245.3, matching the posts' middle hole (from the drive-tray session's mesh check: holes at U centre and ±15.9).
- Ear fills are inset 0.05 mm from the plate's front, back, top and bottom faces (coplanar faces broke the mesh export); below one layer.
- Kept: plate height 44.45 (baseline, fits; not reshaped to the 44.4 wizard standard), four corner slots, modem pocket, rails v2 access-bay idea, hidden screws (all joint screws from behind), light pipes, logo.

## Checks run (digital only)

All three STLs are closed (watertight) single solids; walls measured by slicing. Not printed, no slicer check. Fit, strength, insert retention, thread engagement and key access UNKNOWN.

## Rebuild (PC)

From `src/`: `python extract.py` (baseline parts → `orig/`), then OpenSCAD.exe on `cm1000_m6.scad` with `-D part="rail_l"`, `"rail_r"` and `"id_F"` (→ `orig/id_F.stl`), then the faceplate with FreeCAD:
`"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('faceplate_freecad.py').read())"` (OpenSCAD 2021's CGAL fails on the baseline faceplate's sliver triangles), then `python pack.py`.
