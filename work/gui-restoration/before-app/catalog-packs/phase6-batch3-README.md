# Phase 6 progress — batch 3

2026-10-18. Phase 6 of 7 remains IN PROGRESS. Three bounded catalog batches are complete. Counts describe available representative records, not a percentage of total phase effort or exhaustive hardware coverage.

## Current progress

| Measure | State |
|---|---|
| New Phase 6 records | 20 across three optional packs |
| Total with original starter | 26: 12 screws, 14 inserts |
| Representative screw size coverage | 10 of 14 tracked size families |
| Representative insert size coverage | 8 of 14 tracked size families |
| Straight-hole recommendation records | 8 SPIROL Series19 records with sourced +0.08/-0.00 mm tolerance |
| Rule support | Explicit straight-hole interval checks; legacy exact checks retained; tapered-hole installation stays UNKNOWN |
| Catalog integrity | Hash manifests, provenance, idempotent atomic imports and project revision pins verified |
| Tests | 31 Python tests PASS |
| Active user installation/data | Unchanged; packs require explicit import |
| Physical installation approval | None; insert records remain partial |

## Added in batch 3

| Kind | Thread | Length (mm) | Exact part and primary source |
|---|---|---|---|
| screw | M1.4 x 0.3 | 6 | [SSCF-M1.4-6-A4](https://www.accu.co.uk/metric-cap-head-screws/3937-SSCF-M1-4-6-A4) |
| screw | M1.6 x 0.35 | 8 | [SSCF-M1.6-8-A2](https://www.accu.co.uk/metric-cap-head-screws/3784-SSCF-M1-6-8-A2) |
| screw | M3.5 x 0.6 | 16 | [SSCF-M3.5-16-A2](https://www.accu.co.uk/metric-cap-head-screws/3831-SSCF-M3-5-16-A2) |
| heatset | M2 x 0.4 | 3.99 | [INS 19/M2 / .157L EK](https://shop.spirol.com/item/series-19-20-long-heat-ultrasonic-insert-metric/series-19-long-heat-ultrasonic-insert-metric/150949) |
| heatset | M3.5 x 0.6 | 7.14 | [INS 19/M3.5 / .281L EK](https://shop.spirol.com/item/series-19-20-long-heat-ultrasonic-insert-metric/series-19-long-heat-ultrasonic-insert-metric/150420) |
| heatset | M4 x 0.7 | 8.15 | [INS 19/M4 / .321L EK](https://shop.spirol.com/item/series-19-20-long-heat-ultrasonic-insert-metric/series-19-long-heat-ultrasonic-insert-metric/150421) |
| heatset | M8 x 1.25 | 12.7 | [INS 19/M8 / .500L EK](https://shop.spirol.com/item/series-19-20-long-heat-ultrasonic-insert-metric/series-19-long-heat-ultrasonic-insert-metric/150424) |

Primary supplier pages checked 2026-10-18. The M1.4 screw is A4 stainless; M1.6 and M3.5 screws are A2. Accu's M3.5 specification explicitly says **Not Standardised**; no DIN/ISO conformity is asserted. The under-head measurement convention is recorded separately as a convention for the non-countersunk head type.

SPIROL Series19 Long straight-hole insert additions have nominal recommended holes: M2 3.20 mm, M3.5 4.78 mm, M4 5.61 mm, M8 9.58 mm; each +0.08/-0.00 mm. Overknurl dimensions remain reference values. Usable depth, minimum wall, end type and process/material-specific fit remain unknown. No supplier assets or substantial prose were bundled; CAD/document redistribution rights remain unresolved.

## Coverage after starter and all three optional packs

| Size family | Screw records | Insert records | Evidence state |
|---|---:|---:|---|
| M1 | 0 | 0 | Awaiting source |
| M1.2 | 0 | 0 | Awaiting source |
| M1.4 | 1 | 0 | Screw only; insert awaiting source |
| M1.6 | 1 | 0 | Screw only; insert awaiting source |
| M2 | 1 | 2 | Sourced metadata; inserts partial |
| M2.5 | 1 | 1 | Sourced metadata; inserts partial |
| M3 | 3 | 4 | Sourced metadata; inserts partial |
| M3.5 | 1 | 1 | Sourced metadata; inserts partial |
| M4 | 1 | 2 | Sourced metadata; inserts partial |
| M4.5 | 0 | 0 | Awaiting source |
| M5 | 1 | 1 | Sourced metadata; inserts partial |
| M6 | 1 | 1 | Sourced metadata; inserts partial |
| M7 | 0 | 0 | Awaiting source |
| M8 | 1 | 2 | Sourced metadata; inserts partial |

Awaiting source is not a statement that no supplier offers that size. Empty families remain explicit rather than receiving invented standard parts. Counts include alternate insert families/lengths, not just diameter labels.

## Acceptance evidence

New batch3 integration test imports all three packs twice into a disposable database, reopens it, checks 26 unique records and unchanged pinned project, verifies exact 10/8 family counts and each pack's hash, preserves A4 and nonstandard attributes, confirms sourced hole intervals pass only the dimensional comparison and pitch mismatches fail, and retains usable-depth/wall UNKNOWNs. Full suite:31 PASS. No runtime or frontend code changed this batch; the batch2 tolerance rule was reused.

Protected original SCAD/assembly/Pi reference hashes match Phase5 evidence. Prior pack1/2 hashes match their unchanged manifests. No active database was opened or modified. No fresh browser session, mechanical render, manufacturing export, desktop action, printing, purchasing, release packaging or commit occurred.

## Files and importing

`phase6-batch3.json` contains these seven additions only. `phase6-cumulative.json` contains all20 Phase6 additions, without duplicating the six original starter records. Both have SHA256 manifests. Use the app's existing Hardware JSON file / Import records workflow explicitly; repeated identical imports are safe. Use updated batch2 app code for tolerance-aware checks. The app copy is catalog-packs/phase6-batch3.json.

## Remaining Phase 6 work

1. Establish sourced records or evidenced availability dispositions for screw gaps M1/M1.2/M4.5/M7 and insert gaps M1/M1.2/M1.4/M1.6/M4.5/M7. Do not treat supplier family ranges as proof of availability at every size.
2. Broaden selected lengths/head styles/materials with a stated coverage target; review size/pitch/length/style/material filters and replacement-difference workflow against the beta specification before calling the library milestone complete.
3. Resolve remaining usable-depth, wall and installation guidance where supported by exact sources. Source documentation and a passed dimensional comparison do not establish printed fit or strength.
4. Decide model redistribution rights before bundling CAD; preserve link-only asset handling while unresolved.
5. Complete controlled installation/catalog acceptance without overwriting existing data. This checkpoint verifies the reusable packs and import path, not a live user-library update.

Next bounded target: investigate small-size screw/insert sources and record exact availability gaps, then review the catalog workflow. Phase7 has not started. Four-corner work remains deferred until Brian raises it.
