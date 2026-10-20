# Keystone v4 "golden, tightened" coupon — 2026-10-19

LOCAL / PERSONAL USE ONLY — keystone geometry from Goul's "10 inch shelf TP-Link SG108 Plus Keystone" (BY-NC-SA). Never redistribute. See outputs/Mechanical_Design_App/THIRD_PARTY_LOCAL_ONLY.md.

Why: Brian printed v3 (exact SG108 copy): left/right fit very well, but ~0.4 mm play up/down.
Change: `ks_tight=0.4` in equipment_tray.scad moves the bottom (hook-side) edge of the opening, its hook groove and lip up 0.4 mm. Opening is now 14.8 × 16.2 (was 16.6). Latch side, width and side walls unchanged. Verified in the STL: bottom edge 12.7 → 13.1, top edge 29.3 unchanged.

Check: jack goes in latch-up, clicks, no up/down play, and still releases. If it is now too tight, try ks_tight=0.3. Fit UNKNOWN until printed; result applies only to this printer/material.
