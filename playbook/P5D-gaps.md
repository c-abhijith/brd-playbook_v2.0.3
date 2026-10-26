# Phase 5D — Gap analysis — `/brd-p5d-gaps`

**Follow:** `P0-phase-rules.md` · **Closes with:** APPROVED · **Output:** `brd/P5D-gaps.md`

## Purpose
Bring together everything still missing, unclear or contradictory across all evidence, before the clarification phase.

## Gap types
| Code | Meaning |
|---|---|
| MIS | Expected information missing (for example an input's owner, a rule's threshold) |
| CON | Sources disagree |
| HID | Logic exists only in code; intent unknown |
| ORP | Something documented with no implementation found |
| ORT | Implementation with no documented purpose |
| AMB | Wording allows more than one reading |
| STU | Current or future state unclear |
| ACT | Activity unknown for an object that matters |

## Produce
1. Gap register: `GAP-nnn`, type, what is missing or unclear, sources, why it matters for the BRD, severity (HIGH changes the BRD's meaning; MEDIUM affects detail; LOW wording), suggested question.
2. Counts by type and severity.
3. Which gaps the evidence cannot close (they need people), to drive phase 6.

## Review page
Top HIGH gaps in full, the register, counts.
