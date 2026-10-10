# HANDOFF - southern-ocean-surf-reef-albany (network run + 3D build, fresh agent, 2026-10-10; for main and any later agent)

## 1. Status per stage
- Registry: 28 rows (img-14 ... 28 added 2026-10-10); check_registry.py PASSED. Pending 3D checks left: img-01, img-07 (weak camera-match items).
- Trace: done 2026-10-10, confidence HIGH (position, size, orientation; area -30 %/+20 % by edge definition). shape.json status "verified" (one agent traced and verified; an independent look would help).
- 3D: BUILT 2026-10-10, confidence LOW (plan high, crest medium-low, seabed low, pile height/slopes low, volume medium-low because fitted, tides low-medium). Folder `3d/`. Viewer checked in headless Chrome over http (no JS error; plan, oblique, methods panel, version pop-up previews).
- Page: nothing done in 04_build (main's job): paste `3d/PAGE_TEXTS_FOR_MAIN.json` into data/models3d_combined / curated / caveats, remove the slug from data/models3d_hold.json, run update_page.py. Viewer imports three.js from a CDN import map (as the Borth template); the page build swaps it for the vendored bundle.
- Network fetches done: City of Albany pages/documents, EPA WA referral (BMT 2018 EIA), Raised Water Research gallery, DoT/BoM tide predictions, Esri Wayback (19 releases). Navionics: viewer did not render (not bypassed). AusSeabed/GA: 403 (not bypassed).

## 2. Key decisions and why (full list D1-D10 in 3d/REGISTER_3D.md)
- Default outline = Bluecoast final-design outermost contour (13,104 m2); toggle = visible reef on Esri 2026-01-20 (10,918 m2). Unchanged from the shape run.
- Seabed from the RHDHV 2015 contours (read as AHD), not from BMT soundings (sparse, near-shore value conflicts). Model zero = AHD (about MSL); LAT derived = -0.74 m.
- Built despite the weak seabed (rule: plan, crest, seabed sourced); confidence LOW with the reason on the page.
- Reef surface = loft between a crest ridge (9 m inside the shoreward edge; -1.0 m AHD over the first 15 m from the offshore end, -2.0 m beyond 40 m) and the toe; exponent N = 2.73 FITTED to the stated 34,000 m3; toe slope capped at 1:2.
- Frame: +x NNE (30.26 deg true), +y offshore ESE (120.26 deg), z up, 0 = AHD.

## 3. Key numbers (units, datum, source id; sources S1-S14 = 3d/REGISTER_3D.md)
| item | value | source |
|---|---|---|
| crest | -1.0 m AHD shallowest; -2.0 m AHD over 110 m; 0.74 m below MLLW, 1.34 m below MHHW | S5, S6 (City table, project page) |
| MLLW / MHHW | -0.26 / +0.34 m AHD | S6 (derived from the crest statement) |
| LAT | -0.74 m AHD (2024 predicted extremes mean 0.742 m above LAT; AHD = MSL assumed) | S13 |
| highest predicted tide 2024 | +0.66 m AHD (1.40 m above LAT); HAT not found | S13 |
| tidal range | spring 0.9 m, neap 0.3 m; surge +0.4-1.0 m | S12 (EIA s.5) |
| seabed profile (m AHD at y m from beach-face line) | -0.5 @7, -1 @36, -1.5 @50, -2 @64, -2.5 @75, -3 @88, -3.5 @98, -4 @105, -4.5 @118, -5 @126, -6 @150, -7 @178, -7.5 @250, -8 @330 | S11 (RHDHV 2015 plan, read by colour, +-5 m position) |
| seabed under footprint | -2.1 m (apex, y 67) to -7.4 m (offshore toe, y 234) | profile |
| volume design outline | 34,000 m3 (fitted); unfitted loft 20,826 m3; mean height 2.59 m; max 6.0 m | S5; build_metrics.json |
| volume satellite outline | 30,273 m3 (result) | build_metrics.json |
| volume sensitivity (design) | bed +1 m deeper +7.7k / shallower -7.9k m3; CD = LAT +5.7k; crest all -1.0 m +6.4k, all -2.0 m -1.4k | build_metrics.json |
| rock | 62,800 t, layers belly D50 0.16 m 18 %, core 0.49 m 36 %, armour 0.94 m 46 %; 1.847 t/m3 | S6 |
| BMT soundings (m CD) | 8.4 at (188, 315) agrees (-8.0 AHD); 2.7 at (-53, 32) is 1.6 m deeper than the profile (-1.1): UNRESOLVED | S12, A3 figure |
Earlier numbers of the shape run (area 13,104 / 10,918 m2, crest bearing 278 / 281 deg, 165 m along crest) are unchanged (shape.json).

## 4. File map (07_scale/shapes/southern-ocean-surf-reef-albany/)
- shape.json, METHOD.md, VERIFY.md, sources.md, FEASIBILITY.md (updated 2026-10-10), SOURCE_AUDIT_2026-10-10.md, overlays/, scripts/ (shape scripts, as before).
- src/: shape-run images (Esri tiles, design.jpg, Bluecoast diagram) + NEW: city_docs/ (City PDFs and project page html), epa/ (BMT 2018 EIA 6.4 MB, referral form, determination, advice, Fig 6.9 raster and render, Fig 29 render), rwr_images/ (RHDHV 2015 plan and oblique, renders, video stills), tides/ (DoT/BoM 2024 predictions PDF 1.9 MB, DoT Albany tide page), esri_wayback6543_2022-12-19_z18.png.
- 3d/index.html (viewer), model.js (data; 322 kB), docs.js (METHODS/REGISTER/SOURCES as the viewer panels), METHODS_3D.md, REGISTER_3D.md (sources with how-used, assumptions A1-A12, decisions D1-D10), SOURCES_3D.md (run log), REQUESTS_FOR_LIOR.md, PAGE_TEXTS_FOR_MAIN.json, build_3d.py (regenerates model.js + docs.js + src/build_metrics.json), annotated/A1-A3, preview_*.png.
- 3d/scripts/: geo.py (georeference + frame), prof.py + read_contours.py (contour crossings), tides_from_dot.py, make_annotations.py, make_viewer_from_borth.py (re-creates index.html from the Borth viewer), preview.py, register_images_3d.py (run once; done). 3d/src/: levels2_raw.json, tides_derived.json, provenance.json, confidence.json, build_metrics.json, Esri 1200 m mosaic (9 MB, bulky).
- Not worth opening: src/epa/*.pdf (160-page EIA; only p. 42 and appendix p. 140 matter), src/tides PDF.

## 5. Open issues, discrepancies, pending checks
- Seabed: 2015 RHDHV contours (unstated datum) vs BMT 2018 near-shore sounding: 1.6 m. Resolve with Navionics readings (Lior), the full Bluecoast report / 2017 bathymetry, or the March 2025 as-built survey (e-mail E9 in root REQUESTS).
- Volume of the design outline is fitted (A9); the unfitted loft gives 61 % of the City volume (fuller pile or deeper bed; evidence cannot separate them).
- Which end of the crest is shallowest (A7) and the ridge position (A6): from a design plan, no section.
- Wayback: only 2022-12-19, 2025-01-16, 2026-01-20 exist; the soft offshore edge of the visible patch cannot be re-checked with a second finished-reef image. Google Earth Pro history (Lior) might have more.
- The City FAQ (2023) gives an earlier footprint of about 16,000 m2 and 145 m offshore; the final table gives 140 m (shape decision). Card R15 already records this.
- Dead ends logged in 02_research/dead_ends/southern-ocean-surf-reef-albany.json (11 entries by this run; the file also holds entries written by another agent, check for overlap).
- If kovalam build_shape_json.py is re-run it overwrites the audit additions in shape.json: re-apply from the audit.
- The reef card (02_research/reefs/southern-ocean-surf-reef-albany.*) was not edited; main may add references S11-S13 (RHDHV 2015 plan via RWR, BMT 2018 EIA Fig 6.9 p. 32, DoT/BoM tides 2024).

## 6. Next steps for the next agent, in order
1. Main: paste PAGE_TEXTS_FOR_MAIN.json entries, remove the slug from models3d_hold.json, run update_page.py, view the Albany model on the page.
2. Lior: Navionics readings and the City e-mail (3d/REQUESTS_FOR_LIOR.md); then edit `PROFILE` in build_3d.py (and the A3 text), rerun build_3d.py, make_annotations.py, preview.py, update METHODS_3D 4 and REGISTER_3D A3/A4.
3. If an as-built survey or cross-sections arrive: replace the loft by the surveyed surface, add it as a third outline version (default), drop the fit (A9).
4. Optional: digitise EIA appendix Fig 29 (img-15, 1 m colour bins, 2016 survey) to cross-check the -3 ... -6 m bands.

## 7. CHECKPOINT 2026-10-10 (final for this run)
Fetched, built, documented, registered; nothing half-done. Not touched: 04_build, other reefs, papers/. STATUS and REQUESTS appended. No HANDOFF_STOP.
