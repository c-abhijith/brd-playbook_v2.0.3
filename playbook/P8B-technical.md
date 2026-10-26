# Phase 8B — Technical BRD — `/brd-p8b-technical`

**Follow:** `P8-draft.md` and `P0-phase-rules.md` · **Closes with:** APPROVED · **Output:** `brd/technical/BRD-T_v<n>.md|.html`, `brd/technical/CHANGELOG.md`

## Audience and depth
Technical readers who must maintain, change or rebuild the system: how the current system implements every process step and rule, object by object, in full detail.

## Template (default: `templates/default-technical-template.md`)
| Section | Filled from |
|---|---|
| 0 Document control | as Functional, plus the Functional version it matches |
| 1 Technical overview | BRD definition, P1, P5A |
| 2 System landscape | P5A, memory lineage and EXT items: servers, databases, catalogs, workspaces, connections (diagram); environment notes |
| 3 Technical scope | P2 fence by object: core, supporting, interface, out |
| 4 Data architecture | P5A: layers, data model diagrams, entity → table mapping |
| 5 Data dictionary | P5A, memory cards, P5B: every in-scope table: purpose, columns, types, keys, nulls, code values, volumes, date ranges, activity |
| 6 Processing logic | P5A: every job and pipeline (schedule, trigger, steps); every procedure, view and function (purpose, parameters, inputs, outputs, step-by-step logic, conditions, error handling, dynamic SQL notes) |
| 7 Orchestration and run order | P5A, memory lineage and history: call graph, dependencies, timings |
| 8 Business rules as implemented | P4 + P5A: each BR (same id and statement as Functional) → object, step, exact condition; differences between code, data and documents |
| 9 Data lineage | P5A: table- and column-level source-to-target |
| 10 Interfaces and integrations | P2, P5A: inbound and outbound, other databases, linked servers, foreign catalogs, files; format, frequency, owner |
| 11 Data quality and live evidence | P5B: profiling, broken links, rule compliance, with query ids and dates |
| 12 Error handling, logging and audit | P5A |
| 13 Security and access (as observed) | P5A, P5B: who can read what; sensitive columns (named, never their values) |
| 14 Non-functional observations | P5A, P5B: volumes, growth, run times, retention, hotspots |
| 15 Technical debt and activity | P5A, P5D: inactive objects, copies and duplicates, hard-coded values, commented-out logic, hidden code |
| 16 Technical gaps, risks, assumptions, open questions | P5D, P7 |
| A Object inventory · B Live query log (queries used as evidence) · C Evidence index · D Traceability matrix (BR ↔ object ↔ column) | |
