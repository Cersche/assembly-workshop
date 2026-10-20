# Phase 7 — M3 hardware/source audit

Reviewed 2026-10-18. This is an evidence audit of recorded candidates, not a purchase recommendation or confirmation of hardware owned. No immutable catalog records, packs or pins were changed.

## Screw

The exact [Accu SSCF-M3-8-A2 page](https://www.accu.co.uk/metric-cap-head-screws/3818-SSCF-M3-8-A2) confirms M3, pitch0.5 mm, length8 mm, full thread, A2 stainless/natural finish, head diameter5.5 mm (+0/-0.18), head height3 mm (+0/-0.14), and socket2.5 mm. This agrees with the stored nominal screw fields. Its under-head convention remains the recorded catalog interpretation. A socket size does not establish a driver shaft/handle envelope. Page extraction contains conflicting availability labels, so no availability assertion is made.

## Insert

The exact McMaster 94459A140 product URL could not be retrieved through the web reader. The existing [McMaster heat-set catalog source](https://www.mcmaster.com/products/94459a170/) includes the standard-profile brass 94459A140 row: M3 x0.5 mm, installed length5.7 mm, maximum hole diameter4 mm. The column is explicitly installed length, not usable thread depth. No exact OD, usable depth, generic FDM wall or printed-hole recommendation was established from this row.

## Applicability and disposition

The app's existing `length:5.7` field participates in a nominal body/pocket envelope. Supplier wording does not independently prove every body/seating interpretation used by that envelope. The report must retain its nominal scope. It must not promote 5.7 mm into guaranteed engagement or a measured installed depth. Preserve the partial record rather than inventing a corrected value or silently revising pins.

The recorded pilot4/stack3.3/pocket8/boss9/minimum-engagement3/bottom-allowance0.5 mm configuration remains a digital trial. Existing rules produce7 PASS /0 FAIL /6 UNKNOWN; overall incomplete. Nominal reach4.7 mm exceeds the user target3 mm, but usable thread engagement remains UNKNOWN. Maximum-hole compliance is not installation-fit approval. Outside diameter/minimum wall, installation process, physical bottom clearance, tool/service access, fit and strength remain UNKNOWN.

Point2 disposition: audit complete WITH LIMITATIONS. Exact-part source traceability was checked; unresolved supplier dimensions remain explicit. Neither printer integration nor physical ownership is a software-acceptance gate. Source metadata inspection is offline-capable; external drawings and CAD remain link-only.
