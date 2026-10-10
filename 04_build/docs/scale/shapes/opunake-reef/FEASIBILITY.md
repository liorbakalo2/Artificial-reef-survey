# FEASIBILITY - Opunake reef plan shape and 3D model (2026-10-10, updated after papers/ + Gemini + web check)

Verdict: NOT feasible with what we hold. No plan shape drawn, no 3D model built.

## What we have
- Size, text only: bags "around 90 m long and 20 m wide" (Newsroom 2021, Raised Water Research, SurferToday - one lineage), 27 sand-filled geotextile bags by 2009, north reef only, designed for one right-hand wave (card R1-R4).
- Four Esri World Imagery frames (capture 2025-01-16, 0.115 m/px). Reef not visible (submerged bags, breaking waves and turbid water; frame mostly beach). overlays/search_frame_z20_no_structure.png.
- Rough site: "north side of the cove", township 39.450 S 173.850 E, surf break 39.46 S 173.86 E - position uncertain by several hundred metres.
- Tide hint: surf-forecast sample high 2.94 m / low 0.47 m (datum not stated).

## What is missing
| need | why | who/where |
|---|---|---|
| Plan drawing or as-built survey of the reef (position, outline, bearing) | no shape without it | Black et al. 2004 "Studies for Resource Consent: Opunake Surfing Reef" (ResearchGate 273133845), ASR Ltd design reports, South Taranaki District Council / Taranaki Regional Council consent files, NZ Geographic 078 figure |
| Aerial imagery when the reef was fresh and water clear (2008-2012) or a calm-day imagery | reef may show as a pale bag field | Esri Wayback releases, LINZ Basemaps / Taranaki aerial flights, Google Earth Pro history (Lior) |
| Crest level with a datum (design said wave height 1.8-2.5 m; crest depth not in any source) | 3D crest | consent report; LINZ chart datum / NZVD2016 |
| Seabed depth around the reef | 3D seabed | LINZ nautical chart (Opunake / Cape Egmont), LINZ bathymetry, Navionics app reading (Lior) |
| Tide levels (LINZ tide predictions, nearest port, with datum) | water levels | LINZ tide tables |
| Bag size / volume | volume | consent report |

## Needs network (container allows only package servers)
- https://basemaps.linz.govt.nz and https://data.linz.govt.nz (Taranaki aerial imagery, charts, bathymetry) - position/visibility, seabed.
- Esri Wayback releases for tiles around -39.457, 173.854, z18-20, any date 2008-2025 - structure visible when new / clear water.
- https://www.nzgeo.com/stories/artificial-surf-reefs-coming-to-a-beach-near-you/ (R3) - design figure/dimensions.
- https://www.researchgate.net/publication/273133845 - blocked by bot check (Lior in a browser).
- https://raisedwaterresearch.com/spot/artificial-reef/new-zealand/north-island/opunake/ gallery; southtaranaki.com Opunake pages; Taranaki Regional Council consent records.

## For Lior
Google Earth Pro: historical imagery 2007-2012 over lat -39.457, lon 173.853 (look for a pale rectangle ~90 x 20 m offshore; give date, lat/lon of both ends). Navionics: soundings along a line off the beach. Papers: Black et al. 2004. When any of this exists, re-run the trace (METHOD.md steps) then 3D.

## Checked in the second pass (2026-10-10)
- papers/ (all 5 PDFs, text layer): Opunake appears only in text and tables: Mead & Borrero 2011 p.1,3-4; Rendle 2016 thesis Table 2.1 (p.41) + references (p.298); Blacka et al. 2013 Tables 4.1-4.4 + references. No plan figure, no coordinates, no crest level. The 2007 Mount Maunganui paper is scanned (no text; not OCR'd) and is about Mount Maunganui.
- Gemini extracts: no confirmable original source; its Opunake dimensions are self-contradictory. Not used.
- WebSearch (9 queries, list in sources.md): only text (90 x 20 m, 27 bags, 1.5-2 m high bags). No plan, no coordinates, no survey, no aerial of the bags.
- Old wedge in 07_scale/reefs/opunake-reef.footprint.json is now flagged DO_NOT_DISPLAY inside the file (schematic analogy, not the reef's shape).
- Size values disagree and both are kept on the card: 90 x 20 m (news/RWR lineage) vs 30 m longshore x 100 m cross-shore, depth 1.8-3.0 m, ~300 m offshore, at LAT (Blacka Table 4.2).

## What would give a shape (documents, in order of value)
1. Taranaki Regional Council (2009). Opunake Artificial Reef Monitoring Programme 2005-2009. Technical Report 2009-33, Stratford, NZ. Monitoring surveys, probably bathymetry/bag positions. NOT in papers/. Ask TRC (public technical report) or Lior via a browser/library.
2. Black, K.P. et al. (2004). Studies for Resource Consent: Opunake Surfing Reef. ASR Ltd technical report for South Taranaki District Council (ResearchGate 273133845). NOT in papers/ (full author list and exact title to confirm from the page).
3. Mead, S.T. and Black, K. design report/dossier for Opunake (ASR Ltd, c.2005-06; Gemini cites "Mead & Black 2007 Design Dossier", unverified). NOT in papers/.
4. Moores, A. (2006). Artificial surf reefs - coming to a beach near you. New Zealand Geographic 078 (Mar-Apr). Pre-construction design figure possible. NOT in papers/ (web text only, figure not seen).
5. Dated imagery: Google Earth Pro history 2007-2012, LINZ/Taranaki aerials, Esri Wayback (networks blocked here).
Already in papers/ (no plan): Mead & Borrero 2011, Rendle 2016, Blacka et al. 2013.
Until one of 1-5 arrives: shape.json stays no_source, no outline anywhere (Lior 2026-10-10: do not show shapes of reefs we do not know).
