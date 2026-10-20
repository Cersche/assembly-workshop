# Hardware JSON records

Current schema and scope — 2026-10-19. Hardware catalog coverage is metadata coverage, not manufacturing-adapter or physical-fit support. Historical M3 x 0.5 evidence remains preserved; all new geometry uses the generic equipment adapter. Rack-frame STL export is in scope. See [README](README.md) and [standing guidance](../../AGENTS.md).

## Import, revision and provenance

Import a JSON array. Each entry needs `id` (stable text), positive integer `revision`, `name`, `kind` (`screw` or `heatset`), `diameter`, `pitch`, `source` and `verification` (`custom`, `partial`, `documented`). Dimensions are millimeters. Numeric dimensions must be finite and positive; omitted optional dimensions remain UNKNOWN. Documented records require `part_number`; documentation status is a recorded user assertion, not independent certification.

Use exact manufacturer part numbers and source documents. Manufacturer, material, finish, asset URLs, retrieval dates and licenses are preserved but not independently verified. Hardware CAD assets are not bundled. Supplier models/documents remain link-only until redistribution rights are established; unresolved supplier/Pi assets stay local. Fictional custom sources must be clearly labeled.

Imports are explicit and atomic. Preserve immutable old revisions and saved pins; importing a record does not repin an assembly. Draft comparison does not save. Each saved slot assembly has independent hardware pins, inputs and revisions. Official user data is `../../data/normal-use/`; use `start.bat`, never bare `python app.py`. Do not merge the historical app-local data copy.

## Screw and insert fields

The equipment wizard records **Device → Holes → Ports**. Per-slot tray choices are made in **Place on tray**, opened when placing a library item or from the slot's button. Apply changes the draft; explicit Save stores only differences from the library item in `placement.tray`. Library equipment facts and immutable hardware pins remain separate. Cable ports and clearance screening use the slot settings. With no slot tray settings, the rack shows the library item's build; otherwise it shows an existing exact render from Place on tray → Render exact preview or Generate, or a box sketch identified in the inspector. The sketch follows plate U height, tray size/offset/rotation and rear bracket, with dark blocks for keystone/port openings. `/api/equipment-placement-mesh` only looks up renders; it never renders. Keystone faceplates now pass the mesh check; fit, retention and strength remain UNKNOWN.

Preview quality **Low / Medium / High** is a per-viewer browser preference only. Generic `equipment_tray.scad` STL export quality **Draft / Standard / Fine** uses `$fn` **24 / 48 / 96** (`equipment.EXPORT_QUALITY`). Quality changes curve detail, not hardware verification; fit and strength stay UNKNOWN at every level.

The cable planner supports ports, guides, cables/exits, suggestions and saved-rack wiring sheets. It does not change hardware records or STL geometry. Lengths are planning estimates; jack type, guide capacity and cable fit/strength stay UNKNOWN. The Lab Rax Cable Guide is a local preview only, never redistributed or included in PRINT THE RACK. It does not establish a supported manufactured part.

Screw rule fields: `length`, `length_convention` (supported reach uses `under_head`), `threaded_length`. Inspection fields include `head_diameter`, `head_height`, `drive`, `material` and `finish`. A countersunk overall length does not become a supported under-head reach measurement automatically.

Insert rule fields: `length`, `outside_diameter`, `hole_diameter`, `hole_profile`, `usable_depth`, `min_wall`, `end_type` (`open` or `closed`). `hole_diameter` and `min_wall` must refer to documented installation recommendations, not be inferred from nominal thread diameter. Straight-hole comparisons do not establish support for tapered or stepped geometry.

Project stack is the distance from screw under-head bearing surface to insert entrance, including gaps and washers. The preserved historical joint inputs used 3.3 mm stack and 8 mm available pocket. Minimum engagement and bottom clearance are user targets, not universal fastening standards. Real hardware seating, usable depth and fit remain UNKNOWN unless specifically evidenced.

`hole_max_diameter` is a supplier upper limit: it enables a separate maximum check, not an exact hole recommendation. McMaster 94459A140's standard-profile row describes 5.7 mm as installed length and 4 mm as For Max. Hole Dia. Neither value establishes usable threaded depth, certified OD, wall minimum or printed-pilot compensation. Preserve original immutable records. See [source review](../Phase7_Digital_Acceptance/Hardware_Source_Review.md) (historical evidence path).

## Sourced hole intervals and profiles

Optional `hole_diameter_tolerance_mm` must contain exactly finite nonnegative `plus` and `minus` values, with positive `hole_diameter` and `hole_profile: straight`. The lower bound must be positive and both bounds finite. Only an explicit sourced range enables inclusive interval comparison (epsilon 1e-9 mm); absent tolerance retains the legacy exact-nominal check. This is supplier guidance, not physical approval or print compensation. Recorded SPIROL Series 19 examples use +0.08/-0.00 mm straight holes despite tapered bodies; usable depth, minimum wall and end type remain UNKNOWN where absent.

`recommended_hole_entrance_diameter_mm` is metadata for tapered inserts, separate from straight-hole `hole_diameter`. `hole_included_angle_degrees` is in degrees; dimensional values are mm. Nominal after-knurl/overknurl `outside_diameter` is a reference, not a certified maximum. These fields survive import/export, but unsupported installation geometry and printed fit remain UNKNOWN.

Optional `installation_hole_segments` is a nonempty array of `{z0,z1,diameter0,diameter1,source}`. Positions must be contiguous from zero, lengths/diameters positive finite, sources nonempty; it requires `kind: heatset` and `hole_profile: segmented`. Equal endpoint diameters describe straight segments, unequal endpoints tapered segments; boundary diameter discontinuities describe steps. Geometry/rule support remains UNKNOWN for these profiles.

## Optional catalog packs and evidence

Optional packs use the explicit JSON importer and local SHA-256 validation; they are not automatically loaded. `field_sources` preserves field provenance, `unknown_fields` records evidence gaps. Historical catalog reports record seven packs plus starter as 34 identities / 38 revisions (16 screw / 18 insert identities), with four PEM revision-2 updates preserving old pins. These are historical disposable-verification totals, not a claim about current user data or exhaustive catalog coverage. M4.5/M7 insert research is parked; do not resume it by default. See [catalog documentation](catalog-packs/README.md); filenames retaining retired terminology are historical paths only.

`catalog_evidence.inspect(part)` audits source/missing fields offline without promoting verification. Comparisons include installation segments, `manufacturer_installation_evidence`, `source_document`, `field_sources`, `unknown_fields` and `rights`. Offline support covers metadata; link-only drawings/CAD are not bundled. Source disagreement remains distinct from project source policy. Conditional manufacturer wall guidance is not generic FDM wall guidance.

## Validation limits

Verified 2026-10-19 with `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1`: **95 Python + 152 JS tests passed** on temporary data, with no server or OpenSCAD build. These software checks do not establish physical approval.

Failed checks block affected proposed exports; UNKNOWNs stay visible. Digital screening, mesh closure and supplier metadata do not certify installation, retention, loads, service access, usable thread depth, printed fit or strength. Four rack holes per faceplate U and the 2.5 mm radius limit are settled design direction, not physical approval. The earlier positive specimen report covers only the old two-hole, 3 mm, square-corner specimen. New parts and any artwork-to-STL result remain unvalidated; physical work requires Brian's direction. STL delivery does not require printer/slicer integration.
