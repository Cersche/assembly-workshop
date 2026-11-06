# MoCA rack tray

**Working file: `MRT.scad`** (from 2026-11-05). Released as **MRT-G** on 2026-11-06: `outputs/MoCA_Rack_Tray_MRT-G_2026-11-06/` (what changed and why is in its README). The next change becomes MRT-H; covers then get MRT-H-C1..C3. It is MRT-F rebuilt on `lib/workshop.scad`: plate outline and slots, hidden M6 joint and insert bores come from the library, in the rack frame (X centred). Every part matched MRT-F to within 1.3 mm³ when rendered on the snapshot. Part IDs are unchanged because the geometry is unchanged; a release gets the next free ID.

`MRT-A.scad` to `MRT-F.scad`, `make_*.py`, `check_*.py` and `clash_*.py` are history. Don't edit them or run them for the new file.

**Draft MRT-H (2026-11-06, parked):** stronger walls, screw-on Up/Down coax ramps (`ramp_in_up` etc.), forming jigs MRT-T5..T7. See HANDOFF.md. The release command below needs the four `ramp_*` parts added.

## Checks
Render the device and cable mock-ups first (snapshot, `OPENSCADPATH` set to `lib`), for example into a scratch folder:

```
openscad --backend=manifold -o <scratch>/dev_screenbeam.stl -D part="screenbeam" work/moca-rack-tray/MRT.scad
```

Do the same for `splitter` and `cables`. Then run the full check into a scratch folder. At release, use a new ID and an `outputs/` folder instead:

```
python tools/release_part.py work/moca-rack-tray/MRT.scad --id MRT-G --part plate:MRT-E-P --part tray:MRT-G --part cover_j:MRT-G-C1 --part cover_o:MRT-G-C2 --part cover_i:MRT-G-C3 --part shoe_left:MRT-C-L --part shoe_right:MRT-C-R --turn plate=x90 --turn shoe_left=x-90 --turn shoe_right=x-90 --keepout keepout --cuts cuts=7 --posts 2:both --against <scratch>/dev_screenbeam.stl --against <scratch>/dev_splitter.stl --against <scratch>/dev_cables.stl -o <scratch>/mrt_check
```

Result on 2026-11-05: 0 failed, 3 warnings.

- The warnings are the cover countersinks. The hole scan reads their taper as a 4.15 bore; there is no insert there.
- The keep-out checks the four M6 head recesses, an 8 mm driver path 40 mm straight back from each recess, and the shoe screw heads behind the rear posts. All are clear.
- The three floor windows and four strap slots stay separate.
- No part overlaps the real posts at U2. The tray clears the front posts by 2.12 a side, and the plate and shoes touch the post faces.
- No part overlaps the ScreenBeam, splitter or cables. The nearest cable gap is 1.03 to the tray.

Digital checks only. Shoes print ear face down (x-90). Fit and strength are UNKNOWN.

Devices: `docs/devices/screenbeam-ecb7250.md`, `docs/devices/bridgelink-2way-splitter.md`.
