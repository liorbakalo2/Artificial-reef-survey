# Next steps - start here (written 2026-10-11, end of the cloud session)

Read `CLAUDE.md` first, then this file. Agent rules: `_agent_briefs/common.md` (items 10-11 are new: check `papers/` first;
log dead ends). Source standard: `_agent_briefs/task_source_audit.md`. Who did what: `_agent_briefs/orchestrator.md` section 7.
Lior's to-do list: `REQUESTS_FOR_LIOR.md` (✅ = done/received).

## State on 2026-10-11
- Page tabs: Gallery, Table, 3D only (Map/Scale removed 2026-10-10, archived in `archive/04_build_removed_2026-10-10/`).
- 3D models: Borth, Boscombe, Bunbury, Mount Maunganui, Narrowneck, Palm Beach, Pratte's on the page; Cables (verified on
  WA DoT surveys, 3D medium) and Albany (3D LOW) added 2026-10-11.
- Hidden shapes (no plan source; Lior: "don't show shapes you don't know"): Opunake, Kovalam, Mexico, Burkitts.
- Every reef dialog: Google Maps link; "Checked, nothing useful" section from `02_research/dead_ends/<slug>.json`.
- Network: environment set to Full on 2026-10-10 (web pages, imagery, PDFs reachable; login and bot-check sites still are not).

## INTERRUPTED 2026-10-13 (usage limit) - resume here first
Six agents were stopped mid-work. Their task prompts are saved in `_agent_briefs/workflows/reef-small-tasks-2026-10-13b.js`
(the TASKS list; re-run it with the Workflow tool, or give each prompt to one agent, adding: "a previous agent did part of this;
check the files listed below and the folder's HANDOFF.md, continue, do not redo"). Their partial work is committed (WIP).
| task | state when stopped | what the next agent does |
|---|---|---|
| opunake-uploads | DONE (STATUS entry 2026-10-13): TRC 2009-33 gives consent corners (189 x 94 m area, centre -39.45943, 173.85163) and design 99 x 30 x 3.5 m, ~4,900 m3; no bag layout, so the shape stays hidden; size conflict resolved | main: apply FEASIBILITY.md "Recommendation for main" to the card/page (coords, size); Lior decides whether to show the consent area (option 3) |
| albany-uploads | PARTIAL: uploads OCRed (`05_qa/papers_intake/albany_rwr_pdfs_ocr.md`), 3D docs/model.js/PAGE_TEXTS edited, W8_how_to.png made; card, registry check, dead ends, STATUS not finished | check `3d/METHODS_3D.md` before/after and model.js loads; finish card refs, registry, dead ends, W8 5-line instruction, STATUS |
| cables-fixes | PARTIAL: build_3d.py/model.js rebuilt (default label), METHODS/SOURCES edited, Fremantle datum sources saved in `src/datum/` (Roelse 1975 DNM TR12, PSMSL, BODC GLOSS 53, GA AHD), `scripts/datum_link.py` | verify model.js only changed labels (or a documented level), finish A12 decision, PAGE_TEXTS if needed, HANDOFF, STATUS |
| europe-meta-kovalam | PARTIAL: SeaDataNet CDI pages saved in Boscombe/Borth `src/cdi_2026-10-13/`, SOURCES_3D.md edited, W1/W2 click-point figures made; Kovalam part (web.archive, Navionics, card: Rendle 4,300 m3, bbox 43x24 vs 38x29) NOT started | finish W1/W2 (values that may differ from the models, REQUESTS lines), then the Kovalam part |
| ocr-mm-2007 (Haiku) | NOT started | OCR papers/ Mount Maunganui 2007 PDF to `05_qa/papers_intake/P2_mead_black_moores_2007_ocr.md` (rule 13) |
| page-map-links | NOT started (04_build untouched) | location block in dialog + gallery tile + 3D tab: copy coords, Google Maps/satellite, Google Earth web, KML for Google Earth Pro (outline only for shown reefs; all-reefs KML), Navionics if a centred URL works, EMODnet/GEBCO viewer; checks; update_page --full |
After all six: run `python src/update_page.py --full` from 04_build (apply the PAGE_TEXTS_FOR_MAIN.json changes of Albany/Cables first), commit, push.

## Last page build: 2026-10-11, `update_page.py --full` state saved (check.py 247 PASS, qa_models3d 191 PASS). 9 models on the
page incl. Cables and Albany; dead-ends sections rendered. Details: `04_build/HANDOFF.md` section 0c.

## Small fixes left (quick, do first)
- Cables `3d/model.js` labels version `design_plan_original_1999` "(default)" but the default is `survey_surface_1999_11` (fix in its build_3d.py, rebuild).
- Cables and Albany `3d/METHODS_3D.md`: the 'References' section is a one-line pointer; make it a real list (the page currently takes them from REGISTER_3D.md).
- Kovalam card: add Rendle 4,300 m3 and the bbox mismatch 43x24 vs 38x29 m.
- Albany viewer fixed in `07_scale` 2026-10-11 (pile height is above the seabed); `VIEWER_FIXES` in `04_build/src/compile_models3d.py` is now a no-op and can be removed.

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
8. Optional: photo-match buttons for Narrowneck, Cables, Albany (`04_build/src/photo_match.py` model_rings / scene_map).
9. Mexico: nothing to do until coordinates or a plan appear.

## Lior's open decisions (REQUESTS_FOR_LIOR.md section 6)
D3, D4, D5, D8, D9 (Burkitts: Phase 3 zone now located, LOW, kept hidden), Cables default (surveyed 1999 surface, now default,
vs design plan + extension), Bunbury shown as a 12 m circle from a drone photo (hide if Lior prefers).
