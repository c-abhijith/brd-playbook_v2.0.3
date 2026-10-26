---
name: brd-memory-build
description: Build the whole memory with one command: read, understand, connect, find gaps, check the data read-only, resolve, self-check, then one review page
agent: BRD Reconstruction
---
Run **Memory build** and nothing else.

Follow [MB-memory-build.md](../../playbook/MB-memory-build.md), [reading-protocol.md](../../playbook/reading-protocol.md), [query-protocol.md](../../playbook/query-protocol.md), [large-files.md](../../playbook/large-files.md), [environments-and-duplicates.md](../../playbook/environments-and-duplicates.md), together with [review-loop.md](../../playbook/review-loop.md), [labels-and-versions.md](../../playbook/labels-and-versions.md) and [people-and-confirmations.md](../../playbook/people-and-confirmations.md).

First read `brd-work/PROJECT.md`, `brd-work/STATUS.md` and the manifest of the memory in use, check the workspace type and the step's gate; if it is not met, tell me what is missing and stop.

Run the stages one after another without stopping for review, with a checkpoint in `brd-work/memory/_progress.md` and one progress line in chat after each stage. If a checkpoint exists, continue from it. Work only from `brd-work/index/inventory.md`: never open a source file to measure it and never open one whose status is not `read`; if the inventory is missing or out of date, ask me to run `python tools/prepare-sources/prepare_sources.py`. Read every source file in full (consecutive ranges to the last line; one slice is not a read), write its digest and update the reading ledger before the next file; stage 1 ends only at 100% coverage. Interrupt me only for the stop-now questions of stage 0. Stay within the query budget.

End with the HTML review page and the review message, then stop and wait for FEEDBACK, APPROVED or HALT. Do not start any other step.
