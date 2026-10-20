Phase 6 COMPLETE WITH LIMITATIONS — 2026-10-18

Brian authorized resolving the PEM discrepancy and closing Phase 6. Physical test fitting is scheduled for late Phase 7; no printing or physical test is started by this closeout.

The PEM decision is now explicit and implemented in four revision2 records. Direct download and local rendering succeeded where the web screenshot service had failed. Visual inspection of the manufacturer SI-9 drawing confirms A is axial length, E is after-knurl diameter, and C is pilot diameter maximum. The mounting-hole table prints +0.05 mm. Source PDF hash is recorded in PEM_Resolution.json; the PDF remains research scratch and is not bundled.

We use the published catalog interval as the project's governing dimensional basis. It also equals the overlap of the catalog's +0.05/-0 interval and the product page's +/-0.05 interval. This resolves the app's source decision without asserting a manufacturer erratum. The original discrepancy remains visible in revision2 provenance; revision1 is preserved.

| Insert family | Revision2 hole range | Length | After-knurl OD |
|---|---|---|---|
| M1 and M1.2 | 1.75–1.80 mm | 2.5 +/-0.1 mm | 2.1 +/-0.1 mm |
| M1.4 and M1.6 | 2.15–2.20 mm | 3.0 +/-0.1 mm | 2.5 +/-0.1 mm |

This is nominal dimensional screening, not a printed-fit or strength approval. Conditional manufacturer wall guidance is preserved separately; generic min_wall, usable thread depth, process calibration and physical approval remain unknown. Existing Pi4 geometry support is unchanged.

Primary sources: [PEM SI catalog, SI-9](https://www.pemnet.com/en-sg/wp-content/uploads/sites/2/2022/06/sidata.pdf), [PEM exact M1 product page](https://www.pemnet.com/products/product-finder/msia-m1-250/). Catalog interpretation and project source-selection policy are distinguished in each revision's installation_evidence_resolution.

Final scope: 34 unique hardware identities, 38 stored revisions after explicit import of all seven packs plus starter. All 14 tracked screw families and 12 insert families have representative sourced records. M4.5/M7 inserts remain awaiting_source; exhaustive styles/materials/lengths, arbitrary installation geometry and offline supplier drawing/CAD storage remain documented beta limits. Local metadata and custom axial profiles remain available offline. Old pinned revisions are not automatically upgraded; batch7 import is explicit and does not change project selections.

Verification: 39 Python tests PASS, including all four hole-range endpoints/interior policy boundaries, outside-range rejection, retained UNKNOWN engagement/wall, revision1 pin preservation and idempotency. Catalog frontend/import-handler tests and JS syntax checks PASS. All seven manifests/hashes and three protected mechanical/reference files verify. Earlier six-pack visual acceptance stands; batch7 data/rule additions and static phase wording have automated acceptance, not a newly claimed browser session.

Phase 7 sequencing: first prepare material/process choices, applicable hardware, tool/access evidence, measurements and test criteria; conduct physical test fitting late in Phase 7 at Brian's direction. Printing, purchasing and physical sign-off remain separate actions. The tabled mounting-layout matter remains tabled. Active user data and mechanical baseline are unchanged. No release package or third-party asset bundle was made.
