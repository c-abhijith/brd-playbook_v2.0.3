# Phase 7 — Assumptions, risks and open questions — `/brd-p7-risks`

**Follow:** `P0-phase-rules.md` · **Closes with:** APPROVED · **Output:** `brd/P7-risks.md`

## Purpose
Make sure **nothing open is dropped**: every unresolved item from the memory, the BRD summary, the fence and phases 1–6 lands in exactly one bucket, and the client can see what the BRD rests on.

## 1. Collect every open item
From: open questions and gaps in the memory inside the fence; summary parts marked "not known yet"; borderline fence questions; open questions and gaps from phases 1–6 (including items left open at approval); Conflicting statements; important Inferred statements the documents rely on. Count them.

## 2. Sort each into exactly one bucket
| Bucket | When | Records |
|---|---|---|
| **Risk** (`R-nn`) | it could make the BRD wrong, or affect anyone relying on it | the gap behind it (linked id), impact, likelihood, affected sections of each document, who could resolve it, suggested way to close it |
| **Assumption** (`ASM-nn`) | the BRD goes ahead on the agent's best reading of the evidence | what is assumed, the evidence, what happens if wrong, who could confirm |
| **Open question** (`Q-nn`) | low impact; the BRD holds either way | the question, who could answer |

Fixed rules for summary gaps:
- **Who** or **Not included** still "not known yet" → always a **risk** (audience or boundary uncertain).
- **Where** still "not known yet" → an **assumption** ("the systems in the fence are all the systems involved").

Also always a risk: an important rule still Conflicting; a core object whose activity is Unknown; a core flow whose purpose is only Inferred.

Check: every collected item is in one bucket (show the count reconciliation: collected = risks + assumptions + open questions + closed in this phase).

## 3. Also produce
- **Business, data and process risks** visible in the evidence even without a gap: a rule with no control, a manual step, a single point of knowledge, hard-coded values, an inactive object that may still be needed.
- **Client validation list** (`people-and-confirmations.md` §6): important Inferred statements, Conflicting statements, and *Confirmed by* grouped by person.
- **Corrections the memory should receive**, collected from all phases (also in `brd-work/memory-feedback.md`).

## Review page
Reconciliation count, risks, assumptions, open questions (`### R-…`, `### ASM-…`, `### Q-…`), validation list, memory notes.
