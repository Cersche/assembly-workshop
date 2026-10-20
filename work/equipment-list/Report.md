# Equipment section cleanup — 2026-10-19

Brian approved the 6-step plan. UI text only; no data, geometry, export or render change.

- Originals before edit: originals/workspace.js (SHA-256 257E89B9…292D) and originals/equipment-wizard.js (BD3CBDA6…15C7). Restore by copying them back to outputs/Mechanical_Design_App/.
- workspace.js:19 — removed the stale "More equipment / Additional geometry adapters are not yet supported" box (superseded by C2).
- equipment-wizard.js loadLibrary() — "MY EQUIPMENT" heading always shown; empty state ("No custom equipment yet … Fit UNKNOWN"); load-failure message instead of a silent empty list; each saved item shows its status (PROPOSED — UNVALIDATED) · Fit UNKNOWN.
- Not migrated: the cached render "T" in the preserved app-local data folder (never saved to a library).

Verified: both files parse (browser `new Function`); browser-pane reload against normal 8765 server shows the new empty state. Not exercised: item status line and load-failure state (no library items exist; no failure was induced). Pre-existing console 404 for /rack-references/assembly-studio.js is unrelated and was present before the edit. No server restart; Brian's own tab picks this up only on his refresh.
