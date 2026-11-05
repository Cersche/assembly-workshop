# Fit findings log

One place for every printed-fit result, because prints are slow and fit tests end up spread across different parts and days.
Add a row for each printed piece (what was tight or loose, by how much, what changed). Specimen-specific: a result applies
to that part, material and printer only; fit stays UNKNOWN elsewhere.

## Pattern so far: sleeves are too tight top to bottom

Two different sleeves came out about **0.5 mm too tight in height**, with the sides fine. The app's default sleeve top
clearance is `sleeve_top = 0.3` mm (`equipment_tray.scad`, `SLEEVE_TOP_DEFAULT` in `equipment.py`).
Raising the default (e.g. to 0.8) is **not decided**; until then, set `sleeve_top: 0.8` on new sleeves.

| Date | Part | Result | Change |
| --- | --- | --- | --- |
| 2026-10-21 | OptiPlex sleeve SLV-A | ~0.5 mm too tight up/down, sides fine | Sleeve v2 redesign (task 36) |
| 2026-10-22 | TL-SG108E sleeve, first delivery (`2026-10-22_TL-SG108E`) | Too tight top to bottom | Hidden-screw version uses `sleeve_top: 0.8` (+0.5 mm), unprinted |
| 2026-10-23 | TL-SG108E (Brian printed; version not confirmed, hidden-screw build sets it 17 mm back) | Ports not flush with the rack front; rear retention needed | `2026-10-23_TL-SG108E_flush`: measured depth 100 mm, ports flush, rear stop, keyhole spring detents (0.6 mm bumps), `sleeve_top` 0.8, unprinted |

| 2026-10-23 | KD-D keyhole-detent coupon (3 mm bump, 3 mm floor) | Locks very nicely; arm sticks out the bottom when bent | KD-E + tray: 6.5 mm floor, arm over a pocket, unprinted |

## Other fit results (see HANDOFF.md for details)

| Date | Part | Result |
| --- | --- | --- |
| 2026-10-18 | Clearance v2 tray/faceplate (two-hole) | Fit good |
| 2026-10-19 | Golden keystone v5, `ks_tight=0.2` | Perfect; now the default |
| 2026-10-20 | FP44 plate-height coupons | Perfect; 44.4 mm/U is the standard |
| 2026-10-20 | SLV-A OptiPlex sleeve | Slid in, feet in pockets (later: 0.5 mm tight in height, above) |
| 2026-10-27 | MoCA box first print: sleeve rev A, cradle rev A | Sleeve had no porch screw slots (fixed in rev B). Cradle: ScreenBeam feet (13 mm, 2.25 proud) hold it off the plate; keystone-side pad hits the keystone, so the jumper is ~1 in short of Coax In (cradle rev B) |
| 2026-10-28 | CM1000 bracket: faceplate + rails v2 (screw access bays) | Fits (Brian) |
| 2026-11-01 | CM6A CM1000 bracket (M6) | Too tight: slides in from the rear, jams near the faceplate; forced in, rail rear ends spread to 228 (design 220.46), 3.8 per side. Modem later measured 212 x 44.4, 14 mm end wedge, flat strip along each end; those numbers predict only about 1.3 per side, so the cause isn't fully explained. CM6C rejected unprinted; one-piece test slices follow |
| 2026-11-01 | CM1P-T1 one-piece test slice (0.4 clear, pointed V) | Too tight: had to be REALLY forced on, thin tie strips bowed toward the modem as the blocks levered apart. Modem end has a flat gray strip the V didn't allow for. Next: CM1P-T2 |
| 2026-11-02 | CM1P-T2 one-piece test slice (1.5 clear per side, 8 flat floor, 1.2 nose) | Fits: went on very easily. Total side play about 3.31 (design 3.0), so the modem is about 211.69 across its ends if nothing flexed. Modem front touches the end-block walls. Rack fit and strength not tested |
| 2026-11-02 | CM1P-T3 one-piece test slice (0.75 clear per side, real faceplate pocket and light pipes) | Goes on the modem. Total side play 1.5, exactly the design 1.5, so T2's 211.69 modem width holds. Went on by hand without force; looks seated as far as T2 in photos (not measured). Rack fit and strength not tested |
| 2026-11-02 | CM1P-A full one-piece bracket (0.75 clear per side, 120 mm rails) | Whole modem goes inside easily, a little too much play. Next: CM1P-E at 0.50 per side. Side screw, rack fit and strength not reported |
| 2026-11-02 | CM1P-E full one-piece bracket (0.50 clear per side) | Still too loose: barely holds the modem. Thin strip looks missing at the top of the plate from the front (the middle's 0.5 chamfer against the squared ears, inferred from the mesh). Side screw lines up. With the modem in, squeezing the rails inward firms everything up, so the rails flex that far by hand (how far not measured). Next: CM1P-F at 0.25 per side, front edges squared. Rack fit and strength not reported |
| 2026-11-02 | CM1P-E measured empty, rail tips (Brian) | Outside 221.5 (design 220.46), V floor to V floor 214 (design 212.69), so the channel is about 1.3 wide at the tips. Side play 3 (design 1.0). Rails don't bend when the modem is pushed in (Brian). Modem height in the rack fine, clear of the switch, modem doesn't shrink toward the rear (Brian). Front width and mid-rail not measured |
| 2026-11-02 | CM1000 modem measured (Brian) | 212 end to end, flat strip on each end 3 wide (channels since T2 assumed 8), end wedge 15 (14 used through CM1P-G). Not a printed part; sets the next channel |
| 2026-11-02 | CM1000 modem top face measured (Brian) | Flat top 182 x 106. 182 confirms the 15 end wedge (212 less 2 x 15). 106 leaves 30 of the 136 depth sloping; where it sits, front or rear, is not measured. Not a printed part |
| 2026-11-02 | CM1000 modem front slope measured (Brian) | 25 deep at the front. With the 106 flat top that leaves 5 of the 136 depth unexplained: a rear edge slope, or the depth is really 131. Not a printed part |
| 2026-11-02 | CM1000 modem end slope measured (Brian) | 25 along the sloped face. Brian marked up the section: 20.7 above the strip, 3 strip, 20.7 below, 44.4 total, so the strip is centred. With the 15 wedge that gives 25.6 along the face, close to his 25. Shape stays as modelled. Not a printed part |
| 2026-11-02 | CM1000 modem corner radius, from a top photo Brian supplied | Same on all corners (Brian). Circle fits on the two front corners give 8.0 and 9.1 at 2.37 px/mm, so about 8.5, not measured on the part. Same photo at that scale makes the depth about 129, against 136 in the model and 131 from his 25 + 106. Not a printed part |
| 2026-11-02 | CM1000 modem depth confirmed (Brian) | 131 front to rear, so 25 front slope + 106 flat top, no rear slope. Replaces 136, which all earlier models and channels assumed. Not a printed part |
| 2026-11-02 | CM1000 modem underside measured (Brian) | Underside flat 106, crease to rear edge, no feet or bumps on or near the front slope. So the 25 front slope is the same top and bottom, no longer assumed. Not a printed part |
| 2026-11-02 | CM1P-K test run, modem fit (Brian) | "Perfect fit. No sagging, no play, not tight." The 0.5 up-and-down lip gap, the 43 degree V and 0.25 per side at the tips all work on this print. Side screw is approximately 80 from the faceplate front, past the slot's rear end (slot Y 64.02 to 78.56, centred on the earlier 62.4 to 72 hole measurement). CM1P-M centres the slot on 80. Slicer settings, tip width, lights and rack fit not reported. Strength UNKNOWN |
| 2026-11-02 | CM1P-M report (Brian) | "Everything fits, 2 walls, 10% infill." Taken to mean CM1P-M with its slot centred on 80; revision not named, details on screw, lights and rack not itemised. These settings are the only ones proven for this fit. Strength UNKNOWN |
| 2026-11-02 | CM1P-M rails (Brian) | "Fits perfect", but the rails are a tad too short in the rear. CM1P-N extends them 10, nothing else, unprinted. Strength UNKNOWN |
| 2026-11-03 | CM1P-O light pipes (Brian) | Lights line up with the tubes, but no light gets through. An earlier faceplate on the same modem shines through easily, though its fit is too tight. CM1P-O's tunnels are open in the mesh and the pipes are the same diameter and position, about twice as long (11.3 against 5.8 on the centre line, 16.14 against 8.72 at the top). Cause not proven: pipe length and slicer settings are the suspects. Filament and settings on both prints not reported |
| 2026-11-03 | CM1P-O flashlight test (Brian) | Much more flashlight passes the old plate's pipes than CM1P-O's. Brian had switched to gyroid infill, so infill may be the cause rather than length alone. CM1P-T5A/T5B test both. Which old plate and its settings not reported |
| 2026-11-03 | CM1P-T6 light pipe test slice (Brian) | Best light through the icon-only hole (1.5 of plastic, open tunnel to the LED). Fits every longer pipe passing less, so length is the main loss on this filament. A against B (10% gyroid against 100% infill), the ranking of the other holes and slide-on fit not reported |
| 2026-11-03 | CM1P-O modem fit (Brian) | "O fit very well." Same V and lips as CM1P-K, M and N. Tip width and side play not measured. Strength UNKNOWN |
| 2026-11-03 | SCR5 screen + Pi + Hue tray (Brian) | Tray sags at the rear; supported only at the faceplate. Which printed revision and how far not recorded (the H8 README logs the same on H7, outer side). H9 addresses it, unprinted |
| 2026-10-28 | TL-SG108E `2026-10-23_TL-SG108E_flush` | Printed and tested; fit acceptable (Brian) |
| 2026-10-27 | MoCA porch15 + printed bezel nut | Fits, but nut too tall (above the rim), too thick and too tight; empty corner past the OUTs and closed modem side get in the way (porch rev 2, porch16.scad). Splitter calipered |

- 2026-10-28 TL-SG108E flush (2026-10-23 print): switch face ~1.3 mm proud of the faceplate; ~1 mm spare clearance above the switch in the opening (Brian: 1 mm is already forgiving). Fixed in SG8-M6-B.
- 2026-10-28 SG8-C1 (SG8-M6-B left hidden-screw joint coupon): Brian: fitment great; M6 x 8 button head and head recess good to go. Boss/insert test (SG8-C2) still to do.
- 2026-10-30 SG8-M6-C printed: did not fit. Cause found: B/C cut sleeve_top 1.35 → 0.35 against the proven print. SG8-M6-D restores 1.35, unprinted.
- 2026-10-31 SG8-M6-D printed: switch pocket fits well (Brian). Proven pocket: sleeve_top 1.35, side play 0.5, KD-E detents, rear stop at 100 mm, 1.3 mm set back. SG8-M6-F keeps this pocket exactly (only the floor under it went 6.5 → 5.5 mm, pocket moves down with it).
- 2026-10-31 SG8-M6-F tray printed (photo shows F's side runners; ID not read from the part): switch slides in with a satisfying detent click, seats with ports flush (Brian). Faceplate, post rails, M6 joint and insert still unprinted/unconfirmed.

- 2026-11-01 OptiPlex measured (Brian): 178 deep incl. bezel, not the 194.5 from the STEP. Feet 5 x 20 x 2.8 tall, 15 from each side, front pair 15 from the case front, rear pair 10 from the rear. SLV-F's dips are 16 long, too short for a 20 mm foot, so its click-in can't seat as designed. OPX-A uses 21.
- 2026-11-03 OPX-D printed (Brian): inserting the PC + faceplate into the rack is just a tiny bit too tight. Runner gaps were 0.1 ledge, 0.25 outer, 0.35 hold-down, from SG8-M6-F. OPX-E rails add 0.5 to each. Click-in, rear stops and strength not reported yet.
- 2026-11-03 OPX-E rails printed (Brian): fit improved, still a little too tight in the rails. Rear stops and feet line up fine. Runner gaps were 0.6 ledge, 0.75 outer, 0.85 hold-down. OPX-F rails add another 0.5 to each, unprinted. Strength not reported.
- 2026-11-03 OPX-E rails, empty sleeve (Brian): still needs the plate bent slightly, squeezing the tabs inward, to enter the slots. Backing the rail screws off 1/4 turn did not help. So not the PC's weight; the tabs are too wide for the slots. Whether the sleeve walls splayed or the rails sit closer than modeled is unmeasured.
- 2026-11-04 OPX-F rails printed (Brian): good fit. Proven runner gaps on his rack: 1.1 ledge, 1.25 outer, 1.35 hold-down, 1.1 sideways. Front sag and strength not reported.

## 2026-10-31 SCR5-H plate (rev 4 print) — glass would not go into the window
Brian printed the SCR5-H plate: the Waveshare 5" glass (120.7 x 77.2) would not enter the window (121.1 x 77.6, 0.2/side) — the 0.8 mm side lips behind the glass left only 119.5 mm, so this was a design error, not printer shrink. Rev 5: lips removed, clearance 0.4/side (121.5 x 78.0), screen inserted from the front. Lesson: check the insertion path, not just the final position; flush-glass windows can't have rear lips.

## 2026-10-31 SCR5-H7 print — screen window installed in the rack
Brian installed the printed SCR5-H7 screen unit (window 121.5 x 78.0, 0.4/side): overall a pretty good fit; a little more clearance than needed at the top edge of the glass (visible gap above the screen). The rev 7 test fit also found the missing frame corner tab, the unused Pi standoffs hitting the frame, and the panel ribbon jammed at the glass bottom edge; those are fixed in SCR5-H8 (not printed). **Parked (Brian):** tighten the top clearance later, once all brackets are dialed in.

- 2026-11-04 ER605 router measured (Brian): 158 wide, 101 deep; keyhole round part dia 8, 17.25 from side, 50 from rear edge; slots 4 wide, 8.5 from centre; stepped bar is on the ports edge. Height and room above the keyhole not measured. Not a printed part.
- 2026-11-04 ER605 router measured (Brian): 26 tall without feet (source pocket 25.7 too short), 4 room above the keyhole. Not a printed part.
- 2026-11-04 ER605 ports-end screw heads flush with the case bottom (Brian). Not a printed part.
- 2026-11-04 Right-angle F on the ScreenBeam coax port (Brian): 24.6 from port face to the connector's outer face, as modelled in MRT-E (18.6 + 6). Leaves 1.9 to the tray side wall. Barrel tip 38.2 not confirmed on this port. Not a printed part.
- 2026-11-05 SG8-M6-F (Brian): "the tray did print and everything did fit well." Parts covered by "everything" not itemised, including whether the M6 screws are fitted in the joint. Strength UNKNOWN.
- 2026-11-05 SG8-M6-F joint (Brian): M6 screws are in the joint and fit, but too close to the sleeve lip for comfort; future designs should leave more room. Strength UNKNOWN.
