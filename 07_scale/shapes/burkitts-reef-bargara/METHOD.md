# METHOD - Burkitts Reef, Bargara (plan shape trace)
Run 2026-10-10 (fresh agent, queue item 9). Container network blocked except package servers: all work from local files.

## 1. What is being traced, and the problem
Burkitts Reef is a natural basalt headland platform at the south end of Bargara Beach. In Feb 1997 Greg Redgard moved ~300 m3 of boulders on it with an excavator (card R1, R3, R4). Nothing was built, and no source gives a length, width, footprint, crest level or depth (card "Dimensions": not found; 07_scale/reefs/burkitts-reef-bargara.md; Wikipedia "not a structure in and of itself"). So the "reef" (the reshaped zone) has no defined limits. What can be traced is the visible rock platform that carries it.

## 2. Sources considered
| id | what | use |
|---|---|---|
| img1 (registry img-08) | Esri World Imagery, captured 2025-09-05, z19, 0.271 m/px, georeferenced by sidecar | primary trace |
| img2 (registry img-01) | Redgard petition sketch, 7/9/1980 | context: qualitative only (no scale, no north) |
| registry img-02..05 | construction photo, surf photos | context, no dimension readable |
| registry img-06, 07 | video frames of a different place (marine-park dive site) | rejected, not used |
| 07_scale/reefs/burkitts-reef-bargara.footprint.json | earlier Google Maps estimate 120 x 46 m, 2,480 m2 | not reproducible (no image saved); recorded as alternative only |
Not reachable (network): Esri Wayback dated frames, Navionics, Queensland historical aerials, tide tables (see HANDOFF "needs network").

## 3. Steps
1. Read the sidecar `burkitts_esri_2025-09-05_z19.png.geo.json`: bounds N -24.812875, S -24.817725, E 152.469772, W 152.464429; 1992 x 1992 px; capture date 2025-09-05. Metres per pixel recomputed from the bounds: (E-W) in radians x 6378137 x cos(lat -24.815) / 1992 = 0.2710 m/px (equals sidecar value).
2. Viewed the whole image once (1000 px copy): a dark rock platform runs from a rock ridge at the NW (beside the sandy beach), round the point, and south down the east side beyond the frame; surf breaks along its seaward edge; a pale sand patch inside; vegetation and road inland.
3. Two zoom crops with a 50 px grid in original pixel coordinates (tools/overlay.py zoom): (420,520)-(1420,1170) and (1000,1000)-(1800,1992). Read vertices (image pixel x,y):
   - seaward edge = outer edge of dark rock, set on the line of breaking water: (595,590) ridge tip, (640,665), (700,700), (760,675), (840,715), (940,740), (1040,765), (1130,790), (1180,850), (1230,920), (1290,970), (1350,1000), (1400,1050), (1450,1150), (1500,1250), (1540,1350), (1570,1450), (1590,1550), (1630,1650), (1650,1750), (1630,1850), (1610,1991);
   - south end = image frame (y=1991) from x=1610 to x=1430 (platform continues beyond: truncation, not a real edge);
   - landward edge going north: (1430,1991), (1420,1800), (1400,1650), (1380,1500), (1340,1380), (1280,1250), (1180,1140), (1100,1060) follow the rock/vegetation boundary; (900,1000), (700,1000), (600,990) follow the vegetation / road-side edge of the rock flat; then the rock/sand boundary on the beach side: (520,940), (480,860), (470,760), (520,690), (560,640), back to the ridge tip.
   The full list is in `scripts/pixel_polygon_v1.json`.
4. Rendered with overlay.py render, viewed, adjusted nothing further (edge sits within ~10 m of the breaker line).
5. `scripts/compute_shape.py`: pixel -> lat/lon (linear in Web Mercator y between the sidecar bounds, linear in longitude), -> UTM 56S (EPSG:32756, pyproj); local frame origin at the polygon centroid (+x east, +y north). Output `scripts/computed_v1.json`.
6. Results: area 31,485 m2 in UTM 56S (31,508 geodesic; 31,646 by pixel x 0.271^2: scale-factor difference 0.5%); bbox 321 m E-W x 377 m N-S; perimeter 1,133 m; centroid -24.81574, 152.46750. Edge trends: east-flank seaward edge ~160/340 deg true (seaward normal ~70 deg true, ENE); north-facing edge ~107 deg true.

## 4. Judgements
- Outline level: the platform's visible limit at image time (a rock awash or exposed edge; breaker line). Tide state at capture is unknown (no tide reading available for 2025-09-05), so the waterline edge could move by tens of metres with the tide; no correction applied.
- Frame: shoreline-aligned canonical frame is not meaningful (platform wraps a curved headland), so N-up metres are used and this is stated in shape.json.
- Distance offshore 0 m (attached headland; card, R1, R2, R10).
- The 1980 sketch matches in kind: a boulder mass at the point, linear rock rows at the beach side (= dark ridges in the NW of the frame), surf over the northern side. It gives no metres.
- Gemini (80 x 40 m, uncited; dead URL + homepages) not used.

## 5. Confidence: LOW
Reasons in shape.json: reshaped zone undefined; one image; polygon truncated; waterline edge tide-dependent.

## 6. What would raise it
Dated low-tide imagery (Wayback / Queensland aerials 1997-98 before/after), a Navionics or LiDAR read, a local description of which boulders were moved (Redgard, ABC photo gallery, Bargara Boardriders), a larger frame south.
