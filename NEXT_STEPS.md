# Next steps - start here (written 2026-10-11, end of the cloud session)

Read `CLAUDE.md` first, then this file. Agent rules: `_agent_briefs/common.md` (items 10-11 are new: check `papers/` first;
log dead ends). Source standard: `_agent_briefs/task_source_audit.md`. Who did what: `_agent_briefs/orchestrator.md` section 7.
Lior's to-do list: `REQUESTS_FOR_LIOR.md` (✅ = done/received).

## State on 2026-10-11
- Page tabs: Gallery, Table, 3D only (Map/Scale removed 2026-10-10, archived in `archive/04_build_removed_2026-10-10/`).
- 3D models: Borth, Boscombe, Bunbury, Mount Maunganui, Narrowneck, Palm Beach, Pratte's on the page; Cables (verified on
  WA DoT surveys, 3D medium) and Albany (3D LOW) were being added by the last page agent.
- Hidden shapes (no plan source; Lior: "don't show shapes you don't know"): Opunake, Kovalam, Mexico, Burkitts.
- Every reef dialog: Google Maps link; "Checked, nothing useful" section from `02_research/dead_ends/<slug>.json`.
- Network: environment set to Full on 2026-10-10 (web pages, imagery, PDFs reachable; login and bot-check sites still are not).

## FIRST: check the last page agent finished
`04_build/HANDOFF.md` section 0c should exist and `05_qa/00_STATUS.md` should have its entry. If not, finish its jobs:
the brief is the 2026-10-10 "final page agent" row in orchestrator.md section 7 (pending edits in `05_qa/pending_page_edits/`,
Cables + Albany from their `3d/PAGE_TEXTS_FOR_MAIN.json`, remove both from `04_build/data/models3d_hold.json`, render the
dead-ends section, then `python src/update_page.py --full` from `04_build/` until "state saved").

## Queue (in order of value; one agent each, brief = the task file named)
1. **Lior's new uploads** (`new uploads from lior/`; Lior's folder like `papers/`: never move or rename). Not yet read by any agent.
   - Opunake: `Opunake Artificial Reef monitoring programme 2005-2009.pdf` (TRC, P15) and `New Zyland Geographic.pdf` (P16,
     design figure). May finally give a plan -> `trace_shape.md`, then decide whether Opunake can be shown. Cite fully; update card.
   - Albany: `Albany-Artificial-Surf-Reef-Community-Update-and-FAQs.pdf` + 3 Raised Water Research pages (design, construction,
     "moved rocks"). Check for as-built levels, crest, seabed, changes after construction; update the Albany 3D (now LOW: seabed
     from RHDHV 2015 contours, datum assumed AHD, 1.6 m conflict with BMT 2018), card references, dead ends. One RWR page may
     concern another Australian reef: check which.
2. **EMODnet W1/W2 (Boscombe, Borth survey metadata)**: Lior asked us to try the SeaDataNet portal ourselves first:
   https://cdi.seadatanet.org/search (records 117452, 115084, 1982230). Only if blocked: give Lior a figure of the coast with
   the exact point to click and what to copy.
3. **W8 Albany GA portal**: https://portal.ga.gov.au/persona/marine is only a map to Lior. Give exact lat/lon (reef centre
   -35.018, 117.921) and an annotated screenshot of where to click and which layer, or fetch the data directly (GA services
   gave 403 before: do not bypass).
4. **Kovalam**: retry web.archive.org copies (surfer.com article, ASR brochure) now that the network is Full; Navionics in the
   headless Chrome at /opt/pw-browsers (no login; if it needs one, stop).
5. **Cables**: Fremantle chart datum (LWD) to AHD offset (Transport WA), closes the 0.2-0.3 m datum gap (A12 in its METHODS_3D.md).
6. **OCR**: the Mount Maunganui 2007 PDF in `papers/` has no text layer. Orchestrator installs tesseract quietly (CLAUDE.md), an
   agent writes the text to `05_qa/papers_intake/` (never into `papers/`).
7. Albany dead-ends file: remove duplicates (two agents wrote it).
8. Optional: photo-match buttons for Narrowneck, Cables, Albany (`04_build/src/photo_match.py` model_rings / scene_map).
9. Mexico: nothing to do until coordinates or a plan appear.

## Lior's open decisions (REQUESTS_FOR_LIOR.md section 6)
D3, D4, D5, D8, D9 (Burkitts: Phase 3 zone now located, LOW, kept hidden), Cables default (surveyed 1999 surface, now default,
vs design plan + extension), Bunbury shown as a 12 m circle from a drone photo (hide if Lior prefers).
