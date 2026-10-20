# 18 — Place on tray render sweep (investigation only)

**Goal:** the end-to-end wizard run (`work/equipment-wizard-options/E2E_Acceptance_Report.md`) rendered only three slot placements (pegs 90°, clips 180°, straps 270° with rear support; all passed the mesh check with no nudge). Check that the other Place on tray combinations also give closed meshes. Report only; change no code.

Render in a NEW temporary folder (never data/normal-use or any other user data) with `equipment.render(spec, temp_dir)`, then `mesh_revision.read_mesh()` each part. A placement spec is the library spec with the slot's tray keys on top (see `equipment.allocation_spec()` / `PLACEMENT_KEYS`). Base library spec: `{'name':'Sweep','dev_w':120,'dev_d':80,'dev_h':25,'holes':[[10,10],[110,70]],'ports':[{'x':-30,'z':21,'w':16,'h':14,'r':1}],'rear_ports':[{'x':0,'z':21}]}`. Cover:
- `device_mount` inserts, pegs, clips, straps;
- `dev_rot` 0, 90, 180, 270;
- `dev_off_x` 0, -25, +25 and `dev_off_y` 0, 20;
- `standoff` 3, 6, 12 (not for straps);
- `rear_support` true and false (true adds the `rear_bracket` part);
- `u` 1, 2, 4 with one keystone at ±100 where clean() allows it;
- `quality` draft and fine for at least four cases each;
- `joint='single'` (part "combined") with clips and with rear support.

A full cross product is not needed; pick about 30 renders that touch every value above at least once and every mount × rotation pair at least once. Record per case: pass/fail, `nudge_mm` for each part, any error text. If clean() rejects a case, record SKIP with its message and say whether the message is plain language a user would understand.

**May change:** nothing except the new `18-placement-render-sweep-REPORT.md` (plus your temp folder, deleted at the end). Do not edit `equipment_tray.scad`, `equipment.py`, the mesh check or tests. If something fails, describe the failing case and the bad edges (coordinates of edges not shared by exactly two triangles) in the report.
