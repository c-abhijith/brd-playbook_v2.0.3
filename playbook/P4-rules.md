# Phase 4 — Business rules and controls — `/brd-p4-rules`

**Follow:** `P0-phase-rules.md` · **Closes with:** APPROVED · **Output:** `brd/P4-rules.md`

## Purpose
List every business rule the area applies and the controls that protect them, so the client can confirm which rules are intended.

## Produce
1. **Rules (`BR-nn`), in batches:** rule in plain English; where it is implemented (OBJ id, code location); where it is stated (documents, team BRD); label and state tag. Rules found only in code are From evidence for *what* and Inferred for *whether it is intended*.
2. **Calculations:** formulas, thresholds, rounding, defaults, with examples where helpful.
3. **Controls:** validations, reconciliations, checks, approvals, alerts (in code, jobs or documents), and which rules each protects.
4. **Rules without controls, and controls without a clear rule.**
5. **Conflicts:** rules stated differently in different sources (`### CLM-…`).
6. **Questions:** which rules are intended, thresholds that look arbitrary, behaviour on edge cases (`### Q-…`).

## Review page
Rule table with labels and sources; controls table; conflicts and questions.
