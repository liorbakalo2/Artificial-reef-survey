# Requests for Lior - Narrowneck 3D (2026-10-10)

| tool | exact lat/lon (WGS84, decimal) or place | what to read | datum / units to note | why it matters |
|---|---|---|---|---|
| Navionics app | -27.9866, 153.4341 (south arm, obstruction symbol) | the "0.9" label: full text, units, and the depth datum the app states | metres/feet, datum | tells whether 0.9 is an old crest state (2001-2012, 1 m below LAT) or a current spot depth; not used in the model |
| Navionics app (SonarChart) | transect from the beach to the reef: -27.98677, 153.431634 (y 50 m); -27.98674, 153.432141 (y 100 m); -27.986711, 153.432648 (y 150 m); -27.986681, 153.433156 (y 200 m) | depth at each point and the contour interval | LAT assumed; note the stated datum | the nearshore bed (0-190 m offshore) is an assumption in the model |
| Google Earth Pro | same four points + the reef: -27.9864, 153.4339 | ruler distance from the waterline to the reef; historical imagery date of low-tide shots (sandbar or trough visible?) | metres, image date | checks the 2020 waterline (y = 0) and the surf-zone bar |
| City of Gold Coast (e-mail, by Lior) | Narrowneck Reef Renewal 2017-18 | (a) the vertical offset AHD to LAT used in the 2018 multibeam (0.760 MSQ vs 1.00 in the papers); (b) the post-renewal as-built plan or multibeam grid | m | closes the 0.24 m crest datum question and gives the real footprint (D7) |

Decision D7 (default outline photo vs Option 2): recommendation = keep the photo (see HANDOFF.md).
