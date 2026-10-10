# FEASIBILITY - 3D model of Burkitts Reef (2026-10-10): NOT BUILT

Verdict: the brief's rule is BUILD only if (a) plan shape, (b) crest elevation and (d) seabed depth are sourced. Only (a) exists, at low confidence. No 3D folder was created.

| input | what we have | status |
|---|---|---|
| a. plan shape | photo trace of the visible rock platform, Esri 2025-09-05, 31,485 m2 in frame, low confidence (shape.json). The reshaped zone (the actual reef) is not located by any source. | LOW, partial |
| b. crest level | none. Card: "no shallow-end/minimum depth figure found". Only: boulders worked at low tide with a ~2.5 m tide swing (R4, no datum). Satellite shows the platform awash/exposed, but at an unknown tide. | MISSING |
| c. height, slopes | ~300 m3 moved (R3, R4); with an unknown footprint this gives no height. Natural boulder rock, no designed profile. | MISSING |
| d. seabed depth | none for this site. Dive-site depth "to ~9 m" (R10) is a site-wide maximum, not a profile. No chart, LiDAR or sounding read (network blocked). | MISSING |
| e. tides / datum | ~2.5 m swing (R4); no datum, no MSL/LAT/HAT figures. Nearest port tables (Burnett Heads) not reachable. | MISSING |

Why not "assume and build": a model with an invented platform height and an invented bed would look like data. The reef is also a natural platform: the interesting thing to show is which boulders moved, which nobody recorded.

## What would make it buildable
1. Seabed: Navionics / SonarChart at -24.8153, 152.4671 (z18), or Queensland LiDAR / AusSeabed bathymetry, or Google Earth Pro depth tool (Lior: see REQUESTS_FOR_LIOR.md).
2. Platform crest and tide state: dated low-tide imagery (Esri Wayback releases 2014+, Queensland historical aerials, 1997-98 pair) plus Burnett Heads tide tables for those dates, to calibrate how much rock is exposed at known water level.
3. The reshaped zone: where the ~12 boulders / ~300 m3 were moved. Needs a local account (Redgard, Bargara Boardriders, ABC gallery, Jackson and Corbett 2007) or before/after aerials.
4. A larger south frame (platform continues beyond the current image).
Then the platform could be modelled as a natural shelf (bed -> platform -> reshaped sub-zone) with outline version "photo trace 2025" as default.
