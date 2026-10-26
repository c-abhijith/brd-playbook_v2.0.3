---
kind: brd
title: <BRD name> — Technical BRD
subtitle: How the current system implements the business process, object by object
project: <Project name>
brd_name: <BRD name>
document_type: Technical
brd_version: v<n>
memory_version: <vX.Y>
memory_notice: <only if a newer memory exists>
status: Draft for review
date: <YYYY-MM-DD>
platform: <platforms>
playbook_version: 2.0.3
prepared_by: <operator> with the BRD Reconstruction agent
approved_by: Pending
feedback_file: brd-technical-review-v<n>.json
feedback_folder: brd-work/feedback/
---

<!-- Default Technical BRD template (playbook 2.0). Fill every section completely from the approved phases; never shorten lists
(every in-scope object appears). Labels and sources on every statement. Current state only. Business rules use the same ids and
wording as the Functional BRD. Never write personal data or business rows; name sensitive columns, never their values. -->

## 0. Document control
- Document versions table · memory version per phase · Functional BRD version this document matches · approvals · Confirmed-by summary

## 1. Technical overview
- BRD name and summary in technical terms · systems in scope · how this document was produced (memory version, data checks, environments)

## 2. System landscape
- ```layers or ```flow picture of servers, databases, catalogs and workspaces and how they connect
| System | Platform | Server / workspace | Database / catalog | Role in this process | Environment (note) |
|---|---|---|---|---|---|

## 3. Technical scope
| Ring | Object (OBJ id, full name) | Type | Activity | Why in this ring |
|---|---|---|---|---|
(Core · Supporting · Interface · Out)

## 4. Data architecture
- Layers (raw / staging / cleaned / business / reporting) with the objects in each
- Data model: ```mermaid erDiagram per subject area (or a table of entities and relationships)
| Business entity | Table(s) | Key | Notes (history, soft deletes, snapshots) |
|---|---|---|---|

## 5. Data dictionary
One sub-section per in-scope table:
```
5.n  Sales.sales.invoice · OBJ-0007 · Active · ≈ 4.2M rows (2019-01 → 2026-10)
Purpose: …
| Column | Type | Null | Key | Meaning | Code values / range |
Keys and links · rules in the design (checks, defaults, computed) · Where used (objects and their conditions)
```

## 6. Processing logic
### 6.1 Jobs and pipelines
| Job / pipeline | Schedule / trigger | Steps in order | Runs | Last run · failures |
|---|---|---|---|---|
### 6.2 Procedures, views and functions (one sub-section each)
Purpose · parameters · reads · writes · calls · step-by-step logic with exact conditions and values · error handling · dynamic SQL or outside references · business rules implemented · activity

## 7. Orchestration and run order
- Call graph and run order (```flow) · dependencies between jobs · typical timings (history) · what happens on failure or rerun

## 8. Business rules as implemented
| BR | Rule (same wording as Functional) | Object · step | Exact condition in code | Data check (LQ) | Differences (code vs documents vs data) |
|---|---|---|---|---|---|

## 9. Data lineage
### 9.1 Table level
| Source | Via (job / procedure / view) | Target | Evidence |
|---|---|---|---|
### 9.2 Column level (main outputs)
| Target column | Source column(s) | Transformation | Evidence |
|---|---|---|---|

## 10. Interfaces and integrations
| Direction | Counterpart (system, database, linked server, foreign catalog, file) | Objects | Format | Frequency | Owner |
|---|---|---|---|---|---|

## 11. Data quality and live evidence
| Check | Query (LQ) | Result | As of | Supports / contradicts |
|---|---|---|---|---|

## 12. Error handling, logging and audit

## 13. Security and access (as observed)
Who can read or change what (groups, logins as seen) · sensitive columns (named only)

## 14. Non-functional observations
Volumes and growth · run times · retention · availability · performance hotspots (each with evidence, or To be completed)

## 15. Technical debt and activity
Inactive objects · copies and duplicates · hard-coded values · commented-out logic · hidden or encrypted code · dynamic SQL that cannot be traced

## 16. Technical gaps, risks, assumptions and open questions
Same structure as Functional §12, technical items

## Appendix A. Object inventory
| OBJ | Full name | Type | Ring | Activity | Card |
|---|---|---|---|---|---|
## Appendix B. Data checks used as evidence
| LQ | Purpose | Result | Date |
|---|---|---|---|
## Appendix C. Evidence index
## Appendix D. Traceability matrix
| BR | Object | Column(s) | Functional section |
|---|---|---|---|
