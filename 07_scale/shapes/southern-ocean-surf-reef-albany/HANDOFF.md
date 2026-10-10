# HANDOFF - southern-ocean-surf-reef-albany (queue item 9, fresh agent, 2026-10-10; for main and any later agent)

## 1. Status per stage
- Registry check: done 2026-10-10 (13 rows; img-03, 05, 10, 11, 12, 13 results written; pending 3D checks left: img-01, img-07 = weak camera-match items).
- Trace: done 2026-10-10, confidence HIGH (position, size, orientation; area -30 %/+20 % by edge definition). shape.json status "verified".
- Verify: done 2026-10-10 by the same agent (recomputation + re-render, see VERIFY.md check 8); a second independent look would help.
- 3D: NOT built. FEASIBILITY.md written: seabed depth, pile height and slopes are not in any local source; Navionics/AusSeabed/City are blocked here.
- Page: nothing done in 04_build (main's job). Slug should go in `04_build/data/models3d_hold.json` ("Not yet modelled") until a model exists.
- No HANDOFF_STOP: the work that can be done offline is complete.

## 2. Key decisions and why
- Default outline = Bluecoast final-design outermost contour (design drawing of the built version beats a photo trace; no measured survey found); toggle = visible reef on Esri 2026-01-20.
- The final design is treated as the built reef: City page dimensions equal the design table; satellite wedge matches the plan (rotation -3 deg, IoU 0.84).
- Frame: +x alongshore NNE (30.3 deg true), +y offshore (120.3 deg); true unmirrored plan (+x turned 90 deg clockwise = +y), as Borth/geom.py.
- Shoreline = beach-face line (edge of bright dry sand), not the swash line (foam makes the swash line unmeasurable by threshold; true swash is about 10-15 m seaward).
- Dimension arrows (110 m, 140 m) on the design figure are NOT to the figure's scale bar: only the bar is used.
- State: as built (Mar 2025). 18 rocks moved March 2026 (card R11) = note only.

## 3. Key numbers (units, datum, source id)
### 3.1 Plan (canonical frame, metres)
| item | design_bluecoast (default) | sat_2026 | source |
|---|---|---|---|
| area | 13,104 m2 | 10,918 m2 (objective core mask 7,707 m2) | design_plan 1.52 px/m; sat2026 0.4891 m/px |
| x range / y range | -65.6..63.3 / 66.8..233.5 | -65.4..61.5 / 70.8..223.9 | shape.json |
| along / across the crest | 164.6 / 121.2 m | 157.2 / 116.7 m | analysis_out.json (crest bearing 278.1 / 281.5 deg) |
| centroid y | 160 m | 165 m | from the beach-face line |
| crest-edge bearing | 278.1 deg (design text 270-305 N) | 281.5 deg | |
| nearest edge to beach-face line | 66.8 m | 70.8 m (about 150 m to the vegetation edge) | text says 140 m from "landward toe" (reference undefined) |
Origin lat/lon (-35.017258, 117.919428); reef centroid (-35.018005, 117.920991). Shoreline bearing local 30.3 deg (CI 27.7-33.0); northern rows 16.7, whole beach 27.0.
### 3.2 Levels (AHD, design values)
Crest -1.0 m AHD shallowest (0.74 m below MLLW, 1.34 m below MHHW => MLLW -0.26, MHHW +0.34 m AHD); crest length 110 m at -2 m AHD (design table, img-10; card R3).
### 3.3 Tides
Mean range 0.4 m, spring range 1.1 m, King George Sound (card R5). Local only; no Haifa preset.
### 3.4 Other
62,800 t rock (belly D50 0.16 m 12,400 t 18 %; core 0.49 m 23,600 t 36 %; armour 0.94 m 26,800 t 46 %), about 34,000 m3 (design table; 62,800/1.85 t/m3 is an assumption). Volume over design outline = mean height 2.6 m (inference).
Registry correction: img-10 said volume 54,000 m3; the table reads 34,000 m3 (fixed in images.json and IMAGES.md). The card does not contain 54,000.

## 4. File map (07_scale/shapes/southern-ocean-surf-reef-albany/)
- shape.json: both outline versions (m + lat/lon), sources, angles, dimension checks, verification. Open for numbers.
- METHOD.md / sources.md / VERIFY.md: step log, source table, verification summary.
- FEASIBILITY.md: why no 3D, what is needed, Lior's reading table, needs-network list.
- overlays/: sat2026-01-20_trace.png, design_diagram_trace.png, canonical_versions_m.png, shoreline_fit.png, before_after_2025-01-16_vs_2026-01-20.png.
- src/: Esri 2026-01-20 and 2025-01-16 tiles (+ .geo.json), design.jpg, rwr_bluecoast_design_diagram.png (all registered in 03_images/reefs/southern-ocean-surf-reef-albany/).
- scripts/: trace_mask.py, build_shape.py (frame + metrics -> build_out.json), analysis.py, make_overlays.py, write_shape_json.py, register_images.py, polys_px.json (traced pixel polygons), mask30_px.json, request_points_latlon.json. Re-run order: build_shape, analysis, make_overlays, write_shape_json (then re-add verification block if status must stay "verified": write_shape_json resets status to "traced").

## 5. Open issues, discrepancies, pending checks
- No seabed/pile-height/slope source (blocks 3D). No measured as-built survey found (City, Bluecoast, WA DoT unknown).
- Design position comes from a satellite fit (the figure has no coordinates); a Bluecoast CAD/coordinates drawing would remove that.
- Offshore (east) edge of the visible patch is soft; second dated image (Wayback between 2025-01 and 2026-01) would help.
- "140 m from landward toe" reference undefined; dimension arrows on the figure inconsistent with its bar.
- Gemini sources unverifiable (no URLs; one anachronistic).
- Same agent traced and verified.
### Needs network (exact URLs/tiles and why)
1. https://www.albany.wa.gov.au/council/projects/completed-projects/southern-ocean-surf-reef-sosr.aspx (+ current-projects page): design report / as-built links; re-check design table.
2. https://www.albany.wa.gov.au/documents/803/albany-artificial-surf-reef-community-update-and-faqs: any depth values.
3. https://maps.garmin.com/en-US/marine/ (Navionics) at -35.0180, 117.9210, z18: SonarChart + Nautical: depth over/around reef (points in FEASIBILITY.md).
4. AusSeabed / Geoscience Australia marine portal (https://portal.ga.gov.au/persona/marine): King George Sound / Middleton Beach bathymetry or LiDAR.
5. Esri Wayback releases dated 2025-01-16..2026-01-20 (satellite.py wayback-list; fetch -35.018, 117.9207, r 250, z18): construction progress and a second finished-reef image.
6. EMODnet is irrelevant (Europe only).

## 6. Next steps (in order)
1. When network or Lior's readings arrive: read depth at the points in FEASIBILITY.md (or the Bluecoast report sections); then build 3d/ per _agent_briefs/model_3d.md using borth 3d/ as template (build_3d.py, model.js, docs.js, index.html, METHODS_3D.md, SOURCES_3D.md; versions design_bluecoast + sat_2026; tides AHD, MLLW -0.26, MHHW +0.34).
2. Search for an as-built survey (City, March 2025 practical completion) -> if found, add as a third outline version and make it the default.
3. Main: add slug to models3d_hold.json; shape appears in the Shapes tab from shape.json (default design_bluecoast, toggle sat_2026, versions_info present). Card note: length 165 m is along the crest (bearing about 280 deg), not alongshore.

## 7. CHECKPOINT 2026-10-10 (final for this run)
Traced, verified, registry updated, FEASIBILITY written, STATUS and REQUESTS appended. Nothing half-done. Not touched: 04_build, other reefs, papers.

## Source audit 2026-10-10
SOURCE_AUDIT_2026-10-10.md in this folder holds the sources-with-how-used, statement check, assumptions (A#), decisions (D#), confidence and consistency tables. FEASIBILITY.md / shape.json now carry the why / checked / assumed text (page_status for hidden reefs). Open mismatches are listed in the audit section 2. If kovalam build_shape_json.py is re-run it overwrites the audit additions in shape.json: re-apply from the audit.
