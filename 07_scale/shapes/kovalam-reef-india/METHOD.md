# METHOD - kovalam-reef-india (shape trace)

Run started 2026-10-10 (queue item 9, fresh agent). Network: container reaches package servers only, so no web search, no Esri Wayback, no Navionics. Work from local files.

## Step 0 - what already existed (resume rule)
- `src/` held 7 files fetched 2026-10-04/09-25 (img1_asr_aerial.png, img2_rwr_outline.jpg, six Esri frames with .geo.json, asr_brochure_wayback.pdf). All are registered in `03_images/reefs/kovalam-reef-india/images.json` (img-06 to img-14) with URL and date, so origin is re-established; all kept.
- `pixel_polys_img1.json` + `overlays/img1_*` = a draft 11-vertex polygon (smooth crescent wedge) by an earlier run, never finalised, no METHOD. Treated as an unverified note; superseded here (it drew the whole dark patch, not the bag strips).
- No shape.json, METHOD.md, sources.md or VERIFY.md existed.

## Step 1 - sources reviewed (local only)
1. ASR Ltd brochure aerial (img-07, crop of img-06; also the same photo uncropped in WRL 2013 Fig 4.5, p.71 / PDF p.83, credited "ASR, 2012"): oblique photo from the lighthouse end of the beach looking along Lighthouse Beach. The reef is visible as 5-6 olive-brown parallel strips (sand-filled container courses) fanning to the lower left, with a patch of whitewater at their upper-right end. No scale, no georeference.
2. RWR "Kovalam Outline" (img-08): second oblique photo of monsoon surf with a hand-drawn stepped polyline of the break line. No scale. Break line, not necessarily the structure.
3. Esri frames (img-09 to img-14): reef NOT resolved in any (submerged, 2011-02-28 at z17 and 2026-01-23 at z16-19). The 2011-02-28 frame (img-09) shows the bay shape and the surf-zone foam line one year after construction; used as geometry for the camera fit below.
4. Text: WRL Technical Report 2012/08 (Review of artificial reefs for coastal protection in NSW, June 2013), Table 4.2 p.66 (PDF p.78), Kovalam row: GCs; longshore length 65 m; cross-shore width 85 m ("for V-shape reefs refer to max. alongshore and cross shore dimension"); water depth 1.3-3.7 m; offshore distance 90 m ("distance to the undisturbed shoreline prior construction"); submergence 0.2-3.4 m. Primary data behind it are not given (ASR 2009/2010 reports not held). Papers: Coasts & Ports 2011 "Multi-Purpose Reefs - A Decade of Applications" s.3.1.7/4.1.4: 4,000 m3, completed late Feb 2010, lighthouse end of beach, weekly monitoring photos taken from the lighthouse viewing platform (this fixes the camera position of the aerial: lighthouse end, looking north-west along the beach).
