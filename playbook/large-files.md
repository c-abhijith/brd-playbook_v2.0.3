# Large files

The agent can only hold a limited amount of text in one conversation and has no terminal, so it cannot read a huge file in one go or split it itself.

## 1. Limits
- **Large:** over **200 KB** or over **3,000 lines**. It must be split before it is read. (A larger file does not fit in one conversation; reading it slice by slice in one chat fills the conversation until Copilot stalls.)
- **Not large:** read in full in consecutive ranges, from line 1 to the last line, updating the reading ledger after each range (`reading-protocol.md`).

## 2. The prepare script measures and splits; the agent never does
The agent cannot see a file's size without opening it, and opening a huge file is exactly what freezes a run. So:
- Before every build or update, a person runs `python tools/prepare-sources/prepare_sources.py` (`tools/prepare-sources/README.md`). It measures every file, splits every large one into logical parts with a **hard limit of 150 KB and 2,500 lines per part**, and writes the inventory `brd-work/index/inventory.md` plus its pages.
- The agent **never opens a file to measure it, never tries to split a file, and never opens a file whose inventory status is not `read`**.
- A file under `sources/` that is not in the inventory (new or changed since the script ran): stop and ask the user to run the script again. Find such files by listing folders and comparing names with the inventory pages (search), never by opening the files.
- Problems in the inventory (`convert first`, `too large`) are stop-now questions.

## 3. How split files are used
- The original of a split file has status `split: do not read, read its parts`. Its parts and its short index (`<stem>.index.md`) have status `read`.
- The original is registered as **one evidence item**; locations are given as part and object or section (`EV-012, part 007, object sales.usp_calc_rebate`).
- Which part holds which object: **search** `<stem>.objects.csv` (status `lookup`); never read it whole.
- Parts marked "continued" hold one unit (a procedure, a section, a job) spread over several parts: read them in order, in the same run where possible.

## 4. Splitting is logical
Never by size alone; a unit is never cut (details in `tools/split-large-files/README.md`):
- code and metadata exports: one object per unit, grouped by schema, then business group
- documents: one section per unit, parts never mix chapters
- job and pipeline definitions: one job or pipeline per unit

## 5. Files that cannot be split or read
Word, PDF, Excel, images: the inventory marks them `convert first`; ask for a Markdown or CSV version (`tools/word-conversion/README.md`) and list the file as waiting.
