# FEASIBILITY - mexico-reef-2026-unnamed (Xala Reef, Costalegre, Jalisco) - 2026-10-10

Verdict: a plan shape CANNOT be traced and no 3D model can be built from current evidence. Nothing is drawn; no shape.json was created.
Any outline would be invented. The only shape on file is the earlier text-derived envelope (see 4), which is not a measurement.

## 1. What the evidence is (all checked 2026-10-10 from local files)
- Registry (03_images/reefs/mexico-reef-2026-unnamed/images.json): 2 images, both Raised Water Research (RWR) post images, 2026-03-31
  (https://raisedwaterresearch.com/unveiling-the-new-reef-in-mexico/). img-01 = surfer in a wave, img-02 = drone shot of a peeling left.
  Both: structure_visible false (rock reef submerged), no scale, no coastline, no landmark. Nothing can be measured or georeferenced.
- Card 02_research/reefs/mexico-reef-2026-unnamed.json: lat/lon null (location withheld by RWR until the 16 Apr 2026 event); size "not disclosed";
  gaps list: no length, width, crest depth, volume, contractor, construction timeline; no design report, EIS or as-built drawing found.
  Only facts: quarried boulders, "3,000 truckloads" (Hollywood Reporter 2025-04-22), designer Simon B. Mortensen (DHI Seaport).
- No shape folder, no src/ image, no papers/ item for this reef. The only approximate position is a Google Maps area pin (19.71861, -105.23222)
  near Chalacatepec airport, explicitly NOT the reef (card images_rejected).
- Gemini: its dossier gives "~140 m x ~75 m" with no source and no CAD entry (07_scale/00_gemini_footprints_extract.md); not used (rule 2).
- Network (tested 2026-10-10): raisedwaterresearch.com returns HTTP 403 from this container; map tiles, EMODnet, Navionics blocked.

## 2. Why this fails the rubric (SHAPE_SPEC.md)
No image of the structure, no scaled drawing, no dimensions, no coordinates. Even a "low" confidence trace needs a sketch or figure to trace; there is none.
A submerged boulder reef cannot be seen on the two photos; satellite imagery would only show the wave line, not the reef toe.

## 3. What would be needed (any ONE of A, B+C is enough for a medium/low trace; A is best)
A. A design or as-built plan figure: DHI/Mortensen paper, ICSR/ICCE/Coastal Structures proceedings, a Xala/ACTUR EIA (MIA - Manifestacion de Impacto
   Ambiental, SEMARNAT Gaceta Ecologica, Xala or "Costalegre" project), a DHI Seaport case study page, RWR follow-up post or video with plan graphics.
B. Reef coordinates (from Lior's contacts, the 16 Apr 2026 California Surf Club event, or SEMARNAT MIA documents) so that recent satellite
   imagery (Esri Wayback / Google Earth) can be checked for a break line, shoreline orientation and rock works above the water (a beach
   nourishment/groyne-like head may be visible).
C. At least length, width, crest depth and layout type (e.g. Palm Beach-style V/reef + sand) from a published statement, for a schematic 3D.
For 3D also: nearshore bathymetry (nautical chart, EMODnet does not cover Mexican Pacific well; Navionics reading), local tides (Manzanillo/Cuyutlan,
CICESE or NOAA tide predictions), and as-built crest levels.

## 4. Existing fallback (not a trace)
07_scale/reefs/mexico-reef-2026-unnamed.footprint.json: symmetric 160 x 80 m envelope placed 230-310 m offshore by analogy to Palm Beach Reef;
declared "not a measurement of Xala". It must NOT be shown on the page (Lior, 2026-10-10: shapes we do not know are not shown; footprint.json has display:false).

## 5. Status
Trace: not done (no source). Verify: n/a. 3D: not feasible. Registry: unchanged (2 rows, none new). Re-open when A, B or C arrives.

## Why this reef is hidden on the page, what was checked, what is assumed (source audit 2026-10-10)
Rule (Lior, 2026-10-10): shapes we do not know are not shown. Xala is hidden (no shape.json; footprint.json display:false).
- Why: no plan, no survey, no coordinates, no dimensions and no image of the structure (it is submerged) exist in any source we found. The reef's location was withheld until the 16 April 2026 event.
- Checked, with sources: Raised Water Research post of 2026-03-31 "Unveiling the new reef in Mexico" and its two images (registry img-01, img-02: surfer and drone shot, no scale); The Hollywood Reporter, K. Romeyn, 2025-04-22 ("3,000 truckloads of boulders"); Hospitality Net and the Xala website (location context only); WSCC 2026 speaker bio and RWR Palm Beach / Mortensen pages (designer pedigree, Palm Beach figures); web search 2026-10-10 for Xala dimensions (nothing found); Gemini "~140 x 75 m" (no source). The RWR site was not reachable in the audit (HTTP 403 earlier): the post was not re-fetched.
- Assumed (ASSUMPTION): the April 2026 reef is the Xala reef (identified by an RWR image caption); the 2025 boulder break and the 2026 reef are one structure; a submerged boulder reef would not show on satellite imagery (an expectation, untested); Palm Beach figures say nothing about Xala's size.
- Confidence: every geometric element none; identity of the structure medium. Full tables: SOURCE_AUDIT_2026-10-10.md.
