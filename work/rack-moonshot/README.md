# Rack Moonshot (2026-10-30)

Brian's moonshot: redesign the whole rack in themes, keeping the interface so every existing bracket fits.
Concept page: `Rack_Moonshot.html` (three.js, procedural, no meshes), artifact https://claude.ai/artifact/C92Ryf14S4BB8QoiV8sZGx

Themes: Tachi (The Expanse), Biomech (Giger), Better Worlds (Weyland), Vault 21 (Fallout), Raven Rock (Enclave), Hoover Dam Garrison (NCR), The Strip (New Vegas).

Fixed interface used by every concept: flat 6 mm front/rear flanges, M6 insert holes at X ±118.26 (Ø7.6), 3 per U (centre, ±15.9), 44.45 mm per U, 9U, inner clear opening ±111, body footprint 282 x 240, post centres 17.5 / 222.5 deep (from work/rack-finish/build_rack_finish_3d.py and HANDOFF). Crowns/signs are bolt-on and add height.

## Second pass: Rack Equipment (2026-10-30)

`Rack_Equipment.html`, artifact https://claude.ai/artifact/Fu3VnHAKkcBcoj53KR8TRQ. Same engine and interface; each rack is now a machine from its world: Ops Locker (Expanse avionics locker: O2 bottles, juice manifold, status panel), Incubator (Giger: strut posts, membrane sides with embryos, egg on top), MU/TH/UR 6000 (quilted walls, blinking lamp console, INTERFACE 2037 terminal), ZAX 1.2 (Vault-Tec mainframe: spinning tape reels, gauges, RobCo terminal), Eyebot Dock (Enclave: fusion-core charging bays, radio grilles, hovering Eyebot), Field Set (NCR Signal Corps radio: dial, handset, ammo cans, whip antenna), Lucky 38 Slot (lever spins the topper reels, every third pull is 7-7-7). Each machine lists what it adds outside the 282 x 240 x 9U body (tallest: NCR antenna +190 mm, folds).

Status: concept renders only. Next: Brian picks a theme and a frame strategy (full new frame with themed posts vs skins over the existing Lab Rax posts), then STLs one part family per session (Codex for bulk). Nothing printed; fit/strength UNKNOWN.

## Lab Rax Themes (third pass, keeps the Lab Rax frame)

`build_labrax_themes.py` + `labrax_themes_template.html` build `LabRax_Themes.html` (gitignored: it embeds the creator's BY-NC-SA meshes; private artifact https://claude.ai/artifact/RpGNomVd9Urve6YL3VGTLc). The real frame and final brackets, same placement as work/rack-finish. Eight themes (stock + the seven worlds): filament colour per part group, in-world device names and themed icon frames for the Print-in-color faceplates, roof emblem. The top front beam is split into original ends (|x| >= 112, joints untouched), middle and logo; the middle can be swapped for a crown: **dot strip** (6 x MAX7219 8x8, 192 x 32 mm, 48 x 8 mono, within beam height +2 mm) or **RGB window** (P2 HUB75 64 x 32, 128 x 64 mm, ~+40 mm, Pi HUB75 bonnet or ESP32-S3, own 5 V supply), each running a per-theme animation at true LED resolution. Concept only: beam profile, mounting, wiring, fit and strength UNKNOWN. Preview server: launch.json "Rack moonshot pages" (port 8865).
