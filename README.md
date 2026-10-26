# BRD Reconstruction Playbook (VS Code + GitHub Copilot) — v2.0.3

Rebuilds BRDs for an existing system that was never properly documented.
- **Build the memory once.** One owner runs one command that reads every source, understands and connects it, checks the databases read-only, and shows one review page. The approved memory is published as a release.
- **Everyone else loads it with one command** and builds one BRD per workspace, as three detailed documents: **Functional**, **Technical** and **Summary**, phase by phase, with a person reviewing every step.
- **Ask Me** answers any functional or technical question at any time, like a senior BA, with evidence.

What changed from 1.x: `PLAYBOOK-CHANGELOG.md`.

## 1. What you need
- VS Code with **GitHub Copilot Chat** (agent mode). VS Code offers it, the **SQL Server (mssql)** extension and a Mermaid preview when you open the folder.
- Optional read-only data connections:
  - **SQL Server** through the MSSQL extension: a connection profile per database, with a read-only login
  - **Databricks** through the Databricks SQL MCP server (`.vscode/mcp.dbsql.example.json`), with a read-only token
  - **Genie** and **Azure DevOps** as before

  Without them, the agent uses relay mode: it writes the query, and you run it and save the result.
- Your organisation must allow MCP servers in Copilot for the Databricks, Genie and DevOps connections.

## 2. Memory owner: build and publish (Memory workspace)
1. Unzip into a new folder; open it in VS Code; accept the recommended extensions.
2. Put the sources in `sources/`, one folder per type (`sources/README.txt`): metadata exports from `tools/metadata-extraction/`, documents as Markdown, pipeline JSON, old BRDs, discovery packages. Then run **`python tools/prepare-sources/prepare_sources.py`**: it measures every file, splits large ones logically (no part over 150 KB or 2,500 lines) and writes the inventory the agent reads from. Run it again whenever sources change.
3. In Copilot Chat choose **BRD Reconstruction**:
   1. **`/brd-setup`:** workspace type *Memory*, your name, the scope proposed from the metadata, and the data connections. Each connection is tested step by step, and setup tells you which step fails. Reply `APPROVED`.
   2. **`/brd-memory-build`:** one command.
      - It runs through read → understand → connect → find gaps → check the data → resolve → self-check.
      - It posts a progress line after each stage.
      - It works in **runs**: each run reads a limited amount (about 150 KB of source text), saves, and says "open a NEW chat and run /brd-memory-build". Do that until it reaches the review page. If Copilot shows **Continue** within a run, click it.
      - It interrupts only for stop-now problems: empty sources, unreadable or unsplit files, duplicate databases.
      - At the end you get **one review page**: answer, `FEEDBACK` as often as needed, then `APPROVED` makes **Memory v1.0**.
   3. Optional: **`/brd-check`** for an independent check by the BRD Reviewer.
   4. **`/brd-memory-publish`** writes `shared-memory/memory-v1.0/`.
4. **Share:** zip the workspace **without** `sources/` and `brd-work/`. For later versions, send just the new `shared-memory/memory-vX.Y/` folder.
5. **Updates:** new files or users' `memory-feedback.md` → `sources/inbox/` → `/brd-memory-update` → `APPROVED` (v1.1) → `/brd-memory-publish`.

## 3. Each user: load and build a BRD (BRD workspace)
1. Unzip; open in VS Code; accept the extensions.
2. **`/brd-setup`:** workspace type *BRD*, your name, data connections, and the BRD documents (the three detailed defaults unless the client has templates). Reply `APPROVED`.
3. **`/brd-memory-load`:** loads the latest release with one command and reports what's in it.
4. **`/brd-choose`:**
   - **Name and summary (mandatory).** What, Why and Who are required; Where and Not included must be stated, but "not known yet" is allowed. If you're stuck, the agent proposes candidates and drafts the summary for you to correct.
   - **The logical fence.** The agent builds it from the summary and you confirm it: core, supporting, interface, out.
5. **`/brd-template-map`:** every template section is mapped to the phase that will supply it.
6. **Phases**, each needing `APPROVED`:
   - `/brd-p1-overview`
   - `/brd-p2-scope`
   - `/brd-p3-process`
   - `/brd-p4-rules`
   - `/brd-p5a-technical`
   - `/brd-p5b-data` (read-only data evidence)
   - `/brd-p5c-devops`
   - `/brd-p5d-gaps`
   - `/brd-p6-clarify`
   - `/brd-p7-risks` (every open item becomes a risk, an assumption or an open question)
7. **Documents:**
   - `/brd-p8a-functional` and `/brd-p8b-technical`, in either order
   - then `/brd-p8c-summary`, built only from those two
   - Word output: `tools/word-conversion/`. PDF: print the HTML page.
8. Corrections you find are collected in `brd-work/memory-feedback.md`. Send that file to the memory owner.

## 4. Ask Me
Choose the **Ask Me** agent, or type `/ask <question>`. It answers both ways (business ↔ technical), in eight parts:
1. in business terms
2. where it happens
3. conditions and rules
4. what the database holds
5. live evidence
6. affected areas
7. evidence and confidence
8. gaps

It reads the memory, discovery packages and approved BRDs, checks the data read-only, and never changes anything. If it can't answer, it offers to log the question for the memory owner.

## 5. Reviewing a page
- Open the HTML page named in chat, in a browser.
- **Answer boxes:**
  - **Agree** means accepted as written
  - **Correct it** (or typing an answer) gives your statement
  - **Answered by** is the name of whoever gave the answer; leave it empty if it was you
- **Sections:** Agree or Request a change.
- Enter your name, click **Export review**, save the file into `brd-work/feedback/`, and type `FEEDBACK FILE`.
- **Only your chat reply closes a step:** `FEEDBACK: …` · `APPROVED` (optionally `APPROVED for <name>`) · `HALT`.

## 6. If it looks stuck
- **No new line in the chat and no file change for 10–15 minutes:** stop the agent, open a **new chat**, and run the same command. It reads the heartbeat in `brd-work/memory/_progress.md`, sees the previous run was interrupted, and resumes at the first unread lines. Nothing already saved is lost.
- **`/brd-status`** tells you whether a run is really in progress or was interrupted, and where it will resume.
- **The same file keeps stalling:** run the prepare script with lower limits (`--large-kb 120 --part-kb 100 --part-lines 1500`), or lower *Run budget* in `brd-work/PROJECT.md` (for example to 100 KB).
- **The agent says a file is not in the inventory:** sources changed; run `python tools/prepare-sources/prepare_sources.py` again.
- **A read or edit fails twice:** the agent marks the range as a problem in the reading ledger, stops cleanly and tells you, instead of looping.

## 7. Things to know
- **Labels on everything:** Confirmed (with who and when), From evidence, Inferred, Conflicting. No roles: every answer records a name, and all answers count the same.
- **Read-only always:** SELECT / SHOW / DESCRIBE only; never runs procedures; no query over 15 minutes; every query logged in `brd-work/query-log.md`.
- **Any environment** (dev, test, prod) is fine. The same database from two environments is flagged, and only one copy is used.
- **Current state only, inside the fence.** Future-state items stay in the memory.
- **Versions:** memory `v<master>.<sub>`; each document has its own version (`BRD-F_v1`, `BRD-T_v1`, `BRD-S_v1`). Nothing is overwritten. A newer memory shows a notice and changes nothing by itself.
- `/brd-status` always tells you where you are and the next command.
- **Commands and agents:** `.github/` holds the agents (BRD Reconstruction, BRD Reviewer, Ask Me) and the commands. If your VS Code shows different tool names, adjust the `tools:` lines in `.github/agents/*.agent.md`.
