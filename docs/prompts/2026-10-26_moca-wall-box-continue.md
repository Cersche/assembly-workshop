# Continue the MoCA wall box (2026-10-26)

Paste this into a new session:

```text
Continue the MoCA (ScreenBeam ECB7250) wall box in D:\Projects\assembly-workshop. git pull first, then read only:
- work/wall-box-wizard/Scope.md (bullets from "Splitter estimates" through "Concepts 12-14", plus "Still open")
- work/wall-box-wizard/concepts12-14/ (parts.scad, porch_body.scad, c12.scad, c13.scad, c14.scad)
Don't scan the rest of the repo.

Where we are: Brian likes the splitter-porch idea with the splitter lying flat (back face horizontal), and the
from-below views look great to him. Concept 12 "hanging porch" (splitter back-up, screwed to the box underside,
~33 mm porch, clip-on front cover, cables leave sideways, back OUT right-angle F up into the box, one jumper to the
ScreenBeam) is Claude's pick. 13 = drop-through (cables down through floor slots), 14 = open tray. Brian has not
picked one yet: ask which, then turn the chosen concept into real wall_box parameters/parts (porch as a printable
part with ear inserts), render it, and send the renders.

Rules: scratch renders with "C:/Program Files/OpenSCAD/openscad.exe" (STL in the scratchpad, not committed).
Splitter sizes are photo estimates (+-1 mm); OUT spacing and port axis height still need calipers. Fit, strength and
adapter sizes stay UNKNOWN; no printing without Brian's direction. Leave the untracked hard-drive-tray files alone
(equipment_tray.scad, test_drive_tray.py, outputs/Hard_Drive_Tray_2026-10-25/). Keep turns short; Brian is low on usage.
Commit and push to main when done; update HANDOFF.md at the end.
```
