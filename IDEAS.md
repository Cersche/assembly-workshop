# Ideas parking lot

Write any idea here the moment it comes up, one line with the date. Don't judge it, then get back to work. Once a week, sort each one: move to ROADMAP.md, keep, or cross out (~~like this~~, don't delete).

## Inbox

- 2026-10-28 — Revisit the faceplate painter (Print in color). Brian: "awful experience". Problems from the HDT-M6-A drive tray: (1) every image, SVG included, becomes a 0.4 mm square grid, so curves come out badly pixelated; it needs real vector inlays (smooth outlines, like `outputs/Hard_Drive_Tray_M6_2026-10-28/HDT-M6-A_art.scad`). (2) Clicking Export color STLs with unsaved changes does nothing and shows no message. (3) The default image size was tiny (20 x 24 mm). (4) It rebuilds the faceplate from the saved library item, so hand-made or redesigned faceplates (M6 brackets) can't be painted.

- 2026-10-19 — Equipment placement window when loading equipment onto a tray: move the equipment around, pick its mounting position and mounting method, see where the screws go, with a live preview of it in the tray. Goes with a GUI overhaul of the equipment wizard. Brian wants to review a few options for simplifying "add equipment" (to the library and onto a tray) before anything is built. Fit/retention stay UNKNOWN. Brian chose Option 1 on 2026-10-19 (short library wizard + separate "Place on tray" window; mockups in work/equipment-wizard-options/Options.html). Not built yet. Plan: 1 SCAD placement settings, 2 per-slot placement data, 3 shorter wizard, 4 Place on tray window, 5 rendering quality slider (Brian 2026-10-19: "place a quality slider bar for the rendering"; Brian chose both: the 3D preview and the STL $fn/$fa/$fs; STL default must stay today's $fn=48 output).

- 2026-10-19 — Equipment library pulls from an existing online library. Simplest start: import an offline snapshot of the NetBox device-type library (U height, depth, ports; confirm its license) as a "pick a starting point" that pre-fills the wizard for review. Width/3D models mostly missing, so those stay UNKNOWN. Live search or manufacturer CAD (GrabCAD, TraceParts) is bigger: per-file licenses, sign-ins, network/offline handling. Imports stay local, credited, never in STLs or redistributed; library dimensions are not verified fit.

- 2026-10-19 — Move the whole project to the cloud (one home for code, data and settings). Brian switches devices, two accounts and sometimes another AI, and forgets permissions/settings on each; things get jumbled. Needs a plan first: what goes where (Git repo vs. untracked outputs/work/data, which aren't in Git), keeping creator meshes private (never redistributed), backups, and how each device/account/AI connects. Nothing moves or uploads without Brian's go-ahead.

- 2026-10-19 — Paint themes on the rack frame and export the frame STLs: patterns like camo variants, color schemes, etc. Same themes/customizations on faceplates, all flowing together as one look. First find out what's needed (pattern → per-filament-color STLs like Print in color, or relief), how it fits PRINT THE RACK, and the one-theme-for-everything data model. Today only the Pi 4 faceplate has Print in color; extending it needs Brian's direction. Printed result UNKNOWN.

- 2026-10-20 — Viewer controls done (task 22, Bambu-style, viewer-controls.js). Left over: the remaining clipping in the canvas painter (sorted triangles, no depth buffer), only if it can be fixed without slowing drawing; and the mesh viewer's copied renderer code in viewer.js could become a camera hook in assembly-studio.js.

- 2026-10-20 — When adjusting equipment: (1) pick which face of the 3D model faces the front of the rack (click a face, or choose front/back/left/right/top/bottom). (2) A dialog to draw faceplate cutouts by hand (e.g. rectangles/circles on a 2D faceplate view) for when the automatic cutouts aren't good enough. Manual cutouts should be able to add to or replace the auto ones. Fit stays UNKNOWN until printed.

- 2026-10-20 — Tackle 2026-10-21: while customizing faceplate cutouts, draw the faceplate semi-transparent with the equipment model visible behind it, so the user can clearly see which ports need cutouts. Preview only; the STL is unchanged.

- 2026-10-20 — Gene Simmons success moment: on a successful save/done, show the awkward "Lick It Up" face (Brian's screenshot) as a corner toast, or full screen for big wins, and have Gene randomly say a line each time. Demo and image in work/gene-success/ (geneSuccess(text, big)). Personal use only: the image is his likeness, so keep it out of anything shared.

- 2026-10-20 — Human-friendly pass (anti-slop): every now and then, go over the whole app and make sure it feels made by and for people, not generic AI output. Review copy, layout, defaults and flows with fresh eyes. Revisit after the heavier building work is done.

## After v1 — use the rack (brainstorm once the rack is built)

- 2026-10-19 — Run the app on the workshop laptop. Options, simplest first: remote access to the PC over the home network (one copy of the data), a portable folder with Python and OpenSCAD bundled, a single .exe, or a real installer. Packaging needs Brian's explicit go-ahead. Keep user data separate from the program. Creator meshes are personal-use only, so leave them out of anything shared.

- Wall-mount box wizard (like a small indoor fiber NID enclosure, built with the bracket-wizard tech, plus custom equipment from common parts). See work/notes/2026-10-22-feet-floor-and-wall-box-wizard.md
