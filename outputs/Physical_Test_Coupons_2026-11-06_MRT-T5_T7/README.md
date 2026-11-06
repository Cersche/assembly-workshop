# MRT-T5..T7 coax forming jigs (2026-11-06)

PROPOSED. Fit and strength are UNKNOWN. Source: `work/moca-rack-tray/MRT.scad`, `part="jig_jumper" | "jig_in" | "jig_out"` (copy in `src/`). Print file: `outputs/Final_3MF/MRT-H_moca_tray_ramps_and_T5-T7_jigs.3mf`, together with the MRT-H set. The `MRT-T5_3-parts-print-layout.3mf` here holds only the three jigs.

## The jigs
One jig per cable, so each coax takes its final shape while the tray prints:
- MRT-T5: the jumper.
- MRT-T6: the IN coax.
- MRT-T7: the OUT2 coax.

Each jig is MRT-H's own channel walls, lips and rib for that run, on a 2 mm floor that is 2 lower than the tray's, as on MRT-T4. At each device port is a smooth 8.2 post in its true place, for the F nut to slide over; post fit is UNKNOWN. Tie slots sit where the tray has them; the jumper has no lips, so tie it.

T6 and T7 end in the tray's ramp dock: screw the real MRT-H ramp on (Up or Down) with 2 M3 into M3 x 3 x 5 inserts. For a Down ramp, set the jig with that end over the bench edge, because the ramp reaches about 24 below the jig floor. A ramp can move to the tray afterwards with the cable still tied in.

Hardware: 4 M3 x 3 x 5 inserts (T6, T7) and 4 M3 countersunk screws.

Floors are rounded (r 3) and wide enough to carry the walls' base fillets; the post pillars have r 2 corners. The three port posts stick out sideways, so their undersides are short overhangs: add support from the build plate under them if your slicer flags them.

## Checks
0 failed, 0 warnings; each jig is one closed body. The jigs were not checked against the device mock-ups: the post pillars stand in for the ScreenBeam and splitter.

## Fit report to send back
- The ID on each jig.
- Whether the F nuts slide onto the posts and stay.
- Whether each cable sits in its run without fighting, especially OUT2 into its ramp.
- Jumper length you cut.
- Walls and infill.
