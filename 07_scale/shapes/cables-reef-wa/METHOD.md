# METHOD - cables-reef-wa (Cables Reef, Western Australia)

Run started 2026-10-05


## Step 0 - Resume inspection of src\ (2026-10-05)
src\ held 4 files from an earlier cut-off run, with no sources.md/shape.json/overlays:
- S1_pattiaratchi_reefdesign.pdf (256123 B), S1_fig1_sitemap_full_page.png, S1_fig4_wavebasin_full_page.png (2480x3509), S1_fig7_location_map.png (2409x3900).
- Origin re-established: re-downloaded http://joas.free.fr/studies/bei/g2s/reefdesign.pdf (HTTP 200, 256123 B) - MD5 02a6075b1eac84a68180bbfd89226fea, byte-identical to src PDF. PDF metadata: title "Microsoft Word - rr.doc", author Lorraine, creator Microsoft Word / Acrobat Distiller 3.01, created 1999-04-13. Content: C. Pattiaratchi, "Design Studies for an Artificial Surfing Reef: Cable Station, Western Australia", Centre for Water Research UWA, ref ED1483CP, 5 pages. The 3 PNGs are page renders of that PDF (pages 2-4 contain Fig 1, Figs 3-4, Figs 5-7) -> origin traceable, kept for now; may be replaced by native-resolution embedded-image extracts.
- Card dossier (07_scale/reefs/cables-reef-wa.md) already read: text values 140 m N-S x 70 m max width, 275 m offshore (RWR) / 250 m (paper), 3-6 m depth; previous pass called Fig 4 a V/chevron and could NOT resolve apex direction or scale.

## Step 1a - Paper figures read at native resolution (2026-10-05)
Extracted the embedded rasters of the PDF with PyMuPDF (scratch: %TEMP%\cables): Fig 1 p2 (225x165 px), Fig 3 p3 (225x119), Fig 4 p3 (226x145), Figs 5/6 p4, Fig 7 p4 (226x367 px, placed 225 x 366 pt on page, i.e. ~1 px per pt). The figures are low-res 1999 scans; the earlier full-page PNG renders are just upscales of these.
- Fig 4 "Final design": 3-D oblique contour sketch of the wave-basin model - a V / chevron with unequal arms. Oblique -> no scale, not traceable in plan. Qualitative only.
- Fig 7 "geographic location of the proposed reef": a plan map, printed ROTATED 90 deg (text "INDIAN OCEAN" rotated, "COTTESLOE" top-left, "MOSMAN PARK" top-right, roads/shore contours across the top, depth contours below, '+' grid marks, bold V outline with internal contour lines). Because Cottesloe lies north of Mosman Park and the ocean (west) is at the bottom of the figure, north points LEFT in the figure as printed (map rotated 90 deg counter-clockwise). The V apex points DOWN = OFFSHORE (west); the two arms sweep up toward shore. => resolves the previous run's open "apex direction" question (apex offshore). To be double-checked against satellite below.


## Fresh-agent run 2026-10-10 (queue item 9) - network blocked, local files only
Network check: raisedwaterresearch.com, services.arcgisonline.com, google.com all unreachable from the container (curl code 000). So no satellite, no Wayback, no higher-resolution originals. Everything below uses files already in the repo (images registered in 03_images/reefs/cables-reef-wa/). Scripts: scripts/compute_shape.py, scripts/make_overlays.py (re-runnable); trace pixels in scripts/p05_toe_pixels.json; results in scripts/computed.json.

### Step 2 - Candidate images viewed (each once, downscaled)
- img-05 (RWR 'original design', 478 x 339): CAD plan of the V, hatched rock bands along the outer and inner edge, interior contours labelled 'R.L. -x.x' (digits illegible), section lines, '+' grid crosses, end marks P1, P2, P3. Structure clearly drawn; no legible scale bar. Chosen primary.
- img-06 (RWR 'The extension to the right', 417 x 296): the same outline plus a hatched triangle 'ADDITIONAL FILL AREA', text 'VOLUME = 320 m3, MASS ~ 688 tonne' (rotated, small), bottom axis with ticks (labels illegible), dimension lines '40' / '48' (illegible).
- img-07 (Pitt hand sketch, 321 x 323): proposal plan with scale bar 0-10-50-100-200 m, north arrow pointing right, wave-approach arrow from the top, note 'contours in metres below low water mark (i.e. 0.0 on tide gauge)', existing contours 3.0-7.0 (a '1991' survey is cited; digits partly illegible), '100 metres to sandy shoreline'.
- img-20 (paper Fig 7, native 226 x 367, printed rotated): plan with contours, roads, Cottesloe / Mosman Park labels, bold V. Rotated 90 deg clockwise so INDIAN OCEAN reads upright: north up, west (ocean) left, V apex pointing left = offshore.
- Not traceable: Fig 4 (oblique), Fig 3 / img-10 (section), photos img-01..04 (reef submerged).

### Step 3 - Orientation (scale-free)
Three sheets agree: (1) Fig 7: apex offshore (west), arms open to the shore; (2) Pitt sketch: wave arrow from the top, north arrow to the right, apex at the top; (3) img-05: its arm directions, read as north = right and offshore = up, are 44 deg (north arm) and 47 deg (south arm, bearing 133 deg) from the shoreline, the same as Fig 7 (40 and 47 deg) and equal to the 45 deg peel angle in the paper (S1 p.2). The south arm is the longer one on every sheet (Fig 7, img-05, img-06). Shoreline taken as N-S (Fig 7 shows it within ~5-8 deg of N-S; not measured).

### Step 4 - Trace of img-05
Method: grey threshold (< 200), 2 px dilation, largest connected component, fill holes, 5x5 opening (removes leader lines, labels), 2 px erosion (undo the dilation), 7x7 opening (removes two tick artefacts), marching-squares contour, Douglas-Peucker 0.9 px -> 133 vertices. Result: outer foot of the hatched rock bands (what a rock-mound footprint is), including the P1-P2 and P3 end closures. Visual check: red outline follows the hatched edge within ~2 px all round (overlay). Native bbox 443 x 280 px, area 54,547 px2.

### Step 5 - Extension (img-06 -> img-05)
Triangle vertices picked at 3x zoom in img-06 (P2 tip 76.7,190; P1 165.0,212.7; N 111.7,248.3; +-3 px). P2 and P1 in img-05 are the polygon's left tip (23.0, 261.5) and bottom-left corner (146.5, 300.0). 2-point similarity img-06 -> img-05: scale 1.419, rotation 2.9 deg. Independent check, 4-point fit on apex, P3, inner apex, valley bottom: 1.400 / 2.4 deg, residuals 0.5-4.4 px (3% in scale). Triangle area 338 m2 at 3.6 px/m; img-06 states 320 m3 -> mean fill 0.95 m (plausible). Which end: the south (long) arm, matching the dossier ('extension of the reef's southern end', card R5). The final built extent is not documented.

### Step 6 - Scale of img-05 (the weak point)
No legible scale. Evidence, in order:
a. Text dimensions (card R2, RWR): length 140 m N-S, width 70 m. Traced bbox 443 x 280 px gives 3.16 px/m (length) and 4.0 px/m (width): they disagree by 27%, so at least one of the two numbers (or what they measure) is not what the drawing shows. 'About 140 m' is approximate.
b. '+' grid crosses: 180 px apart in x and in y (x = 94.8, 276, 455.2; y rows at 144-148 and 322-324 px; 2.5x view /2.5). A 50 m grid gives 3.6 px/m = the geometric mean of (a). Plausible round CAD grid, but the value is NOT printed legibly - assumption A1.
c. Fig 7 (separate sheet): '+' grid 50 px; 100 m gives a V of 122 x 76 m and a centroid 271 m from the shore line (text: 250 m S1, 275 m RWR). Independent of img-05 except for the same 'round grid' idea; it reproduces img-05's 123 x 78 m to 1-3%.
d. img-06 axis: major tick spacing ~50 px on a 310 px long outline; 20 m per major tick gives 124 m. Labels illegible.
e. Contour spacing in img-05 (interior contours ~27 px apart, perpendicular) would give 2.7 px/m if they are 0.5 m contours on the paper's 1:20 slope - labels and interval illegible, so only a lower bound for the range.
Decision: s = 3.6 px/m, uncertainty range 2.7-4.5 px/m (+-25%): area 2,900-8,050 m2 at the extremes (4,528 m2 central).

### Step 7 - Other sheets traced
Fig 7: 18 hand-picked vertices (rotated frame), 2 m/px assumed (A2): 122 x 76 m, 4,586 m2. Pitt sketch: 23 hand-picked vertices of the outer contour, scale bar 171 px per 200 m (0.855 px/m): 170 x 159 m, 10,619 m2 - a concept much larger than the built reef (and drawn 100 m off the shore).

### Step 8 - Canonical frame
x = (u - u_c)/s (north = sheet right); y = 270 + (v_c - v)/s (offshore = sheet up); (u_c, v_c) = centroid of the as-built polygon, placed 270 m offshore (Fig 7: centroid 271 m from the shore line with A2; text 250-275 m). Rotation: none needed (sheet axes are the frame axes) - confirmed by hand: apex vertex (295.5, 20) -> x = +13.8 m, y = 270 + (182.9-20)/3.6 = 315 m.

### Step 9 - Results
As-built (default): 4,528 m2, 123 x 91 m. Original: 4,209 m2, 123 x 78 m. Fig 7: 4,586 m2, 122 x 76 m. Pitt concept: 10,619 m2, 170 x 159 m. Arms 43.5 / 46.4 deg to the shore, apex angle ~90 deg. Confidence LOW (reason in shape.json).

### Step 10 - Gemini
Gemini's folder is not part of this repo: nothing used, nothing checked.
