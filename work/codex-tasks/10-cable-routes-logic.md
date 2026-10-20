# 10 — Cable management Step 3: routing and length logic (pure JavaScript module)

**Goal:** a pure, Node-testable module `outputs/Mechanical_Design_App/cable-routes.js` that the rack view calls for cable routes, lengths and draft upkeep. Claude is building the viewport and UI against the API below **in parallel**, so keep the names and return shapes exactly as written. Decisions: [work/cable-management/Step3_Decisions.md](../cable-management/Step3_Decisions.md) (read it). Data shape: the `cabling` block in that file and in task 09. Planning data only; lengths are estimates.

**Module pattern:** copy `cable-ports.js` (IIFE, `root.LabRaxCables = api`, `module.exports = api` under Node). No DOM, no fetch, no globals other than the export. Functions take a context `ctx = {ports: LabRaxPorts, library: [library items]}` where needed; the module must not read `window`.

**Scene facts (mm, X = rack width centre 0, Y = depth with the front of the front posts at 0 and the back of the rear posts at 240, Z up from the floor; U = 44.45):**
- Slot middle height: `zmid(slots, slot) = (slots - slot) * U + U / 2` (slots count down from the top).
- Guide anchor = the guide's position from `rack-scene.js` `guidePose`: X = −118.26 for FL/RL, +118.26 for FR/RR; Y = 254 for rear posts, −14 for front posts; Z = zmid of its slot. Implement the same numbers locally (do not import rack-scene.js).
- Exit anchors: bottom-rear `[0, 250, −10]`; top-rear `[0, 250, slots*U + 10]`; left `[−140, 220, zmid(slot)]`; right `[140, 220, zmid(slot)]`.
- Port anchor: find the port with `ctx.ports.portsFor(rack, placement, item)` (item = the library entry whose `id` equals `placement.equipment`, or undefined) by its `id`; position = `[p.x, p.y, ctx.ports.baseZ(rack, placement) + p.z]`, moved 8 mm along its pointing direction (`front` −Y, `rear` +Y, `right` +X, `left` −X).

**API (exact names):**
- `EXIT_POSITIONS`, `ENDPOINT_KINDS` (value → plain label), `TYPE_STYLE` (port type → `{color:'#rrggbb', diameter_mm}`; use the colours in `cable-ports.js` TYPES; nominal display diameters: rj45 6, usb-a 4.5, usb-c 4, hdmi 7, micro-hdmi 5, dc-barrel 3.5, iec 8, keystone 6, other 4).
- `cableColor(cable)` → `cable.color` or the type colour.
- `endAnchor(rack, end, ctx)` → `[x,y,z]` for a port end; `null` for an endpoint end or `null` end.
- `endFace(rack, end, ctx)` → `'front'|'rear'|null` (port face; endpoint ends count as `'rear'`).
- `autoRoute(rack, cable, ctx)` → `{guides:[ids], exit:id|null}`. Rules: the cable uses one post group — rear posts (RL/RR) unless both ends are port ends with face `'front'`, then front posts (FL/FR). An UNKNOWN face counts as rear (decision 11). Side: left post if the mean X of the known port anchors is < 0, else right. Guides: every guide on that post whose slot lies between the two ends' slots inclusive (an end's slot = the U holding its anchor Z; an endpoint end uses its exit's slot, or the other end's slot when there is no exit), ordered from the `from` end to the `to` end. Exit (only when an end is an endpoint): the existing `cable.route.exit` if it still exists, else the exit whose anchor is nearest to the last route point, else `null`.
- `path(rack, cable, ctx)` → ordered points: from-anchor, guide anchors, exit anchor (if any), to-anchor (port ends only). Unconnected or endpoint ends contribute no point.
- `estimate(rack, cable, ctx)` → `{route_mm, length_m, to_exit: bool, complete: bool}`. `route_mm` = sum of straight segments of `path`. `length_m` = `route_mm/1000` + `service_loop_m` (cable's, else `rack.cabling.settings.service_loop_m`, else 0.15) for each connected port end, rounded **up** to 0.1 m. `to_exit` true when an end is an endpoint (length is to the exit only). `complete` false when an end is `null`.
- `linkedCable(rack, cable, ctx)` → id of the cable on the other face of the same keystone (`passThrough` from `cable-ports.js`), else `null`.
- `portInUse(rack, allocation, port, exceptCableId)` → cable id or `null` (decision 13).
- `nextNumber(rack)` → lowest unused `'C<n>'`.
- `guideLoad(rack)` → `{guideId: number of cables whose route includes it}`; `crowded(rack)` → guide ids above `settings.guide_warn_above` (default 6).
- `upkeep(rack, ctx)` → mutates and returns the rack's cables per decisions 4 and 14: auto routes recomputed; manual routes drop guides/exits that no longer exist and set `route_changed: true` when they did; a port end whose allocation is gone, or whose port no longer exists on that equipment, becomes `null`; an endpoint end whose endpoint is gone becomes `null`. Must be idempotent.
- `warnings(rack, cable, ctx)` → list of plain strings: unconnected end, endpoint without any exit in the rack (decision 6), face UNKNOWN (decision 11), route changed, guide over the crowding setting.

**Tests:** add a Node test file `js-tests/cable-routes.js` (register it in `run_checks.ps1` the way `rack-bom.js` is registered) with fixtures built in code (a 6U rack, a pi4 placement and a fake wizard library item with rear ports and a keystone). Cover: anchors, auto route post choice and ordering, exit choice, length rounding and service loops, keystone link, port-in-use, nextNumber, crowding, upkeep (guide removed from a manual route, allocation released, endpoint deleted, idempotence), warnings.

**May change:** new `outputs/Mechanical_Design_App/cable-routes.js`, new `js-tests/cable-routes.js`, `outputs/Mechanical_Design_App/run_checks.ps1` (registration only). **Keep LF line endings.** Do not touch `workspace.js`, `rack-studio.js`, `cable-ports.js`, `index.html`, `app.py`, the asset manifest or `data/`; Claude wires the module into the page.

**Done when:** `run_checks.ps1` passes and the report lists the API as built (any deviation called out), the files with before/after SHA-256, and the commands run with their results.
