# Notes 2026-10-22 — feet clip through floor; wall-mount box wizard

## 1. Bug: rack feet clip through the "floor" (3D view)
- In the 3D rack view the feet (purple round pads) sit through/below the dark floor plane. Brian's screenshot marked them BAD.
- Likely a floor/ground-plane height vs. foot Z mismatch in the viewer (preview only, not the STL).
- Take to coordinator: fix floor height or foot position in rack-studio viewer.

## 2. Idea: custom wall-mount box wizard
- Build a wizard, using the same tech/approach as the bracket wizard, that makes custom enclosure boxes for wall-mounting equipment.
- Style reference: the boxes that house fiber NIDs on the side of a house, but smaller and more designed for indoor use.
- Should also let Brian build a custom piece of equipment from easily found, common parts (exact parts/standards not yet specified; ask Brian).
- Open questions: how it relates to the existing equipment wizard (equipment_tray.scad) vs. a new adapter; lid/hinge/latch; cable entry; wall mounting method; sizes.
- Take to coordinator; scope decision needed (new adapter, UNVALIDATED until printed).
