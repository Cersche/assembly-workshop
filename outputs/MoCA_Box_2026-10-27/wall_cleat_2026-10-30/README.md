# MoCA box wall plate + French-cleat back plate (2026-10-30)

Brian's idea: put a plate on the wall first, then hang the box on it. He picked a French cleat, with wall plate holes
for anchors and a stud. Source: `work/wall-box-wizard/concept15/cleat16.scad` (`pick=1` back plate, `2` wall plate,
`0` both seated). This back plate replaces the keyhole back plate. Sleeve, lid, cradle and porch are unchanged, and
the old keyhole back plate still fits.

`MoCA_wall_cleat_set.3mf`: both parts side by side in print orientation. Each part also comes as its own STL.

| Part | ID (engraved) | Size on bed (mm) | Orientation |
|---|---|---|---|
| back plate, cleat pocket | MOCA-BC-A (inside face) | 105 x 210 x 10.5 | outer (wall) face down |
| wall plate | MOCA-WP-A + TOP (front face) | 105 x 210 x 11 | wall face down, cleat up |

How it hangs:
1. Screw the wall plate to the wall with TOP up. It is the box's exact outline, so it also works as the template.
   The V notches on the edges mark the hole heights and the centre line, for a level.
2. Lift the box about 9 mm and push it flat to the plate, so the cleat goes into the pocket in the box back. Then
   let it drop. The 45 deg roof pulls the box onto the plate. Left-right play is +-0.6 mm. The box sits 3 mm off
   the wall.
3. Optional lock: one M3 x 8-10 screw from inside the box, through the slot above the ScreenBeam (X38, Z186). It
   goes in through the lid opening, into an M3 heat-set insert in the cleat face. It stops the box being lifted off.

Wall screws: 6 countersunk holes, 4.5 mm with a 9 mm countersink, for #8 / 4 mm wood screws. Use the 4 outer holes
with drywall anchors, or the 2 on the centre line (178 mm apart) for one stud, or both. The heads sit flush.
Brian picks the screws and anchors; their sizes are UNKNOWN.

Hardware: 6 wall screws (+ anchors), 1 M3 heat-set insert, 1 M3 x 8-10 (lock). The box joint keeps its 6
countersunk M3 screws.

Checked digitally: the seated parts don't overlap. The box can lift 8.5 mm and pull straight out without catching.
The cleat band clears the cradle top at +6 mm travel and the top joint blocks. Designed support-free, but the
pocket roof in the back plate is a ~31 mm bridge.

PROPOSED - UNVALIDATED. Not printed. Fit, cleat hold, lock screw, anchor/stud load and strength are UNKNOWN. No
slicer settings are given or implied.
