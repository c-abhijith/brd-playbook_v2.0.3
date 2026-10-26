# Reading protocol — every file, every line

The memory must hold everything that is in `sources/`. A file that is only partly read is treated as **not read**.

## 1. Why this rule exists
Copilot's file-reading tool returns a file in slices (for example "lines 1 to 100"). Reading one slice does **not** read the file. The agent must keep requesting the next range until the end of the file. Search results, file names, the first lines, or "this file looks like the previous one" are never a substitute for reading.

## 2. How to read a file
1. Read in **small consecutive ranges** from line 1, **at most 300 lines per read** (for example 1–300, 301–600 …), with no gaps.
2. Keep going until the **end of the file**: use the line count the tool reports, if it reports one; otherwise continue until a range returns no more lines.
3. Never stop early because the content seems repetitive, irrelevant or already known. Repetitive content is recorded as such in the digest, after it has been read.
4. **Read only what the inventory clears.** The list of files to read is `brd-work/index/inventory.md` and its pages, made by `tools/prepare-sources/prepare_sources.py`. Read every file and part with status `read`, in full. Never open a file to find out its size, never open a file with another status, and never open a file that is not in the inventory (ask the user to run the script again). Large files are read as their parts (`large-files.md`).
5. CSV exports are read in full too (all rows of all parts). Very regular rows can be digested in summary form (counts, objects, patterns), but only after every row has been read.

## 3. Write the digest as you go
**After every range** (not only at the end of the file), add what that range contains to the file's digest in a **small edit**, and update the ledger with the range just read. Never hold a whole file in mind and write its digest in one large edit: large edits are where runs hang. When the last range is done, mark the digest complete. The digest is `<memory>/notes/EV-nnn.md` (`templates/file-digest.md`), and keeps everything the memory may need, with line references:
- what the file is about, state (current / future / unclear), date, origin
- every system, database, table, column, procedure, job, report and interface it mentions
- every process step, business rule, threshold, calculation, exception and control
- every business term and code value, with meanings
- every claim that could be checked against code or data
- every person, team or owner mentioned
- anything unclear, contradictory or referring to missing material
- a "nothing relevant" note for sections that hold nothing useful (so it is clear they were read)

Digests are the bridge between reading and understanding: later stages build the memory from the digests and the metadata, so nothing read is lost when the chat is reset or runs out of room.

## 4. Run budget, heartbeat and resuming

**Run budget.** One run of a command reads at most the amount set in `PROJECT.md` → *Run budget* (default **150 KB of source text, about 3,000 lines**), or finishes one stage if that comes first. Then it saves everything, writes the next action in `_progress.md`, and stops with:
```
Run 3 done: 18 of 212 files fully read (stage 1). Progress saved.
To continue: open a NEW chat and run /brd-memory-build.
```
A new chat starts with an empty conversation, so long builds never overflow. It is still one command; it is simply run several times.

**Heartbeat.** At the start of a run, set `Run status: RUNNING` and `Run started` in `_progress.md`; after **every** range and every checkpoint, update `Last activity: <date time> — <file, lines>`. At a clean stop, set `Run status: STOPPED (budget reached | stage done | waiting for user)`.

**Resuming.** A run that finds `Run status: RUNNING` with `Last activity` more than 15 minutes old treats the previous run as **interrupted**: it says so, resumes the interrupted file at its first unread range (the ledger shows it), discards nothing already written, and continues.

**If a read or edit fails twice in a row,** mark that range "problem: <what happened>" in the ledger, stop the run cleanly and report it, instead of retrying in a loop.

## 5. The reading ledger: `<memory>/01-reading-ledger.md`
One row per file or part (`templates/reading-ledger.md`): evidence id, path, total lines, ranges read, **fully read (yes / no)**, digest written (yes / no), date.
- Update it after every range.
- A file is **fully read** only when the ranges cover line 1 to the last line without gaps.
- On resume (new chat or "Continue"), the ledger says exactly where to carry on.

## 6. Gates
- **Stage 1 of the memory build (and the reading step of an update) is complete only when the ledger shows every file fully read and digested**, apart from files the user explicitly excluded (recorded with name and reason) or files waiting for conversion or splitting (listed as stop-now problems).
- No later stage starts before that.
- The review page starts with **Reading coverage**: files and parts read in full / total, lines read / total, exclusions. Anything below 100% without an agreed exclusion blocks approval.

## 7. Checks
- **Self-check (stage 7):** for at least 10 files, pick content from the **second half and the last lines**, and confirm the digest and the memory reflect it. Any miss means that file is re-read and its digest redone.
- **Use check:** every digest is used by at least one memory statement, or is marked "no relevant content" with a reason. Unused digests are listed on the review page.
- **The BRD Reviewer** (`/brd-check`) re-checks a sample the same way.
