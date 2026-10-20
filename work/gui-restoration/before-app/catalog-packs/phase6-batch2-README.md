# Phase 6 — batch 2: straight-hole records

Phase 6 of 7 remains IN PROGRESS. Seven additional catalog records and sourced hole-tolerance evaluation are complete for this checkpoint.

## Catalog additions

| Kind | Thread | Length (mm) | Exact part and primary source |
|---|---|---|---|
| screw | M2.5 x 0.45 | 8 | [SSCF-M2.5-8-A2](https://www.accu.co.uk/metric-cap-head-screws/3805-SSCF-M2-5-8-A2) |
| screw | M5 x 0.8 | 10 | [SSCF-M5-10-A2](https://www.accu.co.uk/metric-cap-head-screws/3849-SSCF-M5-10-A2) |
| screw | M6 x 1 | 12 | [SSCF-M6-12-A2](https://www.accu.co.uk/metric-cap-head-screws/3865-SSCF-M6-12-A2) |
| heatset | M2.5 x 0.45 | 5.74 | [INS 19/M2.5 / .226L EK](https://shop.spirol.com/item/series-19-20-long-heat-ultrasonic-insert-metric/series-19-long-heat-ultrasonic-insert-metric/150989) |
| heatset | M3 x 0.5 | 5.74 | [INS 19/M3 / .226L EK](https://shop.spirol.com/item/series-19-20-long-heat-ultrasonic-insert-metric/series-19-long-heat-ultrasonic-insert-metric/150419) |
| heatset | M5 x 0.8 | 9.53 | [INS 19/M5 / .375L EK](https://shop.spirol.com/item/series-19-20-long-heat-ultrasonic-insert-metric/series-19-long-heat-ultrasonic-insert-metric/150422) |
| heatset | M6 x 1 | 12.7 | [INS 19/M6 / .500L EK](https://shop.spirol.com/item/series-19-20-long-heat-ultrasonic-insert-metric/series-19-long-heat-ultrasonic-insert-metric/150423) |

Sources checked 2026-10-18. Records preserve supplier-stated millimeter dimensions, source sections, retrieval dates, exact identifiers, material/finish, unknown fields and unresolved asset rights. SPIROL part-number inch length tokens remain intact while numeric dimensions use the page's stated mm values. Series 19's insert body has taper, but its INSTALLATION HOLE is straight; this differs from Series 24's tapered hole in batch 1.

The four Series 19 records specify a straight-hole diameter tolerance of +0.08/-0.00 mm. Their hole ranges are 3.99–4.07 mm (M2.5/M3), 6.40–6.48 mm (M5), and 8.00–8.08 mm (M6). Overknurl OD remains a reference dimension, not a certified maximum. Usable thread depth, minimum wall, end type and material-specific installation remain unknown. Supplier Stocked status is recorded as a source assertion, not a live order guarantee.

## Rule change

`hole_diameter_tolerance_mm` contains exactly `plus` and `minus` nonnegative finite values in mm. With an explicit straight-hole nominal recommendation, the rule compares the pilot to nominal-minus through nominal-plus, inclusive. A 0.000000001 mm numerical epsilon only absorbs floating-point arithmetic; it is not manufacturing allowance. Nonpositive lower bounds, overflow, missing nominal, malformed values, booleans and non-straight profiles are rejected on import. Records without the new tolerance retain the legacy exact-nominal comparison. Tapered profiles continue to report installation fit UNKNOWN.

For the new SPIROL M3 record, pilot 4 mm is inside the stated 3.99–4.07 mm interval. This only passes the diameter comparison. The illustrative M3 alternative assessment remains INCOMPLETE, with usable engagement, actual bottom clearance, boss wall, source completeness and physical/spatial checks unresolved. No saved project or hardware selection was replaced. No insert is approved for physical installation by this result.

## Import

- `phase6-batch2.json`: seven new records only.
- `phase6-cumulative.json`: all thirteen Phase 6 records from both packs; useful for one explicit import. Do not import the manifest as hardware.
- Use the existing app's Hardware JSON file / Import records controls. Repeat import of identical records is idempotent. These packs are not automatically loaded.
- Use the updated app code for range-aware evaluation; older versions only compare nominal diameter.

The app-local batch 2 pack and manifest are in `catalog-packs/`. Active data/ has not been opened or modified. No supplier CAD, images, drawings or PDFs are bundled; redistribution rights for those assets remain unknown.

## Verification

30 Python tests PASS, including three new tests covering combined imports/pin preservation, interval endpoints/interior/outside values and legacy behavior, and atomic rejection of invalid tolerances. Starter plus both packs yields 19 records in a disposable database. Import conflicts roll back, original project pins survive reopening, and existing batch 1 and mechanical asset hashes match prior evidence.

No frontend code changed. Existing HTTP tests pass; no new live browser session or manufacturing render was performed. No desktop actions, printing, purchasing, active-data updates or release packaging occurred.

## Coverage and next work

Representative screws and inserts now exist for M2, M2.5, M3, M4, M5, M6 and M8 across starter plus both packs. M1/M1.2/M1.4/M1.6/M3.5/M4.5/M7 remain awaiting imported records; this is not a claim of supplier unavailability. Straight-hole insert alternatives for M2/M3.5/M4/M8 and small screw families are candidates for the next batch. Coverage remains incomplete across lengths, head styles, materials and installation methods.

The four-corner matter remains deferred until Brian raises it. Phase 5's physical/access/provenance unknowns remain open; Phase 7 has not started.
