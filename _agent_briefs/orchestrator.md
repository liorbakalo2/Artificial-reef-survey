# Orchestrator playbook - for the MAIN session only (agents do not need this file). Written 2026-10-07.

## 1. Role
- You orchestrate: plan, write or point to briefs, spawn agents, check their results, and report to Lior.
- Agents do the research and build work. Lior: "you should orchestrate, not do the work". Small checks are fine
  (grep, a downscaled screenshot, a one-line fix).
- Start each session with:
  - `CLAUDE.md`;
  - this file;
  - the last 2-3 entries of `05_qa/00_STATUS.md`;
  - `REQUESTS_FOR_LIOR.md`.

## 2. Agents
- **Spawning.** Use Sonnet agents (general-purpose, model sonnet, in the background), at most 3 at a time. Spawn only work Lior
  has given the go for.
- **Prompts.** Each prompt names:
  - the files to read: `CLAUDE.md`, `_agent_briefs/common.md`, the task brief, and the folder's `HANDOFF.md`;
  - the exact checkpoint section;
  - the TO DO list.
  Tell the agent not to re-read the sources its HANDOFF already summarises, and to ask "main" (SendMessage) instead of reading
  everything.
- **Restarts.** Never resume a large agent (~300k tokens); subagents cannot be /compacted. After a usage-limit stop, or once an
  agent is large, start a FRESH agent from its checkpoint (HANDOFF.md, the round LOG, 3d/SOURCES_3D.md, VERIFY.md CHECKPOINT).
- **Endings.** Agents end with a ```json summary, or with `HANDOFF_STOP:` / `NEEDS_CLARIFICATION:`. The harness may refuse to let
  a subagent write a "report" file. If so, save it yourself from the hand-back.
- **Usage window.** When Lior's 5-hour usage window nears its end:
  - most agents checkpoint and stop;
  - the page (04_build) agent may run on to its next checkpoint.
- **Reporting.** After a page change, show Lior 2-3 downscaled screenshots (`04_build/QA/...png`) and say what changed. Agents
  take their screenshots in their OWN headless Chrome (random free port, fresh `--user-data-dir`), never in a shared browser.

## 3. Running in the cloud (Linux) instead of Lior's Windows PC
- **Python.** Run `pip install -r requirements.txt`. The scripts were tested on Python 3.14; 3.11 or later should work.
- **Chrome.**
  - Needed for: the page QA and the export of the combined "All (compare)" meshes (`04_build/src/export_combined.py`, run by
    `build.py` / `update_page.py`).
  - Install Chromium, e.g. `pip install playwright && python -m playwright install --with-deps chromium`.
  - `04_build/src/qa_cdp.py` and `qa_shots.py` look for Chrome in this order:
    1. `CHROME_PATH`;
    2. the Windows paths;
    3. chrome / chromium on PATH;
    4. Playwright's Chromium in `~/.cache/ms-playwright`.
    So after the install above nothing needs setting.
  - Suggested cloud setup script:
    `pip install -r requirements.txt playwright && python -m playwright install --with-deps chromium && apt-get install -y tesseract-ocr`.
- **OCR.** `07_scale/tools/ocr_windows.ps1` is Windows-only. On Linux use tesseract: `apt-get install tesseract-ocr`, then
  PyMuPDF's OCR text page or pytesseract. P2 (Mead, Black & Moores 2007) is a scan with no text layer.
- **Network.** Research steps fetch web pages, Esri Wayback tiles, EMODnet, Navionics web charts and papers. The environment
  needs internet access beyond package registries.
- **Hard-coded paths.** About 47 one-off research scripts under `07_scale/` and `05_qa/` use Windows paths. They were already run
  and their outputs are saved. Re-running one means first switching it to repo-relative paths. The page pipeline
  (`04_build/src`) uses relative paths.
- **Gemini folder.** It is not in the repo. Our verified extracts are in `06_gemini_compare/` and
  `07_scale/00_gemini_footprints_extract.*`. Only the final wrap-up (`wrap_report.md` → `SOURCES_AND_GEMINI_REPORT.md`) may need
  more. If it does, ask Lior to add a read-only snapshot.
- **Viewing the page.** Lior views it on his PC: pull the repo, then open `04_build/artificial_reefs.html` (or
  `Artificial reef launcher.html`). Its 3D viewers are separate HTML files under `04_build/3d/`.

## 4. Lior's recorded decisions and defaults (details in REQUESTS_FOR_LIOR.md section 5 and the reef HANDOFFs)
- **D1, Mount Maunganui as-built bed (decided 2026-10-07).**
  - Default −3.6 m CD, written explicitly as an ASSUMPTION.
  - Option "later seabed" −2.8 m CD: later surveys give −2.4 to −3.3. Check the reef stays below the water line (crest −0.9 m CD).
  - Not yet applied to the model.
- **Borth.** Default outline = Welsh Government LiDAR 2022, confidence high. Toggles: design drawing 1020 and the 2024 satellite
  photo. The oval is the BREAKWATER.
- **D2, Boscombe.** Flatten the offshore extension alongshore. Told Lior "proceeding unless you object"; no objection so far.
- **D6, Borth offshore seabed.** Add the HRPP576 Fig 2 −4.0 m contour as nodes and start the EMODnet gradient there.
  Recommended; still open.
- **Bunbury.** Verdict FAILED, despite the developer's claim.
- **Narrowneck default outline.** The 2020 photo (Esri Wayback r9812, 2020-08-08), unless Lior chooses the Corbett 2023
  Option 2 design. Open.
- **Navionics/Garmin.** Used without login. Their datum is inferred by RMS against an independent survey.
- **Photo-match tolerance.** 2 m (or 10 % of length for reefs under 40 m); 4 m for georeferenced pictures. Set by the page agent;
  not yet confirmed by Lior.

## 5. Work queue (each item restarts only on Lior's go; checkpoint files in brackets)
1. **Mount Maunganui update.** RUNNING since 2026-10-07; task file `_agent_briefs/task_mm_update.md` (see section 7).
   - OCR P2 pages 2-6 (design/construction facts). The as-built survey figure (2,800 m³ vs design 6,500 m³) is Fig. 3 of P3
     (Mead & Borrero 2011), not P2; it may give a measured default outline.
   - Apply D1.
   - Add facts from P3 (Mead & Borrero 2011).
   - Then run `update_page.py`.
2. **Narrowneck.** Stage 1 (verification and versions) RUNNING since 2026-10-07; task file `_agent_briefs/task_narrowneck_verify.md`.
   Stage 2 (the 3D model, brief `model_3d.md`) starts after it, from the 3D plan in its `HANDOFF.md`.
   - Resolve the scale conflict: Corbett 2023 Fig 2 crest loops ~85-90 m vs Jackson Fig 7 60-62 m.
   - Versions: 2020 photo (default), Corbett Option 2, the 2004 design, 2011 survey relief, Navionics (indicative only).
   - Then build the 3D model.
3. **Seabed fixes.** RUNNING since 2026-10-07; task file `_agent_briefs/task_seabed_fixes.md`. Covers Borth D6 and Boscombe D2 in
   their `3d/` folders, then `update_page.py`. The Borth "0.89 m" caveat text is
   typed by hand (`04_build/UPDATE_PROTOCOL.md`).
4. **Boscombe from Rendle 2016** (P5, 343 pp): as-built bag layout, crest levels, survey datum.
5. **Papers intake.** P3 (Mead & Borrero 2011) and P8 (Blacka et al. 2013): per-reef facts and figures into cards, HANDOFFs and
   the image registry.
6. **Palm Beach 3D re-check:** `model_3d.md` STEP 0, plus `07_scale/bathymetry/gold_coast/REPORT.md` section 5.3.
7. **Pratte's re-verify:** the `pending_reverification` block in its `shape.json`.
8. **HANDOFF.md** for Pratte's, Bunbury, Palm Beach and `07_scale/bathymetry/*` (they predate the HANDOFF rule).
9. **Remaining reefs:** trace, verify and 3D, or a FEASIBILITY.md, for Cables, Opunake, Kovalam, Albany, Burkitts and Mexico
   (briefs `trace_shape.md`, `verify_shape.md`, `model_3d.md`).
10. **Full page build** (`build_shapes_videos.md`): the Shapes, Images, Videos review and Methods tabs.
11. **Browser QA** (`qa_browser.md`).
12. **Wrap-up** (`wrap_report.md`): `07_scale/METHODS.md` (academic methods paper) and `SOURCES_AND_GEMINI_REPORT.md`.
13. **Cleanup.** Archive or delete smoke tests and temporary scripts (e.g. `04_build/src/qa_round11.py` if it is temporary).
    Folders stay ordered.

**Small page fixes for the next page round:**
- Palm Beach labels are oversized in the "Palm s4" photo-match view.
- At 900 px height, Borth's version block pushes its viewer below the fold.
- Optional: a version toggle in "All (compare)".
- Fold in whatever Lior reports after viewing the page.

## 6. Lior's own open items
All of them are in `REQUESTS_FOR_LIOR.md`:
- papers P4 (optional) and P7 (only via the City of Gold Coast);
- e-mails E1-E8 (Claude never sends e-mail; drafts on request);
- browser pages W1-W3;
- Navionics app and Google Earth readings;
- decisions D2-D6;
- the media review (`05_qa/media_recheck_summary.md`).

## 7. Running agents (live table: update it when you start or finish an agent, and commit)
| Started | Task file | Work folder | Checkpoint a fresh agent continues from | Status |
|---|---|---|---|---|
| 2026-10-07 | `_agent_briefs/task_mm_update.md` | `07_scale/shapes/mount-maunganui-reef/` | `HANDOFF.md` section 0 + `3d/SOURCES_3D.md` CHECKPOINT | STOPPING 2026-10-07 for Lior's usage limit: told to checkpoint + stop. Restart FRESH from the checkpoint (never resume) |
| 2026-10-07 | `_agent_briefs/task_narrowneck_verify.md` | `07_scale/shapes/narrowneck-gold-coast/` | `VERIFY.md` CHECKPOINT + `HANDOFF.md` | STOPPING 2026-10-07 for Lior's usage limit: told to checkpoint + stop. Restart FRESH from the checkpoint (never resume) |
| 2026-10-07 | `_agent_briefs/task_seabed_fixes.md` | Borth and Boscombe `3d/` | each reef's `HANDOFF.md` (Borth first) | STOPPING 2026-10-07 for Lior's usage limit: told to checkpoint + stop. Restart FRESH from the checkpoint (never resume) |

**When an agent finishes:**
- save its report from the hand-back;
- refresh the page: `python src/update_page.py` from `04_build`, after the model agents. Check the SUMMARY and FAIL lines;
- make the hand edits it lists. The Borth "0.89 m" caveat is in `04_build/data/models3d_caveats.json` and `models3d_curated.json`;
- set its row to done;
- commit;
- start the next queue item, keeping at most 3 agents at a time.

**Rules for agents running in parallel:**
- Agents never run git; the orchestrator commits.
- Model agents never edit `04_build`.
- Each agent edits only its own reef folders. Shared root files (`05_qa/00_STATUS.md`, `REQUESTS_FOR_LIOR.md`, `03_images/reefs/NEW_IMAGES_LOG.md`) get short appends only.

## 8. Transfer protocol: Lior's PC to a cloud session
**On the PC (the orchestrator, when Lior says "hand over"):**
1. Tell every running agent (SendMessage) to finish its current step, write its checkpoint (the file in the section 7 table) and stop.
   Wait for the hand-backs; use TaskStop only for an agent that does not respond.
2. Set each row in section 7 to "stopped at <step>, continue from <checkpoint>". Add a dated `05_qa/00_STATUS.md` entry.
3. Commit everything, with the message "handover to cloud <date>". Push to the private GitHub repo. The first push needs Lior: he
   creates the empty private repo and gives its URL, and Git Credential Manager signs him in. Then "Continue in cloud" (or Lior
   opens a new cloud session on that repo).

**In the cloud (the new orchestrator):**
1. Read `CLAUDE.md`, this file (sections 2-3 and 5-8), and the last `05_qa/00_STATUS.md` entry.
2. Run the setup check:
   - `pip install -r requirements.txt`;
   - Chromium (section 3);
   - `python src/update_page.py --dry` from `04_build` must run without errors.
3. For each section 7 row marked stopped or running: start a FRESH agent with the same task file and the checkpoint named in the
   row. Never try to resume PC agents; they do not exist in the cloud.
4. Continue the queue (section 5) only as far as Lior has given the go. On 2026-10-07 he gave it for the queue in order.
   Commit after each finished agent. Push the session branch so Lior can pull and view the page on his PC.

**Back to the PC:** Lior runs `git pull` in the project folder before any local session works there. Work in one place at a time.
