# Playbook change log

## 2.0.3 — 2026-10-27
**Fix: runs still freezing around large files.** Two causes: the agent opened large files to measure them before asking for a split, and the split tool kept an oversized section or object whole, leaving parts that were still too big.
- **New `tools/prepare-sources/prepare_sources.py`** (run by a person before every build or update): measures every source file without the agent, splits every large file automatically, and writes the **inventory** (`brd-work/index/inventory.md` + pages + `inventory.json`).
- **The agent reads only what the inventory clears:** files and parts with status `read`. It never opens a file to measure it, never tries to split, never opens a file missing from the inventory (it asks for the script to be run again).
- **Split tool: hard limit per part** (150 KB and 2,500 lines). Units too large for one part are split at the most natural point and marked "continued": CSV between rows (a single huge cell goes to a side file), Markdown at sub-headings, then paragraphs, then lines; JSON items as indented text. Encodings UTF-8, UTF-16 (SSMS) and Windows-1252 are read. The split index stays small; the object-to-part table moved to `<stem>.objects.csv` (searched, not read).
- Files that change after splitting are split again automatically; unchanged files are left alone.

## 2.0.2 — 2026-10-27
**Fix: runs stalling for hours on large files, and status showing "working" after a run was stopped.**
- **Lower size limit:** files over **200 KB or 3,000 lines** must be split first (was 1 MB / 20,000 lines). The split tool's default part size is now **150 KB**.
- **Small reads:** at most 300 lines per read.
- **Digest as you go:** the file digest is extended after every range in small edits, never written in one large edit at the end.
- **Run budget:** each run reads about 150 KB of source text (setting in `PROJECT.md`), or finishes one stage, then saves and stops with "open a NEW chat and run the same command". A fresh chat each run keeps Copilot from overflowing.
- **Heartbeat:** `_progress.md` records run status and last activity after every range. A run whose last activity is over 15 minutes old is treated as interrupted; the next run resumes at the first unread range.
- **`/brd-status`** now says plainly whether a run is in progress, finished, or was interrupted (and where it will resume), and never reports "working" for a run that is not active.
- **No loops:** a read or edit that fails twice is marked as a problem in the reading ledger and the run stops cleanly.
- README: new section "If it looks stuck".

## 2.0.1 — 2026-10-27
**Fix: every source file is now read in full, every line.** In 2.0.0 the agent could read only the first slice of a file (for example "lines 1 to 100") and move on, so parts of the sources never reached the memory.
- New `playbook/reading-protocol.md`: read in consecutive ranges to the last line; one slice is not a read; never skip a file; search results are not reading.
- **File digests:** each file (or split part) gets `notes/EV-nnn.md` straight after it is read, with everything it says and line references. Later stages build the memory from the digests, so nothing read is lost when a chat resets.
- **Reading ledger** (`01-reading-ledger.md`): ranges read per file, as proof. Stage 1 of the build (and the reading step of an update) ends only at 100% coverage, or with exclusions the user agreed by name.
- The memory review page opens with **Reading coverage**; approval is refused below 100% without agreed exclusions.
- Self-check and `/brd-check` verify that content from the second half and the end of files reached the memory.
- BRD phases and Ask Me read every memory file, card or section they open in full.
- Releases include the ledger and the digests.

## 2.0.0 — 2026-10-26
A redesign. Commands were removed and renamed, so this is a new major version.

**Build the memory once, share it, load it with one command**
- Workspace types: **Memory** (one owner builds and publishes), **BRD** (each user loads and builds one BRD), **Memory + BRD** (one person does both).
- **`/brd-memory-build`** replaces `/brd-memory-collect`, `-map`, `-understand` and `-review`. One command runs eight stages, with checkpoints and progress lines, interrupts only for stop-now problems, checks the data read-only (up to 50 queries), self-checks, and ends with **one** review page. Running it again continues from the checkpoint.
- **`/brd-memory-publish`** writes a release (`shared-memory/memory-vX.Y/`, with RELEASE.md, FILES.md, index and reader guide). **`/brd-memory-load`** loads the latest release with one command, checks it is complete, and reports in chat.
- Users never change the memory; corrections and unanswered questions go to `brd-work/memory-feedback.md`, which the owner feeds into `/brd-memory-update`.

**Choosing the BRD**
- The **summary is mandatory**. What, Why and Who are required; Where and Not included must be stated ("not known yet" allowed). Missing parts are suggested from the memory and only the gaps are asked. Vague, too broad, too narrow and contradictory summaries are handled explicitly.
- A **logical fence** is built from the summary (seeds → relationships → hubs not followed → Core / Supporting / Interface / Out) and confirmed. It is saved in `brd/00-brd-definition.md` and binds every later step.

**Data connections**
- Direct **read-only** checks through the **Databricks SQL MCP server** and the **MSSQL extension**, alongside optional Genie and DevOps, with relay mode as the fallback (`playbook/query-protocol.md`).
- Setup tests each connection step by step and says which step failed. The scope (catalogs, databases, schemas) is **proposed from the metadata** and only confirmed.
- Phase 5B is now **Data evidence** (`/brd-p5b-data`). Any phase may settle gaps with read-only queries.

**People**
- **No roles and no weighting.** Setup asks only who runs the workspace. Every answer records the name of who gave it (chat `per <name>`, or the new **Answered by** field in the review page). **Agree** means accepted as written. Approvals record the sign-off name. The validation list shows Inferred and Conflicting items plus *Confirmed by* per person.

**Other changes**
- **Environments:** any environment is accepted (recorded as a note). Duplicate databases and catalogs are detected and flagged; one copy is primary, the other is a comparison copy that is never used as evidence.
- **Large files:** files over 1 MB or 20,000 lines are split **logically** with `tools/split-large-files/split_export.py` (by schema, business group, object, section; never cutting an object or section; with an index), then read as parts.
- **Phase 7** sorts every open item (memory, summary, fence, phases) into a risk, an assumption or an open question, with a count reconciliation. Summary gaps: Who or Not included unknown → risk; Where unknown → assumption.
- **Three detailed default templates** (Functional, Technical, Summary), used when the client has none.
- **Ask Me agent** (`/ask`): a super BA answering functional and technical questions in eight parts, with live read-only evidence and sources.
- **Closing words:** FEEDBACK / APPROVED / HALT. PROCEED is retired.
- **Phase 1** is now **Overview** (`/brd-p1-overview`).
- **Memory files:** new `00-README.md`, `05-index.md`, `15-data-facts.md`, `35-reference-data.md`, `query-log.md`; table cards have a *Where used* block.

**Upgrading from 1.x**
1. Start a new workspace with 2.0; keep the old one for reference.
2. **Existing memory:** copy the old `brd-work/memory/` into the new Memory workspace's `brd-work/memory/` and run `/brd-memory-update`. It adds the index, reader guide and reference-data files and re-labels role-based confirmations with names only. Then publish.
3. **BRDs in progress:** finish them on 1.2, or start them again in a BRD workspace on 2.0 (the summary and fence are new and required).

## 1.2.0 — 2026-10-23
**New:** one BRD scope, up to three documents: **Functional**, **Technical** and **Summary**, each in its own client template.
- `/brd-setup` registers each template with its type and reviewer (`PROJECT.md` → "BRD documents"). Defaults for each type: `templates/default-functional-template.md`, `default-technical-template.md`, `default-summary-template.md` (the old `default-brd-template.md` is now the Functional default).
- New step **`/brd-template-map`** after `/brd-choose` (APPROVED): reads every template and maps each section to the phases that feed it (`brd/template-map.md`). Phase 1 now needs it.
- Phases 1–7 cover the sections the map assigns to them and ask the questions it lists (`P0-phase-rules.md` rules 1 and 12).
- Phase 8 split: **`/brd-p8a-functional`**, **`/brd-p8b-technical`** (either order) and **`/brd-p8c-summary`** (only from the approved Functional and Technical BRDs). Shared rules in `P8-draft.md`; `/brd-p8-draft` now asks which document to draft.
- Each document has its own folder, version line and change log: `brd/functional/BRD-F_v<n>`, `brd/technical/BRD-T_v<n>`, `brd/summary/BRD-S_v<n>`. Cross-document flags in `STATUS.md`: may need revisiting, out of date.
- `/brd-check` checks consistency across documents. The viewer shows the document type.
- `tools/word-conversion/README.md`: Word templates → Markdown, and finished documents → Word in the client's styles (pandoc).

**Upgrading a workspace on 1.1.0**
1. Replace `.github/`, `playbook/`, `tools/` and `README.md` with the 1.2.0 copies. Do not touch `brd-work/` or `sources/`.
2. Put the extra templates in `sources/template/` and re-run `/brd-setup` (it keeps your answers and adds the documents table).
3. Run `/brd-template-map`. If phases are already approved, sections they don't cover go to the next open phase, P6, or the drafting step as questions. Approved phases are not changed.
4. A `BRD_v<n>` already drafted under 1.1.0 stays where it is; the next draft goes into the new folders as the document type you choose.


## 1.1.0 — 2026-10-22
**New:** discovery packages keep their labels.
- Folders in `sources/agent-memory/` whose `MANIFEST.md` says `producer: SQL Discovery Playbook` or `producer: Databricks Discovery Playbook` keep their own labels on import: From evidence stays From evidence, Inferred stays Inferred, Confirmed keeps its confirmer, Conflicting stays Conflicting. The package and its version are one evidence item; its own ids (OBJ, BR, PUR, WR, LQ) are cited as locations.
- Other agents' memory files and team BRDs still enter as Inferred (unchanged).

**Files:** `playbook/labels-and-versions.md` §1 · `M1-collect.md` · `M3-understand.md` · `MU-memory-update.md` (step 7, upgrade) · `MASTER.md` · `templates/evidence-register.md` · `.github/prompts/brd-memory-collect.prompt.md` · `README.md` · version stamps.

**Upgrading a workspace that is already running 1.0.0**
1. Replace `.github/`, `playbook/` and `README.md` with the 1.1.0 copies. Do **not** touch `brd-work/` or `sources/`.
2. Nothing already written is restamped: earlier pages, memory versions and BRD drafts keep "1.0.0"; new pages say "1.1.0".
3. Only if you already imported a SQL or Databricks discovery package: copy the package into `sources/inbox/` and run `/brd-memory-update`. Its statements get their own labels back, shown as changes, in one new memory sub-version.
4. Approved BRD phases are not changed. If relabelled statements were used in them, the update page lists the phases; revisiting is your decision.

## 1.0.0
First release.
