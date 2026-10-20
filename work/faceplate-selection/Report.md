# Faceplate selection context — 2026-10-18

Selecting a faceplate now applies a cyan perimeter and subtle blue tint to its actual WebGL surface. The effect shares normal depth testing, so it cannot paint over foreground rack geometry. Clicking the mesh or selecting the corresponding allocation in the left tree uses the same selected-slot state. Selecting another slot clears the plate highlight. Any reserved slot within a multi-slot allocation maps to that allocation's faceplate.

Selection is a transient renderer argument, never an appearance/document mutation. Saved colors and artwork remain unchanged; no Save is required. The original rack-scene.js remains untouched. Updated rack-studio.js bytes were explicitly registered in the existing integrity manifest.

Verified: JS syntax and three protected-asset/route tests PASS. On disposable data, directly clicking the faceplate visibly highlights it and selects Slot 3 in the tree/inspector. Selecting empty Slot 4 updates the context and clears the selection. Save remains disabled, status stays Saved locally, and no console warnings/errors were observed. No need to repeat unrelated manufacturing or persistence suites for this preview-only change.

The current normal tab had Save disabled and no hardware-dirty text. Reloaded it safely and restored its prior Slot 1 selection; the plate now visibly highlights there. Screenshot: Normal_Selected_Faceplate.jpg. Source safety copies and normal data fingerprints are retained here. No user-data save, geometry build/export or physical action occurred.
