# Phase 7 readiness and validation plan

Prepared 2026-10-18 from the local handoff at commit 9b44e5c and its referenced app documentation. Status: PREPARATION ONLY; physical work not started.

## Current state and constraints

Phases 1–6 complete, with Phase 5/6 limitations retained. Seven optional packs plus starter supply 34 identities / 38 revisions. Imports are explicit; saved pins do not automatically upgrade. This preparation did not inspect active user data or running app state. Preserve the original app, user data, immutable revisions, project pins, outputs/work and clearance-v2 mechanical baseline. The mounting matter remains tabled and outside this plan.

Digital screening is bounded. Whole-Pi solid conversion, containment/global clearance, actual installation and service access, printed fit and strength remain UNKNOWN. No physical approval follows from passing software tests. Small PEM records are not substitutes for the selected Pi4 M3 joint.

## Ordered readiness gates

1. **Freeze the intended configuration.** Identify the intended project and baseline/proposal revision by hash before any later validation. Obtain Brian's confirmation of the actual board revision, rack environment, accessories and intended service conditions. Record intended loads, temperatures, cable forces and service cycles as UNKNOWN until provided. Do not repin active projects as part of evidence collection. Exit: an explicit configuration record; any missing item remains an open gate.

2. **Confirm exact hardware identity and applicability.** The prior disposable trial used screw `accu-sscf-m3-8-a2` revision 1, Accu SSCF-M3-8-A2, M3 x 0.5, 8 mm under head, fully threaded, A2, recorded head diameter 5.5 mm / height 3 mm, 2.5 mm hex drive; and insert `mcmaster-94459a140` revision 1, McMaster 94459A140, M3 x 0.5, brass, recorded body length 5.7 mm, open end. Trial quantity was two screws and two inserts. These are recorded candidates, not a claim about hardware Brian owns or live selections. Match exact packaging/markings and supplier evidence before approval. Obtain exact insert drawing, OD bounds, usable threaded depth, installation pilot recommendation/tolerance, compatible materials/process, wall guidance and installation instructions. Existing 4 mm value is a supplier maximum, not a printed-hole target. Generic wall and usable depth remain UNKNOWN. Exit: applicable evidence tied to exact part/revision; unresolved gaps block affected claims.

3. **Specify actual material and manufacturing process.** Record printer/model, nozzle, material manufacturer/product/lot, condition/drying method, orientation, layer height, perimeter count, infill, temperature settings, cooling, supports, slicer/version and compensation. All currently UNKNOWN. Obtain applicable material and installation guidance before choosing settings. Do not invent a polymer, shrink compensation, installation temperature, load rating or strength. Exit: a versioned process sheet with reasons and uncertainty; printing still requires separate approval.

4. **Prepare installation and tool access evidence digitally.** Identify exact heat tool and tip, temperature-control method, fixture/support, approach, insertion depth/stop, cooling sequence and handling method. Identify the actual 2.5 mm hex driver including bit, shaft, handle, working length and torque capability/calibration. Record full envelopes and swept approach/removal paths at both joint axes; drive size alone is insufficient. Include Pi insertion/removal and actual cable plugs/bend envelopes/accessories in the intended rack surroundings. Use verified dimensions or provided drawings; unknown envelopes stay UNKNOWN. Any fresh desktop-control session requires Brian's approval. Exit: collision/access evidence for the chosen revision and explicit unresolved paths; nominal surface screens cannot approve access.

5. **Define metrology and acceptance before making specimens.** Record instrument identity, range/resolution, calibration/check status, measurement method, uncertainty and environmental conditions. Plan measurements of as-made pilot at multiple depths/directions, insert seating/depth/tilt, surrounding wall, screw under-head length, stack, available pocket, thread reach, bottom clearance and relevant joint/cable clearances. Use suitable methods for inaccessible/small features; do not claim a caliper proves usable thread depth. Trial inputs pilot 4, stack 3.3, pocket 8, boss diameter 9, engagement target 3, bottom allowance 0.5 mm are historical digital inputs, not measured dimensions or approved requirements. Exit: each criterion has an approved limit, method, uncertainty treatment and owner. Unspecified limits remain UNKNOWN and cannot pass.

6. **Prepare a reviewable specimen and observation protocol.** Before any print, define specimen identifiers, revision/source hashes, material/process sheet, feature scope, sample count and repeatability rationale, control specimen, measurement sequence and failure recording. A coupon should represent the intended joint's wall, orientation and thermal surroundings; representativeness must be justified. Pilot variants must follow applicable evidence and approved trials rather than arbitrary compensation. No coupon geometry or manufacturing files are generated by this plan. Digital dimensional screening can precede manufacturing; failed checks block proposed exports. Exit: reviewed protocol and approved criteria. No print/purchase is authorized.

7. **LATE Phase 7 only: authorized physical validation.** Wait for Brian's direction before any test fitting or physical testing; printing requires separate authorization. First inspect and measure approved specimens, then perform installation with the recorded process, allow documented cooling, and measure seating/damage. Only then assess screw assembly and tool access, Pi insertion/removal, cable service and rack interface within the approved scope. Apply torque/retention/cycle tests only after numeric limits, fixtures, method and stopping conditions are agreed. Stop on cracking, insert spin/pullout, bottoming, cross-threading, interference or unsafe access; record failure and quarantine affected specimens. Do not improvise increased torque, temperature or geometry. Exit: traceable observations, failures and measurements, not an assumed pass.

8. **Review evidence and disposition.** Compare results against pre-agreed criteria including uncertainty; borderline or incomplete evidence remains UNKNOWN. Record each criterion PASS/FAIL/UNKNOWN and the exact hardware, specimen/process, revision and method it covers. Failures require a separate proposed revision and targeted revalidation; preserve prior records. Brian reviews scope and residual limitations before sign-off. No release packaging is included.

## Acceptance matrix to complete before physical work

| Area | Required acceptance basis | Current disposition |
|---|---|---|
| Hardware | Exact identity, M3 x 0.5 compatibility and applicable sourced dimensions | Candidate records only; actual items UNKNOWN |
| Pilot and wall | Applicable supplier/process limits plus measured uncertainty | Exact printed fit / generic wall UNKNOWN |
| Reach and bottoming | Verified stack, usable thread depth, agreed engagement and bottom allowance | Trial targets only; usable depth UNKNOWN |
| Installation | Approved material/tip/process; seating tolerance and damage criteria | Numeric limits and process UNKNOWN |
| Tool/service access | Actual envelopes and successful permitted approach/removal across defined paths | UNKNOWN |
| Fit | Predefined measurable clearances and seating limits for exact configuration | Physical fit UNKNOWN |
| Torque/retention | Agreed torque, retention direction/load/duration and service-cycle criteria, justified for use | All numeric limits and strength UNKNOWN |
| Evidence integrity | Exact revision, hardware, process, method, observations and uncertainty recorded | Blank register prepared |

No physical criterion can pass solely because a digital check passes. Do not use a trial target or nominal dimension as a measured result.

## Scope clarification — Brian, 2026-10-18

STL output is sufficient for the end user's printing workflow. Printer/slicer/material-profile integration is outside the current app scope. Lack of a selected printer/material does not block Phase 7 software work. Earlier printer/process planning gates apply only if a separately authorized, bounded physical validation is later undertaken; they are not requirements to configure the end user's machine.

Continue Phase 7 with: (1) traceable hardware and honest dimensional UNKNOWNs, (2) supported geometry and source-to-STL identity, (3) existing mesh integrity and export safeguards, (4) artifact/revision traceability and reproducible digital acceptance, and (5) clear remaining physical-validation limits. Hardware actually owned and installation tools matter only when making claims about a specific installation or planning later physical work; they do not block auditing the recorded software configuration. Existing agreed geometry remains unchanged. Do not revisit the tabled mounting matter. No printing, physical tests or release packaging are authorized.
