# Genie log

Every question put to Genie, what it said, and whether a human confirmed it.
Statuses: PENDING-CONFIRM · CONFIRMED · CORRECTED · REJECTED · ESCALATED (Genie could not answer; human asked instead)

## Summary
| Status | Count |
|--------|-------|
| PENDING-CONFIRM | 0 |
| CONFIRMED | 0 |
| CORRECTED | 0 |
| REJECTED | 0 |
| ESCALATED | 0 |

## Entries

```
### GQ-000 · <stage> · <area> · SEVERITY · STATUS
Why asked: (doubt or gap, with GAP-/INV- ids)
Question to Genie: "..."
Genie answered?: ANSWERED | PARTIAL (which part) | NOT_ANSWERED (why)
Genie answer (plain English):
SQL used:
As of: (date-time asked; reruns that differ become a new GQ and mark this one SUPERSEDED-BY)
SQL verification: SQL-VERIFIED | SQL-MISMATCH | SQL-NOT-AVAILABLE | SQL-NOT-READ-ONLY
  0 read-only · 1 objects · 2 scope · 3 logic · 4 result matches prose · 5 complete (pass/fail each)
  Notes:
Evidence: (counts, non-sensitive sample values, objects found; say if it is a sample)
Cross-check (query 2, for HIGH): (question, SQL, result, consistent?) / not needed
Affects: (requirement, rule, object or BRD section)
Compared with documents: consistent | conflicts with SRC-x <loc> (-> GAP-nnn)
Human verdict:            Correction/comment:            Reviewer / date:
```
