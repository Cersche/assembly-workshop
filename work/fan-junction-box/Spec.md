# Fan junction box (Wago case + post cleat): agreed spec (Brian + Claude, 2026-11-07)

Discussion result only. No part geometry has been drafted, and nothing is printed or released. Fit, strength, cleat play, insert fit and wire retention are all UNKNOWN. Drafts stay viewer-only until Brian says he is printing (then device card + `/new-part` checklist + `tools/release_part.py`).

## What it does
It splits the 12 V brick power for the rack fans in the top corner of the rack. Power plan: `docs/devices/fan-200mm.md` (2026-11-07).

## Contents (agreed)
- **Only power is spliced.** Two **Wago 221-413** (Brian has 412/413/415 on hand):
  - **12 V bus:** brick + (from the screw-terminal socket tip), CT200 12 V, 12 V down to the Pi's 40 x 10 fan.
  - **GND bus:** brick -, CT200 GND, GND down to the Pi. Brick ground is tied to Pi ground once, at the Pi end.
- **Passing straight through, unspliced:** CT200 ARGB (5 V, DATA, GND), PWM and TACH. Brian chose to wire PWM and tach now ("build it all now"), even though both fans run full speed at first.
- **Fan stays unmodified:** it plugs into a 4-pin PWM extension and a 3-pin ARGB extension. Only the 4-pin lead's 12 V and GND go into the Wagos; its PWM/TACH wires and the ARGB lead carry on to the Pi.
- **Down the rack to the Pi (slots 5-6):** 6 conductors: 12 V, GND, 5 V, DATA, PWM, TACH (length UNKNOWN).
- **At the Pi, not in the box:** 74AHCT125 level shifter (DATA to **GPIO10 / pin 19, SPI**; fan PWM through a spare channel from GPIO12 or GPIO13, pins 32/33); TACH to a GPIO with a 3.3 V pull-up; ARGB 5 V from pin 2/4, GND pin 6; optional MOSFET for the Pi fan if it is 2-wire. ARGB moved off GPIO18 because the WS2812 library's PWM mode and fan hardware PWM would share the same peripheral.
- **12 V input:** the GuanTing brick's included **screw-terminal DC socket tip** (5.5 x 2.1 female barrel + green +/- screw block, Brian's photo 2026-11-07). The TF-C rear-edge DC jack pocket stays as released and is not used. **Update 2026-11-07 (Brian):** the socket tip sits at the power strip, not in the rack; a new 2-wire lead runs from it up to the box.
- Diagram: `wiring_concept.svg` (it still shows the earlier 4 x 221-412 pass-through version; the passthroughs were dropped for compactness).

## Wago 221-413 (datasheet values; Brian: "this company has been accurate", use them)
Width 18.7 (across the levers), depth 18.6 (wire entry to back), height 8.3 lever closed. Wire range 0.14-4 mm² flexible / 0.2-4 solid (24-12 AWG UL); 26 AWG fan leads are at the bottom of the range (ferrule or fold back). Lever-open height and wire-hole height not in the datasheet text: leave the lid off to rewire, so they don't size the case. Measuring diagram (if ever needed): `wago_measure.svg`. Sources: WAGO 221 datasheet via ews.uk.com / leds.shop; element14 listings.

## Placement (agreed)
Right rear corner of **slot 1 (U9)**, behind the CM1000 (modem envelope ends ~Y 140), just under the TF-C top. Concept: `placement_concept.scad` (rack frame of `rack_top_fan.scad`), viewer https://claude.ai/artifact/23GjqncMvU6fzYKy9YzwNt (v2; simplified posts, CM1000 envelope, our TF-C parts).
- Case roughly **46 x 36 x 18** (concept X 78..124, Y 165..201, Z 365..383), two 413s side by side, entries facing -Y with ~12 mm of wire room in front.
- **Brick socket stays down at the power strip** with the brick (Brian, 2026-11-07, cleaner look; supersedes the outside cradle): a new 12 V pair runs up the rack and enters the case through the floor slot, beside the outgoing 6-conductor bundle. No cradle on the case.
- CT200 leads enter from the top (short run through the 15 mm gap under the fan ledge); the 6-conductor bundle leaves at the bottom and runs straight down the rear post lane (X ~111..127, in front of the rear flange) to the Pi.

## Mounting: cleat (agreed)
- **Receiver** (separate part, stays on the rack): plate on the **front face of the right rear post's flange** (Y 234), **one M6 x 8 button head into an M6 heat-set insert in the post's U9 middle hole** (X 118.26, Z 377.8; hole is a 7.6 insert bore; whether that hole already has an insert is UNKNOWN, post card ref G). Vertical **dovetail channel, open at the bottom, closed at the top** (the top is the stop, so the case can't ride up into the fan top).
- **Case** has the matching dovetail cleat on its back. **Slides UP** into the receiver from below; removal = slide down, needs ~one case length free below (behind the ER605 in slot 2: check in the draft).
- **Lock (Brian picked Claude's recommendation):** a small lip at the bottom of the case meets the receiver's bottom edge; **one M3 countersunk screw up through the lip into an M3 x 3 x 5 heat-set insert** in the receiver (4.2 bore x 4 deep, boss >= 9 OD). No snap latch.
- **Lid:** M3 countersunk screws into M3 inserts in the case corners. No self-tapping anywhere.

## Still to settle in the draft session
- Cable entries and strain relief: zip-tie anchor or comb at the bottom exit for the bundle, and at the top entry for the fan leads (Brian dropped tie anchors on CSB-C, so ask before adding them).
- Clearances to check in the model: CM1000 rear cables (positions scaled, not measured), the slide-down room behind the ER605, the TF-C rear edge underside, the rear post fillet (X 124.5..127.1).
- CT200 cable exit corner and length, Pi fan wire count/label, cable lengths, Pi 5 V headroom (all UNKNOWN).
- Part IDs at release: proposal **JBC-A** (case) and **JBR-A** (receiver), modelled on the parts. Dovetail fit needs a small test coupon with its own ID first (Brian's call).
- Hardware: M6 x 8 button head + M6 insert (receiver), M3 countersunk + M3 inserts (lock + lid). All on hand.

Draft geometry is small and design-heavy: Claude drafts it with `/new-part` (pinned OpenSCAD snapshot, `lib/workshop.scad`); no Codex task needed unless the release packaging grows.

## Option B with fan lead extensions (Brian, 2026-11-07; B picked over A)
Brian: the CT200's own leads won't reach the Pi, so they are extended **in the box**. Supersedes "passing straight through" above for option B. The Pi fan still runs from the same 12 V feed.
- **4-pin:** CT200 4-pin plugs into a female 4-pin PWM extension inside the box. The extension is cut: its 12 V and GND go into the two 221-413s; its PWM and TACH continue down to the Pi in the bundle.
- **3-pin ARGB:** CT200 3-pin plugs into a 3-pin ARGB extension that runs uncut to the Pi.
- **Retention:** both mated pairs lie stacked (4-pin below, ARGB on top) in one pocket in a front bay, with end stops at both ends (corner tabs, 7.5 mm wire gap) so they can't vibrate apart; the lid holds them down. No signal splices, no extra Wagos.
- **Wago ports (3 each):** 12 V: brick, CT200 (via the cut extension), Pi fan. GND: same. The Pi fan's 12 V pair goes down the rear post in the same bundle.
- **Path:** fan leads lay in through a lid notch at the -X edge into the drop room at the pocket's -X end; the pairs run +X; the extension wires turn back into the post-side lane to the Wagos and the corner exit (no U-turn). Lid tie bridge moved beside the new notch.
- **Draft sizes (TYPICAL, UNKNOWN):** mated pair 26 x 11.5 x 7.5 each; pocket 28.5 x 12.5. Extension lengths UNKNOWN (expect ~30 cm route). Where to measure: `pair_measure.svg`.
- Geometry: `fan_junction_box_B.scad` (draft 2). Option A (`fan_junction_box.scad`) is unchanged.

## RESTART: box at the power brick (Brian, 2026-11-08) — supersedes everything above
Everything above (top-corner case, post cleat, options A and B, JBC-A/JBR-A drafts) is history; files kept, not deleted.
- **Location:** a small box clamped onto the GuanTing brick's body (preferred) or onto the power strip itself. No rack-post mount.
- **Inside:** two Wago 221-413 (12 V, GND) and the brick's screw-terminal socket tip; the brick's barrel plug enters through a hole in the box wall. Socket tip leads go into Wago port 1.
- **Outputs:** Wago ports 2 and 3 = 12 V/GND pairs to the CT200 and to the Pi's 40 mm fan.
- **Not in the box:** everything to the Pi (CT200 ARGB, PWM, tach) runs on Brian's own extensions; he has the 4-pin power/signal split at the fan handled.
- **Excess brick cord:** bundled ~25 x 85, held by a zip-tie anchor on the outside of the box.
- **Needed before drafting:** brick W/H/D, cord exit, prong position; socket tip length, barrel OD, block size; plug body OD/length. Where to measure: `brick_measure.svg`. All UNKNOWN until measured.
- Fit, strength, clamp grip and heat UNKNOWN. Viewer-only drafts until Brian says he is printing; new part ID at release.
