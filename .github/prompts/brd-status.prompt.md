---
name: brd-status
description: Where are we - workspace type, memory in use, steps, documents, open questions, next command. Changes nothing.
agent: BRD Reconstruction
---
Read `brd-work/PROJECT.md`, `brd-work/STATUS.md`, the memory manifest and any `_progress.md`. Show, briefly:
1. Workspace type, operator, memory in use (version; newer release available in `shared-memory/`?).
2. Each step: state, round, built on which memory version, signed off by.
   For a memory build or update in progress, read `Run status` and `Last activity` in `_progress.md` and say plainly which it is:
   - **RUNNING, last activity under 15 minutes ago:** "A run is in progress (last activity <time>: <what>)."
   - **RUNNING, last activity over 15 minutes ago:** "The last run was interrupted at <time> while <what>. Nothing is running now. Open a new chat and run /brd-memory-build to resume from <file, line>."
   - **STOPPED:** "Run <n> finished (<reason>). <n of N files fully read / stage>. Open a new chat and run /brd-memory-build to continue."
   Never say "working" for a run that is not active.
3. The BRD (name, summary approved?, fence approved?), each document's latest and approved version, and any "may need revisiting" / "out of date" flags.
4. Open counters: questions, conflicts, relay files waiting, memory feedback items not yet sent.
5. The single next command.
Change nothing.
