Continue the MoCA (ScreenBeam ECB7250) wall box in Z:\Projects\assembly-workshop (same repo as
D:\Projects\assembly-workshop, reached over the network share). git pull first, then read only:
- HANDOFF.md, top section "2026-10-27 MoCA wall box: concept 15"
- work/wall-box-wizard/Scope.md, the "Concept 15" bullet and its sub-bullets, plus "Still open"
- work/wall-box-wizard/concept15/ (porch15.scad, c15.scad, body15.scad)
Don't scan the rest of the repo.

Where we are: the porch side is settled for now (Brian, 2026-10-27). Concept 15: splitter lying flat under the box in a
rounded printable porch; splitter IN clamped to the porch's left wall by a threaded bezel nut; modem coax out the
porch's right window; back OUT -> right-angle F up through a floor slot -> F male-male barrel -> Brian's braided
~220 mm jumper up the ScreenBeam's right side to Coax In on top. Two M3 x 40 screws from below hold porch + splitter
into captive nut sliders inside the box. Ethernet keystone low on the box's right wall; power lead out low on the left
wall beside the incoming coax. ScreenBeam in a printed cradle with ±6 mm vertical slots on four back-wall insert bosses,
strapped with Velcro. Porch and cradle were made support-free.

Next: work on the MoCA box itself (body15.scad, now a hand-edited concept copy of the wall_box template output).
Start by showing Brian the box as it stands and asking what he wants changed (look/style, size, lid, vents, wall
mounting, anything else). Candidates already noted: box height may shrink now the layout is fixed (box ~105 x 75 x 210);
the style pick from 2026-10-22 (soft slab, louvre, picture frame, pill, two-tier) is still open; the box changes made
in concept 15 (floor slots, right-wall keystone, left-wall power hole, cradle bosses) should eventually go into the
wall_box template as parameters instead of a hand-edited copy.

How to render: OpenSCAD at "C:/Program Files/OpenSCAD/openscad.exe", run from PowerShell (Git Bash cannot start it).
Build concept15/body15.stl from body15.scad first, then render porch15.scad (pick=0 assembly, 1 porch, 2 bezel nut,
3 nut slider, 4 cradle; pass -D pick=N, PowerShell mangles quoted string -D values). Put STLs/PNGs in a scratch folder;
delete body15.stl after rendering; commit renders as PNG only, never STL. OpenSCAD -o can fail on very long output
paths; use a short folder such as %TEMP%\boot15render.

Rules: splitter sizes are photo estimates (+-1 mm; OUT spacing and port axis height still need calipers); ScreenBeam
port positions on its ends, adapter/barrel lengths, fit, strength, thread and insert sizes stay UNKNOWN; no printing
without Brian's direction. Leave the untracked hard-drive-tray files alone (equipment_tray.scad, test_drive_tray.py,
outputs/Hard_Drive_Tray_2026-10-25/) and other untracked files. Keep turns short; Brian is low on usage. Commit and push
to main when done; update HANDOFF.md at the end.
