# Memory manifest

The single source of truth for the memory version. This playbook writes v1.0 when the memory build is approved and raises the **sub** number with each approved update. A consolidation agent may raise the **master** number (vN.0); this playbook then builds on it.

current_version: v0
master: 0
sub: 0
owner: <name>
last_changed:
changed_by:
playbook_version: 2.0.3

## History
| Version | Date | Type (build / update / consolidation) | Files | Change log | Approved by |
|---|---|---|---|---|---|

## Releases
| Version | Published | Folder | Files | By |
|---|---|---|---|---|

## Processed source files
Files listed here are not processed again by /brd-memory-update.

| File (or split index) | Evidence id | Registered in version | Notes (supersedes, split into parts, comparison copy, quality) |
|---|---|---|---|

## Memory files
| File | Holds |
|---|---|
| 00-README.md | reader guide: what each file holds, labels, how to cite, version to quote |
| 00-evidence-register.md | every source: type, date, environment note, state tag, default label |
| 01-reading-ledger.md | proof every source was read in full: ranges read per file, digest written |
| notes/EV-nnn.md | one digest per source file (or part): everything it says, with line references |
| 05-index.md | lookup: object, column, rule, term, code value, purpose → where described |
| 10-catalog/<db>.<schema>.md | one card per table (with Where used), view, procedure, function, trigger, job, pipeline |
| 15-data-facts.md | results of read-only data checks (with LQ ids and times) |
| 20-lineage.md | data flows and run order, source to consumer |
| 30-business-map.md | purposes (PUR), processes, business rules (BR), glossary |
| 35-reference-data.md | code values and meanings; hard-coded values and where used |
| 40-claims.md | statements from documents, team BRDs, agent memory (CLM) |
| 50-relationships.md | areas, how they relate, hubs, candidate BRD areas |
| 60-future-state.md | future-state items (FS), linked to current processes |
| 70-open-questions.md | gap register (GAP) and open questions (Q) |
| 80-summaries.md | summaries: object group, area, whole system |
| query-log.md | every data check made while building or updating the memory |
| changes/ | one change log per version |
