# METHODS_3D - Southern Ocean Surf Reef ("Midds Reef"), Middleton Beach, Albany WA

Written 2026-10-10 (3D agent, fresh run with network access). Model files: `model.js`, `docs.js`, `index.html`; regenerate with `python -I build_3d.py`. Source register, numbered assumptions and decisions: `REGISTER_3D.md` (also in the viewer, Methods tab). Run log: `SOURCES_3D.md`.

## 1. Summary
The model shows the rock reef as built in March 2025 (18 rocks moved in March 2026 are a note only). The **plan** (toe outline) is the Bluecoast final-design outer contour, 13,104 m2, positioned on the satellite image; the toggle is the dark rock patch visible on the Esri image of 2026-01-20, 10,918 m2. The **crest** levels are the City of Albany design values (-1.0 m AHD shallowest, 110 m of crest at -2 m AHD). The **seabed** is a single shore-normal profile read from contour lines of a 2015 Royal HaskoningDHV design plan (depth datum not stated, taken as AHD), so the pile height (up to 6.0 m, mean 2.6 m over the design footprint) is only known to about +-1 m. The reef surface is a loft between a crest ridge and the toe outline; its fullness (exponent N = 2.73) is **fitted** so that the design outline holds the stated 34,000 m3, so that volume is not a check. **3D confidence: LOW** (plan high, crest medium-low, seabed low, tides low-medium).

## 2. Data sources
Full list with "how used": `REGISTER_3D.md` section 1 (S1-S14). Short form:
- Esri World Imagery 2026-01-20, 2025-01-16 and 2022-12-19 (Wayback release 13192 / 6543): plan, frame, shoreline, georeferencing base. No other capture exists between 2025-01-16 and 2026-01-20 (19 Wayback releases tested: all repeat one of these three images), so there is no construction-sequence image.
- Bluecoast design plan (via Raised Water Research) and City of Albany design table: toe outline; crest -1.0 m AHD; 110 m at -2 m AHD; 34,000 m3 on 2017 bathymetry; 62,800 t.
- Royal HaskoningDHV (2015) Option B plan with depth contours, as reproduced by Raised Water Research (registry img-16): seabed.
- BMT (2018) Environmental Impact Assessment, Fig 6.9 (img-14): spot soundings in m CD, cross-check; text: tidal range, surge.
- WA Department of Transport / Bureau of Meteorology 2024 Albany tide predictions: LAT and mean level.
- City of Albany executive summary of the Detailed Design Report (2020), FAQs (2023), project profile (2024), 2015 feasibility executive summary, project page: dimensions, concept history; none gives the seabed depth.

## 3. Methods
### 3.1 Frame and datum
Canonical frame of `shape.json`: origin = foot of the perpendicular from the reef centroid onto the beach-face line (-35.0172584, 117.919428); +x alongshore toward NNE (bearing 30.26 deg true), +y offshore toward ESE (120.26 deg); z up, **z = 0 at AHD, taken as MSL (A2)**. LAT is at z = -0.74 m: the mean of the 1,043 predicted high and low waters of 2024 (WA DoT/BoM, datum LAT) is 0.742 m above LAT (`scripts/tides_from_dot.py`, `src/tides_derived.json`), and AHD is assumed equal to MSL. Equations: depth below LAT = -z + 0.74; z_AHD(bed) = -(depth below CD) - 0.74 if the chart datum is LAT. MLLW = -0.26 and MHHW = +0.34 m AHD are the City's own statement ("crest -1.0 m AHD is 0.74 m below MLLW and 1.34 m below MHHW"). The slider top is the highest predicted tide of 2024 (+0.66 m AHD); true HAT was not found.

### 3.2 Seabed
1. The RHDHV Option B plan (`src/rwr_images/..._plan_2015.jpg`, 609 x 354 px, a Google Earth view with coloured depth contours -0.5 ... -8 m) was georeferenced onto an Esri 2025-01-16 mosaic (`3d/src/esri_wayback13192_2025-01-16_z18_wide1200m.png`, 0.489 m/px) with 4 control points (the Surfers car park, two dune tracks, the caravan-park buildings): similarity transform, scale 2.56 m per plan pixel, rotation 0.1 deg, residuals 6.6-12.4 px of the Esri image (3.2-6.1 m) (`scripts/geo.py`). A check: the beach-face line and the Bluecoast outline fall where they should on this plan (annotated A1).
2. Along 8 shore-normal transects (x = -160 ... 0, 20 m apart) the image was sampled every 0.25 m; contour lines were detected as colour peaks against the local median water colour and assigned to depth levels by colour (hue) in order from the black -1 m line (`scripts/prof.py`, `scripts/read_contours.py`, raw crossings in `src/levels2_raw.json`). The level colours were taken from the plan legend. Transects at x > 0 were not used because they run into the contours of the Option B structure drawn on that plan.
3. Medians over the transects give the profile nodes (y from the beach-face line): -1 m at 36, -1.5 at 50, -2 at 64, -2.5 at 75, -3 at 88, -3.5 at 98, -4 at 105 m (n >= 5 transects); -4.5, -5, -6, -7 m at 118, 126, 150, 178 m (n = 2-8; set by eye from the colour sequence, +-10 m). Spacing between lines varies along the shore by about +-20 %.
4. Beyond the nodes: +1.0 m at y = -30 and +2.0 at -60 (beach, ASSUMED A5), -0.5 m at y = 7 (the -0.5 contour), -7.5 at 250, -8.0 at 330, -8.3 at 420 m (the -8 contour of the plan; BMT sounding 8.4 m CD at y = 315 agrees). The profile is **linear interpolated and alongshore uniform** (A4): the seabed grid is 5 m, x -260 ... 260, y -60 ... 420.
5. Not used: the BMT 5 m line and spot soundings near the shore (see 4), EIA appendix Fig 29 (regional model bathymetry in 1 m colour bins, about 10 m pixels, registered img-15 for the record).

### 3.3 Reef surface
1. Toe polygon = the outline of the version (shape.json). The toe sits on the seabed.
2. Crest ridge = the polyline of the first 8 (design) or 6 (satellite) outline vertices along the steep shoreward (+x) edge, offset 9 m into the footprint (A6). Ridge level z_c: -1.0 m AHD over the first 15 m from the offshore (east) end, a linear rise to -2.0 m at 40 m, -2.0 m beyond (A7: the City gives -1.0 m "shallowest" and "110 m at -2 m" but not where).
3. Surface for each 1 m cell inside the outline: z = z_c + (z_b - z_c) * (d_c / (d_c + d_t))^N, with d_c the distance to the ridge, d_t the distance to the toe, z_b the seabed (lofting between crest and toe; no side-slope rule is given by any source, A8); a toe-slope limit (height above the bed <= 0.5 x distance to the toe line, i.e. no slope steeper than 1:2, A8), then a 1.2 m Gaussian smoothing inside the outline.
4. N is found by bisection so that the design outline holds 34,000 m3 (A9): **N = 2.73**. The satellite version uses the same N, ridge rule and seabed, so its volume (30,273 m3) is a result.
5. Resulting slopes: median 1:16, 90th percentile 1:4.5, steepest 1:2.0 (the limit). The design text says "mild seaward slopes and a broad 3D shape"; the design plan shows dense contours along the shoreward edge and wide spacing toward the SW.
6. Rock mass = volume x 1.847 t/m3 (62,800 t / 34,000 m3, A10).

## 4. Validation
| check | result |
|---|---|
| Volume implied by the loft with N = 1 (no fit) | 20,826 m3 = 61 % of the stated 34,000 m3. A fuller body (N = 2.73) or a deeper seabed (+1.5 m) is needed; the shortfall cannot be assigned to either (evidence: none). |
| Mean pile height over the design footprint | 2.59 m (stated volume / area gives 2.6 m, as it is fitted). Maximum 6.0 m near the offshore end. |
| Crest > -2 m AHD | model area 860 m2 (a ridge about 100-110 m long and 9 m wide), consistent with "crest length 110 m at -2 m AHD". |
| Seabed under the outline | -2.1 m at the shoreward apex (y = 67) to -7.4 m at the offshore toe (y = 234). Sat-version outline: -2.3 ... -7.3 m. |
| Water colour (Esri 2025-01-16, red channel along y at x = -160, -120, -80) | red falls from about 200 at y = 20 m to 115 at y = 60-70 m, then slowly to 95 by 100-120 m and stays flat beyond: bed visible to about 4-5 m, consistent with the contour profile (-3 m at 88 m, -5 m at 126 m), not with a 5 m depth at 40-50 m. Qualitative only. |
| BMT 2018 Fig 6.9 sounding 8.4 m CD at (188, 315) | profile -8.0 m AHD at y = 315: agrees within 0.4 m (CD = AHD) or 0.3 m (CD = LAT). |
| BMT 2018 sounding 2.7 m CD at (-53, 32) | profile gives -1.1 m AHD: **the sounding is 1.6 m (CD = AHD) or 2.3 m (CD = LAT) deeper. UNRESOLVED.** The BMT figure also draws a thin 5 m line along the inshore edge of its development area; by our georeferencing (position read by eye) it lies about 40-70 m from the beach-face line, where the RHDHV contours give -1.5 to -2.5 m. Possible causes: different survey dates (2015 vs 2018, the beach bar moves), label offsets (+-11 m), a different datum. If the BMT values are right the seabed near the shoreward apex is 2-3 m deeper and the pile there 2-3 m higher. |

## 5. Uncertainty
Height of pile above bed h = z_c - z_b: u(h) = sqrt(u_c^2 + u_b^2) with u_c about 0.3 m (design tolerance, not stated) and u_b about 1 m (profile +-0.25 m for position, +-0.74 m datum, up to 2 m near the apex if BMT is right): u(h) about 1.0 m, rising to 2+ m at the shoreward apex. Volume: +-1 m bed = +7.7k / -7.9k m3 (+-23 %) on the design outline (+6.2k / -6.5k on the satellite one); CD = LAT instead of AHD = +5.7k m3; crest all at -1.0 m = +6.4k, all at -2.0 m = -1.4k; ridge offset 5 or 14 m = -1.2k / +1.2k (all with N fixed). Vertical exaggeration (x1 ... x5) changes only the displayed heights; plan and the water level are true.

## 6. Confidence
| element | level | reason |
|---|---|---|
| plan | high | traced and verified on the satellite image; design outline scaled by its bar (shape.json) |
| crest level | medium-low | City design values, no as-built survey; which end is shallowest is assumed |
| seabed | low | a 2015 design contour plot of unstated datum, georeferenced by hand (+-5 m), conflicting with a 2018 sounding by 1.6 m near the shore, 2017 City bathymetry not found |
| pile height, slopes | low | follow from the seabed and from an assumed loft; no section drawing or survey |
| volume | medium-low | design outline fitted to the City figure (not independent); satellite outline volume (30,273 m3) is a result of the same rules |
| tides | low-medium | LAT from 2024 predictions and AHD = MSL; MLLW/MHHW from the City statement |
| **overall** | **LOW** | |

## 7. Limitations and what would resolve them
- No as-built or bathymetric survey, no section drawing: the Bluecoast Detailed Design Report (full, with the 2017 bathymetry) and the practical-completion survey (March 2025) would fix seabed, heights and slopes. Not on the City website (only the executive summary, 5 pages). Lior: request from the City of Albany (e-mail not sent by us).
- Navionics / Garmin Marine Maps did not render in headless Chrome (no map tiles; no login or CAPTCHA was involved, nothing bypassed). Lior can read depths at the points in `REQUESTS_FOR_LIOR.md`; they would test the profile and the datum.
- AusSeabed / Geoscience Australia services returned 403 to this environment.
- The 2015 contours predate construction by 10 years; sand-bar movement of 1-2 m is plausible.
- Rock grading (belly/core/armour) and the real armour slopes are not modelled.

## 8. References
Full citations, author-year, with locations: `REGISTER_3D.md` section 1. Key: BMT Western Australia (2018); Bluecoast / City of Albany (2020, 2023, 2024); Royal HaskoningDHV (2015); WA Department of Transport and Bureau of Meteorology (2024); Esri (2022, 2025, 2026).
