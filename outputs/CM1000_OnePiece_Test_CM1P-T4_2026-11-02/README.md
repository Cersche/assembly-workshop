# CM1000 one-piece bracket, test slice 4 — test-print ID CM1P-T4 (2026-11-02)

PROPOSED — UNPRINTED. CM1P-T3 with only the channel changed, to test the V and clearance planned for CM1P-G before another full part. Printed fit UNKNOWN. No rack slots and no side slot: it does not test rack fit, the side screw or strength. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA): personal use, never redistribute.

Print `CM1P-T4_test_slice.3mf`: one object, front face on the bed, no supports, same as T3. 220.46 x 44.45 x 30 mm, about 94.5 cm3 of solid volume. ID engraved on the top face.

## What changed from CM1P-T3

- V floor 8 to 4 wide, slopes re-aimed so they run parallel to the modem's. Brian measured the modem's end strip at 3; 4 keeps the printed corners from binding.
- Clearance 0.75 to 0.25 per side at the floor. Floors 213.19 to 212.19 apart, read from the mesh at Y 25.
- Largest gap between slope and modem about 0.6, on the assumed straight slope. CM1P-E had up to 2.2.
- Nothing else.

## Why a slice can't answer everything

CM1P-E's channel measured 214 at the rail tips against 212.69 designed, and its outside 221.5 against 220.46: the rails lean out on the full-length part. A 30 mm slice has no long rails, so T4 cannot show lean or the tip correction. That needs CM1P-G.

## Risk

Brian's calipers read the modem at 212. The 211.69 used here comes from T2 and T3 play, which fits prints coming out about 0.3 wide; that is a reading of the evidence, not a measurement. If it's wrong, the real clearance is about 0.1 per side and T4 may be hard to get on.

## Report

Does it go on by hand, total side play (design 0.5), and how firm it feels up and down compared with T3.

## Checks run (digital only)

FreeCAD: one valid solid. `python pack_check.py` from `src/`: 0 bad edges, 488/972 vertex/triangle tags, 0 of 6804 sampled points inside the modem envelope (211.69 wide, 3 strip, straight slopes, coarse sample). Section at Y 25 read back as designed. No slicer check.

## Rebuild (PC)

Needs `outputs/CM1000_M6_2026-10-28/src/orig/`. From `src/`: OpenSCAD.exe `-o id.stl id.scad`; `"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_t4_freecad.py').read())"`; `python pack_check.py`.
