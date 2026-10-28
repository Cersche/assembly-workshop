# SG8-C1 — screw-joint coupon for SG8-M6-B (2026-10-28)

Brian asked (2026-10-28) for a test of just the left hidden-screw joint of SG8-M6-B, which is cramped: the boss sits ~0.4 mm above the switch and the head recess leaves ~0.3 mm of upright at its bottom/top. Accepted as is for now.

- `SG8-C1_screw_joint_coupon.3mf`: tray slice + faceplate slice, print orientation. STLs alongside.
- Slice: X −104..−80, Y ≤ 24 of the SG8-M6-B parts (sleeve wall, floor, top lip, upright; plate + boss). Exact same geometry there.
- ID **SG8-C1** engraved 0.4 mm: outside of the sleeve wall (tray) and plate front above the window (faceplate).
- Hardware: 1 rack M6 heat-set insert + 1 M6 x 8 button head.
- Check: insert goes in without splitting the boss, head seats in the recess, screw pulls the plate tight, the thin recess edges survive.
- Source: `SG8-C1_faceplate_src.scad` (SG8-M6-B source, clipped); `SG8-C1.scad` (tray: SG8-M6-B tray rendered with `coupon=[-104,-80,24]`, then engraved). Not printed; fit/strength UNKNOWN.
