# Cable inventory and parts order: proposed decisions

2026-10-19. ROADMAP "Next". **Confirmed by Brian 2026-10-19.** Codex task 14 builds the pure logic to these defaults; each one is a small constant, so a change from Brian is cheap. Lengths are planning estimates; fit, capacity and strength stay UNKNOWN.

1. **Source.** Built from the **saved** rack only, like the wiring sheet ("Save first" otherwise).
2. **Cables are grouped** by type (RJ45, USB-C, …) and **stock length**: the smallest of 0.15, 0.3, 0.5, 1, 1.5, 2, 3, 5 m that is at least the estimate. Longer than 5 m → "custom length (≥ N m)".
3. **Keystone links** (rear run + front patch) stay two cables, counted separately.
4. **Incomplete cables** (an unconnected end, or a removed port/endpoint) are still counted, flagged "check: incomplete", so the order never silently shrinks.
5. **Spares:** none added by default. A per-rack "spares per group" setting is a later option.
6. **Keystone jacks:** one per keystone pass-through on each placed faceplate (`ks-N`), "buy". Jack type UNKNOWN (category/shielding not recorded).
7. **Cable guides:** one per saved guide, marked "print (local model, not in PRINT THE RACK)". Never bundled or redistributed.
8. **Not included yet:** rack frame parts (already in the rack BOM), screws/inserts, power strips, cable ties, patch panels.
9. **Output:** a "Parts order" card in Review next to the Wiring sheet: a table plus a CSV download. No purchases, links or prices.
