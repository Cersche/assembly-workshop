# 16 — Keystone faceplate render sweep (investigation only)

**Goal:** confirm the keystone non-manifold fix (`ks_golden()` in `outputs/Mechanical_Design_App/equipment_tray.scad`, see `work/equipment-wizard-options/Wizard_Fixes_Report.md`) holds beyond the cases Claude rendered. Report only; change no code.

Render in a NEW temporary folder (never data/normal-use or any other user data) with `equipment.render(spec, temp_dir)`, then `mesh_revision.read_mesh()` each part. Base spec: `{'name':'Sweep','dev_w':100,'dev_d':80,'dev_h':20,'device_mount':'inserts','joint':'screw','holes':[[10,10]]}` (raise `dev_h` only if clean() asks for more U). Cover:
- keystone X at -105, -100, -90, -80, -75, 75, 80, 90, 100, 105 mm (skip any clean() rejects, and say which/why);
- two keystones at once (-100, 100) and (-90, 95);
- u = 1, 2, 3, 5;
- `quality` draft, standard, fine;
- `joint='single'` (part "combined") for at least u=1 and u=2 with a keystone.

A full cross product is not needed; pick a set that touches every value above at least once (about 25 renders). Record per case: pass/fail, `nudge_mm` for each part, any error text. Also run `AW_RENDER_TESTS=1` with `python -B -m unittest test_keystone_mesh -v` from the app folder.

**May change:** nothing except the new `16-keystone-render-sweep-REPORT.md` (plus your temp folder, deleted at the end). Do not edit `equipment_tray.scad`, the mesh check or tests; if something fails, describe the failing case and the bad edges (coordinates of edges not shared by exactly two triangles) in the report.
