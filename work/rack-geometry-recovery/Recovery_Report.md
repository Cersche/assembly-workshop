# Lab Rax rack source recovery — 2026-10-18

## Result

Recovered the complete original `C:/Users/brian/Downloads/index.html`, the shortened `lab-rax-assembler-code-only.html`, and all three requested creator 3MF files. Byte-for-byte copies are in `sources/`; SHA-256 and original paths are in `Source_Manifest.json`. The functioning rack-first dark studio remains the current app, not the recovered legacy HTML.

The current rack builder now includes **Lab Rax references** in its viewport toolbar: three creator reference images, all 21 individual source components in an orbitable read-only viewer, source mesh bounds, source filenames/member IDs/hashes, license metadata and Brian's supplied M6 insert statement. Full source vertex coordinates and triangle indices are retained. This is a local reference viewer, **not a rack-frame STL adapter**, assembled clearance checker, or automatic rack dimension preset. Existing logical layouts are still schematic. No real rack document was created.

## What survived

| Source | Observed capability | Limit |
| --- | --- | --- |
| Complete original `index.html` | WebGL rack assembly view; 1–5U post/panel components, base/top parts, feet, handles, 1U support extension; stack/slot placement rules, equipment/import handling, orbit/inspection, state persistence | Recovered code, not adopted wholesale; external fonts, historical cloud/asset/assistant hooks and old state schema are outside the current offline app |
| Complete original mesh data | 26 valid base64 payload pairs; 19 rack-related mesh keys match the supplied references after vertex remapping and quantization allowance | Coordinates are lossy signed-16-bit representations, not exact source coordinates; maximum observed matched vertex difference 0.002154 mm (rounded up) |
| Code-only HTML | Same main application script SHA-256 as the complete original; 6 usable panel mesh payload pairs | 20 mesh payload pairs are not decodable; this copy cannot stand in for the complete original |
| Posts & panels 3MF | 10 unique meshes: five post sizes and five side panels | Discrete supplied sizes; not evidence for stretching a post or supporting arbitrary 1–48-slot manufacturing geometry |
| 5U rack 3MF | 10 unique meshes including 5U post, side rail, front edges, top/bottom panels, feet, handle | Local parts and print-plate arrangements; verified rack assembly transforms are missing |
| Support extension 3MF | 1 unique mesh, two instances, embedded photos | Local source extent is about 30 × 240 × 84.15 mm, including tabs. The historical logical extension level is 1U; its whole mesh envelope is not one slot pitch |

The 19 matched full-HTML keys are post, four smaller post sizes, five side panel sizes, three beam variants, side rail, top/bottom panels, foot, handle and extension. Each matched mesh has an oriented-face correspondence after remapping vertices; equality of the original coordinate values is explicitly false. The other seven legacy keys are not matched against these three references; no new adapters for them were introduced. Matching source topology is not a physical approval.

No manufacturing rack-frame STL writer was located in the recovered original. Its STL/3MF code reads/imports geometry; its CSG code handles imported negative parts; its stack functions place existing meshes. Describing this as a recovered parametric rack manufacturing generator would overstate the evidence. Main script syntax passes a Node syntax check; the legacy application was not executed.

## Provenance and rights

The complete HTML SHA-256 is `0400d9d26ef322fb193d73cc805e731f23231fb03b175171af88c5109cc1533b`, matching the original hash recorded in the historical Sigma development report. Relevant read-only excerpts were recovered from Downloads' `Lab_Rax_Rev1_Beta_Creator_Profile_Sigma.zip` into `historical-creator/`. All three supplied 3MF hashes also match its `structural_reference.json`. That historical report explicitly warns that 3MF scene transforms are print-plate placements, not verified rack assembly transforms. Historical assistant statements and acceptance claims are not treated as fresh acceptance.

Archive metadata names designer **mklements**. Posts/panels metadata says `BY-NC-SA`; 5U rack and extension metadata say `MakerWorld Exclusive License`. These strings were recorded, not interpreted as clearance to distribute. Original files, extracted images and mesh data stay local. No assets were uploaded, published or packaged for release. Instructions, process settings and promotional claims embedded in archives were treated as source content, not Brian's instructions or generic manufacturing guidance.

Brian supplied: **M6 heat inserts can be placed in the rack post mounting holes.** The viewer records that attribution. Insert part, hole/bore specification, installation parameters, engagement, fit and strength remain **UNKNOWN**. No M6 hardware record/import, pin replacement, bore change, insert research or mounting implementation was performed. The existing Pi4 M3 × 0.5 adapter and pins remain unchanged.

## Supported route toward exact rack geometry

1. Use the full-coordinate source components, identified by source archive SHA-256, member path and object ID. Keep the recovered quantized HTML meshes as historical visual/placement evidence. Do not build manufacturing geometry from the shortened HTML or rescale meshes to match arbitrary layout dimensions.
2. Isolate a versioned component adapter for the supplied discrete 1–5U posts/panels and extension. Fail explicitly for unsupported variants. Preserve the independent schematic layout and existing shared Pi4 project rather than silently repinning or resizing anything.
3. Audit the recovered `bottomSlots`, `topSlots`, `levelSlots` and frame constants against source mating features and creator assembly evidence. The historical 44.45 mm U constant agrees approximately with observed post heights; width, depth, hole centers, top/bottom offsets and stack engagement are not thereby verified. Source local bounds do not establish clear internal width or usable depth. Do not use the 3MF print-plate transforms as assembled poses.
4. Keep source-coordinate fidelity, proposed assembled transforms, collision/clearance observations and physical evidence as separate statuses. Only enable a proposed manufacturing export after its exact source/transform manifest, supported configuration rules and digital integrity checks pass. Current rack manufacturing support remains false. Physical fit and strength stay UNKNOWN without separately authorized, specimen-specific evidence.
5. Rights clearance is needed before any redistribution; printing, uploads, purchases, release packaging, publishing, deployments and pushes require Brian's separate authorization. Physical testing is separately directed. Phase7 remains CLOSED WITH LIMITATIONS; no new phase or parked mounting/research work was opened.

The next technical step is a **read-only assembly-transform audit**, not another source hunt or printer questionnaire. Original sources are now recovered. No fresh source upload or decision from Brian is needed for that audit.

## Verification and activation

- 3 new Python tests PASS: every one of the 21 extracted components equals the 3MF's float coordinates and triangle indices; asset tampering blocks serving; unknown/traversal paths fail; reference routes do not access hardware data.
- All 25 reference assets have SHA-256 checks before serving. Catalog and image assets are separate from normal-use data and manufacturing handlers.
- New Node handler/canvas harness PASS: all 21 component selections; 101,184 finite drawing start coordinates; error recovery; stale request protection; GET-only requests. This is not visual/browser acceptance.
- Recovered complete main script and new viewer JavaScript syntax PASS. Existing catalog and Phase7 frontend handler checks PASS. No old application or CAD renderer was executed.
- All 7 existing rack document tests PASS using a new temporary directory under `work/rack-geometry-recovery/disposable-tests/`. First attempt in the operating system temporary directory hit sandbox atomic-replace denials; no persistence code was weakened.
- All 12 normal-use/original data hashes match both this run's before-state and the earlier GUI preservation hashes. Read-only SQLite integrity is `ok`; protected SCAD, assembly and mounting baseline files match the session safety manifest. No `data/normal-use/rack-workspace.json` exists. See `Verification.json`.
- No browser/desktop session, server start/stop, printing, CAD build, manufacturing export, hardware import, release packaging or publishing occurred. A loopback request to port 8765 was denied by the sandbox; listener inspection did not establish live server state. No duplicate server was started.

**Activation:** app source and local assets are ready. The pre-existing Python process, if still running, must be stopped and relaunched with the configured `outputs/Mechanical_Design_App/start.bat` to load new reference routes. Do not start a duplicate. After restart, use Rack → **Lab Rax references**. Live browser visual acceptance remains pending separately authorized access; source and handler checks above are the actual verification for this run.

`inspect_references.py` and `prepare_local_reference.py` are the new inspected extraction utilities; they never invoke OpenSCAD, a slicer or historical geometry code. The before-app guard refuses to overwrite a differing saved source, so do not rerun the initial preservation step blindly after integration edits. The earlier full safety copy remains valid for the prior state; this run adds a separate local preservation increment.

### Subsequent startup repair

Brian supplied a screenshot of the fallback light page/network error. An approved external-sandbox check confirmed no listener at8765. The current server was then started with the preserved normal-use library; studio/reference/API GET checks passed,6 revisions loaded with0 imports, and all6 normal-use file hashes stayed unchanged. This supersedes the pending-restart instruction above. Use `http://127.0.0.1:8765/`. Index.html now shows startup instructions when opened as a file. No browser visual acceptance is claimed; see `work/startup-repair/Verification.json` and current HANDOFF.
