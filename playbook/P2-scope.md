# Phase 2 — Scope and boundaries — `/brd-p2-scope`

**Follow:** `P0-phase-rules.md` · **Closes with:** APPROVED · **Output:** `brd/P2-scope.md`

## Purpose
Turn the confirmed fence into the formal scope: exactly what this BRD covers and where it stops.

## Produce
1. **In scope:** the fence's **core**: processes, flows, data, reports and the technical objects behind them (OBJ ids).
2. **Supporting data:** the fence's **supporting** items, and which parts of each the core uses.
3. **Out of scope:** the fence's **out** ring and anything deliberately excluded (including inactive objects unless the user wants them documented), with the reason.
4. **Inputs (upstream):** each source system or area: what data, format, frequency, owner. Missing details become questions (or data checks: volumes, frequency from history).
5. **Outputs (downstream):** each consumer: what data, grain, freshness, interface.
6. **Hand-overs:** the fence's **interface** items: where this BRD touches other areas, and who owns the shared data.
7. **Summary parts still "not known yet"** (Who, Where, Not included): ask again; if still unknown, they go to phase 7 (`P7-risks.md` §2).
8. **Future-state line:** exactly one line: "Future-state material relating to this area (N items, FS-002, FS-007 …) is held in the memory and excluded from this BRD."
9. **Questions** on anything that decides scope (`### Q-…`). If the scope changes the fence, record it in `00-brd-definition.md` → *Change log*.

## Review page
In / supporting / out lists, inputs and outputs tables, a ```layers picture of the fence, the future-state line, questions.
