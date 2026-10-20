# Pi 4 fit inspection

The detailed Pi STEP is positioned on the revised tray in the temporary Bambu Studio review. No further tray or faceplate geometry was changed and nothing was printed. This review is not a print-ready project.

| Check | Result |
|---|---|
| Pi mounting holes | Four 2.7 mm bores match the tray's 58 x 49 mm pitch. |
| PCB seat | PCB underside at Z=16 mm, touching the four standoff tops as intended. PCB envelope X=-44..41, Y=13..69 mm. |
| Alignment tongues | Two tongues sit in matching pockets; nominal side and vertical clearance is 0.15 mm per side; tip clearance 0.2 mm. |
| Joint screw bores | Coaxial along Y at X=+/-40, Z=21 mm. Ear bores 3.4 mm; boss pilots 4.2 mm. Boss-to-ear gap 0.3 mm. |
| Squareness | Tray floor and faceplate are perpendicular in the source geometry, seated at the intended contact plane. Physical printed squareness remains untested. |
| Detailed component clearance | FAIL: one USB connector metal feature intersects the inner right gusset centered at X=34 mm near Y=15, Z=14.16 mm. |

The USB interference was first detected at 11 Pi mesh vertices. Maximum sampled vertical penetration is 0.0468 mm. A separate OpenSCAD solid intersection of that connected USB mesh and the gusset produced a nonempty, simple 3D solid, confirming that this is more than a visual overlap. The exact maximum penetration may differ slightly between mesh triangles.

The nominal PCB-only check passed earlier because it excluded components beneath the PCB. This detailed STEP check supersedes any interpretation that the previous tray was fully cleared for the complete Pi.

No penetrating Pi vertices were detected in the screw ears, socket rails, or PCB standoff solids. This vertex screen is not an exhaustive whole-model clearance certification. The tray floor is at Z=10 mm and the lowest Pi model point is at Z=13.900 mm. Cables, heatsinks, real screw heads, insert engagement, rack engagement, assembly insertion path and printing tolerances remain unverified.

Suggested next change, requiring approval: lower the gusset crest by 1 mm and repeat the detailed fit check, targeting a useful clearance instead of barely removing the overlap. No such change has been made.

## Reference review file

`Pi4_fit_review_REFERENCE_ONLY.3mf` contains the faceplate, unchanged revised tray, and a tessellated Pi reference at their assembly coordinates. It contains no printer configuration. Bambu loads geometry only and may report non-manifold edges in the detailed Pi model; do not repair or print this reference assembly. The separate tray and faceplate exports remain the manufacturing candidates, subject to the unresolved clash above.

Alignment of the Bambu-exported STEP mesh: X'=X-44, Y'=69-Z, Z'=Y+13.9000091553 mm. This is a rigid 90 degree rotation about X plus translation; the PCB is 85 x 56 x 1.6 mm. All four measured hole rings have radius 1.35 mm at source X=3.5/61.5 and Z=3.5/52.5 mm.
