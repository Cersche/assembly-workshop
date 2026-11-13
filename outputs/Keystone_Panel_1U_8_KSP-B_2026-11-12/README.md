# KSP-B: 1U keystone panel, 8 keystones, stiffened, labelled (2026-11-12)

KSP-A plus engraved labels (Brian, 2026-11-12). ID **KSP-B** is engraved on the rear face of the top frame bar, centre. Supersedes KSP-A, which was never printed.

## Labels (keystone 1 = far left, seen from the front)
blank · Hue · MoCA · Pi LAN · Win PC · OptiPlex · blank · Pi USB

Simple original icons (bulb, coax end, raspberry, four panes, monitor) plus 3 mm bold text, engraved 0.6 mm into the front face. "Pi Ethernet" and "PC/Windows" were shortened to "Pi LAN" and "Win PC" to fit over one jack. **Two colours:** `KSP-B_two-colour_labels.3mf` is one object with two parts, panel and label inlay, face down and in place (made by `work/keystone-panel/make_color_3mf.py` from the released STLs; no overlap, the inlay fills the 0.6 mm engraving exactly). In the slicer, give the "labels (second colour)" part its own filament. `KSP-B_1-parts-print-layout.3mf` stays the one-colour version.

## Changed from KSP-A
- Keystones moved down 3 mm: the label strip above them is 6.7 mm (was 3.7), and the strip below is 4.2 mm (was 7.2).
- ID moved to the top frame bar.

## Kept
Plate 252 x 44.4 x 4, four-corner slots, golden keystones `ks_tight=0.2` (shapes unchanged, only moved), 8 at 27.5 pitch, 12 mm rear frame X ±110.1 with a pocket around each block. No screws or inserts.

## Checks
`release_report.md`: 0 fails, 0 warnings; real 4U posts at U7 on both sides, no overlap; 8 pockets separate.

## UNKNOWN
Label legibility at 3 mm, fit of the frame against the posts, jack tilt-in past the frame, stiffness and strength. Print face down (front on the bed).
