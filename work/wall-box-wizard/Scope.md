# Wall-mount box wizard — scope (Brian, 2026-10-22)

Idea from `work/notes/2026-10-22-feet-floor-and-wall-box-wizard.md`: an indoor, smaller take on the fiber NID boxes on the side of a house; custom enclosures for wall-mounting equipment, and a way to build custom equipment from common parts.

## Decisions (Brian, 2026-10-22)

- **Separate wizard**, its own designer outside the rack flow (not a variant of the equipment wizard). It may still reuse code (STL/STEP import, port detection, keystone geometry).
- **Lid: all three options**, user picks per box: screw-on (M3 into heat-set inserts), hinged + latch, snap-fit.
- **Wall mounting: all three**, user picks: keyhole slots, screw tabs, French cleat (separate rail STL).
- **Common parts library:** MoCA adapter, keystone jacks (golden keystone), small boards on standoffs (Pi/ESP32/Arduino-style), power parts (barrel jack, USB-C panel, switches, small PSU), cable glands (PG7/PG9).

## Still open

- Where it sits vs. v1: ROADMAP says new ideas wait until v1 is done unless Brian moves them into Now/Next.
- Which MoCA adapter (make/model, for dimensions).
- Size limits (max box) and wall thickness default (generic wall guidance stays UNKNOWN).
- Ventilation needs (PSU/MoCA heat).

## Limits

New manufacturing adapter: PROPOSED — UNVALIDATED. Fit, hinge/snap/latch function, wall-mount load and strength UNKNOWN until Brian prints and tests. STL only; no printing without Brian's direction. Imported third-party part models stay local.
