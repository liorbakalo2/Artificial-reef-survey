# sources.md - opunake-reef (2026-10-10)

Images (all private research copies; reuse rights not cleared). Registry ids in 03_images/reefs/opunake-reef/images.json.

| id | kind | title | url / tile | page/figure | image date | credit | licence | retrieved | local file | registry | role |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sat_z20 | satellite | Esri World Imagery z20, centre -39.4577, 173.8545, r 250 m | https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x} | tiles z20, 4338 px, 0.115 m/px | 2025-01-16 (capture date field) | Esri, Maxar, Earthstar Geographics, GIS User Community | Esri terms (not stated as open) | 2026-10-04 | 07_scale/shapes/opunake-reef/src/opunake_sat_z20.png | opunake-reef-img-10 | context (reef not visible) |
| sat_mid | satellite | same service, mid zoom | same | - | see .geo.json | same | same | 2026-10-04 | src/opunake_sat_mid.png | img-08 | context |
| sat_wide | satellite | same, wide | same | - | see .geo.json | same | same | 2026-10-04 | src/opunake_sat_wide.png | img-09 | context |
| sat_current | satellite | same, "current" | same | - | see .geo.json | same | same | 2026-10-04 | src/opunake_sat_current.png | img-07 | context |
| ov_search | overlay | our annotation of sat_z20 (scale bar + negative finding) | - | - | made 2026-10-10 | this project | private | 2026-10-10 | overlays/search_frame_z20_no_structure.png | annotated_files of img-10 | documentation |

Text sources (card references, not re-fetched; network blocked): R1 Newsroom 2021-12-06; R2 Raised Water Research Opunake; R3 NZ Geographic 078 (2006); R4 SurferToday; R9 ResearchGate 273133845 (snippet only). Values taken: footprint ~90 x 20 m, 27 bags (2009), single right-hand wave design. No coordinates, bearing, depth or volume with a datum.

## Search log 2026-10-10 (item 9b: local papers, Gemini extracts, WebSearch). Result: NO plan source.
Local papers/ (PyMuPDF text layer, grep Opunake; WebFetch/download unavailable):
| paper (file in papers/) | Opunake pages (PDF) | content |
|---|---|---|
| Mead & Borrero (2011) Multi-Purpose Reefs - A Decade of Applications | 1 (Fig 1 world map), 3-4 (3.1.5) | 4,800 m3, start 2006, last work May 2008, 1,400 m3 short, no drawing |
| Rendle (2016) PhD thesis, Univ. Plymouth, 343 pp | 41 (Table 2.1), 298 (refs) | 4,800 m3, A$760,000, "not officially completed"; cites TRC (2009) monitoring report. No Opunake figure |
| Blacka et al. (2013) Review of artificial reefs for coastal protection in NSW, WRL | 75, 77, 79, 81, 102 | Tables 4.1-4.4: 30 m x 100 m, depth 1.8-3.0 m, ~300 m offshore, "At LAT", tide >3.0 m, A$0.93M; ref list TRC (2009) Tech. Rep. 2009-33. No plan |
| Mount Maunganui 2007 (6 pp, 1,404 chars text; mostly scanned) | none in text layer | image-only pages not OCR'd (tesseract not installed, no installs allowed); title says Mount Maunganui, not expected to cover Opunake |
| Narrowneck Renewal 2023 (7 pp) | none | - |
Gemini extracts (06_gemini_compare/02_gemini_extract.*, README; 07_scale/00_gemini_footprints_extract.*): only Gemini's own Opunake polygon (dimensions 80 x 30 m, polygon 30 x 67 m, inverted, per its own audit; our card 90 x 20 m) and three unverifiable/fabricated quotes. No original source cited that we could confirm. NOT used.
WebSearch (standard unless noted), all 2026-10-10; none returned a plan, coordinates, crest datum or survey:
1. "Opunake surfing reef geotextile bags plan drawing dimensions crest depth Black ASR" -> raisedwaterresearch.com/?p=3339, artificialreefs.org Stuff article (2009), theinertia.com/?p=261061, geosyntheticsmagazine.com; text only (90 x 20 m, 1.5-2 m high bags, 27 bags 2009).
2. "Opunake artificial reef monitoring programme Taranaki Regional Council Technical Report 2009-33 ..." -> report itself not found online.
3. "Black Mead Opunake surfing reef resource consent studies 2004 ..." -> nothing on the 2004 study; TRC hits were Opunake Power hydro consents (unrelated).
4. "Opunake surf reef aerial photo bags visible offshore ... coordinates" -> surf-forecast, tourism pages; no aerial of the bags.
5. "Mead Black Opunake reef design ... Coasts and Ports OR ..." -> nzgeo.com/stories/artificial-surf-reefs-coming-to-a-beach-near-you/ (R3, text), newsroom.co.nz (R1), ICCE tdl.org downloads (general surfing-reef papers, not Opunake).
6. "trc.govt.nz Opunake artificial reef monitoring report bathymetry ..." -> none from TRC.
7. "icce-ojs-tamu.tdl.org article 8509 ... Opunake" -> no Opunake paper.
8. "researchcommons.waikato.ac.nz 10289/12221 Opunake" -> handle not identified.
9. (extended) "Opunake Artificial Surf Reef Trust STDC reef survey plan crest chart datum bags layout" -> stuff.co.nz/taranaki-daily-news/news/5456452/Money-for-surf-reef-a-wipeout (NZ$400k write-off), surfertoday, ausleisure ASR liquidation; text only.
Candidate leads found (not fetched; downloads blocked): https://www.stuff.co.nz/taranaki-daily-news/news/5456452/Money-for-surf-reef-a-wipeout ; https://www.ausleisure.com.au/news/asr-liquidation-cast-doubts-over-future-of-artificial-surf-reefs ; https://geosyntheticsmagazine.com/2023/06/07/why-have-most-geotextile-artificial-reefs-never-really-worked/ . None expected to hold a plan.
