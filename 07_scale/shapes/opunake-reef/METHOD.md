# METHOD - opunake-reef plan shape (item 9 run, 2026-10-10)

Run started 2026-10-10 (fresh agent; earlier 2026-10-04 run left only src/ images + 3 overlays, no sources.md / shape.json).

## Step 0 - registry and resume check
- 03_images/reefs/opunake-reef/images.json holds 10 rows. None shows the structure (rows 01-06 photos/video frames: site/surf context; rows 07-10 = the four Esri satellite frames in src/, "reef not visible"). No row has for_3d_check.pending true.
- src/ holds 4 Esri World Imagery PNGs (+ .geo.json sidecars): z20 (4338 px, 0.115 m/px, imagery capture 2025-01-16, bounds N -39.45545 S -39.45995 E 173.85741 W 173.85159), mid, wide, current. Origin traceable (Esri World Imagery tile service, retrieved 2026-10-04, see sidecars) -> kept, listed in sources.md.
- overlays/ held 3 PNGs from the 2026-10-04 run (wide_zoom_pier, mid_zoom_nw, wide_zoom_beach) with no record of what they trace; moved to overlays/archive_unverified_2026-10-04/ (not results).

## Step 1 - source search (local only; network blocked)
- Network test 2026-10-10: services.arcgisonline.com, data.linz.govt.nz, www.nzgeo.com all refused by the egress proxy (connect_rejected, organisation policy). Esri Wayback, LINZ, EMODnet, Navionics therefore not reachable.
- Local material read: reef card 02_research/reefs/opunake-reef.md (R1-R12) and the earlier schematic 07_scale/reefs/opunake-reef.footprint.json (verified 2026-09-25).
- Plan-view evidence in the card: NONE. Text only: bags "cover an area around 90 m long and 20 m wide" (R2, R4, R1), 27 geotextile bags by 2009, north reef only built, designed for a single right-hand wave, no bearing, no shape description, no depths with a datum, no volume. The footprint file's wedge (-10,110),(10,110),(0,200) is an admitted schematic placeholder by analogy to Mount Maunganui; it is not evidence of shape.
- Papers in papers/ : not searched (brief limits reading); Black et al. 2004 "Studies for Resource Consent: Opunake Surfing Reef" (card R9) is the likely source of a design plan and is not held.

## Step 2 - look for the structure in the held satellite imagery
- Viewed opunake_sat_z20.png once, downscaled to 1100 px (full frame ~500 m square). It shows the NW headland and boulder foreshore, the surf-zone/whitewater at lower left, wet black-sand beach at low tide, camping ground and township. No bag field, no regular rectangular/linear pale or dark feature in the water, and no marker line. The frame is mostly land/intertidal: the water part (lower-left corner, ~150 x 200 m) is only breaking waves and deeper turbid-green water. The card's own location is only "north side of the cove"; the card coordinates (39.450 S 173.850 E township; 39.46 S 173.86 E surf break) are ~0.5-1 km apart, so the reef's position is unknown to better than several hundred metres. No overlay can be drawn: "do not trace what you cannot see".
- Saved overlays/search_frame_z20_no_structure.png (the frame with scale bar and the negative finding).
- Conclusion: images held give role "context" only.

## Step 3 - decision
Plan shape not traceable: no plan figure, no georeferenced position, no visible structure. Per SHAPE_SPEC rubric this is "low: no image of the structure" (fallback = text bbox 90 x 20 m only, no outline). 3D feasibility (plan, crest datum, seabed) also fails -> FEASIBILITY.md, no 3d/.

## Step 4 - Gemini
Card enrichment (2026-09-25) already rejected Gemini's quotes. Gemini footprint extract (07_scale/00_gemini_footprints_extract.*) not opened in this run; its cited "Mead & Black 2007 Design Dossier" and "Taranaki Regional Council Monitoring Records 2010" were found inaccessible by the 2026-09-25 verification (footprint file, orientation_notes). Verdict: unverifiable, not used.
