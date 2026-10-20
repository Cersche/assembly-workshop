Phase 6 progress and remaining acceptance — 2026-10-18

Estimate: three focused work blocks remain. This is a planning estimate, not a percentage or a promise of three chat turns. Source clarification can extend the evidence block. Physical installation/load testing belongs to Phase 7; the previous report incorrectly mixed that work into Phase 6 closeout.

This pass adds optional batch6 with two exact partial screw records:

- [Ideal Fasteners / MW Components M4.5-.75X8MM_FH_TX_AL_SP](https://www.mwcomponents.com/shop/m4-5-75x8mm-fh-tx-al-sp): M4.5 × 0.75, 8 mm, steel, TORX flat head. Length convention and head geometry remain unknown; reach remains UNKNOWN.
- [Metric Threaded Products 9129007025](https://metric-threaded.com/details/item?itemID=9129007025): M7 × 1, 25 mm, full thread, alloy steel class 12.9, thermal black oxide. Supplier head dimensions 12 mm width/6 mm height are retained as stated, without extrapolating nominal-size standards. Actual manufacturer identity and dimensional tolerances remain unknown.

All six packs plus starter now contain 34 unique records: 16 screws and 18 inserts. All 14 tracked screw families are represented; 12/14 insert families are represented. This is representative coverage, not exhaustive lengths, heads, materials, or supported geometry. Import remains explicit and project pins remain unchanged.

| Remaining block | Concrete acceptance |
|---|---|
| Source dispositions and record completeness | Retain honest M4.5/M7 insert states; document scoped manufacturer-family searches; fill supported missing metadata and make remaining unknowns inspectable. No negative web search is proof of supplier unavailability. |
| Installation evidence and catalog representation | Verify PEM A/E/C drawing interpretation and conflicting hole tolerances; distinguish conditional manufacturer guidance from rule inputs and print calibration; review straight/tapered/segmented hole representation, source/drawing inspection, and offline asset handling against the spec. Scope unsupported capabilities explicitly instead of treating partial records as validated installation designs. |
| Final integration acceptance | Exercise latest six-pack import, filter/replacement/custom-part/source inspection workflows, offline metadata and pin preservation; resolve failures, document any agreed deferrals, and run the final regression/visual acceptance needed for changed UI. No release packaging. |

Already accepted: catalog filtering, explicit atomic imports, immutable revisions/pins, replacement differences, verified-pack inventory, and scoped browser acceptance of the earlier four-pack workflow. Five/six-pack inventory is automated tested; no fresh visual review is claimed.

Targeted additional searches of SPIROL, PEM, Accu and Bollhoff did not establish exact M4.5/M7 heat-set parts. SPIROL's [Series24 family listing](https://shop.spirol.com/en-gb/viewitems/series-24-25-heat-ultrasonic-tapered-insert-metric/series-24-heat-ultrasonic-tapered-insert-metric) and [design guide](https://www.spirol.com/assets/files/ins-threaded-inserts-design-guide-us.pdf) remain sources for supported listed sizes; gaps stay awaiting_source. Thread-repair coils and cutting-tool insert screws do not fill plastic heat-set gaps.

Verification: 35 Python tests PASS, including all-family screw coverage, idempotent six-pack imports, saved-pin preservation, unknown flat-head reach, and unchanged conditional installation behavior. All six pack manifests/hashes and three protected mechanical/reference files verify. Active user data and mechanical implementation untouched. Phase 6 remains IN PROGRESS; physical installation/strength and Phase 7 remain open. The mounting-layout matter remains tabled.
