---
name: brd-template-map
description: Read the three BRD templates (Functional, Technical, Summary) and map each section to the phases that feed it
agent: BRD Reconstruction
---
Run **Template map** and nothing else.

Follow [11-template-map.md](../../playbook/11-template-map.md), together with [review-loop.md](../../playbook/review-loop.md), [labels-and-versions.md](../../playbook/labels-and-versions.md) and [people-and-confirmations.md](../../playbook/people-and-confirmations.md).

First read `brd-work/PROJECT.md`, `brd-work/STATUS.md` and the manifest of the memory in use, check the workspace type and the step's gate; if it is not met, tell me what is missing and stop.

Read every template registered in `PROJECT.md` → BRD documents completely. Write `brd-work/brd/template-map.md`.

End with the HTML review page and the review message, then stop and wait for FEEDBACK, APPROVED or HALT. Do not start any other step.
