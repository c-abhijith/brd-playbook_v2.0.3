---
name: brd-choose
description: Choose the BRD: name and mandatory summary, then the logical fence (core, supporting, interface, out)
agent: BRD Reconstruction
---
Run **Choose the BRD** and nothing else.

Follow [10-choose-brd.md](../../playbook/10-choose-brd.md), together with [review-loop.md](../../playbook/review-loop.md), [labels-and-versions.md](../../playbook/labels-and-versions.md) and [people-and-confirmations.md](../../playbook/people-and-confirmations.md).

First read `brd-work/PROJECT.md`, `brd-work/STATUS.md` and the manifest of the memory in use, check the workspace type and the step's gate; if it is not met, tell me what is missing and stop.

One BRD per workspace: if one is already chosen, say so and stop. Never accept a name without a complete summary (What, Why and Who required; Where and Not included stated). Suggest missing parts from the memory and ask only about the gaps.

End with the HTML review page and the review message, then stop and wait for FEEDBACK, APPROVED or HALT. Do not start any other step.
