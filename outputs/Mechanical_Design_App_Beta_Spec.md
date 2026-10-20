# Mechanical Design App — Consolidated Beta Specification

Status: proposed implementation specification, based on the requirements readable in this conversation. This document is not an implemented app.

## Product direction

The mechanical design tool developed during the Lab Rax Pi4 work becomes the main app, replacing the initial app concept. The user intends to build it with Claude. Its local hardware library is a core capability. The Pi4 assembly is the first practical validation project.

The original app description could not be recovered: the linked chat returns assistant content-reference placeholders and model/image attachments, rather than readable original requirements or application source. The user has explicitly waived recovery of the original requirements. This specification is the new baseline; recovering the original app is not a prerequisite.

## Requirements and their origin

| Requirement | Evidence/status |
|---|---|
| Make this design tool the main application | Explicit user direction |
| Store hardware locally inside the app | Explicit user direction |
| Make screws and heat-set inserts across M1–M8 available when practical | Explicit user direction; catalog coverage must reflect actual sourced products |
| Select hardware for a design | Explicit user direction |
| Ask before desktop control | Explicit user preference |
| Require approval before printing | Established user constraint |
| Use Pi4 tray/faceplate as a validation project | Existing work, carried forward |
| Offline catalog search, revision pinning, BOM and rule-driven pockets | Proposed implementation to meet the requirements |
| Original app recovery | Waived by the user; use this specification as the baseline |

## Beta workflow

1. Create or open a local project with explicit millimeter units.
2. Import reference parts and preserve their original units, orientation and provenance. Support STEP through a CAD-capable adapter; use tessellated STL/3MF for display and mesh checks. Clearly distinguish editable solids from reference meshes.
3. Define an assembly joint and select its screw, insert, mating thickness and installation direction.
4. Evaluate dimensional constraints and available hardware. Show why a candidate fits, fails or lacks information.
5. Preview the proposed hole, boss and clearance changes; apply them as a new design revision.
6. Run appropriate checks and report pass, fail or inconclusive with the method and tolerances.
7. Export manufacturing parts, assembly references, a BOM and validation notes separately.
8. Generate a small joint coupon before a full prototype. Printing requires a separate explicit action and approval.

Desktop access is a separate permission-controlled operation. Local project processing does not imply desktop permission. No automatic purchasing, printing or external uploads.

## Local hardware library

Use a versioned catalog stored with the app's local data. A proposed storage layout is SQLite for searchable metadata and a content-addressed asset directory for CAD files, drawings and source documents. Keep the storage implementation behind an adapter so the geometry engine and UI can evolve independently.

Catalog navigation covers M1 through M8 and common intermediate metric sizes, including M1.2, M1.4, M1.6, M2.5, M3.5 and M4.5. Include only thread pitches and combinations verified against a source. Do not invent heat-set inserts to fill a size gap.

Each size family has an explicit state: sourced, awaiting source, unavailable from the supported suppliers, or custom user part. Missing catalog entries must not silently become generated standard parts.

Start the first usable catalog with exact M3 hardware for the Pi4 joint, then expand by sourced families. A complete M1–M8 catalog is a milestone, not a current capability. 'All screws' is an open-ended range of head styles, materials, lengths and pitches; expose coverage by family rather than claiming exhaustive coverage.

### Required part records

Common fields: stable internal ID, revision, category, manufacturer, manufacturer part number, supplier SKU/URL, source document/URL, retrieval date, units, thread designation, nominal diameter, pitch, material, finish, availability state, dimensional verification state and redistribution/license status.

Screw fields: head style, drive style/size, length and measurement convention, threaded length, head diameter/height, shank diameter, countersink angle if relevant, dimensional tolerances, CAD asset references and provenance. Record strength/property class only when sourced.

Insert fields: installation method, length, major outside diameter, pilot diameter, flange dimensions if applicable, recommended installation-hole profile and depth, supported plastics/process, manufacturer boss/wall guidance, thread usable depth, dimensional tolerances, CAD assets and installation documentation. Distinguish heat-set from press-in, molded-in and self-tapping inserts.

Represent a hole profile as axial segments so straight, stepped and tapered holes can be described. Distinguish manufacturer guidance from experimentally calibrated print compensation.

Asset records: format, SHA-256, local relative path, source, license/use constraints and verification state. A manufacturer CAD model does not automatically grant redistribution rights. Support user-managed downloads where bundling is not permitted.

Never substitute outside insert diameter for the recommended printed-hole diameter. Never infer fit from the label 'M3' alone.

### Library actions

Search/filter by size, pitch, length, head style, material and installation method. Inspect a dimension drawing and source. Import an exact part, create a clearly labeled custom part, validate required fields, and mark a part selected for a joint.

Support offline use of downloaded records/assets. Catalog updates are explicit and must preserve project-pinned revisions. Selecting a replacement shows dimensional differences and identifies affected design features.

## Hardware selection and design rules

Inputs include mating thickness, material, manufacturing process, installation direction, space envelope, required engagement, screw-head/driver access and intended load where known.

Hard checks include matching thread/pitch, insert length versus pocket/boss depth, supplier hole-profile guidance, residual wall thickness, screw reach, bottoming risk, head and driver envelopes, nearby component clearance and installation-tool access.

A simplified reach calculation uses the screw's under-head length minus the actual stack between its bearing surface and insert entrance. Account for washers, gaps and recesses explicitly. Countersunk screws use their distinct length convention. Compute usable engagement and remaining bottom clearance separately; do not impose a universal engagement or torque rule without a source.

Rank candidates only after hard checks. Explain the ranking using stock owned by the user, fit, useful engagement, installation access and sourced guidance. Unknown strength or material behavior remains unknown. A dimensionally compatible recommendation is not a certified load rating.

Generated feature dimensions are linked to the chosen part revision. Store the rule inputs and provenance with the feature. A catalog refresh cannot silently change existing geometry.

## Geometry and validation

Preserve assembly transforms, units and source meshes. Retain the source solid and its tessellation relationship where available. Check manifoldness before solid booleans. An empty result accompanied by an import/conversion error is inconclusive, never a pass.

Record the algorithm, objects, transforms, clearance threshold, contact exclusions and errors for each check. Distinguish vertex screening, triangle intersection, solid intersection, signed clearance and actual physical testing. A vertical clearance check must not be labeled a minimum clearance in every direction.

Intentional seating contact must be explicitly named. Artificial offsets used to exclude contact must be recorded. Reference parts cannot be merged into manufacturing exports accidentally.

Digital checks cover placement, holes, contact, interference and available tool envelopes. Physical checks cover print tolerance, insert installation, assembly access, squareness under tightening, strength, cable fit and rack fit.

## Pi4 acceptance project

Baseline: Lab_Rax_Pi4_Assembly_Beta_Clearance_v2 in this workspace's outputs.

Retain the 58 x 49 mm PCB hole pattern, PCB underside Z=16 mm, joint axes at X=+/-40 and Z=21 along Y, two tongue/socket pairs and the lowered four gussets. The earlier USB/gusset clash is a regression case. The detailed Pi reference has non-manifold edges, so its whole-object CGAL result cannot be used as a clearance pass.

The current 4.2 mm insert pilot is provisional. Before calling the assembly hardware-ready, choose an exact insert, validate its pocket and installation direction, select an exact screw with adequate reach and head/driver space, and recheck geometry. Assess Pi mounting hardware separately; the current PCB boss bores are 2.8 mm and must not be assumed to accept the same M3 system as the joint.

Beta acceptance:
- Open a project offline and load its pinned hardware records/assets.
- Select a sourced screw/insert combination and generate linked joint features.
- Reject incompatible thread/pitch, insufficient reach, bottoming and inadequate documented boss geometry.
- Preserve the Pi reference transform through project save/reopen and export.
- Detect the previous USB/gusset interference; distinguish it from intentional PCB seating contact.
- Mark failed solid conversion inconclusive even if the output is empty.
- Export manufacturing parts without the Pi reference and generate a matching BOM.
- Demonstrate a desktop permission gate and a separate print approval gate.
- Record joint coupon and full prototype results before claiming physical fit or strength.

## Delivery sequence

1. Build from this specification as the approved baseline. Initial implementation: local Python/SQLite service and browser UI, with geometry operations added through adapters.
2. Implement the catalog abstraction and source/asset import with a small verified M3 dataset; retain M1–M8 coverage states.
3. Implement project selection, revision pinning, BOM and joint-rule evaluation.
4. Connect geometry feature generation and validation through explicit adapters.
5. Import the Pi4 v2 project and complete regression checks.
6. Expand catalog coverage across M1–M8 using supplier data and permitted assets.
7. Prepare a coupon and full beta prototype after material/hardware selection; print only with approval.

## Catalog source starting points

- SPIROL inserts and CAD: https://shop.spirol.com/en-gb/category/inserts-for-plastics
- SPIROL heat/ultrasonic product/design guidance: https://www.spirol.com/product/threaded-inserts-for-plastics/heat-ultrasonic-inserts/
- McMaster heat-set catalog: https://www.mcmaster.com/products/heat-set-inserts/
- Ruthex product CAD downloads: https://www.ruthex.de/products/ruthex-m2-m3-m4-m5-gewindeeinsatze-sortimentskasten-lotspitzen-set-70-100-50-50-stuck-gewindebuchsen-aus-messing

These were identified during this chat. No complete catalog or CAD collection has been downloaded, licensed for redistribution or installed.
