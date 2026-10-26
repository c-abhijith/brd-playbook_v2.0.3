# Phase 5B — Data evidence — `/brd-p5b-data`

**Follow:** `P0-phase-rules.md`, `query-protocol.md` and (if Genie is used) `genie-protocol.md` · **Closes with:** APPROVED · **Output:** `brd/P5B-data-evidence.md`, entries in `brd-work/query-log.md` (and `genie-log.md`)

## Purpose
The systematic data pass for this BRD: settle with read-only queries every fact the BRD relies on that the data can settle, so the documents rest on evidence, not inference.

## If no connection is available (no live connection, no relay, no Genie)
Write a short page: "No data connection for this BRD. No data evidence was collected." List the facts that would have been checked, close with APPROVED. They stay Inferred or open and appear in phase 7.

## Otherwise
1. **Choose what to check** (inside the fence, HIGH first): facts marked for P5B in the template map; important rules (how many rows follow or break each rule; edge cases); key uniqueness and broken links; null rates on key columns; value ranges; code values and frequencies; volumes and growth; how often each job or flow runs (history, last data change); whether "inactive" objects really have no recent data; definitions missing from the export.
2. **Plan** the queries on the page first (fact, connection, query shape, size check).
3. **Run them read-only** through the registered connections (direct query, relay file, or Genie with the SQL check). One fact per query; a second, differently written query for the most important facts.
4. **Label:** query results are From evidence with LQ id and time (sampled / approximate marked). Genie answers not SQL-checked are not used.
5. **Never** return row-level business or personal data; counts and patterns only.

## Review page
Data evidence table (fact · connection · query id · result · supports / contradicts which statement), findings that change earlier phases (information only), findings to confirm (`### GQ-…` or `### Q-…`), queries that could not run.
