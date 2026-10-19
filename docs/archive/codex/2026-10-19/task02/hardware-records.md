# Hardware JSON records

Import a JSON array. Each entry needs `id` (stable text), positive integer `revision`, `name`, `kind` (`screw` or `heatset`), `diameter`, `pitch`, `source` and `verification` (`custom`, `partial`, `documented`). Dimensions are millimeters. Numeric dimensions must be finite and positive; omitted optional dimensions remain unknown. Documented records require `part_number`; documentation status is a user assertion.

Use exact manufacturer part numbers and source documents. Additional metadata such as manufacturer, material, finish, asset URLs, retrieval dates and licenses is preserved with the record but not independently verified. This release stores metadata, not CAD assets.

Screw rule fields: `length`, `length_convention` (`under_head` for this version), `threaded_length`. Optional inspection fields include `head_diameter`, `head_height`, `drive`, `material` and `finish`.

Insert rule fields: `length`, `outside_diameter`, `hole_diameter`, `hole_profile` (`straight` for this version), `usable_depth`, `min_wall`, `end_type` (`open` or `closed`). `hole_diameter` and `min_wall` must refer to the documented installation recommendation, not be inferred from nominal thread diameter. Tapered/stepped holes remain unsupported in the initial rules.

Project stack means the distance from the screw's under-head bearing surface to the insert entrance, including gaps and washers. Pocket means the depth available for the insert body. For the Pi4 baseline, the stack is provisionally 3.3 mm and the pocket 8 mm; verify real hardware and seating. Minimum engagement and bottom clearance are user targets, not universal fastening standards.

`hole_max_diameter` records a supplier upper limit. It adds a separate maximum check and does not substitute for an exact `hole_diameter` recommendation.


## Phase 6 optional pack
`catalog-packs/phase6-batch1.json` contains sourced M2/M4/M8 screws and partial tapered heat/ultrasonic inserts. Import explicitly; do not replace existing starter revisions. `field_sources` records field provenance. `unknown_fields` records evidence gaps. `recommended_hole_entrance_diameter_mm` is metadata for tapered inserts and is deliberately separate from the straight-hole rule field `hole_diameter`. `hole_included_angle_degrees` is in degrees; dimensional record values are mm. Overknurl `outside_diameter` is a reference value, not a certified maximum. These fields survive import/export, but tapered geometry remains unsupported and installation fit UNKNOWN. Supplier models/documents are link-only until redistribution rights are established.


## Sourced straight-hole tolerance (Phase 6 batch 2)
Optional `hole_diameter_tolerance_mm` must be an object with exactly finite, nonnegative numeric `plus` and `minus` values, a positive `hole_diameter`, and `hole_profile: straight`. The lower bound must be positive and both bounds finite. Only an explicit sourced range enables inclusive interval comparison (numerical epsilon1e-9mm); absent tolerance retains the legacy exact-nominal check. This range is supplier dimensional guidance, not print compensation or physical-fit approval. The batch2 SPIROL Series19 inserts use +0.08/-0.00mm; their tapered bodies use straight holes. Usable depth/minimum wall/end type remain unknown. See catalog-packs/phase6-batch2-README.md.


Phase 6 batch5 (2026-10-18): optional five-record source pack closes M1.2 screw and M1/M1.2/M1.4/M1.6 insert source gaps. All five packs plus starter yield32 records. See catalog-packs/phase6-batch5-README.md for conditional installation evidence, tolerance conflict and remaining M4.5/M7 gaps. Explicit import only; active data unchanged.

Phase6 evidence review (2026-10-18): catalog_evidence.inspect(part) audits source/missing fields offline without promoting verification. Optional installation_hole_segments is a nonempty array of {z0,z1,diameter0,diameter1,source}; mm positions must be contiguous from0, lengths/diameters positive finite, and each source nonempty. Requires kind heatset and hole_profile segmented. Equal endpoint diameters describe straight segments, unequal endpoints tapered segments, discontinuous diameters at segment boundaries describe steps. Geometry/rule support is deliberately UNKNOWN for these profiles. Custom fictional sources must remain clearly labeled. Replacement comparisons include this metadata, manufacturer_installation_evidence, source_document, field_sources, unknown_fields and rights. Offline support covers metadata only; link-only drawings/CAD require network and are not bundled. Phase6 final acceptance pending review; no physical approval.


LATEST: Phase6 COMPLETE WITH LIMITATIONS (2026-10-18). See catalog-packs/phase6-closeout.md. Batch7 explicitly imports four PEM revision2 records with visually verified catalog dimensions and shared catalog/product-page hole intervals. 34 identities/38 revisions across7packs+starter. Old pins preserved. Physical test fit late Phase7; no test started.

## Phase 7 audit note — 2026-10-18

Current software scope is STL delivery, without printer/slicer integration. Phase 6 is closed with limitations; historical pending-acceptance statements above are superseded by phase6-closeout.md. McMaster's standard-profile row for 94459A140 labels 5.7 mm as installed length and 4 mm as For Max. Hole Dia. The stored length must not be promoted into usable threaded depth, a certified OD, wall minimum or a printed-pilot recommendation. Original immutable records remain unchanged. See ../../outputs/Phase7_Digital_Acceptance/Hardware_Source_Review.md for source applicability and retained UNKNOWNs.
