# Memory update — `/brd-memory-update`

**Closes with:** APPROVED → next **sub-version** · **Needs:** Memory v1.0 or later; workspace type Memory or Memory + BRD · **Writes:** memory files, `MANIFEST.md`, `changes/v<x.y>.md` · **Review page:** `reviews/memory-update-v<x.y>-r<N>.html`

In a **BRD workspace** this command is refused: "The memory here is a published release and cannot be changed. Send `brd-work/memory-feedback.md` to the memory owner; they update the memory and publish a new release."

## Purpose
Add new evidence at any time without rebuilding: new files, users' memory feedback, answers to open questions, a fresh export. **Everything in one update is one sub-version.**

## Work (same stages as the build, only for what is new)
1. **Pre-flight** (as build stage 0, from the inventory only: the user runs `tools/prepare-sources/prepare_sources.py` first): unreadable or large files, duplicates. Runs follow the same run budget and heartbeat as the build (`reading-protocol.md` §4).
2. **Find new files:** every file anywhere in `sources/` (normally `inbox/`) not in `MANIFEST.md` → *Processed source files*. None → say so and stop.
3. **Read every new file in full, digest it and register it** (build stage 1 and `reading-protocol.md`); the update continues only when the ledger shows all new files fully read. A file that replaces an older one: the older stays registered; statements it changes are marked superseded.
4. **Memory feedback files** (`memory-feedback.md` from BRD workspaces): each correction → apply as **Confirmed** with the name and date it carries (or Conflicting if it contradicts the evidence); each question → an open question (`Q-`) or a gap, with who asked.
5. **Extract and compare** (build stages 2–3 for the affected objects and areas). Sort every finding: **New** · **Changes** (old → new) · **Contradicts** (→ Conflicting, with a question) · **Confirms** (source added; Inferred stays Inferred unless a person confirmed).
6. **Gaps and data checks** (build stages 4–6) for what changed, within the query budget.
7. **Finish** (build stage 7): self-check of the changed parts, summaries, index, reader guide, end-of-file lines.
8. **Memory from playbook 1.x** (first update after copying an old memory into a 2.0 Memory workspace): add the files that are missing (`00-README.md`, `05-index.md`, `15-data-facts.md`, `35-reference-data.md`, `query-log.md`, *Where used* blocks on table cards), rewrite role-based confirmations as name-only ("Confirmed by A. Rao (Client SME)" → "Confirmed by A. Rao"), and list these as **Changes** on the page.
9. **Version:** next sub-version (v1.2 → v1.3); a higher master set by the consolidation agent is accepted (v2.0 → v2.1).

## Review page
Reading coverage of the new files, version change, files in this update, new / changes / contradicts / confirms, feedback files applied (with names), gaps closed from data, open questions (`### Q-…`, `### CLM-…`), BRD impact note ("BRD workspaces that loaded an older release will see a memory notice after loading this one"). Then `review-loop.md`.

## On APPROVED
`MANIFEST.md` new version and History row; `changes/v<x.y>.md`; files added to *Processed source files*. Next command: `/brd-memory-publish`.
