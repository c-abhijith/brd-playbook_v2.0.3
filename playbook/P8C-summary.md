# Phase 8C — Summary BRD — `/brd-p8c-summary`

**Follow:** `P8-draft.md` and `P0-phase-rules.md` · **Closes with:** APPROVED · **Needs:** the Functional and Technical BRDs approved (whichever are registered) · **Output:** `brd/summary/BRD-S_v<n>.md|.html`, `brd/summary/CHANGELOG.md`

## Rules
- Built **only** from the approved Functional and Technical BRDs, at the versions recorded in `based_on`. No new facts; nothing taken from the memory or phases directly.
- Every statement points to the sections it summarises ("→ F 6.2, T 8.1") and keeps the strongest caveat of its sources: a summary of Inferred items stays Inferred and is never phrased as settled.
- About 3–6 pages, unless a client template says otherwise. Detailed enough for a decision maker to understand the area, its risks and what is still open, without reading the other two.

## Template (default: `templates/default-summary-template.md`)
| Section | From |
|---|---|
| 1 At a glance | name, summary, key figures (F, T) |
| 2 Business purpose and value | F 1–2 |
| 3 Scope | F 3 (the fence in one view) |
| 4 Main processes | F 5, one picture |
| 5 Key rules and controls | F 6, F 9, T 8 |
| 6 Systems and data | T 2–5, one picture |
| 7 Dependencies | F 10, T 10 |
| 8 Top risks, gaps and decisions needed | F 12, T 16, with who must act |
| 9 Confirmation status | F 13, T approvals: what is confirmed, by whom, what is pending |
| 10 Document set and next steps | versions of F and T this summary is based on |
