# Labels, tags, activity and versions

## 1. Statement labels (exactly one per statement)

| Label | Use when | Must record |
|---|---|---|
| **Confirmed** | A person confirmed it | who (name), date, where (chat / page round) — `people-and-confirmations.md` |
| **From evidence** | Seen directly in a source: a document, code, a pipeline definition, metadata, a logged read-only query result (`LQ-`), or a SQL-checked Genie finding | evidence id + location (file, section, object and step, query id) |
| **Inferred** | The agent's reading: for example the likely purpose of a procedure, a link guessed from column names, or a statement from a team BRD or another agent's memory | what it is based on |
| **Conflicting** | Two or more sources (or people) disagree | every source and name, and what each says |

Rules:
- Statements from `sources/team-brds/` and `sources/agent-memory/` enter as **Inferred**, even if they sound certain.
  **Exception: discovery packages.** A folder whose `MANIFEST.md` says `producer: SQL Discovery Playbook` or `producer: Databricks Discovery Playbook` keeps its own labels. Register the package and its version as one evidence item and cite the package's own ids (OBJ, BR, PUR, LQ, EV) as locations.
- Code and data tell *what* the system does (From evidence). *Why* it does it is Inferred until a person confirms it.
- A query result is From evidence **as of the time it ran**; sampled or approximate results say so next to the figure.
- A label only moves up to Confirmed through a person. The agent never promotes its own inference.
- Never present an Inferred statement as fact. Say "appears to", "likely", and show the label.

## 2. State tags

| Tag | Meaning |
|---|---|
| **Current state** | How the system works today |
| **Future state** | What the client plans to build (target designs, roadmaps, "to-be", "will", "phase 2") |
| **State unclear** | The agent cannot tell |

- Metadata, code, pipeline definitions, run history, query results and Genie findings are **Current state** (they describe what is running in the environment they came from).
- Documents can be either; tag at document, section or statement level. A document describing something the code does not do is **State unclear**: ask, never decide silently.
- BRDs use **Current state** only. Future-state items live in `<memory>/60-future-state.md`.

## 3. Activity of technical objects
Every table, view, procedure, function, job and pipeline is marked:
- **Active:** evidence of use or change in the last 90 days (job runs, lineage events, usage stats, table history, last data change from a date column).
- **Inactive:** evidence it has not run or changed for a long time, or a person says so.
- **Unknown:** no evidence either way. Unknown is never treated as inactive.

The environment the evidence came from (dev, test, prod…) is recorded as a note only. See `environments-and-duplicates.md`.

## 4. Memory versions: v<master>.<sub>
- The first build ends at **v1.0** when `/brd-memory-build` closes with APPROVED.
- Every `/brd-memory-update` closed with APPROVED raises the **sub** (v1.1, v1.2 …). Everything in one update is one sub-version.
- The **master** is raised only by the separate consolidation agent (v2.0). This playbook accepts it and builds on it (next update v2.1).
- A **release** (`/brd-memory-publish`) copies one approved version into `shared-memory/memory-v<X.Y>/`; it does not create a new version.

## 5. The manifest: `<memory>/MANIFEST.md`
The single source of truth for the memory version (`templates/MANIFEST.md`): current version, owner, history, processed source files, memory files, releases. Files listed under "Processed source files" are not processed again by `/brd-memory-update`. A loaded release carries the manifest it was published with.

## 6. Stamps and notices
- **Every review page and phase output** records the memory version it was built on.
- **Each BRD document** carries its type and own version (`BRD-F v<n>`, `BRD-T v<n>`, `BRD-S v<n>`), the memory version, the playbook version, the BRD name and summary, and a table of which memory version each phase was approved on. The Summary also carries `based_on: Functional vX, Technical vY`.
- **Memory notice:** whenever the memory in use is newer than what a page or document was built on, show it ("Built on Memory v1.2 · memory in use is now v1.4"). The agent changes nothing because of it; revisiting is the user's decision.

## 7. BRD document versions
- Each document has its own version line: `BRD-F_v1`, `BRD-T_v1`, `BRD-S_v1`; each redraft is v2, v3 … The three numbers move independently.
- Never overwritten. Each document folder has a `CHANGELOG.md`: date, what changed, why, memory version used (Summary: also the Functional and Technical versions it was based on).
- A new version of one document never changes another by itself: `STATUS.md` marks the others "may need revisiting" (Summary: "out of date").
