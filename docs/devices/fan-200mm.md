# 200 mm exhaust fan (rack top): Thermaltake CT200 ARGB (Brian, 2026-11-05)

Device card for the rack-top fan. Brian chose the Thermaltake CT200 (ARGB Sync, PWM) over the Noctua NF-A20 and Cooler Master MF200R. Values from retailer listings, not measurements; not yet confirmed in hand. Mark each value measured once the fan is in hand.

| Value | Source | Measured | Status |
| --- | --- | --- | --- |
| Frame | **195 x 195 x 30** (Thermaltake dimension drawing, sent by Brian 2026-11-06; listings said 200) | | from source, not measured |
| Corner radius / frame shape | round blade ring with square corner tabs at the holes (drawing); corner-to-corner 174 per drawing text | | from source |
| Hole pattern | 155 x 155 (drawing); not used, the grille clamps the fan | | from source |
| Power | 12 V 0.16 A (4-pin PWM) + 5 V 0.31 A (3-pin ARGB) (Milwaukee PC / Performance-PCs listings) | | from source, not measured |
| ARGB LED count | | | UNKNOWN (find by test; needed by the WS2812 library) |
| Cable exit (corner, length) | | | UNKNOWN |
| Weight | | | UNKNOWN |

Power plan (Brian, 2026-11-07; replaces the 2026-11-05 buck-board plan):
- **Supply:** GuanTing universal AC adapter, 12 V 2 A, 5.5 x 2.1 plug, comes with a screw-terminal tip (Amazon). Plugs into the power strip; DC panel jack (5.5 x 2.1) in the new rear top edge.
- **12 V loads:** the CT200 (0.16 A) and the Pi's 40 x 10 fan (listed 12 V, ~0.1 A assumed until its label is read). This fixes the Pi fan's voltage mismatch (only 5 V at the Pi/screen FAN pads). Total ~0.3 A of 2 A. Both fans run at full speed (no PWM signal; assumed, check). Optional later: Pi-switched MOSFET for the Pi fan (then tie the brick ground to Pi ground).
- **ARGB:** driven by the Pi, no separate controller or buck board: fan 5 V to Pi pin 2/4, GND to pin 6, data to GPIO10 (pin 19, SPI; changed from GPIO18 on 2026-11-07 so fan PWM can use the hardware PWM pins), WS2812 library (rpi_ws281x / Adafruit NeoPixel). Pi data is 3.3 V: a 74AHCT125 level shifter is recommended for the long run to the top. Pi 5 V headroom for +0.31 A UNKNOWN (depends on that Pi's supply and loads).
- Wiring from the top to the Pi: 12 V pair for the Pi fan + 3-wire ARGB, bundled along the rack. Cable lengths UNKNOWN.
- **PWM + tach wired now (Brian 2026-11-07):** CT200 PWM via a spare 74AHCT125 channel from GPIO12 or GPIO13 (pin 32/33), tach to a GPIO with a 3.3 V pull-up. Whether the CT200 stops at 0 % is UNKNOWN.
- **Junction box:** two Wago 221-413 (12 V and GND) in a small case on a cleat at the right rear post, U9; brick input via its screw-terminal socket tip; 6 conductors down to the Pi. Spec: `work/fan-junction-box/Spec.md`.
- No dual-rail/SATA brick (Brian's HDD supply is separate and not part of this).

Earlier candidates: Noctua NF-A20 PWM 200 x 200 x 30, holes 154 x 154 / 170 x 170 / 110 x 180 (noctua.at); Cooler Master MF200R ARGB 200 x 200 x 25, 259 g.
