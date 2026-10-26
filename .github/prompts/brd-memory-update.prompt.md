---
name: brd-memory-update
description: Add new sources or memory feedback files to the memory (one sub-version), with the same stages as the build
agent: BRD Reconstruction
---
Run **Memory update** and nothing else.

Follow [MU-memory-update.md](../../playbook/MU-memory-update.md), [reading-protocol.md](../../playbook/reading-protocol.md), [query-protocol.md](../../playbook/query-protocol.md), [large-files.md](../../playbook/large-files.md), [environments-and-duplicates.md](../../playbook/environments-and-duplicates.md), together with [review-loop.md](../../playbook/review-loop.md), [labels-and-versions.md](../../playbook/labels-and-versions.md) and [people-and-confirmations.md](../../playbook/people-and-confirmations.md).

First read `brd-work/PROJECT.md`, `brd-work/STATUS.md` and the manifest of the memory in use, check the workspace type and the step's gate; if it is not met, tell me what is missing and stop.

Work only from `brd-work/index/inventory.md`: never open a source file to measure it and never open one whose status is not `read`; if the inventory is missing or out of date, ask me to run `python tools/prepare-sources/prepare_sources.py`. Refuse in a BRD workspace and explain how memory feedback reaches the owner. Everything in this update is one sub-version.

End with the HTML review page and the review message, then stop and wait for FEEDBACK, APPROVED or HALT. Do not start any other step.
