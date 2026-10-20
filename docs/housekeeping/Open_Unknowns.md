# Open UNKNOWNs and limits

Updated 2026-10-19. Nothing here is marked passed. Digital checks do not establish physical fit, strength or retention. What gets worked on next is in [ROADMAP](../../ROADMAP.md).

The earlier version of this file, including its line-by-line ledger of quotes from older reports, is preserved byte-for-byte at [pre_roadmap_20261019/Open_Unknowns.md](../archive/handoffs/pre_roadmap_20261019/Open_Unknowns.md).

## Physical — UNKNOWN until Brian directs a print/test

| Item | Notes |
| --- | --- |
| Four-hole, 4 mm, 2.5 mm-corner faceplate | Fit and strength UNKNOWN. The old two-hole/3 mm specimen's positive fit does not transfer. |
| Wizard trays/faceplates | 1U and multi-U, keystone and port openings, snap tabs, clips, pegs, straps, single-piece joints, rear support: all unprinted. |
| Rack frame (PRINT THE RACK) and 1U extensions | Fit, strength, installation and movable-joint geometry UNKNOWN. Rear post back face at y=240 is an assumption. |
| Pi4 "Print in color" | Printed color result, fit and strength UNKNOWN. Rack-view artwork is preview only. |
| Keystone retention | Jacks latch on a 2 mm wall; retention UNKNOWN. |
| Hardware | Usable thread depth, insert OD tolerance, generic FDM wall/process guidance, screw/insert installation, torque, retention and cycles. Nominal after-knurl OD is not a certified maximum. |
| Pi4 assembly | Whole-Pi solid containment/global clearance, board seating, cable/tool/heat-tip/service access, installation approval. |

## Software limits (known, not bugs)

| Item | Notes |
| --- | --- |
| Wizard detection | STL units assumed mm; hole detector misses solid-box features and non-circular slots; port detector merges touching connectors and misses recessed ports. |
| SCAD import | `include`/`use` of external files is not supported in text-only import. |
| Generic equipment assemblies | May carry unused copied Pi4 pins; library span changes do not resize saved allocations. |
| Older cached library items | Keep the old plate until explicitly re-saved; no automatic regeneration. |
| Legacy entries without integrity manifests | Preserved, but affected downloads are blocked. |
| BOM | Four-post assumption unconfirmed; segment split is automatic (largest-first), not the exact chips clicked. |
| Per-instance component editing | Not complete. |
| Page-level logic tests | Save controller and viewer startup are verified by hand only. |
| Artwork-to-STL | Pi4 "Print in color" only; wizard faceplates show images in the rack view only. |

## Standing restrictions

- Supplier/Pi assets with unresolved rights and creator parts (BY-NC-SA, personal use) stay local; never redistribute.
- Source disagreement and project source policy stay distinct; draft and import do not save or repin.
- No printing, physical tests, release/publication, uploads or deployments without Brian's explicit direction.

## Parked

- Niche insert research (Brian's direction).
