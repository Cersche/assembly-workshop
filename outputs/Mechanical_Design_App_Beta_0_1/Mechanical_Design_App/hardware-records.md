# Hardware JSON records

Import a JSON array. Each entry needs `id` (stable text), positive integer `revision`, `name`, `kind` (`screw` or `heatset`), `diameter`, `pitch`, `source` and `verification` (`custom`, `partial`, `documented`). Dimensions are millimeters. Numeric dimensions must be finite and positive; omitted optional dimensions remain unknown. Documented records require `part_number`; documentation status is a user assertion.

Use exact manufacturer part numbers and source documents. Additional metadata such as manufacturer, material, finish, asset URLs, retrieval dates and licenses is preserved with the record but not independently verified. This release stores metadata, not CAD assets.

Screw rule fields: `length`, `length_convention` (`under_head` for this version), `threaded_length`. Optional inspection fields include `head_diameter`, `head_height`, `drive`, `material` and `finish`.

Insert rule fields: `length`, `outside_diameter`, `hole_diameter`, `hole_profile` (`straight` for this version), `usable_depth`, `min_wall`, `end_type` (`open` or `closed`). `hole_diameter` and `min_wall` must refer to the documented installation recommendation, not be inferred from nominal thread diameter. Tapered/stepped holes remain unsupported in the initial rules.

Project stack means the distance from the screw's under-head bearing surface to the insert entrance, including gaps and washers. Pocket means the depth available for the insert body. For the Pi4 baseline, the stack is provisionally 3.3 mm and the pocket 8 mm; verify real hardware and seating. Minimum engagement and bottom clearance are user targets, not universal fastening standards.
