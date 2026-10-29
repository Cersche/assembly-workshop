# Waveshare 5inch DSI LCD (C) — vendor dimensions

Source: Waveshare product drawing pasted by Brian, 2026-10-28. Vendor nominal values; NOT measured. Confirm on the real part.

| Item | mm |
|---|---|
| Glass outline (W x H) | 120.70 x 77.20 |
| Active area | 109.00 x 65.80 (offset inside glass not dimensioned) |
| Total thickness, glass to rear parts | 12.60 |
| PCB outline | 121.00 x 76.00 |
| Corner holes (stand), M2.5 x 4 mm | 4.00 from each edge -> 113.00 x 68.00 pattern |
| Pi mounting holes (Pi pattern) | 58.00 x 49.00; nearest hole 41.5 from PCB edge (4 + 37.5), rear view |

Rear view, read off the picture only (approx.): DSI FPC connector stands vertical about 8 mm in from the rear-view right edge, i.e. the **left edge seen from the front**, in the upper half. Buttons (backlight, brightness +/-) sit on the top edge, rear side. The touch I2C header and a small FPC are mid-board.

Plan (Brian, 2026-10-28): option A, 2U plate at U4-U3 (88.8 mm tall; 5.8 mm per side around the glass). Driven by the U5 HP4-M6-A Pi (board X 46..102) over the 160 mm cable. Fit and ribbon reach UNKNOWN.
