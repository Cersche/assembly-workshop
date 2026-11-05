# Shared OpenSCAD library

Use `include <workshop.scad>` and, if needed, `include <BOSL2/std.scad>` in new parts. `tools/release_part.py` sets the library path and freezes the files a part uses into its `src/lib/`.

- `workshop.scad`: faceplate, slots, golden keystone, insert bores, hidden M6 joint and proven fit values. Post rails are not here yet; copy them from the newest proven bracket (OPX-F) and move them in when a second bracket needs the same shape.
- `BOSL2/`: pinned copy, commit `f5ca93de39ca12959a751e5247c57df0fd6b6a9c`, BSD 2-clause (see its LICENSE). Only the `.scad` files and the license are kept.
- Don't change a shape in `workshop.scad` without rerunning `python -m unittest tools/test_workshop_lib.py`. Released parts keep their frozen copy, so changes don't affect them.
- The golden keystone derives from a BY-NC-SA model: local and personal use only, never redistributed.
