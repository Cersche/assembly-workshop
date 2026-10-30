# SCR5-E — SCR5-D split for printing (U4–U3)

**SCR5-E = SCR5-D (Pi cooling) split so every part prints without supports** (Brian, 2026-10-29: SCR5-D "an absolute NIGHTMARE to print"; assembly is fine).

| Part (3MF object) | Print orientation | Notes |
| --- | --- | --- |
| `SCR5-E_plate.stl` faceplate | front face down | unchanged from SCR5-C/D |
| `SCR5-E_frame.stl` rear frame | rear face down | unchanged (ID only) |
| `SCR5-E_floor.stl` floor and walls | floor down | Pi standoffs, floor and right-wall vents, rear wall with two **open-top** cable notches (no bridge), left wall, corner post, five Ø8 wall-top bosses for M2.5 inserts (pilot Ø3.4 × 6 deep). |
| `SCR5-E_deck.stl` Hue shelf deck | deck down | Hue cradle, fan hole and screw holes, two M6 tabs, five Ø2.9 holes for M2.5 × 7 screws into the wall bosses; ID engraved mirrored on the underside. |

- **Joining:** the deck sits on the wall tops at Z 40.5, a flat contact checked as zero-volume. The five screws are at (−41, 39), (−10, 40), (−96, 144), (−55, 144) and (−15, 144). All the heads sit outside the Hue footprint. Extra BOM: 5 × M2.5 inserts + 5 × M2.5 × 7.
- **Depth:** the tray is now 148 deep (was 142) so the rear screws clear the cradle.
- **Ribbon gap:** the deck and floor behind the screen now start at Y 36 (was 32). The DSI ribbon drop gap between the frame/screw heads (Y 24–26.5) and the deck is now ~9.5 mm.
- **Ribbon route:** screen connector ≈ (−19, 13, 66) → straight back through the frame's open centre → down the gap → under the deck → round the Pi's rear end into its DSI connector (≈ X −74, Y 81). That end is low, so ~16 mm of bend room is left under the deck. Path ≈ 145 mm: the stock 160 mm is borderline and 200 mm is comfortable. No cut-out shortens it much, because the Pi connector sits at the board's far end (USB faces front).
- **Assembly order:** floor and walls → fit the Pi and the fan wiring → screw the deck on → screen and frame on the plate → plug the ribbon in → slide the tray onto the plate tongues and fit the two M6 × 8 (Hue out) → Hue in.
- **Checks:** each STL is one closed shell with no bad edges. Clash checks are empty for tray vs frame, screen, frame-screw driver paths, M6 driver paths and fan vs Hue. Floor vs deck, plate vs tray and the Pi standoffs are contact-only. 3MF plain tags 15,873 / 31,926, four named objects.
- Not printed. Fit, strength, airflow and ribbon reach UNKNOWN. The M6 tab counterbores are horizontal Ø11.5 holes: a short bridge, judged printable (UNKNOWN).

The rest below is carried over from SCR5-D/SCR5-C.

---

# SCR5-D — 2U screen + Pi 4 + Hue + keystone unit with Pi cooling (U4–U3)

**SCR5-D = SCR5-C + Pi cooling** (Brian, 2026-10-29: "pi could get a little hot"). Additions to the tray only:
- **Fan:** a 30 × 30 × 7 mm 5 V fan sits on the shelf deck over the Pi's front half, centred at X −74 / Y 30 and blowing down through a Ø28 deck hole. Four Ø3.4 holes on a 24 mm pitch take the fan's screws from below (head clearance under the deck about 1.3 mm above the Pi envelope). Power from the Pi GPIO 5 V/GND. Fan Y 15–45: clear of the M6 tabs (Y ≤ 14.3) and the Hue (Y ≥ 45.5); fan top Z 50.5, just under the keystone jack body (Z ≥ 51, jack not modelled).
- **Floor vents:** 7 slots, 3 × 45 mm, under the Pi between its standoffs (X −92…−56, Y 30–75).
- **Wall vents:** 12 slots, 4 × 20.3 mm, in the right wall behind the screen (Y 40–128). Air path: fan down onto the Pi, out through the floor slots, the right wall and the rear cable window.
- Clash checks are empty for fan vs tray, fan vs Hue and fan vs plate. Fan airflow and the Pi's temperatures are UNKNOWN; a heatsink on the SoC is recommended (fits under the deck).
- Plate and frame geometry is identical to SCR5-C except the frame's engraved ID. Tray 11,918 tris, one closed shell; 3MF plain tags 13,741 / 27,654.

The rest of this README is carried over from SCR5-C, with the ID changed:

---

# (from SCR5-C)

Claude, 2026-10-29 (Codex usage ran out, so Claude built it; spec `work/codex-tasks/50-scr5-c-screen-pi-hue-2u.md`). An **option** beside SCR5-B, not a replacement: SCR5-A/B, HP4-M6-A/B and `outputs/Final_3MF/` are untouched. **Not printed. Fit, preload, shelf strength, ribbon reach, heat and access UNKNOWN.**

Layout (Brian, 2026-10-29), seen from the front: **Pi 4 lower left**, **Hue Bridge on a shelf top left**, which runs back behind the screen, **golden keystone top left**, **screen on the right**. U5 is freed. Brian chose "Pi left, screen right" so the DSI ribbon stays short (the screen connector is on its left edge).

## Parts
| File | What |
| --- | --- |
| `SCR5-D_plate.stl` | 252 × 88.8 × 4 plate (R2.5, eight four-corner slots as SCR5-B), screen pocket/lip/M2.5 bosses at screen centre X +33, HP4-M6-B Pi openings (USB ×2, Ethernet) at the same X as HP4-M6-B, golden keystone at X −92.5 / Z 66, two M6 deck-joint bosses with tongues at X −71 / −50. |
| `SCR5-D_frame.stl` | SCR5-B rear clamp frame, unchanged except moved to X +33; engraved SCR5-D on its rear. |
| `SCR5-D_tray.stl` | One piece: Pi floor (Z 8.225–11.225, same height as HP4-M6-B), four Pi standoffs (Ø7 × 6, Ø3.2 pilots), shelf deck (Z 40.5–43.5), rear wall with cable window, right wall, left wall behind the Pi, corner post, Hue cradle on the deck, two M6 tabs (HP4-M6-B geometry, base moved to the deck). SCR5-D engraved on the floor behind the screen. X −102..−6, depth 142 (HP4: 123.4; the Hue sits further back to clear the keystone jack). |
| `SCR5-D_screen_pi_hue_set.3mf` | All three as separate named objects, side by side, 12 mm gaps. The plate prints front face down, the frame rear down (so the pads rise), the tray upright (**the shelf deck needs slicer supports**). Plain `<vertex>`/`<triangle>` tags, no `ns0` (11,597 / 23,270). |

Source: `src/SCR5-D.scad` (+ `SCR5-D_screen_config.scad` = SCR5-B config copy; `SCR5-D_hp4lib.scad` = HP4-M6-B copy + overrides, `use`d only for the golden keystone and the Hue cradle). The cradle is imported in place from `C:/Users/brian/Downloads/Swanky Rottis.stl` (never copied). Build: `"C:/Program Files/OpenSCAD/openscad.exe" -o SCR5-D_<part>.stl -D 'part="plate|frame|tray"' --export-format binstl src/SCR5-D.scad`, then `py -3.10 src/SCR5-D_pack3mf.py` and `py -3.10 src/SCR5-D_meshcheck.py SCR5-D_*.stl`.

## Hardware (BOM)
- 2 × rack M6 heat-set inserts in the plate bosses + 2 × M6 × 8 button heads (tray to plate).
- 4 × M2.5 inserts (4 long × 3.5 OD) + 4 × M2.5 × 7 socket caps (screen frame, as SCR5-B).
- 4 × M2.5 inserts/screws for the Pi standoffs (as HP4).
- 8 × the usual rack-faceplate fasteners.

## Checks run (Claude, 2026-10-29)
- Each STL is one closed, consistently wound shell: no open or duplicated edges, no degenerate faces, positive volume. Plate 6,964 tris; frame 9,092; tray 7,214.
- Plate bounds X ±126, Z 0.05–88.85 (88.8 tall), Y −4.08 to 20 (the golden keystone face is 0.08 proud, as on HP4). The slot and screen modules are SCR5-B's source, unchanged; the screen parts are only translated by +33 in X.
- OpenSCAD intersections **empty**: tray∩frame, tray∩screen envelope (12.6 deep), tray∩frame-screw head+driver paths (all four, straight back), tray∩M6 driver paths, Pi∩Hue, screen∩Hue. **Boundary contact only** (zero-volume): plate∩tray (floor/deck front at Y 0), plate∩frame (Y 20 seat), plate∩screen (lip at Y 0), plate∩Pi and tray∩Pi (standoff tops).
- **Hue box vs cradle:** a 90.7 × 90.4 × 30.7 Hue box overlaps the cradle posts by 5,171 mm³. This is the same cradle-to-Hue relationship as HP4-M6-B (cradle centred on the Hue, unchanged import). The box is a generous envelope, not a measured clash.
- **Hue vs top-left frame screw:** the driver path for the top-left frame screw (X −32.5, Z 67) runs through the Hue box. Lift the Hue out before removing the frame.

## Assembly and service
1. Fit the M6 inserts and the M2.5 inserts in the plate, and the Pi standoff inserts in the tray.
2. Screen from the rear into the pocket, frame on, four M2.5 × 7 (as SCR5-B). Do this **before** the tray goes on: the deck sits behind the screen's left part.
3. Pi on the standoffs. Plug the DSI ribbon into the screen, then slide the tray forward onto the two plate tongues and fasten the two M6 × 8 from behind (Hue out of the cradle).
4. Hue into its cradle; keystone into the plate; patch the Hue to the keystone.
Service: Hue out → two M6 screws → tray rearward → frame screws → screen.

## Open points (UNKNOWN)
- **DSI ribbon:** screen connector ≈ (−19, 13, 66) → rearward through the frame's open centre → down at Y≈29 in front of the deck → under the deck to the Pi DSI connector ≈ (−74, 81–88, 22). Polyline ≈ 160 mm + the usual 41 mm allowances ≈ **200 mm. The stock 160 mm cable is too short. Use a 200–300 mm Pi 4 DSI cable (Type A, 15-pin, 1.0 mm pitch); 300 mm is the safe choice.**
- **Pi HDMI / USB-C side faces the left rack wall** (about 2 mm away), the same as HP4-M6-B. With the left wall behind the Pi only from Y 92, the side is open at Y 45–74, but plugs will not fit against the rack post. Check on the rack; turning the Pi would change the front openings.
- **Keystone jack** sits behind the plate at X −92.5, Z 51–84.5; the Hue front is at Y≈45.5, leaving about 10 mm behind a ~30 mm jack for the patch cable bend.
- Shelf strength: the Pi floor hangs from the deck walls, and the deck from two M6 joints plus the walls. Nothing goes to the rear posts. Strength, sag and heat (Pi under the Hue) are UNKNOWN.
- Screen depth (12.6 nominal), pad preload, M2.5 fits: as SCR5-B, all UNKNOWN until the screen arrives.
