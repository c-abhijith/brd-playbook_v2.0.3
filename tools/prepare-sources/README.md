# Prepare the sources (run by a person, before every build or update)

```
python tools/prepare-sources/prepare_sources.py
```
Run it from the workspace folder (the one that holds `sources/`). Needs Python 3, no extra packages. It never changes or deletes your files.

## What it does
1. **Measures every file** in `sources/` (size and lines). The agent never has to open a file to find out how big it is (that is what used to freeze it).
2. **Splits every file over 200 KB or 3,000 lines** into logical parts in `<file>.parts/`, with a **hard limit: no part over 150 KB or 2,500 lines**.
   - Splitting follows the content: a procedure, a table's rows, a document section or a job stays together whenever it fits. Something too big for one part is split at the most natural point (between rows; at sub-headings, then paragraphs; between lines) and marked "continued".
   - Reads any common encoding (UTF-8, UTF-16 as saved by SSMS, Windows-1252).
   - Files that changed since they were split are split again; unchanged ones are left alone.
3. **Writes the inventory** in `brd-work/index/`: `inventory.md` (summary and problems), `inventory-01.md` … (every file and part with size, lines and status), `inventory.json`.

The agent reads **only** files with status `read`, each in full, and never opens anything else.

## Statuses
| Status | Meaning |
|---|---|
| `read` | safe to read in full (a small file, a part, or a split index) |
| `split: do not read, read its parts` | the original of a split file |
| `lookup: search only` | which-part-holds-which-object table; searched, never read whole |
| `convert first` | Word, PDF, Excel, images…: provide Markdown or CSV (`tools/word-conversion/`) |
| `too large` | could not be split safely: the inventory says why |

## When to run it
Before the first `/brd-memory-build`, and again whenever you add or change source files (before `/brd-memory-update`). If the agent finds a file that is not in the inventory, it stops and asks you to run this again.

## If a run still stalls
Lower the limits, for example:
```
python tools/prepare-sources/prepare_sources.py --large-kb 120 --part-kb 100 --part-lines 1500
```
