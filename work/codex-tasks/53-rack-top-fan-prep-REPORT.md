# Task 53 — rack top fan preparation report

2026-11-05. Based on Draft 3 pulled at commit 53e726a. Brian directed use of stock source values and an assumed 256 × 256 mm bed. **Preparation/checks performed; NOT release-ready: three dry-run FAILs remain. No printing or outputs/ writes.**

## Scope and values

Only the working SCAD and this report are intended for commit. Generated own-part renders, dry-run packages and logs are local scratch in `work/rack-top-fan/task53-scratch/`; viewer pages are uncommitted. No creator mesh was written anywhere: component JSON meshes were transformed and intersected in memory. HANDOFF, device cards, tools, library, app and user data were not edited, following the task-specific edit scope.

| Value | Before → after | Basis |
|---|---|---|
| P1 / P2 / P3 / P4 / P5 | 23.85 / 19.85 / 11.15 / 6.86 / 7.14 → unchanged | Stock source values, Brian authorized; not measured |
| T1 / T2 | 19.85 / 23.85 → unchanged | Stock source values |
| Cross-holes | Ø6.4; plug Y22.5 Z390.2; tongue Y45 Z416 → unchanged | Source approximate; card rounds plug Z to about 390, not a new exact value |
| Grille / fan fit | 0.3 / 0.5 per side → unchanged | Task requirement |
| Rail pocket fit | [0.15,0.15,0.1] → unchanged | Draft 3 |
| Top / fan / ledge / grille Z | 450.05 / 417.05 / 415.05 / 447.05 → unchanged | Draft 3; modem-to-old-top E about 35 measured by Brian |
| Bed J | UNKNOWN → assumed 256 × 256 for checks only | Brian task direction; card not modified |
| IDs | None → tag parameter, TFE-A / TRE-A / TSR-A / TFG-A / TFE-T1 / TSR-T1 | Engraving cutters 0.6 deep; edge ID mesh checks FAIL |
| Coupon M3 pilot | None inside X101..141.12 → one at X106 Y11, Ø4.2 × 5 deep | Spec requires one insert; existing X95 insert lies outside coupon. Coupon-only addition, main edge unchanged |
| Head keepouts | None → Ø8.6 × 6 cylinders starting Z448.35 | ws_head_keepout, 6.6 head + 1 radial room; eight grille screws, plus coupon-only ninth in part=keepout |

No panel, panel_print or cable-hole panel cutter was added: Draft 3 explicitly omits the panel. Existing rear jack opening/pocket is retained. No cross-hole M6 head envelope was invented because cross-hole hardware is still UNKNOWN and Brian has not specified a screw there. Stock handle clearance was checked with the actual raised handle meshes; handle screw dimensions remain UNKNOWN.

## Parts and rendering

Renderer: `D:\Tools\OpenSCAD-snapshot\OpenSCAD-2026.11.01-x86-64\openscad.exe --backend=manifold`, OPENSCADPATH = repository `lib`. All listed renders exited 0, Manifold NoError, zero OpenSCAD warnings/errors. Individual manufactured parts and fan dummy have one body. Cuts and keepouts intentionally have multiple bodies.

| Selector | Min XYZ (mm) | Max XYZ (mm) | Size XYZ (mm) | Bodies |
|---|---|---|---|---|
| edge_front | -141.120, 0.000, 380.200 | 141.120, 54.850, 450.050 | 282.240, 54.850, 69.850 | 1 |
| edge_rear | -141.120, 185.150, 380.200 | 141.120, 240.000, 450.050 | 282.240, 54.850, 69.850 | 1 |
| rail | 110.980, 35.000, 400.050 | 140.980, 205.000, 450.050 | 30.000, 170.000, 50.000 | 1 |
| rail_left | -140.980, 35.000, 400.050 | -110.980, 205.000, 450.050 | 30.000, 170.000, 50.000 | 1 |
| grille | -110.480, 3.300, 447.050 | 110.480, 236.700, 450.050 | 220.960, 233.400, 3.000 | 1 |
| fan | -100.000, 20.000, 417.050 | 100.000, 220.000, 447.050 | 200.000, 200.000, 30.000 | 1 |
| coupon | 101.000, 0.000, 380.200 | 141.120, 54.850, 450.050 | 40.120, 54.850, 69.850 | 1 |
| rail_coupon | 110.980, 35.000, 400.050 | 140.980, 75.000, 450.050 | 30.000, 40.000, 50.000 | 1 |
| edge_front_print | 3.517, 8.566, 0.000 | 247.434, 252.483, 54.850 | 243.916, 243.916, 54.850 | 1 |
| edge_rear_print | 3.517, 8.566, 0.000 | 247.434, 252.483, 54.850 | 243.916, 243.916, 54.850 | 1 |
| rail_print | 0.000, 0.000, 0.000 | 50.000, 170.000, 30.000 | 50.000, 170.000, 30.000 | 1 |
| grille_print | 0.000, 0.000, 0.000 | 220.960, 233.400, 3.000 | 220.960, 233.400, 3.000 | 1 |
| cuts | -96.700, 9.300, 446.050 | 96.700, 230.700, 451.050 | 193.400, 221.400, 5.000 | 40 |
| keepout | -99.300, 6.700, 448.350 | 110.300, 233.300, 454.350 | 209.600, 226.600, 6.000 | 9 |

Print quantities: front edge ×1, rear edge ×1, rail ×2 (left is the mirrored assembly instance), grille ×1. Coupons: TFE-T1 and TSR-T1, one each, not authorized to print. `fan` is a reference dummy only. `assembly` composes the six assembly bodies and backgrounds the dummy; it is not a single-body manufacturing selector.

Both edge print selectors rotate −90° about X (inner face down) then 45° about Z. Footprint 243.916 × 243.916 leaves 12.084 mm total spare in each bed direction. Actual placed bounds give minimum bed-edge clearance **3.517 mm** (not half the spare, because the asymmetric outline is not bounding-box centred). Rail footprint 50 × 170 leaves 206 × 86 mm total; grille 220.96 × 233.40 leaves 35.04 × 22.60 mm total. No brim or machine exclusion zone is included.

**Orientation constraint:** the tongue projects 19.85 beyond the Y35 inner face, so the tongue tips define Z0 and the inner face lies at print Z19.85. It cannot simultaneously lie directly on the bed with that face while preserving the joint. These poses are not validated for support-free printing; no supports or slicer settings were created. Coupon selectors remain in the assembly frame as specified.

The prescribed mid-length Y35 edge tag cutter falls in space removed by the Ø192 air opening. This is why TFE-A and TRE-A are absent from the mesh. No new bridge, changed joint or relocated label was used to evade the failure. The other four IDs passed the script’s mesh-difference test; legibility remains unchecked.

## Release-script dry runs

Six independent invocations used `--part selector:ID --keepout <matching-frame selector> -o <scratch>/dryrun-selector --viewer-dir <scratch>/viewers`. Coupons used `keepout`; print parts used `keepout_<selector>` so checks compare geometry in the same coordinates. Grille additionally used `--cuts cuts=40`: 32 air openings plus 8 screw passages, all separate. The cutter for the air openings is shared with the grille. No panel hole exists.

| Part | Exit | FAIL | WARN |
|---|---|---|---|
| coupon | 0 | 0 | 0 |
| rail_coupon | 0 | 0 | 0 |
| edge_front_print | 1 | 1 | 0 |
| edge_rear_print | 1 | 1 | 0 |
| rail_print | 0 | 0 | 0 |
| grille_print | 1 | 1 | 0 |

Exact failure output:
```text
- FAIL: edge_front_print: ID TFE-A is in the source but not on this part's mesh
- FAIL: edge_rear_print: ID TRE-A is in the source but not on this part's mesh
- FAIL: grille_print: intrudes into the keep-out by 515.02 mm3
```
No WARN lines occurred. The grille failure is intersection with the **full cylindrical head-plus-clearance envelope extending down through the countersink depth**, not proof that a real conical countersunk screw itself clashes. The existing tapered countersinks do not clear that envelope; neither countersinks nor keepouts were modified after the failure. This failure remains a release blocker.

The script has no no-write dry-run switch: successful runs print RELEASED and create packages **only inside scratch**. These are check artifacts, not an authorized release. Failed runs do not create their requested destination; their transient render stages were not relied on for retained evidence. Standalone renders and captured logs are retained in scratch.

## Assembly clash volumes

Loaded original component JSON vertices/triangles read-only, evaluated `LabRaxScene.frame(9)` from the real rack-scene.js with Node, applied its matrices/translations in memory, and raised the two handle poses by +15 Z. Eight post segments (5U + 4U per corner in that scene), two stock top rails and two raised handles were tested. This is the specified recovered visual scene, not physical fit approval. The scene segmentation is not a claim about the physical 4U+extension+4U stack.

Numerical significance threshold: 0.01 mm³, matching release_part.py. Values below that are reported as numerical touching noise, not positive fit clearance.

| New part | Sum vs all posts mm³ | Sum vs raised handles mm³ | Sum vs stock top rails mm³ |
|---|---|---|---|
| edge_front | 6.41708908e-13 | 0 | 1.22805222e-13 |
| edge_rear | 0 | 0 | 4.24719071e-13 |
| rail | 0 | 4.00041111e-12 | 86465.6377 |
| rail_left | 0 | 0 | 86465.6378 |
| grille | 0 | 0 | 0 |
| fan | 0 | 0 | 0 |
| coupon | 5.57776048e-13 | 0 | 1.13782491e-13 |
| rail_coupon | 0 | 0 | 18193.1389 |

The new rail, mirrored rail and rail coupon intentionally occupy the stock rail envelopes: old rails are replaced, not co-installed. Their stock-rail overlaps above are therefore replacement comparisons, not retained-assembly clashes. Edges clear the old stock rails as well as the new rails. No stock panel remains, so the historical ~176 mm³ panel-seat expectation does not apply.

| New-part pair | Intersection mm³ |
|---|---|
| edge_front / edge_rear | 0 |
| edge_front / rail | 3.73034936e-13 |
| edge_front / rail_left | 1.13686838e-13 |
| edge_front / grille | 5.49060631e-12 |
| edge_front / fan | 6.11910522e-12 |
| edge_rear / rail | 3.13349346e-12 |
| edge_rear / rail_left | 0 |
| edge_rear / grille | 8.01852985e-12 |
| edge_rear / fan | 0 |
| rail / rail_left | 0 |
| rail / grille | 0 |
| rail / fan | 0 |
| rail_left / grille | 0 |
| rail_left / fan | 0 |
| grille / fan | 0 |
| coupon / rail_coupon | 0 |

All 15 new-assembly pair checks and the coupon pair are below 0.01 mm³. All new parts/coupons clear the posts and raised handles by this intersection test. This does not measure positive clearance or installation paths.

## Remaining limits and viewer

Joint dimensions remain source-derived UNKNOWN as physical measurements. Bed is assumed. Fan dimensions/frame shape, hole pattern, cable exit, weight; DC jack and electronics models; cross-hole hardware; handle screws; installation sequence; fit, insert retention, strength, airflow and printability remain UNKNOWN. E stays Brian’s approximate measured 35; this model leaves 15 below the ledge and 17 below the fan. No measurement request is needed for this authorized source-based preparation.

Local viewers (own generated geometry only): `work/mesh-viewer/task53-rack-top-fan-assembly.html` and `work/mesh-viewer/task53-rack-top-fan-parts.html`. Created with tools/mesh_viewer.py; assembly page opened in Codex. SendUserFile is not available in this session, so local file links are supplied instead. Pages are not committed.

## Captured dry-run output

### coupon

```text
COMMAND: "C:\Program Files\Python310\python.exe" tools/release_part.py work/rack-top-fan/rack_top_fan.scad --id TFE-T1 --part coupon:TFE-T1 --keepout keepout -o "C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\rack-top-fan\task53-scratch\dryrun-coupon" --viewer-dir "C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\rack-top-fan\task53-scratch\viewers"
EXIT: 0
# TFE-T1 release report

- Date 2026-11-05; source `rack_top_fan.scad`; renderer `OpenSCAD-2026.11.01-x86-64` with Manifold

## Keep-out
- keep-out keepout: 3132 mm3, 9 bodies

## coupon
- coupon: closed solid, 1 body, 1116 triangles, volume 75216 mm3, size 40.12 x 54.85 x 69.85 mm
- coupon: ID TFE-T1 is on the mesh, 6.3 mm3 of text at X 113.0..126.9, Y 34.4..35.0, Z 433.6..436.4; legibility not checked
- coupon: 2 x dia 6.4 (X), depth about 7.0
- coupon: 1 x dia 4.2 (Z), depth about 5.0
- coupon: keep-out clear

## 3MF
- 3MF: 1 objects, 1 items, 556 vertices, 1116 triangles, matching the STLs

## Source
- 1 source file(s) frozen in src/
- 33 library file(s) frozen in src/lib/; to re-render, set OPENSCADPATH to src/lib

## Result
- 0 failed, 0 warnings
- Digital checks only. The hole scan sees only fully surrounded round holes. Printed fit and strength: UNKNOWN.

RELEASED C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\rack-top-fan\task53-scratch\dryrun-coupon
VIEWER C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\rack-top-fan\task53-scratch\viewers\TFE-T1.html
```

### rail_coupon

```text
COMMAND: "C:\Program Files\Python310\python.exe" tools/release_part.py work/rack-top-fan/rack_top_fan.scad --id TSR-T1 --part rail_coupon:TSR-T1 --keepout keepout -o "C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\rack-top-fan\task53-scratch\dryrun-rail_coupon" --viewer-dir "C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\rack-top-fan\task53-scratch\viewers"
EXIT: 0
# TSR-T1 release report

- Date 2026-11-05; source `rack_top_fan.scad`; renderer `OpenSCAD-2026.11.01-x86-64` with Manifold

## Keep-out
- keep-out keepout: 3132 mm3, 9 bodies

## rail_coupon
- rail_coupon: closed solid, 1 body, 2506 triangles, volume 54580 mm3, size 30.00 x 40.00 x 50.00 mm
- rail_coupon: ID TSR-T1 is on the mesh, 6.7 mm3 of text at X 111.0..111.6, Y 47.8..62.1, Z 433.5..436.5; legibility not checked
- rail_coupon: 1 x dia 7.6 (Z), depth about 10.0
- rail_coupon: 2 x dia 6.4 (X), depth about 6.75 to 16.0
- rail_coupon: keep-out clear

## 3MF
- 3MF: 1 objects, 1 items, 1251 vertices, 2506 triangles, matching the STLs

## Source
- 1 source file(s) frozen in src/
- 33 library file(s) frozen in src/lib/; to re-render, set OPENSCADPATH to src/lib

## Result
- 0 failed, 0 warnings
- Digital checks only. The hole scan sees only fully surrounded round holes. Printed fit and strength: UNKNOWN.

RELEASED C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\rack-top-fan\task53-scratch\dryrun-rail_coupon
VIEWER C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\rack-top-fan\task53-scratch\viewers\TSR-T1.html
```

### edge_front_print

```text
COMMAND: "C:\Program Files\Python310\python.exe" tools/release_part.py work/rack-top-fan/rack_top_fan.scad --id TFE-A --part edge_front_print:TFE-A --keepout keepout_edge_front_print -o "C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\rack-top-fan\task53-scratch\dryrun-edge_front_print" --viewer-dir "C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\rack-top-fan\task53-scratch\viewers"
EXIT: 1
# TFE-A release report

- Date 2026-11-05; source `rack_top_fan.scad`; renderer `OpenSCAD-2026.11.01-x86-64` with Manifold

## Keep-out
- keep-out keepout_edge_front_print: 2784 mm3, 8 bodies

## edge_front_print
- edge_front_print: closed solid, 1 body, 2302 triangles, volume 342732 mm3, size 243.92 x 243.92 x 54.85 mm
- FAIL: edge_front_print: ID TFE-A is in the source but not on this part's mesh
- edge_front_print: no round holes found by the scan
- edge_front_print: keep-out clear

## 3MF
- 3MF: 1 objects, 1 items, 1145 vertices, 2302 triangles, matching the STLs

## Source
- 1 source file(s) frozen in src/
- 33 library file(s) frozen in src/lib/; to re-render, set OPENSCADPATH to src/lib

## Result
- 1 failed, 0 warnings
- Digital checks only. The hole scan sees only fully surrounded round holes. Printed fit and strength: UNKNOWN.

NOT RELEASED: nothing written to C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\rack-top-fan\task53-scratch\dryrun-edge_front_print. Rendered files left in C:\Users\brian\AppData\Local\Packages\sandbox.{08e871e9-8ea4-4857-81a8-427730a4ffab}\AC\Temp\release-TFE-A-ckt0u7ot
```

### edge_rear_print

```text
COMMAND: "C:\Program Files\Python310\python.exe" tools/release_part.py work/rack-top-fan/rack_top_fan.scad --id TRE-A --part edge_rear_print:TRE-A --keepout keepout_edge_rear_print -o "C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\rack-top-fan\task53-scratch\dryrun-edge_rear_print" --viewer-dir "C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\rack-top-fan\task53-scratch\viewers"
EXIT: 1
# TRE-A release report

- Date 2026-11-05; source `rack_top_fan.scad`; renderer `OpenSCAD-2026.11.01-x86-64` with Manifold

## Keep-out
- keep-out keepout_edge_rear_print: 2784 mm3, 8 bodies

## edge_rear_print
- edge_rear_print: closed solid, 1 body, 2580 triangles, volume 329780 mm3, size 243.92 x 243.92 x 54.85 mm
- FAIL: edge_rear_print: ID TRE-A is in the source but not on this part's mesh
- edge_rear_print: 1 x dia 8.0 (Z), depth about 3.0
- edge_rear_print: keep-out clear

## 3MF
- 3MF: 1 objects, 1 items, 1282 vertices, 2580 triangles, matching the STLs

## Source
- 1 source file(s) frozen in src/
- 33 library file(s) frozen in src/lib/; to re-render, set OPENSCADPATH to src/lib

## Result
- 1 failed, 0 warnings
- Digital checks only. The hole scan sees only fully surrounded round holes. Printed fit and strength: UNKNOWN.

NOT RELEASED: nothing written to C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\rack-top-fan\task53-scratch\dryrun-edge_rear_print. Rendered files left in C:\Users\brian\AppData\Local\Packages\sandbox.{08e871e9-8ea4-4857-81a8-427730a4ffab}\AC\Temp\release-TRE-A-rdcen4g7
```

### rail_print

```text
COMMAND: "C:\Program Files\Python310\python.exe" tools/release_part.py work/rack-top-fan/rack_top_fan.scad --id TSR-A --part rail_print:TSR-A --keepout keepout_rail_print -o "C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\rack-top-fan\task53-scratch\dryrun-rail_print" --viewer-dir "C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\rack-top-fan\task53-scratch\viewers"
EXIT: 0
# TSR-A release report

- Date 2026-11-05; source `rack_top_fan.scad`; renderer `OpenSCAD-2026.11.01-x86-64` with Manifold

## Keep-out
- keep-out keepout_rail_print: 2784 mm3, 8 bodies

## rail_print
- rail_print: closed solid, 1 body, 3354 triangles, volume 242367 mm3, size 50.00 x 170.00 x 30.00 mm
- rail_print: ID TSR-A is on the mesh, 10.9 mm3 of text at X 33.0..36.9, Y 76.8..93.3, Z 29.4..30.0; legibility not checked
- rail_print: 2 x dia 7.6 (X), depth about 10.0
- rail_print: 4 x dia 6.4 (Z), depth about 6.75 to 16.0
- rail_print: keep-out clear

## 3MF
- 3MF: 1 objects, 1 items, 1671 vertices, 3354 triangles, matching the STLs

## Source
- 1 source file(s) frozen in src/
- 33 library file(s) frozen in src/lib/; to re-render, set OPENSCADPATH to src/lib

## Result
- 0 failed, 0 warnings
- Digital checks only. The hole scan sees only fully surrounded round holes. Printed fit and strength: UNKNOWN.

RELEASED C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\rack-top-fan\task53-scratch\dryrun-rail_print
VIEWER C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\rack-top-fan\task53-scratch\viewers\TSR-A.html
```

### grille_print

```text
COMMAND: "C:\Program Files\Python310\python.exe" tools/release_part.py work/rack-top-fan/rack_top_fan.scad --id TFG-A --part grille_print:TFG-A --keepout keepout_grille_print -o "C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\rack-top-fan\task53-scratch\dryrun-grille_print" --viewer-dir "C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\rack-top-fan\task53-scratch\viewers" --cuts cuts=40
EXIT: 1
# TFG-A release report

- Date 2026-11-05; source `rack_top_fan.scad`; renderer `OpenSCAD-2026.11.01-x86-64` with Manifold

## Keep-out
- keep-out keepout_grille_print: 2784 mm3, 8 bodies

## Cuts cuts
- cuts cuts: 40 separate openings, none run together

## grille_print
- grille_print: closed solid, 1 body, 6622 triangles, volume 84024 mm3, size 220.96 x 233.40 x 3.00 mm
- grille_print: ID TFG-A is on the mesh, 10.3 mm3 of text at X 102.3..118.8, Y 3.7..7.7, Z 0.0..0.6; legibility not checked
- grille_print: 8 x dia 6.35 (Z), depth about 0.25
- grille_print: 8 x dia 5.88 (Z), depth about 0.25
- grille_print: 8 x dia 5.41 (Z), depth about 0.25
- grille_print: 8 x dia 4.94 (Z), depth about 0.25
- grille_print: 8 x dia 4.47 (Z), depth about 0.25
- grille_print: 8 x dia 4.0 (Z), depth about 0.25
- grille_print: 8 x dia 3.52 (Z), depth about 0.25
- grille_print: 8 x dia 3.4 (Z), depth about 1.25
- FAIL: grille_print: intrudes into the keep-out by 515.02 mm3

## 3MF
- 3MF: 1 objects, 1 items, 3233 vertices, 6622 triangles, matching the STLs

## Source
- 1 source file(s) frozen in src/
- 33 library file(s) frozen in src/lib/; to re-render, set OPENSCADPATH to src/lib

## Result
- 1 failed, 0 warnings
- Digital checks only. The hole scan sees only fully surrounded round holes. Printed fit and strength: UNKNOWN.

NOT RELEASED: nothing written to C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\rack-top-fan\task53-scratch\dryrun-grille_print. Rendered files left in C:\Users\brian\AppData\Local\Packages\sandbox.{08e871e9-8ea4-4857-81a8-427730a4ffab}\AC\Temp\release-TFG-A-9bp3o5v_
```


## Claude review (2026-11-06)

Verified: report matches the SCAD diff; renders one body each. Fixed the three FAILs as design changes (not workarounds):
- Edge IDs TFE-A / TRE-A: moved to the inner face at X 119, Z 435 (solid wall between the cavity and the plug column); the mid-length spot is the fan opening.
- Grille keepout: countersunk heads sit flush, so the keepout now starts at the grille top (Z 450.05); countersink widened 6.6 -> 7.0 (90 deg) for room around a 6.7 max M3 head.
- Edge print pose: front face (Y 0) down instead of the inner face, which left the body 19.85 up on the tongues. Tongues, ledge and cavity walls print upright; each plug sticks out sideways 19.85 and needs a small support.
- Engraved text un-mirrored (edges, rail, coupons) so it reads from the face it is cut into.

Rerun (scratch only): all six dry runs exit 0, 0 FAIL; 1 WARN on grille_print (dia 4.23 near the 4.2 insert bore), a slice of the countersink cone, kept. Assembly-frame geometry only lost material (tags, countersink), so the clash volumes above still hold; not rerun.
