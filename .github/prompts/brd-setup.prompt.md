---
name: brd-setup
description: Set up this workspace: type (Memory / BRD / Memory + BRD), operator, sources, scope from metadata, BRD documents, data connections tested step by step, duplicates
agent: BRD Reconstruction
---
Run **Setup** and nothing else.

Follow [00-setup.md](../../playbook/00-setup.md), [query-protocol.md](../../playbook/query-protocol.md), [environments-and-duplicates.md](../../playbook/environments-and-duplicates.md), together with [review-loop.md](../../playbook/review-loop.md), [labels-and-versions.md](../../playbook/labels-and-versions.md) and [people-and-confirmations.md](../../playbook/people-and-confirmations.md).

First read `brd-work/PROJECT.md`, `brd-work/STATUS.md` and the manifest of the memory in use, check the workspace type and the step's gate; if it is not met, tell me what is missing and stop.

Ask only who runs the workspace (a name, no role). Propose the databases, catalogs and schemas from the metadata for me to confirm; never ask for them from scratch. Test every connection step by step and tell me exactly which step fails. Never ask me for tokens or passwords.

End with the HTML review page and the review message, then stop and wait for FEEDBACK, APPROVED or HALT. Do not start any other step.
