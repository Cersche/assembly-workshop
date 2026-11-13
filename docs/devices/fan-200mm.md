# 200 mm exhaust fan (rack top): Thermaltake CT200 ARGB (Brian, 2026-11-05)

Device card for the rack-top fan. Brian chose the Thermaltake CT200 (ARGB Sync, PWM) over the Noctua NF-A20 and Cooler Master MF200R. Values from retailer listings, not measurements; not yet confirmed in hand. Mark each value measured once the fan is in hand.

| Value | Source | Measured | Status |
| --- | --- | --- | --- |
| Frame | **195 x 195 x 30** (Thermaltake dimension drawing, sent by Brian 2026-11-06; listings said 200) | | from source, not measured |
| Corner radius / frame shape | round blade ring with square corner tabs at the holes (drawing); corner-to-corner 174 per drawing text | | from source |
| Hole pattern | 155 x 155, centred (20 in from each frame edge), standard fan holes (~4.3, Brian 2026-11-07); drawing image re-sent by Brian 2026-11-07. **The fan must be screwed down through these (Brian 2026-11-07); TF-A..C only clamped it under the grille, fixed in TF-D** | | from source |
| Power | 12 V 0.16 A (4-pin PWM) + 5 V 0.31 A (3-pin ARGB) (Milwaukee PC / Performance-PCs listings) | | from source, not measured |
| ARGB LED count | | | UNKNOWN (find by test; needed by the WS2812 library) |
| Cable exit (corner, length) | leads 900 mm PWM + 900 mm ARGB (retailer listing); exit corner UNKNOWN | | from source |
| Lead wire gauge / colours | | | UNKNOWN (wire by pin number, not colour) |
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

## Wiring for the brick box BRB-A (Brian, 2026-11-08; RESTART plan)
Diagram: `work/fan-junction-box/wiring_brick.svg` (artifact https://claude.ai/artifact/SZZQi8ZmPMWf1DFno96FE2). Supersedes the rear-post junction box wiring (`wiring_B.svg`, history). The "Junction box" bullet above is history too.
- **Power (in the box):** brick 5.5 x 2.1 plug (centre + assumed, check label) → screw-terminal socket tip → tip − into GND Wago port 1, tip + into 12 V Wago port 1 (two WAGO 221-413). Port 2 = CT200 4-pin pin 1 GND / pin 2 +12 V; port 3 = Pi 40 x 10 fan −/+.
- **CT200 4-pin** (standard PC fan pinout): 1 GND, 2 +12 V, 3 TACH, 4 PWM. Brian's extension is split: pins 1–2 to the Wagos, pins 3–4 to the Pi. Usual colours black/yellow/green/blue; CT200 colours UNKNOWN.
- **Direct to the Pi first (Brian, 2026-11-08):** no level shifter and no resistors to start; add them only if a problem shows. Items below marked *(if needed)* are not wired at first.
- **ARGB 3-pin** (5V-D-key-G): +5 V → Pi pin 2; DATA → GPIO10 / pin 19 (SPI MOSI) direct; GND → Pi pin 34. *(If needed: LEDs flicker or wrong colours → 330 Ω in DATA, then a 74AHCT125 3.3 → 5 V shifter heat-shrunk inline; no box.)*
- **PWM:** GPIO12 / pin 32 (PWM0, 25 kHz, needs the pwm overlay) → CT200 pin 4 direct. The fan pulls its PWM wire up to ~5 V inside (weak pull-up), a small risk to the 3.3 V pin; accepted by Brian. *(If needed: through a 74AHCT125 channel.)*
- **TACH:** CT200 pin 3 → GPIO6 / pin 31 (Brian 2026-11-08), Pi's built-in pull-up (~50 kΩ) turned on in software. *(If RPM readings jump: 10 kΩ from pin 31 to 3.3 V, pin 1.)* Before connecting, meter TACH→GND with the fan powered: must be ≤ 3.3 V.
- **74AHCT125 (only if needed):** VCC 14 ← 5 V (pin 4), GND 7 + 1OE 1 + 2OE 4 → GND, unused 3A 9 / 4A 12 → GND, 3OE 10 / 4OE 13 → 5 V, 0.1 µF VCC–GND. Rule of thumb: 3.3 V WS2812 data often works to ~0.5–1 m; the run here is ~0.5–1.5 m (UNKNOWN).
- **Ground tie (required, Brian chose it 2026-11-08):** PWM, TACH and DATA need brick GND and Pi GND joined. One jumper at the Pi end from the Pi fan's GND wire (= brick GND) to Pi pin 39. Both adapters are isolated, so this is safe. If the CT200 joins ARGB GND to fan GND inside (UNKNOWN), that is a harmless second tie. 12 V never touches the Pi header.
- **Current:** CT200 0.16 A + Pi fan ≤ 0.20 A (UNKNOWN, budgeted; Brian doesn't know its label or wire count yet, 2-wire assumed) = ≤ 0.36 A of the brick's 2 A (~18 %). ARGB 0.31 A is from the Pi 5 V (headroom UNKNOWN).
- **Wago 221-413:** 0.14–4 mm² fine-stranded, 0.2–4 mm² solid/stranded (24–12 AWG), strip 11 mm (WAGO datasheet). CT200 lead gauge UNKNOWN: 24 AWG or thicker goes straight in; 26 AWG or thinner: fold the strip back double or crimp a ferrule, then tug-test.

## Pi connection test, 2026-11-09 (Brian wired the CT200; Claude ran `work/fan-junction-box/pi_tests/fan_test.py` on the Pi 4, `pihole`)
Only the CT200 is wired (12 V via the brick box Wagos; TACH → GPIO6 pin 31, PWM → GPIO12 pin 32, brick GND → Pi pin 39). ARGB not tested.
- First runs read noise only (~14,600 RPM): the fan was unplugged. Ground tie added and fan plugged in before the good run.
- **TACH: connected.** Steady 1854 / 1860 RPM at full speed (counting 2 pulses per rev). The real RPM is UNKNOWN until checked against the CT200's rated speed: the pulses per rev may differ, or edges may be double-counted.
- **PWM: connected.** Holding PWM low dropped the tach count to 1050 (57 % of full). **The CT200 does not stop at 0 %.**
- PWM line reads 0 against the Pi's pull-down, so no strong pull-up inside the fan is visible on this wire (the ~5 V pull-up risk to the 3.3 V pin looks lower than assumed; not measured with a meter).
- The 50 % step (lgpio software PWM, 10 kHz) is invalid: it read 26,538, which is the PWM signal coupling into the tach. A real speed curve needs hardware PWM at 25 kHz (`dtoverlay=pwm` on GPIO12), which is not set up yet.
- **Hardware PWM, 2026-11-09:** `dtoverlay=pwm,pin=12,func=4` added to the Pi's /boot/firmware/config.txt (line 57; backup config.txt.bak-pwm), rebooted; `/sys/class/pwm/pwmchip0/pwm0` works at 25 kHz. Curve (`pi_tests/fan_curve.py`, run via `pi_tests/run_curve.cmd`; tach debounce 1 ms): 100 % 1908, 80 % 2424, 60 % 1980, 40 % 3324, 20 % 3144, 0 % 1050, 100 % 1890. Only the steady levels (0 % and 100 %) give believable readings; while PWM is switching, the tach count is inflated, most likely PWM switching picked up on the tach wire, which only has the Pi's weak ~50 kΩ pull-up. Planned fix from the wiring plan: 10 kΩ from pin 31 to 3.3 V (pin 1). Whether the fan really steps down at 20–80 % is UNKNOWN until the tach is clean (or by ear).
- **ARGB, 2026-11-09:** wired direct (5 V pin 2, DATA GPIO10 / pin 19, GND pin 34; no shifter, no resistor), driven over SPI0 at 6.4 MHz without extra libraries (`pi_tests/argb_test.py`; colour picker `pi_tests/argb_gui.py` on http://pihole:8750, started by `pi_tests/run_argb_gui.cmd`, which turns SPI on for the boot if it's off). First runs: colours showed, then the LEDs fell back to white. Cause: the Pi 4 core clock dropped to 200 MHz at idle (`core_freq_min=200`), which stretched the SPI bits so every bit read as 1 (full white). **Fix:** `core_freq_min=500` added to /boot/firmware/config.txt (backup config.txt.bak-corefreq), rebooted; **colours now hold (Brian)**. 3.3 V data works direct so far. LED count and colour order (GRB assumed) still UNKNOWN; SPI isn't enabled in config.txt (turned on per boot by the run script).
- **Tach pull-up + curve, 2026-11-09:** Brian added 10 kΩ from the tach wire to 3.3 V. Steady readings halved (100 % 936–954, 0 % 522–528): before it, each pulse was counted twice. A 4 ms debounce changed nothing. Curve with 99/95/90/1 % steps: 100 % 954, 99 % 1890, 95 % 1830, 90 % 1764, 80 % 1608, 60 % 1272, 40 % 1062, 20 % 1056, 1 % 1056, 0 % 528. Brian heard no difference between 99 % and 100 %, and 1 % reads exactly 2x 0 %: **while PWM switches, the count is doubled** (cause UNKNOWN; long edges, not short spikes). Corrected curve (2 pulses/rev assumed): **~950 RPM max, 95 % ~915, 90 % ~880, 80 % ~805, 60 % ~635, 40 % and below ~530 (floor; the fan doesn't stop)**. `fan_curve.py` now halves the count while PWM switches. True pulses/rev UNKNOWN (check ~950 against the CT200 rated speed).
- **After Brian rewired the fan, 2026-11-10:** curve read 100 % 942/948 and 0 % 522 (unchanged), but every switching step read ~470–595 (with the halving), so the in-between speeds no longer tracked the duty. Cause not found yet (ground tie, PWM wire or the doubling correction). ARGB was dark until Brian fixed a wire; colours back. Rerun `run_curve.cmd` with the fixed wiring.
