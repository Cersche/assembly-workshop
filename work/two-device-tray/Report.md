# Two devices on one tray — Report (2026-10-20)

Brian: "we should be able to mount two devices on a tray, space permitting." He picked option A (device tabs) from [Plan.html](Plan.html).
Fit, retention and strength of both devices stay UNKNOWN. Nothing was exported or printed.

## What was built
- **Data:** a slot can carry `second: {equipment, tray}`. `second.tray` holds only the second device's own keys
  (`dev_off_x, dev_off_y, dev_rot, device_mount, standoff, insert_pilot, board_t`). Everything else (U, joint, keystones,
  rear support, bezel) is shared and stays in the slot's `tray`. Slots without `second` load and build exactly as before;
  a one-device SCAD source is byte-identical (tested). Old revisions are untouched.
- **Checks** (`equipment.clean_pair`, mirrored in `tray-pair.js`; any one blocks Apply/export):
  both footprints inside the 204 mm limit (tray stays centred, grows to the outer device + 8 mm);
  at least 4 mm between footprints, more when clips (2.5), straps (5.5) or flat stops (6.2) reach outside them;
  devices may also sit one behind the other; openings of the two devices keep a 2 mm web; all openings stay on the plate,
  clear of keystones and the (re-placed) tray screw joints; keystone collars clear the wider tray; each device's own
  checks (height, holes, flat gaps, rear depth). Not allowed with two devices: Sleeve, Flush/Set back front position,
  mixing Sits flat with a raised floor, rear keep-clear zones on the second device.
- **SCAD:** `template_source` copies the template's `dp()` and device feature modules with every device name renamed
  to `dev2_*`, adds them to the tray, and overrides `tray_w`/`tray_d`. Test render (scratchpad only) confirmed both
  devices' features: [screens/5-openscad-test-render-top.png](screens/5-openscad-test-render-top.png).
- **Window:** tabs "1 · device / 2 · device ✕ / + Add a second device…". Position and Mounting edit the selected tab;
  Faceplate stays shared. Adding a device puts it beside the first and centres the pair. Drag either device in the top view.
- **Elsewhere:** rack view sketch/exact lookup, cable ports (`d2-` ids, labelled with the device name), clearance
  screening (shared width, taller/deeper device), library delete counts the second device as in use.

## Verified
- `run_checks.ps1`: all checks passed (new `test_tray_pair.py`, `js-tests/tray-pair.js`).
- Browser, disposable data on port 8801: add, overlap blocked, drag clear, Apply (server check), Save, rack view and
  ports list. Screens in [screens/](screens/).

## Not done / limits
- Print in color, rear-bracket keep-clear zones and front-window modes do not cover the second device.
- Slot inspector text doesn't name the second device yet.
- The 4 mm gap is a PROPOSED number.
