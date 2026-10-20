Phase 6 source and installation checkpoint — 2026-10-18

Five source gaps now have exact, partial catalog records in optional batch5:

| Part | Thread | Installation evidence retained |
|---|---|---|
| Accu SIPL-M1.2-1.8-RENY | M1.2 × 0.25 | 1.8 mm pan screw, plastic RENY; threaded length unknown |
| PEM MSIA-M1-250 | M1 × 0.25 | Minimum hole depth 3.27 mm |
| PEM MSIA-M1.2-250 | M1.2 × 0.25 | Minimum hole depth 3.27 mm |
| PEM MSIA-M1.4-300 | M1.4 × 0.3 | Minimum hole depth 3.77 mm |
| PEM MSIA-M1.6-300 | M1.6 × 0.35 | Minimum hole depth 3.77 mm |

The verified catalog now offers 32 unique records after explicit import of all five packs: 14 screws and 18 inserts. Representative family coverage is 12/14 for both categories. Remaining exact-source gaps are M4.5 and M7 screws and inserts. Coverage is not a phase-completion percentage. Active user data was not imported or changed.

PEM's [manufacturer catalog](https://www.pemnet.com/wp-content/uploads/sites/9/2023/10/sidata.pdf), SI-9, supplies exact pitches, named A/E/C dimensions, hole depths and conditional wall guidance. The product pages label hole tolerance ±0.05 mm, while the catalog labels +0.05 mm. That discrepancy remains explicit. Named drawing values are stored under manufacturer_installation_evidence; length, outside_diameter, hole_diameter and generic min_wall remain unset pending visual drawing interpretation and applicability review. Usable engagement depth remains unknown. The browser PDF screenshot fetch failed; text extraction was available. No drawing inspection is claimed.

The 0.7/0.8 mm wall entries carry the catalog's ABS/polycarbonate test condition. They are not generic printed-material wall minima. Performance values were not imported as design allowables. Exact sources and field provenance are in the pack. No manufacturer drawings, PDFs or CAD are bundled.

The [SPIROL design guide](https://www.spirol.com/assets/files/ins-threaded-inserts-design-guide-us.pdf) additionally establishes a general post-mold minimum hole-depth rule of insert length plus two thread pitches. Its 2–3× OD boss guidance is an optimum range, not a universal minimum wall. These findings are documented here; no existing SPIROL immutable revision was overwritten or silently upgraded. Process/material applicability and tolerance treatment must be resolved before adding an automated installation rule.

Next acceptance work: resolve the PEM tolerance conflict and drawing interpretation; select the actual printed material/process and insert; compare measured pilot/depth/boss dimensions with applicable guidance; document installation tool access, process settings, installed position, cracking and thread access; then record physical retention/torque evidence against an agreed load requirement. This checkpoint does not start printing or claim physical acceptance. Phase 6 remains in progress; Phase 7 has not started.

Verification: 34 Python tests pass, including explicit import/idempotency/pin preservation and tests ensuring conditional evidence cannot create generic hole/wall/depth passes. Frontend implementation was unchanged. Mechanical baseline and earlier packs are preserved. Five-pack inventory is automated-tested; no new live browser acceptance is claimed. The mounting-layout matter remains tabled.
