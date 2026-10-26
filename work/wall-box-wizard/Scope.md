# Wall-mount box wizard — scope (Brian, 2026-10-22)

Idea from `work/notes/2026-10-22-feet-floor-and-wall-box-wizard.md`: an indoor, smaller take on the fiber NID boxes on the side of a house; custom enclosures for wall-mounting equipment, and a way to build custom equipment from common parts.

## Decisions (Brian, 2026-10-22)

- **Separate wizard**, its own designer outside the rack flow (not a variant of the equipment wizard). It may still reuse code (STL/STEP import, port detection, keystone geometry).
- **Lid: all three options**, user picks per box: screw-on (M3 into heat-set inserts), hinged + latch, snap-fit.
- **Wall mounting: all three**, user picks: keyhole slots, screw tabs, French cleat (separate rail STL).
- **Common parts library:** MoCA adapter, keystone jacks (golden keystone), small boards on standoffs (Pi/ESP32/Arduino-style), power parts (barrel jack, USB-C panel, switches, small PSU), cable glands (PG7/PG9).

- **MoCA adapter:** ScreenBeam ECB7250. Dimensions UNKNOWN until measured or taken from an official datasheet; never guessed.
- **Max size:** 250 mm on any outer axis.
- **Air vents:** optional, user picks per box (and per wall).
- **Priority:** Brian moved this ahead of v1 ("screw the roadmap", 2026-10-22). ROADMAP Now.

## First box (Brian, 2026-10-23)

- **No cable-slack storage** in the box (Brian: "don't gotta hold the slack"). The coax bend-radius drum idea is dropped.
- **Contents:** the ScreenBeam ECB7250 MoCA adapter and a **2-way coax splitter**. Incoming coax goes to the splitter; one output leaves for the modem, the other goes to the ECB7250. The ECB7250 also needs its power lead and an Ethernet cable out.
- **Wall openings (Brian, 2026-10-23):** a coax coupler on the left side and one on the right side; inside, they feed the splitter, whose two outputs go to the ECB7250 and (back out through a coupler) to the modem. An Ethernet keystone on the right side carries the ECB7250's Ethernet to the switch. **Decided (Brian, 2026-10-23): keystone F couplers** for both coax openings, so all three openings are the golden keystone (ks_tight 0.2). Fit of a keystone F coupler in that opening is UNKNOWN (only Ethernet keystones were printed). Which coupler is the coax input and how the ECB7250 gets power are still open.
- **Sides and size (Brian, 2026-10-23):** coax comes in on the **left**; the **right** side has the coax coupler to the modem, the Ethernet keystone and a **barrel connector for the ECB7250's power**. ECB7250 measured by Brian: **120 x 65 x 30 mm including rubber feet**.
- **Photos (Brian, 2026-10-23):** [splitter](photos/splitter-bridgelink-220-SP1XD-001.jpg), [ECB7250 top](photos/screenbeam-ecb7250-top.jpg).
  - ECB7250: **Coax In on the left end; Ethernet and Power on the right end** (matches the box: coax in left, power/Ethernet out right). Vent grille on the top face, so mount it top towards the lid and give the lid vents over it. LEDs (Power, Coax) on the front long edge.
  - Splitter: **Bridgelink 220-SP1XD-001**, 2-way, 5-1670 MHz. IN on one long side, both OUTs on the opposite side; two mounting ears with screw holes; ground screw on one end. Its dimensions are UNKNOWN until measured (not taken from the photo). It came with the ECB7250 and worked well in Brian's testing, so it stays (its 1670 MHz label is not a concern).
- **Layout concept 3 (2026-10-23, scratch renders only):** outer ~240 x 75 x 175; splitter IN joined straight to the left keystone F coupler with an F male-male adapter, splitter low near the bottom vents; right-angle F on splitter OUT 1 and on the ECB7250 coax; OUT 2 straight along the bottom to the modem keystone (same height); right-angle Ethernet and barrel plugs. Brian likes the direction; height may shrink.
- **Jumper candidate (Brian, 2026-10-23):** NECABLES RG179 F-male/F-male, 6 in for OUT 1 -> ECB7250 and 8 in for OUT 2 -> modem keystone (Claude's suggestion). Thin and flexible; Brian is wary of RG179 loss (2026-10-23), so the plan moves to: rigid F adapters (no cable) from splitter OUT 1 to the ECB7250, and a short RG6 jumper for the straight run to the modem keystone.
- **Concept 4 (Brian asked, 2026-10-23; scratch render only):** outer ~240 x 75 x 155. Solid adapter chain, no cable: splitter OUT 1 -> right-angle F (up) -> right-angle F (right) -> ECB7250 coax in. RG6 jumper OUT 2 straight along the bottom to the modem keystone. **Adjustable, then locked (Brian):** the ECB7250 sits in a cradle with four slotted tabs (M3 screws into back-wall inserts; top slots run left-right, bottom slots up-down); the splitter's ears sit on slotted bosses. Assemble the chain loose, let the parts find their spots, then tighten to lock. Depth alignment (front-back) by printed shims if needed. Fit, slot range and hold UNKNOWN.
- **Power cable (Brian, 2026-10-23):** the ECB7250's barrel plug is **45 mm long before the cable** and dislikes strain; power should come in from the **left** with the coax. A lying-flat ECB7250 cannot fit a straight 45 mm plug plus a bend inside 250 mm width.
- **Concept 5 (scratch render only):** ECB7250 **standing**, coax end down, Ethernet/power end up; outer ~155 x 75 x 235. One right-angle F from splitter upper OUT straight up into its coax (no cable); lower OUT -> RG6 jumper -> right-side modem keystone. Plug goes straight up 45 mm, makes a gentle U and runs down the left side to a 13 mm entry hole on the left wall, with a strain-relief clamp inside. Ethernet keystone top right. Same slotted lock-in cradle. Height is near the limit; real splitter/port positions decide it.
- **Concept 6 (Brian's idea, 2026-10-23; scratch render only):** outer ~240 x 75 x 165, ECB7250 flat again. Splitter mounted on the **inside of the left wall** (slotted standoffs), ports up/down. **Both coax keystones on the left wall**: IN (top) -> right-angle F -> down into splitter IN; splitter OUT 2 -> right-angle F -> EXIT keystone (bottom) to the modem, no cable. OUT 1 -> one RG6 jumper -> right-angle F on the ECB7250 coax. The ECB7250 sits ~50 mm from the left wall, so the 45 mm power plug goes straight out its right end, U-turns, and runs back over the top to a 13 mm entry on the left wall (strain-relief clamp inside). Right wall: only the Ethernet keystone. Supersedes the coax-exit-on-the-right plan if Brian keeps it.
- **Splitter size from Brian's ruler photo (2026-10-26, [photo](photos/splitter-bridgelink-ruler.jpg)); photo estimates, about ±1 mm, confirm with calipers before final geometry.** Scale is checked against the F thread (reads 9.5 mm = 3/8 in). Body about 38 x 22 mm (along the ears x across the ports); overall length ear tip to ear tip about 55 mm. The two OUT ports are on one long side, about 22 mm apart centre to centre. IN is on the opposite side, roughly in the middle. Each F port sticks out about 12 mm. The two ears sit at diagonally opposite corners: holes about 5 mm across, about 48 mm apart along the length and about 14 mm offset sideways. The ground screw is beside the lower ear. Body thickness (depth) is not visible in the photo and stays UNKNOWN.
- **Look:** friendlier for indoor use; five style concepts shown 2026-10-22 (soft slab, louvre, picture frame, pill, two-tier); Brian has not picked one yet.

## Still open

- Splitter: body thickness, plus caliper checks of the photo estimates above.
- Style pick.

- Default wall thickness is a parameter; generic wall guidance stays UNKNOWN.
- ECB7250: which measurement is which (120 long x 65 wide x 30 tall assumed), port heights on the ends.
- Panel barrel connector model and its panel hole size.

## Limits

New manufacturing adapter: PROPOSED — UNVALIDATED. Fit, hinge/snap/latch function, wall-mount load and strength UNKNOWN until Brian prints and tests. STL only; no printing without Brian's direction. Imported third-party part models stay local.
