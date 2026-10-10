# HANDOFF - cables-reef-wa (imagery + bathymetry run 2026-10-10, network open; supersedes the first run's handoff, archived in 3d/archive/pre_imagery_2026-10-10/HANDOFF.md)

## 1. Status per stage
| stage | state | confidence and why |
|---|---|---|
| trace | done; shape.json status "verified" (2026-10-10), georeferenced ("geo") | HIGH for the original design plan (DoT WA soundings Nov 1999: 91.0 % of rock soundings inside, free scale 0.979; 5 Esri images), LOW for the drawn south-arm extension (not confirmed) |
| verify | DONE (VERIFY.md: R1-R11, before/after table) | overlay match good; extension not confirmed; design volume low vs survey |
| 3D | REBUILT 2026-10-10 (3d/): 6 versions, default = Nov 1999 surveyed surface, measured bed | MEDIUM: surveyed single-beam surface (+-0.3 m, interpolated between ~5 m lines), measured bed, datum link RL/AHD unresolved by 0.2-0.3 m |
| registry | done: img-01..40 (new: 32-36 Esri tiles, 37 overlay montage, 38-40 survey figures); NEW_IMAGES_LOG lines added; img-30/31 refreshed | check_registry: cables ok (40 rows) |
| source audit | first audit 2026-10-10 + Addendum 1 (rows 28-37 etc.) in SOURCE_AUDIT_2026-10-10.md; METHODS_3D A1-A17, X1-X13, section 11 (changes) | - |
| page | NOT done (main adds the model; texts in 3d/PAGE_TEXTS_FOR_MAIN.json, revised, with old_to_new) | - |

## 2. Key decisions and why (details METHODS_3D section 10)
- X2 (revised): DEFAULT = Nov 1999 DoT surveyed surface on the original-plan footprint (standing rule 4: measured survey > design drawing). Design plan with the extension is a toggle labelled "not confirmed".
- X3: datum reading A kept as the default for design versions (survey-implied RL - AHD = 0.5-0.6 m vs A 0.78, B 0); surveyed versions are AHD (= MSL, A12) and ignore the A/B switch.
- X4 (revised): seabed = measured (DoT 1998 soundings + Perth_5m); no volume is fitted.
- X9: Nov 1999 rather than Feb 2002 as default surveyed surface (closest to completion). X10: extension demoted. X11: georeference by fitting to soundings, imagery only as a check. X12: bed sources. X13: frame keeps the drawing's axes (9.7 deg from true north).
- Primary plan source remains Blacka (2013) Fig A.2 (img-26); RWR originals re-downloaded: identical files (no higher resolution exists).

## 3. Key numbers (units, datum, source)
- Georeference: anchor (vertex mean of the original plan, canonical x 3.738, y 271.446 m) at 32.015644 S, 115.748462 E (MGA50 E 381801.49 N 6457145.86, GDA94); canonical +x bearing 350.3 deg T, apex pointing 260.3 deg T; theta 9.74 deg ccw [scripts/georef.json; DoT1999, DoT1998].
- Footprint: 4,049 m2, 121 x 76 m (original plan); 4,355 m2, 121 x 89 m with the drawn extension (347 m2 triangle, 320 m3 drawn) [img-26, img-06].
- Rock volume (m3): surveyed 4,671 (Nov 1999) and 5,219 (Feb 2002), +-1,000; design surface on the measured bed 3,920 (original) / 4,249 (with extension); stated 5,500 (Blacka A.1.3), 5,000 (Rendle p.41; Mead and Borrero 2011), 3,500 (Wikipedia). Mean thickness 1.15 / 1.29 m surveyed, 0.97 m design; max 2.76 / 2.69 / 2.30 m.
- Crest: design RL -1.0 = -1.78 m MSL (A) / -1.00 (B); surveyed highest sounding -1.40 m (Nov 1999), -1.67 m (Feb 2002) AHD; surveyed surface top -1.55 / -1.71 m.
- Datum: design ramp RL minus surveyed AHD 0.59 (Nov 1999, n 454) / 0.50 m (Feb 2002, n 236), sd 0.58; BoM Fremantle MSL 0.773 m above gauge zero (= Fremantle LWD), 1992-2011; highest recorded 1.947 m (16 May 2003), lowest -0.100 m (1 Jan 1987) above gauge zero; HAT / LAT not found.
- Seabed: -3.68 m AHD at the anchor; along the original outline 2.84-6.63 m below MSL (A) (stated 3.0-6.0 m); 1995 vs 1998 surveys mean 0.09, sd 0.29 m; Perth_5m bias +0.085 m (reef excluded).
- Shoreline bearing 7.8 deg T; anchor to the 0 m AHD line 254 m (090) - 263 m (080/100). Arm bearings 35 / 128 deg T, 27 / 60 deg to the shoreline.
- Extension test: Feb 2002 +0.43 m (n 23) in the triangle vs +1.29 m in the plan, +0.19 m ring.

## 4. File map (07_scale/shapes/cables-reef-wa/)
- shape.json (verified, geo, versions, confidence); VERIFY.md; METHOD.md (first-run trace log + 2026-10-10 note); sources.md; SOURCE_AUDIT_2026-10-10.md (+ Addendum 1).
- scripts/: first-run chain trace_a2.py -> compute_shape.py -> make_overlays.py -> make_shape_json.py; NEW chain: georef_fit.py -> georef.json; make_bed.py -> bed_measured.json (+ 3d/bed_measured_canonical.npz); survey_volume.py -> survey_volume.json; shore_and_datum.py -> shore_datum.json; add_geo_to_shape.py (run once on the archived shape.json); make_imagery_figs.py; register_imagery_images.py (run once).
- src/: paper PDF + renders (first run); imagery/ (Esri z19 tiles + .geo.json, annotated/ overlays); bathymetry/ (DoT FR.zip, FR_selected/ the four surveys + ReadMe, DoT_Perth_5m_clip_reef.npz/.json, figures/); datum/ (BoM metadata PDF, monthly sea levels HTML). Total src about 17 MB.
- 3d/: index.html (viewer; patched for survey versions), model.js (1.3 MB, bulky, do not open), docs.js, build_3d.py (+ b3d_lib.py, provenance.py), METHODS_3D.md, SOURCES_3D.md, PAGE_TEXTS_FOR_MAIN.json, REQUESTS_FOR_LIOR.md, bed_measured_canonical.npz, annotated/, previews, aux/ (make_index.py is the one-off generator of the first index.html; index.html was patched by hand afterwards: surveyVer(), contours, water plane, labels), archive/pre_imagery_2026-10-10/ (first-run model.js, docs.js, md, build files, shape.json, previews, handoff).
- Not worth opening: model.js, the preview PNGs, DoT zip.

## 5. Open issues
1. Fremantle chart-datum to AHD offset and HAT / LAT: Transport WA (Tides@transport.wa.gov.au); the 0.2-0.3 m gap between survey and reading A is unresolved (A12).
2. Extension: not confirmed (23 soundings); needs a later survey or Pattiaratchi (2003, 2007) / Bancroft (1999).
3. Papers not obtained (dead ends logged in 02_research/dead_ends/cables-reef-wa.json): Bancroft 1999, Ranasinghe 2001, Pattiaratchi 2003 (ResearchGate / UWA repository 403), Pattiaratchi 2007 Shore and Beach 75(4):80-92.
4. No survey after Feb 2002; Pitt 2009 'crest ~1.5 m below the lowest tide' untested. Wayback capture dates unavailable (Google Earth Pro history by Lior).
5. Reef card (02_research/reefs/cables-reef-wa.json; not edited here): 275 m offshore, 5,500 m3, coordinates if rounded 32 00 S 115 45 E (true 32.0156 S 115.7485 E): main to update. Granite (Blacka) vs limestone (Mead and Borrero 2011).
6. check_registry.py reports errors for other reefs (albany, mexico), not for cables.

## 6. Next steps (in order)
1. Main: add the model per 04_build/UPDATE_PROTOCOL.md using 3d/PAGE_TEXTS_FOR_MAIN.json (revised; default version survey_surface_1999_11); remove cables-reef-wa from data/models3d_hold.json if present; python src/update_page.py --full; also add the 'Checked, nothing useful' dead ends from 02_research/dead_ends/cables-reef-wa.json.
2. If a higher-quality survey (multibeam / lidar) or Navionics readings arrive: replace the surveyed surface (build_3d.py survey_version) and recheck A15-A17.
3. If Transport WA gives the CD-AHD offset: set A12 / the reading default and update METHODS_3D 3.1.
4. If Pattiaratchi 2003/2007 or Bancroft 1999 arrive: extension size and date; as-built levels.

## 7. CHECKPOINT 2026-10-10 (end of imagery + bathymetry run)
All stages complete except the items in section 5. Values in model.js, shape.json, METHODS_3D, SOURCES_3D, VERIFY, PAGE_TEXTS agree (checked by the final consistency script in the run). No stage is half-written.
