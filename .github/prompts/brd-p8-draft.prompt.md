---
name: brd-p8-draft
description: Phase 8 - asks which BRD document to write (Functional, Technical or Summary), then writes it
agent: BRD Reconstruction
---
Run **BRD phase 8 (one document)** and nothing else.

Follow [P0-phase-rules.md](../../playbook/P0-phase-rules.md), [P8-draft.md](../../playbook/P8-draft.md), together with [review-loop.md](../../playbook/review-loop.md), [labels-and-versions.md](../../playbook/labels-and-versions.md) and [people-and-confirmations.md](../../playbook/people-and-confirmations.md).

First read `brd-work/PROJECT.md`, `brd-work/STATUS.md` and the manifest of the memory in use, check the workspace type and the step's gate; if it is not met, tell me what is missing and stop.

Look at `PROJECT.md` → BRD documents and `STATUS.md`. If more than one document can be written now, ask me which one, then follow its file (`P8A-functional.md`, `P8B-technical.md` or `P8C-summary.md`). If only one can, say which and write it.

End with the HTML review page and the review message, then stop and wait for FEEDBACK, APPROVED or HALT. Do not start any other step.
