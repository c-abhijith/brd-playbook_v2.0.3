---
name: brd-memory-load
description: Load the latest published memory release from shared-memory/ with one command
argument-hint: (optional) a version, for example v1.2
agent: BRD Reconstruction
---
Run **Memory load** and nothing else.

Follow [ML-memory-load.md](../../playbook/ML-memory-load.md), [memory-release.md](../../playbook/memory-release.md).

First read `brd-work/PROJECT.md`, `brd-work/STATUS.md` and the manifest of the memory in use, check the workspace type and the step's gate; if it is not met, tell me what is missing and stop.

Pick the highest version unless I named one. Check the release is complete before loading.

Report in chat what was loaded and the next command, then stop.
