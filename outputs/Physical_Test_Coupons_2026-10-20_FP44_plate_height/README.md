# FP44 plate-height coupons — 2026-10-20

**Question:** does a 44.4 mm-tall faceplate fit in the Lab Rax rack, both on its own and stacked in the next U? Today's plate is 42 mm tall.
**Status:** PROPOSED, UNVALIDATED. Fit is **UNKNOWN** until Brian prints these and reports back. The app's default plate is still 42 mm and has not been changed.

Each coupon is the right-hand ear of the faceplate, cut 40 mm wide. It has the full plate height, both rack slots (10 × 7 mm capsules at the real positions), the real 2.5 mm corner radius and our 4 mm thickness. The ID and the height are engraved 0.6 mm deep on the front face, between the cut edge and the slots, away from every edge being tested.

The plate stays centred on its slots, so a taller plate grows by the same amount at the top and the bottom. The slots stay exactly where they are on the rack (plate centre ± 15.902 mm).

| ID | Height | Grows top/bottom vs 42 | Gap to the next plate (44.45 pitch) | What it tests | File |
|---|---|---|---|---|---|
| **FP44-A** | **44.4** (target) | +1.20 / +1.20 | 0.05 mm | the target height; same as the OptiPlex bracket panel that Brian says fits | `FP44-A_h44.4.stl` |
| FP44-B | 44.2 | +1.10 / +1.10 | 0.25 mm | fallback if A rubs | `FP44-B_h44.2.stl` |
| FP44-C | 44.0 | +1.00 / +1.00 | 0.45 mm | second fallback | `FP44-C_h44.0.stl` |
| FP44-D | 42.0 (today's plate) | 0 / 0 | 2.45 mm | **control**: our current gold standard, same coupon shape. If D sits differently from a real 42 mm plate, the coupon method is off, not the height. | `FP44-D_h42.0.stl` |

Why D was added: it is the only way to tell "44.4 is too tall" apart from "the coupon itself (print size, cut edge, slot position) is off". It costs one small print.

Source: `FP44_plate_height_coupon.scad` (one file; ID, height and label are set with `-D`, see the comment at its top). Exported with OpenSCAD.exe 2026-10-20.

## Printing

- The STLs are already laid flat, front face up (the engraved side is on top). Bounding box: 40 × height × 4 mm.
- Print **two of each** you want to stack-test. Two copies with the same ID are identical. Scratch a 1 or 2 on the back if you want to tell them apart.
- Start with a pair of FP44-A plus one FP44-D. Print B and C only if A rubs.
- Elephant's foot or over-extrusion makes a print a little taller. A 44.4 pair has only 0.05 mm of nominal gap, so a slightly oversized print may touch its neighbour even when the design is fine. If A pairs touch, measure the printed height with calipers and write it down.

## How to check

1. **Single coupon.** Bolt one coupon to a front post in a middle U with both slots, like a real faceplate. Does it sit flat on the post? Do both screws go through without forcing the slots? Does the top or bottom edge rub on anything?
2. **Stacked pair.** Bolt two of the same ID in two adjacent U on the same post. Look at the joint between them. Is there a gap, do they touch, do they rub, or does one push the other out of flat? Do the slots of both still line up with the post holes?
3. **Mixed pair (optional).** Put a 44.4 coupon next to a real 42 mm faceplate already in the rack, to check the change-over between old and new plates.
4. **End slots (optional).** Try one coupon in the lowest U and one in the highest U. The plate now reaches 1.2 mm lower and higher than before, so check it doesn't touch the bottom beam or the top beam.
5. **Left post.** The same coupon fits the left post: turn it upside down (rotate it in its own plane, front face still towards you). The slots are symmetric, so it lines up the same way. The text will read upside down.

Please report for each ID: fits alone yes/no, stacked pair gap/touch/rub, slot alignment, and any measured printed height.

## Limits

- This checks height clearance and slot alignment only. Strength, retention and the full 252 mm-wide plate stay **UNKNOWN**.
- The result applies only to these printed specimens on Brian's rack and printer. It does not certify other printers or materials.
- Changing the gold-standard plate to 44.4 needs Brian's go-ahead after he reports back.
