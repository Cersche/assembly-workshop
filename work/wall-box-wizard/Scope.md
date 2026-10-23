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
  - Splitter: **Bridgelink 220-SP1XD-001**, 2-way, 5-1670 MHz. IN on one long side, both OUTs on the opposite side; two mounting ears with screw holes; ground screw on one end. Its dimensions are UNKNOWN until measured (not taken from the photo).
- **Look:** friendlier for indoor use; five style concepts shown 2026-10-22 (soft slab, louvre, picture frame, pill, two-tier); Brian has not picked one yet.

## Still open

- Splitter measurements: body L x W x H, F-port length and spacing, ear hole spacing and diameter.
- Style pick.

- Default wall thickness is a parameter; generic wall guidance stays UNKNOWN.
- ECB7250: which measurement is which (120 long x 65 wide x 30 tall assumed), port heights on the ends.
- Panel barrel connector model and its panel hole size.

## Limits

New manufacturing adapter: PROPOSED — UNVALIDATED. Fit, hinge/snap/latch function, wall-mount load and strength UNKNOWN until Brian prints and tests. STL only; no printing without Brian's direction. Imported third-party part models stay local.
