# HANDOFF - opunake-reef (item 9 agent, 2026-10-10)

Read this first. Result: FEASIBILITY ONLY - plan shape not traceable, no 3d/. Source ids = sources.md.

## 1. Status per stage
| stage | state | date | confidence / reason |
|---|---|---|---|
| trace | not possible; shape.json status "no_source", canonical null | 2026-10-10 | LOW: no plan figure, reef not visible on Esri 2025-01-16 z20 |
| verify | VERIFY.md (negative finding only) | 2026-10-10 | - |
| 3D | NOT built; FEASIBILITY.md | 2026-10-10 | plan, crest datum, seabed all missing |
| registry | 10 rows (none shows structure); img-10 gets annotated_files + how_used | 2026-10-10 | - |
| page | main may add slug to 04_build/data/models3d_hold.json ("Not yet modelled"); nothing else | - | - |

## 2. Key decisions
- Did not trace the old wedge schematic (07_scale/reefs/opunake-reef.footprint.json): a placeholder by analogy to Mount Maunganui, not evidence.
- Old overlays (3) archived in overlays/archive_unverified_2026-10-04/ (origin unrecorded).
- Network probe 2026-10-10: Esri, LINZ, nzgeo refused -> everything needing them is in the list below.

## 3. Key numbers
Text only: ~90 x 20 m footprint, 27 bags (2009), north reef only (card R1-R4). z20 frame 0.1153 m/px, capture 2025-01-16, bounds in src/opunake_sat_z20.png.geo.json. No crest, volume, seabed, bearing.

## 4. File map (07_scale/shapes/opunake-reef/)
METHOD.md (log), sources.md, VERIFY.md, shape.json (no_source), FEASIBILITY.md (what is missing), overlays/search_frame_z20_no_structure.png, src/ (4 Esri PNGs 6-28 MB, not worth opening; registry has 3000 px copies in 03_images/reefs/opunake-reef/).

## 5. Open issues / needs network
- Network pass 2026-10-10 done (section 9): LINZ aerials 2011-12 and 2021-22, Esri Wayback 2015-2024: reef NOT visible. Still no plan source.
- Still needed (browser or library): NZ Geographic 078 figure (nzgeo.com, Cloudflare check), TRC Technical Report 2009-33 (trc.govt.nz, Cloudflare check), Black et al. 2004 (ResearchGate, login), STDC consent plans, Google Earth Pro history 2007-2010, Navionics soundings, LINZ chart (login).

## 6. Next steps
1. When network or papers arrive: locate reef (consent plan or historical aerial), georeference, trace (METHOD.md steps), set outline_versions (design drawing vs photo trace).
2. Then crest datum + seabed (LINZ), tide levels (LINZ), then build 3d/ using Borth as template.

## 7. CHECKPOINT 2026-10-10
Stage reached: feasibility only; HANDOFF_STOP for network/papers. Nothing in progress.

## 8. CHECKPOINT 2026-10-10 (second pass, item 9b)
Checked papers/ (5 PDFs), Gemini extracts and 9 web searches: still NO plan source; shape.json stays no_source. Details: FEASIBILITY.md "Checked in the second pass", sources.md "Search log". Done: flag DO_NOT_DISPLAY/display:false added at top of 07_scale/reefs/opunake-reef.footprint.json (file kept); card 02_research/reefs/opunake-reef.json/.md got R15 (Rendle 2016 Table 2.1: A$760,000, 4,800 m3) and the TRC 2009 report lead; no new images (none exist locally). WARNING for main: 04_build/src/compile_data.py load_footprint() still reads that footprint file and may draw the wedge in the reef dialog ("Footprint & how we drew it"); it does not check the new flag (04_build is off-limits to this agent). Ask the 04_build owner to skip footprints with DO_NOT_DISPLAY/display false and add opunake-reef to models3d_hold.json.
Next: only when TRC 2009-33, Black et al. 2004 or dated imagery arrive (see FEASIBILITY "What would give a shape").

## Source audit 2026-10-10
SOURCE_AUDIT_2026-10-10.md in this folder holds the sources-with-how-used, statement check, assumptions (A#), decisions (D#), confidence and consistency tables. FEASIBILITY.md / shape.json now carry the why / checked / assumed text (page_status for hidden reefs). Open mismatches are listed in the audit section 2. If kovalam build_shape_json.py is re-run it overwrites the audit additions in shape.json: re-apply from the audit.

## 9. NETWORK PASS 2026-10-10 (fresh agent)
- Open public data works: LINZ imagery on AWS (s3://nz-imagery/taranaki/..., COG tiles read by HTTP range, no login), Esri Wayback config https://s3-us-west-2.amazonaws.com/config.maptiles.arcgis.com/waybackconfig.json. WebFetch does not resolve these hosts; use curl. LINZ Basemaps tiles need an API key (not used); nzgeo.com and trc.govt.nz return a Cloudflare challenge (not bypassed).
- Result: no structure visible in LINZ 2011-12 (clear water, 0.4 m) or 2021-22 (0.25 m), nor in 4 distinct Wayback versions. Saved to src/ (linz_aerial_*, esri_wayback_*; .geo.json sidecars) and registered as opunake-reef-img-11..16 (structure_visible false). shape.json untouched (no_source, hidden). Card: R16, R17 and md section. Details: FEASIBILITY.md, sources.md (search log), METHOD.md.
- Next: only a document (P9, P15, P16) or Google Earth history can give a shape; then trace using the LINZ crops as georeferenced base (2011-12 crop: EPSG:2193, 0.4 m/px, top-left 1672970.8 E / 5632659.2 N).
