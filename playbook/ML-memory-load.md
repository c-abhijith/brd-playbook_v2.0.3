# Memory load — `/brd-memory-load`

**Needs:** setup APPROVED; workspace type BRD; at least one release in `shared-memory/` · **Writes:** `PROJECT.md` (*Memory in use*), `STATUS.md` · **No review page:** one command, then a summary in chat. Rules: `memory-release.md`.

## Work
1. List the folders `shared-memory/memory-v*/`. None → "No memory release found. Ask the memory owner for the release folder and put it in shared-memory/." Stop.
2. Pick the **highest version** (compare master, then sub). If the user named a version (`/brd-memory-load v1.2`), use that one.
3. **Check the release:**
   - `RELEASE.md`, `FILES.md`, `MANIFEST.md`, `00-README.md`, `05-index.md` present
   - every file in `FILES.md` exists and ends with `<!-- end of file -->` (use search; do not read whole files)
   - `RELEASE.md` needs the same playbook **major** version as this playbook (2.x)
   If any check fails: say exactly what is wrong ("12 files missing: …", "3 files cut off: …"), do not load, and suggest asking the owner to resend the release.
4. **Record** in `PROJECT.md` → *Memory in use*: path, version, owner, published date, loaded date, loaded by. Keep a history line for earlier loads. `STATUS.md`: Memory load → LOADED vX.Y.
5. If an older release was loaded before and BRD phases were already approved on it: note that pages will show the memory notice; change nothing.

## Report in chat
```
Memory v1.3 loaded from shared-memory/memory-v1.3/ (owner: Ravi Kumar, published 2026-10-26).
Contains: 212 sources · 1,940 objects (1,512 active) · 64 flows · 38 purposes (21 confirmed) · 142 rules · 27 open questions.
Changed since v1.2: <2–4 lines from RELEASE.md>          (only if v1.2 was loaded before)
Next: /brd-choose
```
