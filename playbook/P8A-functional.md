# Phase 8A — Functional BRD — `/brd-p8a-functional`

**Follow:** `P8-draft.md` and `P0-phase-rules.md` · **Closes with:** APPROVED · **Output:** `brd/functional/BRD-F_v<n>.md|.html`, `brd/functional/CHANGELOG.md`

## Audience and depth
Business readers. What the business does and why, in business language, in full detail. Technology appears only to explain a step ("the nightly go-live run") and as references to the Technical BRD.

## Template (default: `templates/default-functional-template.md`)
| Section | Filled from |
|---|---|
| 0 Document control | STATUS, memory versions per phase, approvals, Confirmed-by summary |
| 1 Overview | BRD definition (name, summary), P1 |
| 2 Business context and objectives | P1, memory purposes |
| 3 Scope | P2 (fence in business words: core, supporting, hand-overs, out; current-state statement; future-state line) |
| 4 Stakeholders and users | P1, P2, people mentioned in evidence |
| 5 Business processes | P3: end-to-end picture; per process a step table (actor, trigger, input, action, output, timing, system step reference); variants, exceptions, manual steps |
| 6 Business rules and calculations | P4: every BR in plain words with exact condition and values, a worked example where evidence allows, exceptions, source, label, confirmed by |
| 7 Business data | P1, P4, memory reference data: entities in business terms, key attributes, code values and meanings |
| 8 Reports and outputs | P2 outputs, P3 |
| 9 Controls | P4 controls |
| 10 Hand-overs to other areas | P2 interface items, P3 hand-offs |
| 11 Business issues observed | P5D gaps, P5B data findings (business view), manual workarounds |
| 12 Assumptions, risks and open questions | P7 |
| 13 Client validation list | P7 |
| 14 Glossary | memory glossary inside the fence |
| A Traceability matrix | process step ↔ BR ↔ technical object (→ Technical BRD section) |
| B Evidence index | every EV, LQ, confirmation used |
