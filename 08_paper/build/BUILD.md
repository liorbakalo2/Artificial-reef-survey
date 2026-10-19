# Build of paper.pdf

Rebuild (from `08_paper/build/`): `python3 build.py`
- Concatenates the files in `../sections/ORDER.txt` into `paper.md` (page break before References and Appendix A).
- pandoc: `paper.md -s --mathml --toc --toc-depth=2 --resource-path .. -c paper.css --embed-resources -o paper.html`.
- python playwright (`pip install playwright`, uses `/opt/pw-browsers/chromium-1194/chrome-linux/chrome --no-sandbox`) prints A4 with a page-number footer (`footerTemplate`). The plain Chrome flag `--no-pdf-header-footer` would remove the numbers.
- Style: `paper.css`. Figure numbers come from the captions in the section files (Figures 1-12 in text order; `fig8_stability.png` = Figure 11, `fig9_haifa_envelope.png` = Figure 12; Figure B1 in Appendix B).

Result: `paper.pdf`, 50 pages A4 = title and contents pp. 1-3 (abstract on p. 3), main text Sections 1-9 pp. 3-28 (about 26 pages, over the 15-20 target; no cuts made), References pp. 29-35, Appendices A-D pp. 36-50. 13 figures embedded (12 + B1), no raw Markdown or LaTeX found in the text layer.

## To confirm (Lior)
- Course name: the title page says "Coastal Engineering course paper" (placeholder in `sections/00_front.md`, `subtitle:`). Add course name/number/instructor.
- Abstract appears after the contents list (pandoc order); move if the instructor wants it before.
- Other open points: `../sections/OPEN_ISSUES.md`; reference problems: `REFERENCE_ISSUES.md`.

## Known issues
- Some white space below figures (figures are not split across pages).
- Main text is longer than the 15-20 page target (OPEN_ISSUES item 2 lists cut candidates).
