# Memory publish — `/brd-memory-publish`

**Needs:** an approved memory version in `brd-work/memory/` (Memory or Memory + BRD workspace) · **Writes:** `shared-memory/memory-v<X.Y>/` · **No review page:** confirms first, then reports in chat. Rules: `memory-release.md`.

## Work
1. Read `MANIFEST.md`. The version to publish is the current **approved** version. If an update is still in review, refuse: "Memory v1.4 is still in review; approve it first, or publish v1.3."
2. If `shared-memory/memory-v<X.Y>/` already exists: "v1.3 is already published." Stop.
3. **Confirm** with the user (ask-questions tool): version, number of files, what changed since the last published release (from `changes/`), who publishes (default: the operator, recorded as memory owner).
4. **Copy** every memory file into `shared-memory/memory-v<X.Y>/`, keeping folder structure, in batches with a checklist in `_progress.md`. Skip `_progress.md`. Make sure every copied file ends with `<!-- end of file -->`.
5. Write `RELEASE.md` (`templates/RELEASE.md`) and `FILES.md` (every file with its number of lines).
6. Record the release in `MANIFEST.md` → *Releases* and in `STATUS.md`.

## Report in chat
```
Memory v1.3 published: shared-memory/memory-v1.3/ (148 files).
To share: zip this workspace without sources/ and brd-work/ (or send only shared-memory/memory-v1.3/ to people who already have the playbook).
Users load it with /brd-memory-load.
```
