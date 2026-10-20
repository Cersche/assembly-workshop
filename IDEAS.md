# Ideas parking lot

Write any idea here the moment it comes up, one line with the date. Don't judge it, then get back to work. Once a week, sort each one: move to ROADMAP.md, keep, or cross out (~~like this~~, don't delete).

## Inbox

- 2026-10-19 — Equipment placement window when loading equipment onto a tray: move the equipment around, pick its mounting position and mounting method, see where the screws go, with a live preview of it in the tray. Goes with a GUI overhaul of the equipment wizard. Brian wants to review a few options for simplifying "add equipment" (to the library and onto a tray) before anything is built. Fit/retention stay UNKNOWN. Brian chose Option 1 on 2026-10-19 (short library wizard + separate "Place on tray" window; mockups in work/equipment-wizard-options/Options.html). Not built yet. Plan: 1 SCAD placement settings, 2 per-slot placement data, 3 shorter wizard, 4 Place on tray window, 5 rendering quality slider (Brian 2026-10-19: "place a quality slider bar for the rendering"; Brian chose both: the 3D preview and the STL $fn/$fa/$fs; STL default must stay today's $fn=48 output).

- 2026-10-19 — Equipment library pulls from an existing online library. Simplest start: import an offline snapshot of the NetBox device-type library (U height, depth, ports; confirm its license) as a "pick a starting point" that pre-fills the wizard for review. Width/3D models mostly missing, so those stay UNKNOWN. Live search or manufacturer CAD (GrabCAD, TraceParts) is bigger: per-file licenses, sign-ins, network/offline handling. Imports stay local, credited, never in STLs or redistributed; library dimensions are not verified fit.

- 2026-10-19 — Move the whole project to the cloud (one home for code, data and settings). Brian switches devices, two accounts and sometimes another AI, and forgets permissions/settings on each; things get jumbled. Needs a plan first: what goes where (Git repo vs. untracked outputs/work/data, which aren't in Git), keeping creator meshes private (never redistributed), backups, and how each device/account/AI connects. Nothing moves or uploads without Brian's go-ahead.

- 2026-10-19 — Paint themes on the rack frame and export the frame STLs: patterns like camo variants, color schemes, etc. Same themes/customizations on faceplates, all flowing together as one look. First find out what's needed (pattern → per-filament-color STLs like Print in color, or relief), how it fits PRINT THE RACK, and the one-theme-for-everything data model. Today only the Pi 4 faceplate has Print in color; extending it needs Brian's direction. Printed result UNKNOWN.

## After v1 — use the rack (brainstorm once the rack is built)

- 2026-10-19 — Run the app on the workshop laptop. Options, simplest first: remote access to the PC over the home network (one copy of the data), a portable folder with Python and OpenSCAD bundled, a single .exe, or a real installer. Packaging needs Brian's explicit go-ahead. Keep user data separate from the program. Creator meshes are personal-use only, so leave them out of anything shared.
