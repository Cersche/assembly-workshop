Continue the MoCA (ScreenBeam ECB7250) wall box in Z:\Projects\assembly-workshop (same repo as D:\Projects\assembly-workshop,
reached over the network share). git pull first, then read only:
- HANDOFF.md, top section "2026-10-27 MoCA wall box: box finished as a concept, print file ready"
- work/wall-box-wizard/Scope.md, the "Concept 15" bullet and sub-bullets, plus "Still open"
- outputs/MoCA_Box_2026-10-27/README.md
- work/wall-box-wizard/concept15/body15.scad and porch15.scad only if a change is asked for
Don't scan the rest of the repo.

Where we are: box and porch are complete as a concept and exported as one print-oriented 3MF (8 parts). Brian decides
whether to print. Likely next asks: changes after a test print, splitter caliper numbers, or moving the concept 15 box
features (floor slots, keystone, power hole, cradle bosses, M3 hinge sets, magnets, louvres, back plate + sleeve split,
labels) into the wall_box template as parameters.

How to render: OpenSCAD at "C:/Program Files/OpenSCAD/openscad.exe" from PowerShell (Git Bash cannot start it). body15.scad
parts: -D part="sleeve"|"back"|"lid"|"body" (PowerShell mangles quoted -D strings: call through cmd /c with \"...\", or use a
small wrapper .scad with `use <body15.scad>`). porch15.scad: -D pick=0 assembly (needs concept15/body15.stl built from
body15.scad first; delete it after), 1 porch, 2 bezel nut, 3 nut slider, 4 cradle. Scratch output in %TEMP%\boot15render.
PowerShell: [IO.File] calls resolve relative paths against C:, so use full Z: paths; variable names are case-insensitive.

Rules: splitter sizes are photo estimates (+-1 mm); ScreenBeam port positions, adapter/barrel lengths, fit, strength,
thread, insert and screw sizes, magnet hold stay UNKNOWN; no printing without Brian's direction. Commit renders as PNG
only, never STL/3MF. Leave the hard-drive-tray files (equipment_tray.scad, test_drive_tray.py,
outputs/Hard_Drive_Tray_2026-10-25/) and other untracked files alone. Keep turns short; Brian is low on usage. Commit and
push to main when done; update HANDOFF.md at the end.