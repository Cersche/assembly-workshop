# OptiPlex bracket study: their bracket vs our wizard output

2026-10-20. Study only. No code changes, no exports, no commits, no pushes, no printing.

**Their bracket** = `DellOptiplex10InchRackMount.3mf`. It is the same mesh as `Dell Optiplex 10 Inch Flush Front.stl` (58,482 triangles, same volume). Brian confirmed it fits ("a tight squeeze but it fits"). That fit is Brian's report about this bracket only. It does not carry over to our design. Our fit and strength stay **UNKNOWN**.
**Ours** = the saved disposable revision `c9e8fa8c…` in `%TEMP%\aw-beta-data` (OptiPlex, flat mount, 1U, screw joint, made earlier today). I measured its `tray.stl`/`faceplate.stl`. I did not export or render anything new.
Third-party files were read where they are, in Downloads, with `python -I`. My scripts are in my scratchpad, not in the repo. Nothing was copied into the repo.

## What their bracket is

It is one printed piece: a 10-inch panel with a closed 1U **sleeve** behind it. The OptiPlex slides through a window in the panel. Its front ends up flush with the panel front.

- Panel: 254 × 44.4 mm, 3 mm thick, with gussets from the ears to the sleeve.
- Rack holes: 4 slots, 10 × 7 mm, two per ear. They are 7.5 mm in from each edge (±119.5 mm from centre), at heights of about 6.3 and 38.1 mm.
- Window: 183.0 × 37.0 mm. It is exactly the inside of the sleeve, so the device passes straight through.
- Sleeve: 201 mm wide outside and 176.5 mm deep, with 9 mm side walls. The walls have lightening windows (28 mm long, on a 40 mm pitch).
- Floor and roof: both are 3.7 mm thick. They are full width only for the first 21 mm behind the panel. After that, 15.5 mm ledges run along each wall for the full depth, top and bottom. The centre is open.
- Inside space: 183.0 wide × 37.0 tall. The device gets about 0.25 mm per side across (182.5 mm across), which explains the "tight squeeze".
- How the device is held: it is boxed in on four sides (walls plus floor and roof ledges). Front and back are open. There is no front or rear stop, so friction is the only thing stopping it sliding.
- Attachment to the rack: only the front ears. Nothing at the rear.

**Other files (not part of the confirmed bracket):**
- `optiplex_flush_split.scad` cuts the same STL into a faceplate plus a tray, joined by 6 × M3 screws into heat-set inserts in the 9 mm walls.
- `optiplex_flush_faceplate.stl` is 4 mm thick, not the 3 mm in that script, so it came from an edited version.
- The 16-Oct rear parts look like a separate add-on: `rear_stop` (a 206.2 × 45 × 44.4 U-frame), `rear_receiver_L/R` (20 × 43 × 48 blocks) and `rear_support_shoe` (220 × 88 × 44.4).
- **Answered (Brian, 2026-10-20):** none of the 16-Oct split or rear parts were ever printed. The only printed piece is the one-piece reference bracket (.3mf / Flush Front STL). Treat the others as unprinted ideas.

## Side by side

| | Their bracket | Ours (flat, as saved) |
|---|---|---|
| Device across the front | **182.5 mm** | **194.5 mm** (device turned 90°, `dev_rot=0`) |
| Device depth | 194.5 (sticks out past the 176.5 sleeve) | 182.5 |
| Overall width behind the panel | 201 mm (3.5 mm clear of 208 each side) | **210.5 mm (1.25 mm into each post)** |
| Panel | 254 × 44.4 × 3 mm | 252 × 42 × 4 mm (Brian's settled plate) |
| Rack holes | 4 slots 10 × 7, ±119.5 mm | 4 slots 10 × 7, ±118.26 mm (from Brian's 1U blank; the slots overlap) |
| Depth behind the panel | 176.5 mm sleeve | 202.5 mm tray (12 front gap + 182.5 + 8) |
| Floor | 3.7 mm, mostly side ledges | 3 mm full plate, at 0.5 to 3.5 mm |
| Device bottom above slot bottom | 3.7 mm | 4.7 mm (the floor top is at 3.5 in plate coordinates; the plate sits 1.225 mm above the slot bottom; corrected 2026-10-20 by the FP44 coupon session) |
| Height used | the whole 44.4 mm (it has a roof) | floor plus stops; joint risers reach 22.5 mm |
| Device held by | sleeve on 4 sides, 0.25 mm per side, 37 mm tall gap | 8 corner stops 6 mm tall (0.2 mm clearance), nothing on top, optional strap slots |
| Front/back sliding | free (friction only) | stopped by the corner stops |
| Front of device | **flush through a window**: power button, front USB and intake are open | **behind a solid plate with a 12 mm gap**; open only where port cut-outs are entered (0 were found) |
| Panel to device joint | one piece (or 6 × M3 in the split version) | 2 screw tongues plus bosses at the bottom centre |
| Rear support | none | none (`rear_support` is available but off) |
| Stiffness (my reasoning, not tested) | 44 mm-tall walls act like a box beam | a flat 3 mm plate hanging off two small tongues |

Measured clear height inside their bracket is 37.0 mm, but the STEP model says the device is 38.8 mm tall. Since it fits, the extra 1.8 mm is probably feet or other bumps (my assumption). That means our 38.8 mm envelope is on the safe side.

## Gaps, ranked

1. **The device is turned 90° in our wizard, so the tray is too wide.** *Blocks a trustworthy STL.*
   - The bracket shows the 182.5 mm side is the front. Our saved spec puts 194.5 mm across, which gives a 210.5 mm tray against a 208 mm opening. It probably also explains the 0 front ports, because the wizard was looking at a side panel.
   - **Fix now, no code:** press **Rotate 90°** in Place on tray. The tray becomes 182.5 + 16 = 198.5 wide and 214.5 deep, which fits. This still needs checking in the wizard.
   - **Fix in code (small, Claude):** suggest rotating when the rotated footprint would fit.
2. **Our hard width limit is 230 mm, not the rack's opening.** *Blocks a trustworthy STL.*
   - `MAX_TRAY=230` in `tray-placement.js:10`, the 230 check in `equipment.py:240`, and `assert(tray_w<=230)` in the SCAD. The 208 mm check in `equipment-wizard.js:186` is only a heads-up. So a tray that hits the posts can still be built and saved.
   - **Fix:** block when the tray is wider than the rack's inside width minus some clearance (for example ≤ 204 mm on a 208 rack, so 2 mm a side; the number needs Brian's OK). The same limit has to go in Python, JS and SCAD, with tests. **Codex task** (small, but in three places).
3. **There is no flush or through-window front.** *Blocks a usable PC mount.*
   - Our solid plate covers the power button, front USB and (my assumption) the front air intake. Their bracket's whole point is the flush window.
   - **Workaround now:** add a front cut-out the size of the device front by hand. Our 12 mm gap still sets the device back from the plate.
   - **Fix:** a "Flush front" option. Cut a device-sized window (plus clearance) and set the device front at the plate front. The screw tongues and bosses would have to move out to the sides of the window, and the front-gap asserts would change. **Codex task.**
4. **The device is barely held, and the tray is likely floppy.**
   - Our 6 mm stops stop sliding, but nothing holds the device down except an optional strap. A heavy PC also hangs off a 3 mm plate and two tongues.
   - **Fix:** a "Sleeve" option: side walls to device height plus top lips, like their ledges. Their sleeve is the proven shape for this device, but not proven in our design. Either do this together with gap 3 or switch on the existing `rear_support`. **Codex task.**
   - Retention and strength stay **UNKNOWN** either way.
5. **Port detection after rotating.** Rotated front openings are kept "as entered", so ports may not be found again after rotating. Check this in the wizard once gap 1 is done. A flush window (gap 3) makes most front cut-outs unnecessary. **Small (Claude check).**
6. **Rear parts.** Their confirmed bracket has no rear support. Brian's rear stop, receivers and shoe suggest he wanted one. Whether he did depends on his answer to the question above. If yes, our `rear_support` bracket is the place to compare. **Ask Brian first.**

Not gaps: rack hole positions match closely (ours come from Brian's settled blank). The plate size and thickness are Brian's settled choices. Device height above the slot bottom is close (4.7 vs 3.7 mm, see the correction in the table).

## What blocks an STL Brian can trust

Gaps **1 and 2** block it. As saved, the tray hits the rack posts, and the app does not stop that. Gap 1 can be fixed today by rotating. Gap 2 is needed so the app stops it in future. Gap **3** blocks a *useful* PC mount (the power button is covered), but not a geometrically valid one. Gap 4 is about strength and retention, which stay UNKNOWN until Brian directs physical testing.

No Codex tasks have been written. That waits for Brian's OK.

## Follow-up: orientation check (2026-10-20, later)

I re-imported the STEP into the wizard on my own server (port 8798, `%TEMP%\aw-beta-data`). I edited "OptiPlex flat test" and closed it **without saving**. Nothing was saved, rendered or exported.

- **X is up** gives 194.5 × 182.5 × 38.8. That is the wrong way round; the wizard warns 210.5 > 208 but does not suggest rotating.
- **X is up + Rotate 90° once** gives 182.5 × 194.5 × 38.8. The width warning goes away and 12 possible front ports are found. They are a uniform row along the top, which looks more like a rear I/O or vent row (my guess).
- **X is up + Rotate 90° three times** gives the same size, with the other end at the front. It finds 3 possible front ports (a wide slot, a small square and a tall rectangle), which looks more like the real front (my guess).
- **Brian to confirm:** the power-button end must be at the orange edge.
- The saved items in that data folder still say 194.5 wide (`dev_rot=0`). If Brian rotated in his own browser, it has not been saved there.
- **Feet:** the model shows feet under the case, which is why it is 38.8 mm tall. Their bracket only has 37.0 mm between floor and roof ledges, and the ledges sit at the edges where the feet appear to be. So the feet are probably squashed or removed in the real fit (the "tight squeeze"). That is my assumption; ask Brian.

Brian's direction (2026-10-20): the sleeve option is the way to go. The OptiPlex is heavy, so it is a good test case for the tray supported at the rear posts (`rear_support`). With flat mount, the rear-joint assert needs front gap + depth ≤ 228.5 mm; 12 + 194.5 = 206.5, so it passes on paper.

## Follow-up: the foot grooves (2026-10-20)

Brian pointed out that the bracket has indents for the PC's feet. They are there: two grooves, 2.00 mm deep and 5.5 mm wide, at X 51-56.5 and 197.5-203 (about 16-21 mm in from each side wall), running 14.5-91 mm behind the front face. The case sits on the 37 mm-high floor and the feet drop into the grooves, which leaves 39 mm where the feet are.

My first scans missed them. The STL is three overlapping bodies, so counting surfaces along one ray gave wrong answers, and I read the symmetric panel upside down. The grooves are in the face I had called the "roof".

The method is now kept in the project:
- `outputs/Mechanical_Design_App/mesh_study.py` splits a mesh into its bodies, ray-casts each one separately and merges the results. It reports floor and roof levels with their grooves and bumps.
- `test_mesh_study.py` rebuilds the same trap: overlapping bodies plus a hidden groove. It is part of the standard checks.
- Run on the bracket: `python -I mesh_study.py recesses "<bracket.stl>" 1 0.5 0.3`.
- It also reports that the bracket mesh has 2,305 open edges, a property of the third-party file.

Next step: Codex task 28, which makes the wizard find a device's feet and cut pockets for them in the floor. Idea for later (not yet in IDEAS.md): let Brian load a reference bracket that already works and have the app list what it learns from it (clear sizes, grooves, joints), so they can be compared with our design.
