# Progress (brd-work/memory/_progress.md)

Command: /brd-memory-build | /brd-memory-update | /brd-memory-publish
Run status: RUNNING | STOPPED (budget reached | stage done | waiting for user) | INTERRUPTED
Run number: <n> · Run started: <date time>
Last activity: <date time> — <what: file, lines n–m, or stage step>
Run budget: 150 KB of source text per run · used this run: <n> KB
Build started: <date> · Last checkpoint: <date time>

## Stages
| Stage | Status | Batches done | Notes |
|---|---|---|---|
| 0 Pre-flight | done / waiting for user (<what>) | — | |
| 1 Read in full and register sources | | files fully read n of N (lines n of N) | ledger: 01-reading-ledger.md |
| 2 Technical map | | n of N (by database / schema / part) | |
| 3 Business understanding | | | |
| 4 Connect and find gaps | | | |
| 5 Check the data | | queries n of budget 50 | relay file waiting: R-nnn |
| 6 Resolve | | | |
| 7 Self-check and finish files | | | |
| 8 Review page | | | round N |

## Batch checklist (current stage)
- [ ] <batch>

## Query plan (stage 5)
| Gap | Connection | Query (short) | Size check | Status |
|---|---|---|---|---|

## Next action
<exactly what to do when the command runs again>
