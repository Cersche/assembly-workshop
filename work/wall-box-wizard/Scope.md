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

## Still open

- Default wall thickness is a parameter; generic wall guidance stays UNKNOWN.
- ECB7250 measured dimensions and port positions (Brian to measure, or a datasheet).

## Limits

New manufacturing adapter: PROPOSED — UNVALIDATED. Fit, hinge/snap/latch function, wall-mount load and strength UNKNOWN until Brian prints and tests. STL only; no printing without Brian's direction. Imported third-party part models stay local.
