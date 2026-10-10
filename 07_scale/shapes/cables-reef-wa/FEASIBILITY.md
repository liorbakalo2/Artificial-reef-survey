# FEASIBILITY - 3D model of cables-reef-wa (2026-10-10): NOT BUILT, inputs too weak or missing

Rule used (brief model_3d.md step 1): build if plan (a), crest (b) and seabed (d) are sourced; c (height/slopes) and e (tides) may be estimated. Here a is only partly sourced, b and d are verbal ranges, and e has one number with an unstated datum. A model would be mostly invented values, so none was built.

| input | what we have | quality | what is missing |
|---|---|---|---|
| a. plan | traced design-plan outline, 123 x 91 m, 4,528 m2 (shape.json, confidence LOW) | scale assumed, +-25%; no survey or satellite | a georeferenced aerial / satellite image or survey to fix scale and the built extension |
| b. crest depth | Pattiaratchi 1999: design raises the bed 'up to the 1 m contour of the existing reef' by a 1:20 slope (datum not named); RWR: crest 1-3 m below the surface on average tides; 2009 review (Pitt): ~1.5 m below the lowest tide | three statements, three references; not reconcilable (1 m contour vs 1.5 m below lowest tide) | surveyed crest level and its datum (chart datum / AHD) |
| c. height, slopes | 1:20 shoreward slope (S1); hatched outer rock bands ~3 m wide in plan (img-05, scale assumed); 10,000 t granite, 3,500-5,000 m3 | estimated | cross-section with levels (img-10 / Fig 3 have no numbers), as-built volume |
| d. seabed | RWR 3-6 m water depth; S1: model to the 7 m contour, ~350 m from the shore; Pitt sketch contours 3.0-7.0 m below low water (labels partly illegible); Fig 7 contours unlabelled | one profile could be guessed, no measured bathymetry | Perth coastal bathymetry (WA Dept of Transport / Landgate LiDAR bathymetry, AusSeabed), or a Navionics SonarChart reading |
| e. tides | S1 wave-basin runs used 'mean tide level of 0.78 m above datum'; datum not named (probably Fremantle chart datum); the card says tidal range not found | one number | Fremantle LAT, MSL, HAT relative to AHD / chart datum (Transport WA / BoM tide tables) |

Conclusion: feasibility only. With any of these arriving the model becomes buildable in about one session using the Borth template (07_scale/shapes/borth-coastal-defence-reef/3d/): a georeferenced image (fixes a), a bathymetry grid (fixes d, and likely b), and the Fremantle datum table (e).
Lior can help with: Google Earth Pro (historical imagery with the reef visible: measure the V's length and width with the ruler, note the date) and the Navionics app (depth at the apex, at the arm ends, 100 m and 300 m offshore) - listed in REQUESTS_FOR_LIOR.md.
