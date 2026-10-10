# VERIFY - opunake-reef (2026-10-10)

No shape was traced, so there is no outline to verify. Checks run instead on the claim "the plan shape cannot be supported":
1. Overlays: the 2026-10-04 overlays have no recorded origin (archived as unverified). New overlay overlays/search_frame_z20_no_structure.png: reef not visible. overlay_match: n/a.
2. Design version / state: card says only the north reef was built (27 bags by 2009, never finished to design), later bag/sand changes and seabed change by 2010 (R2/R4), no removal reported. Which state any drawing would show is therefore unknown; no as-built survey found.
3. Scale: 0.115 m/px from the Esri sidecar (z20 at lat -39.46 : 156543.03*cos(39.4577 deg)/2^20 = 0.1153 m) - agrees. Nothing measured with it.
4. Dimensions vs text: only text value 90 x 20 m (R1,R2,R4, agree with each other, one lineage). Axis assignment (90 m offshore?) is an inference of the earlier footprint file, not stated.
5. Provenance: every image in src/ has a source row; the earlier schematic polygon is flagged placeholder and not carried into shape.json.
6. Gemini: its Opunake-specific sources were inaccessible/unverifiable (2026-09-25 footprint file); not used.
7. Confidence: LOW (rubric: no image of the structure).
