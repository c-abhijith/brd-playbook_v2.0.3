# Memory releases — build once, share, load

## 1. What a release is
A read-only copy of one **approved** memory version, in its own folder:

```
shared-memory/
  memory-v1.3/
    RELEASE.md        version, owner, date, playbook version it needs, counts, what changed since the last release, how to load
    FILES.md          every file in the release (path and number of lines)
    MANIFEST.md       the memory's manifest at this version
    00-README.md      reader guide: what each file holds, how to cite, labels, version to quote
    05-index.md       lookup: object, column, rule, term, code value, purpose → where they are described
    01-reading-ledger.md  notes/ (one digest per source file)
    00-evidence-register.md  10-catalog/  15-data-facts.md  20-lineage.md  30-business-map.md  35-reference-data.md  40-claims.md
    50-relationships.md  60-future-state.md  70-open-questions.md  80-summaries.md  query-log.md  changes/
```

Every memory file ends with the line `<!-- end of file -->`. Load uses it to check that no file was cut off when copying or zipping.

## 2. Rules
- **One owner** publishes, from the Memory workspace. Users never change a release.
- **Source files are not included.** Citations in the memory still name the evidence id and file; in a BRD workspace they are shown as "source held by the memory owner".
- **Releases are never overwritten.** A new version gets a new folder; old ones can stay or be removed by the owner.
- **No secrets, no personal data** in any release (the memory never holds them in the first place).

## 3. Sharing
Zip the workspace **without** `sources/` and `brd-work/` (so: `.github/`, `.vscode/`, `playbook/`, `tools/`, `shared-memory/`, `README.md`, `PLAYBOOK-CHANGELOG.md`) and send it. For a new version, sending just the new `shared-memory/memory-v<X.Y>/` folder is enough.

## 4. Loading (`/brd-memory-load`)
Finds the highest version in `shared-memory/`, checks it (§1 files present, every file in `FILES.md` exists and ends with the end-of-file line, `RELEASE.md` playbook version compatible: same major version), records it as the memory in use, and reports in chat. Details: `ML-memory-load.md`.

## 5. Feedback back to the owner
BRD workspaces never change the memory. Corrections found during BRD work, and questions Ask Me could not answer (when the user agrees to log them), are written to `brd-work/memory-feedback.md`. The user sends that file to the owner, who puts it in `sources/inbox/` and runs `/brd-memory-update`; the next release carries the result.
