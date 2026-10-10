# METHODS_3D - Cable Station artificial surfing reef (cables-reef-wa)

Run 2026-10-10. Re-generate model.js / docs.js with `python3 build_3d.py` (needs ../shape.json, ../scripts/computed.json, ../scripts/a2_trace.json, METHODS_3D.md, SOURCES_3D.md). Annotated sources: `annotated/`. Viewer: `index.html`.

## 1. Summary
The model shows the 1999 Cable Station reef at its DESIGN levels: a V-shaped rock mound (121 m alongshore x 76 m cross-shore, 4,049 m2, plus a drawn 347 m2 extension of the south arm = 4,355 m2) whose surface is a ramp that rises 2.0 m from a set-out line at RL -3.0 (offshore edge) to a crest line at RL -1.0 (inner V edge), with rock side slopes down to the existing bed. The plan and the levels are read from the printed design drawing (Lyons 1992, reproduced in Blacka et al. 2013 Fig A.2), scaled from its own printed dimensions (6.51 px/m, +-3%). Three things are not sourced and are modelled: (i) the datum of the drawing's RL values (two readings, 0.78 m apart, switch in the viewer), (ii) the existing seabed under and around the reef (plane, gradient 1:30 from the Pitt sketch, level fitted so the rock volume equals the stated 5,500 m3), (iii) the side-slope surface. 3D confidence: LOW (plan medium, drawing levels exact but datum ambiguous, bed modelled, nothing surveyed after construction).

## 2. Data sources
Full records in SOURCES_3D.md and `../sources.md`. Registry ids are in brackets.
- Blacka, M.J., Shand, T.D., Carley, J.T. and Mariani, A. (2013) A Review of Artificial Reefs for Coastal Protection in NSW. WRL Technical Report 2012/08, UNSW Water Research Laboratory, for the NSW Office of Environment and Heritage. https://doi.org/10.4225/53/58e1dc7368c7a. Lior's copy in papers/. Fig A.2 (p.93) [cables-reef-wa-img-26]: plan with contours RL -1.00 to -2.50, slopes 1:20 / 1:15 / ~1:13, dimensions 40.0 / 26.0 / 30.0 m. Text A.1.1: 'V shaped in planform, longshore length approximately 140 m, cross shore width of 70 m, crest submergence of 1 - 2.5 m below MSL ... approximately 275 m offshore'; A.1.3: 5,500 m3 of 1.5 t and 3.0 t granite boulders; Table 4.2 (p.65): water depth 3.0-6.0 m; Table 4.3 (p.67): tide range 0.8 m.
- Pattiaratchi, C.B. (1999) Design studies for an artificial surfing reef: Cable Station, Western Australia. Centre for Water Research, UWA, ref ED1483CP. http://joas.free.fr/studies/bei/g2s/reefdesign.pdf [img-15..23]: 3 m depth contour extended offshore, 1:20 slope up to the 1 m contour of the existing reef; mean tide level 0.78 m above datum; model area shoreline to the 7 m contour (~350 m); 250 m offshore; 45 deg peel angle; Fig 7 plan [img-20].
- Raised Water Research (2019) Cables Reef. https://raisedwaterresearch.com/spot/artificial-reef/australia/western-australia/cables-reef/ : drawings 'original design' [img-05], 'additional fill area' [img-06: 320 m3], 'Cables Drawing' (Pitt) [img-07: contours 3.0-7.0 m, scale bar].
- Mead, S. and Borrero, J. (2011), paper P3 in papers/ (intake note 05_qa/papers_intake/P3_mead_borrero_2011.md): 5,000 m3. Card R1/R4: 3,500 / 5,000 m3, > 10,000 t.

## 3. Methods
### 3.1 Frames and datum
- shape.json canonical frame: x alongshore (+ north), y offshore (+ west), origin on the shoreline (assumed N-S) with the footprint centroid 270 m offshore. Model frame (model.js): x_model = -x_canonical (+ south) so that (x south, y west, z up) is right-handed in three.js, as in the Borth viewer.
- Heights in the source are RL (reduced level of the design datum). Reading A (default): RL is the tide-gauge / chart datum (the paper and the Pitt note give 'datum' and '0.0 on the tide gauge' for the same contours that the design extends); the mean tide level is 0.78 m above it (S1 p.3): `z_MSL = z_RL - 0.78`. Reading B: Blacka (2013) writes 'crest submergence 1-2.5 m below MSL' for the same numbers, i.e. RL = MSL: `z_MSL = z_RL`. The 3D scene is built with z_scene = z_RL - 0.78; reading B only moves the water plane by -0.78 m. Evidence for A: the drawing's set-out line RL -3.0 is 'the existing 3 m depth contour extended offshore' (S1) and Pitt's contours are below low-water mark; evidence for B: Blacka's wording. A weak check: the modelled bed under the footprint is 2.0-5.0 m below RL 0; the stated water depth 3.0-6.0 m fits better if measured at MSL under reading A (2.8-5.8 m).
- Water levels (z_MSL): datum -0.78 (S1), typical low/high water -0.40 / +0.40 (range 0.8 m, Blacka Table 4.3; estimate, A7), MSL 0.

### 3.2 Plan
Scale: four printed-dimension readings on Fig A.2 give 6.57 (26.0 m transect), 6.49 (30.0 m transect), 6.52 (0.5 m contours at 1:20 = 10 m) and 6.46 px/m (40.0 m = RL -3.0 to -1.0 at 1:20): mean 6.51, sd 0.05 (annotated/A1). Outline: silhouette of the drawn structure = outer foot ('interface line'), 111 vertices (../METHOD.md steps 4-5). Extension: 'additional fill area' triangle of img-06 registered on corners P2 and P1 (../METHOD.md step 6). Versions: default = design plan + extension; original design plan; Fig 7 V and Pitt concept (plan only, no design levels).

### 3.3 Design surface (RL)
The drawing shows two hatched rock bands (outer along the apex and arms, inner along the V's shoreward edge) and, between them, contours RL -2.5, -2.0, -1.5 (and -1.0 at the inner edge, -3.0 at the outer one). The region between the bands (the 'ramp', 3,113 m2) is traced as a polygon (dense-hatch mask removed from the silhouette, smoothed by a 1.5 m open-close). With d_out and d_in the distances from a point to the outer (set-out) and inner (crest) edge of the ramp:
`z_RL = -3.0 + 2.0 * d_out / (d_out + d_in)`.
Check against the drawing: on the centreline the model gives RL -2.59, -2.20, -1.62 where the drawing has -2.5, -2.0, -1.5 (rms 0.14 m); on the 26.0 m and 30.0 m transects the model's -2.5/-2.0/-1.5 crossings lie within 0.4, 0.1, 0.7 m and 1.1, 1.4, 0.6 m of the drawn ones (3-8% of the distance; 0.1 m or less in height). Overlay: annotated/A1.

### 3.4 Side slopes, bed and volume
- Side slopes (A5): in the bands (footprint minus ramp) the surface falls linearly from the ramp-edge level to the bed over the drawn band width (3-7 m): the hatched bands are taken as the rock side slopes meeting the existing bed at the interface line. Implied slopes about 1:2 to 1:4.
- Extension (A6): footprint known, only the volume (320 m3, img-06) is stated; the fill is given a pyramid-like thickness (proportional to the distance from the edge) scaled to 320 m3.
- Existing bed (A3, A4): `z_bed_RL(y) = -(D0 + (y - 270)/30)`; the gradient 1:30 is read from the Pitt sketch's 3.0-7.0 m contours (28-33 m per metre of depth, annotated/A4). D0 is the single free parameter: it is fitted so the modelled rock volume (ramp + side slopes + extension, above the bed) equals Blacka's 5,500 m3: D0 = 3.50 m (annotated/A3; 5,000 m3 -> 3.36 m, 3,500 m3 -> 2.92 m). This is a calibration to a stated quantity, not a measurement of the bed.
- Seabed around the reef: the same plane for y = 190-420 m, x = -150..150 m. Not modelled: the nearshore profile (no data), the shore line (235-310 m east of the reef).
- Rasters: 0.5 m (volumes), exported at 1 m.

## 4. Validation
| check | model | source | verdict |
|---|---|---|---|
| plan dimensions | 121 x 76 m (original), 121 x 89 m with extension | text 140 x 70 m (Blacka Table 4.2, RWR) | -13% / +9% (original); text is 'approximately' |
| contours on the centreline | -2.59, -2.20, -1.62 | -2.5, -2.0, -1.5 (Fig A.2) | rms 0.14 m |
| contour crossings on the transects | within 0.1-1.4 m | Fig A.2 | good |
| ramp drop | 2.0 m over 26 m and 30 m | 1:13, 1:15 labels | consistent |
| rock volume | 5,500 m3 (fitted); original design alone 5,169 m3 | 5,500 (Blacka), 5,000 (P3/ICM), 3,500 (Wikipedia) | calibrated, so not independent; mean thickness 1.26 m, max 2.9 m |
| density | 10,000 t / 5,500 m3 = 1.82 t/m3 | granite placed with voids 1.6-1.9 | plausible |
| bed depth under the footprint | RL -2.0 (shoreward edge) to -5.0 (offshore edge); +0.78 = 2.8-5.8 m at MSL (A) | 3.0-6.0 m (Blacka, RWR) | agrees under A, 1 m shallower under B |
| bed at y = 350 m | RL -6.2 m | S1: ~7 m contour at ~350 m (approximate) | 0.8 m shallower |
| extension | 347 m2, 320 m3 -> 0.92 m mean | img-06 text | by construction |
| crest-line arm lengths | south 49 m, north 52 m | S1: ride 50-80 m right-hander, 30-40 m left-hander | inconclusive |
| registry images | see SOURCES_3D.md | | img-05/06/07/17/20/23/26 results written to the registry |

## 5. Uncertainty
- Plan: scale +-3% -> area +-6% (4,105-4,629 m2), edge +-0.5 m. Extension +-30%.
- Crest and set-out levels: labels exact; `crest depth over the crest at water level h = h + 1.78 m (A)` or `h + 1.00 m (B)`; datum reading +-0.78 m dominates. Design levels may differ from the built reef (Pitt 2009: crest about 1.5 m below the lowest tide).
- Bed under the reef: +-0.3 m from the spread of stated volumes (2.92-3.50 m), plus gradient uncertainty 1:28-1:33 (< 0.15 m over the footprint). `delta V = area * delta D0 = 4,355 m2 * 0.3 m = +-1,300 m3`. Seabed at 350 m offshore: +-1 m.
- Side-slope surface: +-0.5 m locally, volume effect included in the bed term.
- Vertical exaggeration (1-5x, default 1x): heights only; plan is true; always shown on screen.

## 6. Confidence
LOW. Against the rubric: the plan is MEDIUM (design drawing with printed scale, within 14% / 9% of the text, no survey or image of the built reef); the vertical inputs are mixed: crest and ramp exact in RL but in a datum that is not stated (0.78 m), seabed modelled from a hand-sketch gradient and a fitted level, tides from one paper and one table. Nothing was checked against bathymetry or imagery because the network was blocked.

## 7. Limitations and unknowns (and what resolves them)
1. Datum of RL (0.78 m): the full drawing set or the WA Department of Transport / Marine and Harbours datum note (needs network or a paper). Lior: none directly.
2. Built shape and levels: a dated aerial / satellite image showing the reef (Esri Wayback, Google Earth Pro history, Nearmap, Landgate) to check the outline, the extension and the V angles; Lior can use Google Earth Pro history.
3. Bed: measured bathymetry (WA Dept of Transport / Landgate LiDAR bathymetry, AusSeabed) or Navionics SonarChart readings by Lior at the apex, the arm ends and 100 / 300 m offshore (3d/REQUESTS_FOR_LIOR.md).
4. Tides: Fremantle LAT / MSL / HAT against chart datum and AHD (Transport WA tide tables); here only the range 0.8 m and MTL 0.78 m.
5. Extension size and date: the drawing is low resolution; Pattiaratchi (2003) or Ranasinghe et al. (2001) may state it.
6. Settlement or damage: Blacka reports 'no information on long-term stability'; later changes are not modelled.

## 8. References
Blacka et al. (2013) as in section 2. Pattiaratchi (1999) as in section 2. Lyons, M. (1992) Design studies for an artificial surfing reef. Unpublished report, Dept of Environmental Engineering, UWA (the design drawing, as reproduced in Blacka 2013). Pitt, A. (1990s) concept sketch via Raised Water Research (2019). Raised Water Research (2019) Cables Reef. Mead, S. and Borrero, J. (2011), see papers intake P3. Ranasinghe, R. et al. (2001) and Pattiaratchi (2003), cited by Blacka, not read.
