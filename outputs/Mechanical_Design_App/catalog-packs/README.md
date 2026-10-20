# Phase 6 — batch 1

Phase 6 of 7 is IN PROGRESS. This completes the first bounded source/import checkpoint, not all M1–M8 coverage.

## Ready-to-import pack

Choose `phase6-batch1.json` with the existing app's **Hardware JSON file** control, then click **Import records**. This pack adds six records explicitly; it is not loaded at app startup. No active user database has been changed. Existing M3 starter records are unchanged. The identical pack also lives in the app's `catalog-packs/` folder.

| Size | Screw | Heat/ultrasonic insert |
|---|---|---|
| M2 × 0.4 | Accu SSCF-M2-8-A2, 8 mm | SPIROL item 151313, INS 24/M2 / 5 EK |
| M4 × 0.7 | Accu SSCF-M4-8-A2, 8 mm | SPIROL item 151317, INS 24/M4 / 7.5 EK |
| M8 × 1.25 | Accu SSCF-M8-16-A2, 16 mm | SPIROL item 151320, INS 24/M8 / 12 EK |

All dimensions use mm. Every record includes retrieval date, exact SKU/part identifier, source URL, field-level source sections and unknown fields. Accu screw records retain stated full threading, head dimensions/tolerances and drive sizes. Length convention follows the non-countersunk DIN 912 / ISO 4762 type.

SPIROL Series 24 inserts require an **8° included tapered hole**. The manufacturer's entrance values are stored separately from `hole_diameter`; they are not straight-hole recommendations. The current rule engine correctly leaves installation-hole fit UNKNOWN. Overknurl outside diameters are reference values, not tolerance-bounded maxima. Usable thread depth, minimum wall and material-specific installation behavior remain unknown. SPIROL lists these products as not stocked/made-to-order; no ordering was performed.

## Primary sources checked 2026-10-18

- [Accu M2 × 8](https://www.accu.co.uk/metric-cap-head-screws/3793-SSCF-M2-8-A2)
- [Accu M4 × 8](https://www.accu.co.uk/metric-cap-head-screws/3837-SSCF-M4-8-A2)
- [Accu M8 × 16](https://www.accu.co.uk/metric-cap-head-screws/3885-SSCF-M8-16-A2)
- [SPIROL M2 item 151313](https://shop.spirol.com/item/series-24-25-heat-ultrasonic-tapered-insert-metric/series-24-heat-ultrasonic-tapered-insert-metric/151313)
- [SPIROL M4 item 151317](https://shop.spirol.com/item/series-24-25-heat-ultrasonic-tapered-insert-metric/series-24-heat-ultrasonic-tapered-insert-metric/151317)
- [SPIROL M8 item 151320](https://shop.spirol.com/item/series-24-25-heat-ultrasonic-tapered-insert-metric/series-24-heat-ultrasonic-tapered-insert-metric/151320)

Only concise factual metadata is included. No supplier CAD, drawings, images, PDFs or substantial descriptions are bundled. Their redistribution rights remain unresolved. The manifest pins this local pack's SHA-256.

## Verification

27 Python tests PASS, including three new catalog tests. Disposable-database checks verify repeated imports remain idempotent, conflicting imports roll back atomically, old revisions remain immutable, pinned project snapshots survive import/reopen and newer catalog revisions, and empty size families remain empty. Rule tests confirm tapered installation, usable depth, wall and unsupported Pi4 head checks remain UNKNOWN; M2/M4/M8 cannot enter the M3-only geometry adapter.

The existing suite also verifies unchanged original assembly coordinates and Pi reference checks. No geometry render was needed for metadata additions. No desktop action, release packaging, purchasing, printing or active-data update occurred.

## Remaining Phase 6 work

M1, M1.2, M1.4, M1.6, M2.5, M3.5, M4.5, M5, M6 and M7 remain awaiting sourced importable records in this checkpoint; do not interpret that as supplier unavailability. Further lengths/styles/materials and insert families are incomplete. Next batch should prioritize straight-hole inserts with exact thread pitch and installation evidence plus missing common size families, before adding tapered-hole geometry support.

CNC Kitchen's manufacturer product pages and dimension poster were also reviewed as candidates. Their poster documents physical dimensions and hole/wall guidance, but exact thread pitch was not established for these candidates in the inspected material. No inferred-pitch CNC Kitchen record was imported.

The four-corner matter remains deferred until Brian explicitly raises it. Phase 5's physical/access/provenance unknowns carry forward; Phase 7 has not started.


## Batch 2 now available
See `phase6-batch2-README.md` and `phase6-batch2.json` for seven additional records and range-aware straight-hole checks. The above batch 1 coverage is historical. Starter plus both packs has19 records in disposable verification; active data remains unchanged. Phase6 stays in progress.


## Current status after batch 3
See `phase6-batch3-README.md` for the latest progress report and source links. `phase6-batch3.json` adds seven records; all three packs add20 records to the original six. Representative coverage10/14 screw and8/14 insert size families. Historical batch1/2 sections above are checkpoints, not current gap lists. Phase6 remains in progress; imports remain explicit.


## Current workflow checkpoint / batch 4
The app now offers explicit verified pack import, structured filters, replacement differences and source-gap evidence. `phase6-batch4.json` adds the exact M1 countersunk part, retaining overall-length UNKNOWN reach. Total27 starter+pack records;11/14 screw families,8/14 insert families. No user-library update is automatic. `source-gaps.json` records unresolved exact-source evidence. Phase6 remains in progress; scoped catalog browser acceptance passed in an approved disposable session.


Phase 6 batch5 (2026-10-18): optional five-record source pack closes M1.2 screw and M1/M1.2/M1.4/M1.6 insert source gaps. All five packs plus starter yield32 records. See catalog-packs/phase6-batch5-README.md for conditional installation evidence, tolerance conflict and remaining M4.5/M7 gaps. Explicit import only; active data unchanged.

Phase6 batch6 (2026-10-18): optional exact M4.5/M7 screw pack. All six packs plus starter yield34 records (16screws/18inserts),14/14 screw and12/14 insert families. Remaining insert gaps M4.5/M7 stay awaiting_source. See catalog-packs/phase6-batch6-README.md for source limits and remaining acceptance. Explicit import only; active user data unchanged.


LATEST: Phase6 COMPLETE WITH LIMITATIONS (2026-10-18). See catalog-packs/phase6-closeout.md. Batch7 explicitly imports four PEM revision2 records with visually verified catalog dimensions and shared catalog/product-page hole intervals. 34 identities/38 revisions across7packs+starter. Old pins preserved. Physical test fit late Phase7; no test started.
