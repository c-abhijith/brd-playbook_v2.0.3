# Phase 5A — Technical analysis — `/brd-p5a-technical`

**Follow:** `P0-phase-rules.md` · **Closes with:** APPROVED · **Output:** `brd/P5A-technical.md`

## Purpose
Go deeper than the memory map for the objects in this BRD's scope, so every rule and process step is backed by a precise technical account.

## Produce, in batches
1. **Object inventory for this BRD:** every in-scope table, view, procedure, function, job and pipeline, with activity (Active / Inactive / Unknown).
2. **Data model:** entities, keys, relationships, history handling, as found.
3. **Procedure and job walkthrough:** for each, step-by-step logic in plain English, reads and writes, parameters, error handling, and which BR and process steps it implements.
4. **Lineage for this BRD:** source to consumer, with evidence for each link.
5. **Technical facts behind rules:** confirm or challenge each BR from phase 4 against the code; mismatches become `### CLM-…`.
6. **Technical gaps:** missing code, dynamic SQL, objects referenced but not found, duplicate copies (`environments-and-duplicates.md`). Settle what the data can settle with read-only queries (`query-protocol.md`).

## Review page
Inventory, model, walkthroughs, lineage, rule-vs-code checks, gaps.
