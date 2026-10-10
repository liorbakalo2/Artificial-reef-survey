# VERIFY - cables-reef-wa (2026-10-10, no network: PARTIAL verification, internal checks only)

Status: shape.json stays "traced" (not "verified"): the checks that could break the trace (satellite / aerial imagery, a legible scale) need the network.

| # | check | verdict | evidence |
|---|---|---|---|
| 1 | Overlays re-rendered from shape.json data and viewed | pass | overlays/cables-reef-wa-img-05_toe_outline_and_extension.png (outline follows hatched outer edge within ~2 px), -img-06_extension_triangle.png, -img-20_fig7_V_outline_rotated.png, -img-07_pitt_concept_outline.png; scripts/make_overlays.py regenerates them from scripts/computed.json |
| 2 | Design version | partial | img-05 is the 'original design'; img-06 shows the extension (dossier: southern end extended during construction, card R5). Built extent and any later change are not documented in any local source. Pitt 2009 recommends a shallower reef / longer nose: a recommendation, not built. |
| 3 | Scale | FAIL to confirm | No legible scale on img-05/06/20; 3.6 px/m rests on an assumed 50 m grid (assumption A1) that also fits the text 140 x 70 m (-12% / +11%). Re-derived by hand: bbox 443 x 280 px; 443/140 = 3.16, 280/70 = 4.0, geometric mean 3.57 -> 3.6. Uncertainty kept at +-25%. |
| 4 | Arithmetic | pass | shapely areas re-run (4,208.9 m2 original, 4,528.3 as-built); canonical vertex checked by hand (apex -> x +13.8 m, y 315 m); the make-canonical tool of 07_scale/tools was NOT used, so its old rotation bug does not apply (sheet axes = frame axes, no rotation) |
| 5 | Dimensions vs text | within 12% (length), 11% (width, original) | 123 vs 140 m; 77.8 vs 70 m. With the extension the width is 90.7 m (+30%); the text most likely describes the original design. |
| 6 | Independent agreement | pass, with caveat | Fig 7 (assumed 100 m grid) gives 122 x 76 m; img-05 (assumed 50 m grid) gives 123 x 78 m; img-06 axis (assumed 20 m major ticks) gives ~124 m. All rest on 'round grid' guesses, so they support each other but are not proof. |
| 7 | Shape / angle test (scale-free) | pass | arms 43.5 and 46.4 deg to the shore, apex ~90 deg, versus the 45 deg design peel angle (S1 p.2); same arm angles on Fig 7 (40 / 47 deg by hand); long arm to the south on all three sheets |
| 8 | Orientation | inferred | apex offshore from Fig 7 (INDIAN OCEAN label) and Pitt north arrow; shoreline assumed N-S (Fig 7: within ~5-8 deg) |
| 9 | Provenance | pass | every source has URL, figure, date, credit (sources.md, shape.json, registry ids); image dates are 'undated 1990s' because RWR gives none |
| 10 | Gemini findings | not applicable | Gemini folder not in this repo |
| 11 | Confidence | LOW, honest | design drawing without scale, no survey, no georeferenced image; shape proportions good, size +-25% |

Corrections to earlier notes: the earlier footprint file 07_scale/reefs/cables-reef-wa.footprint.json (verified 2026-09-25) assumed apex offshore at low confidence and drew a thin 140 x 70 m V of 2,299 m2 (a ~10 m wide band); the design drawing shows a solid mound (platform + slopes) of ~4,200 m2. The text 'max width 70 m' therefore fits the V's cross-shore extent, not an arm width. Apex-offshore is now supported by Fig 7 labels.

What would turn this into a verified shape (needs network, see HANDOFF.md): a dated aerial/satellite image where the reef is visible, to georeference the outline, fix the scale and check the extension.
