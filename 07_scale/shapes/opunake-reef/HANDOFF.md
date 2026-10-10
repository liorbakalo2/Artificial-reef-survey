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
- LINZ Basemaps / Data Service Taranaki aerials, chart, bathymetry (position, visibility, seabed).
- Esri Wayback releases 2008-2025 around -39.457, 173.854 (z18-20): look for the bag field when new.
- NZ Geographic 078 article (R3) figure; RWR Opunake gallery; STDC / TRC consent files.
- Papers/Lior: Black et al. 2004 resource-consent study (ResearchGate 273133845); Google Earth Pro history; Navionics soundings.

## 6. Next steps
1. When network or papers arrive: locate reef (consent plan or historical aerial), georeference, trace (METHOD.md steps), set outline_versions (design drawing vs photo trace).
2. Then crest datum + seabed (LINZ), tide levels (LINZ), then build 3d/ using Borth as template.

## 7. CHECKPOINT 2026-10-10
Stage reached: feasibility only; HANDOFF_STOP for network/papers. Nothing in progress.

## 8. CHECKPOINT 2026-10-10 (second pass, item 9b)
Checked papers/ (5 PDFs), Gemini extracts and 9 web searches: still NO plan source; shape.json stays no_source. Details: FEASIBILITY.md "Checked in the second pass", sources.md "Search log". Done: flag DO_NOT_DISPLAY/display:false added at top of 07_scale/reefs/opunake-reef.footprint.json (file kept); card 02_research/reefs/opunake-reef.json/.md got R15 (Rendle 2016 Table 2.1: A$760,000, 4,800 m3) and the TRC 2009 report lead; no new images (none exist locally). WARNING for main: 04_build/src/compile_data.py load_footprint() still reads that footprint file and may draw the wedge in the reef dialog ("Footprint & how we drew it"); it does not check the new flag (04_build is off-limits to this agent). Ask the 04_build owner to skip footprints with DO_NOT_DISPLAY/display false and add opunake-reef to models3d_hold.json.
Next: only when TRC 2009-33, Black et al. 2004 or dated imagery arrive (see FEASIBILITY "What would give a shape").
