# Review loop — every step that closes with APPROVED

Every such step ends with an HTML review page, feedback from people, redrafts, and a closing word typed in chat.

## 1. Closing words

| Word | Meaning |
|---|---|
| `FEEDBACK: …` | change something; the agent redrafts this step as the next round. `FEEDBACK FILE` means "read the exported feedback file" |
| `APPROVED` | the step is done: record it and stop. Optionally with the sign-off name: `APPROVED for Anna Weiss` |
| `HALT` | stop now; resume later from the same point |

- Only a chat message closes a step. Clicks in the page (Agree, Correct it) are feedback, never approval.
- `PROCEED` (from earlier versions) is not used any more. If typed, say so and ask whether the user means APPROVED or FEEDBACK.
- **Loop exit:** before accepting APPROVED, the agent states either "I have no further questions for this step" or lists what is still open, and asks: "Approve anyway, leaving these open?" The answer is recorded; open items go to phase 7 (BRD steps) or stay as open questions in the memory (memory steps).
- Who signs off is recorded by name (`people-and-confirmations.md` §5).

## 2. Writing the review page

1. Round number: from `STATUS.md` for this step (first run = round 1).
2. Write `brd-work/reviews/<step>-r<N>.md` from `templates/review-page-template.md`. Front matter: `kind: review`, title, subtitle, project, stage, brd_name (once chosen), round, `memory_version` (the version this step was built on), `memory_notice` (only if a newer memory exists), status, date, platform, `genie`, `devops`, `connections` (one line: which data connections are in use), `playbook_version: 2.0.3`, `feedback_file: feedback-<step>-r<N>.json`, `feedback_folder: brd-work/feedback/`.
3. Plain English for someone who has not read the sources. Every statement carries its label, its state tag where relevant, and its source.
4. Everything needing an answer is a `###` heading starting with an id (`Q-`, `CLM-`, `PUR-`, `STU-`, `FS-`, `OBJ-`, `GAP-`, `GQ-`, `WI-`, `BR-`, `CD-`, `EXT-`, `REL-`, `R-`, `ASM-`, `ITEM-`). The page gives each an answer box with **Agree**, **Correct it**, a text box and an **Answered by** field.
5. **Least certain first:** order questions and items by how much they matter and how unsure the agent is.
6. Copy `playbook/templates/viewer.html` to `brd-work/reviews/<step>-r<N>.html` and replace everything between the marker comments `BLUEPRINT-MARKDOWN-START` and `BLUEPRINT-MARKDOWN-END` with the page Markdown (identical text). Don't change the CSS or JavaScript. Large pages: several edits, each inserted just before the END marker. Never write `</script` inside the Markdown.
7. Never overwrite an earlier round.
8. Update `STATUS.md`: PRESENTED, round, page path, memory version used.
9. Tell the person in chat, then stop:

```
<STEP>: round N ready for your review.
Open: brd-work/reviews/<file>.html
Built on: Memory vX.Y   <+ "Newer memory vX.Z exists" if so>
Summary: <3-5 lines>
Needs you: <n questions, n items to confirm>
Data checks this step: <n queries (live / relay), longest <duration>> | none
Reply: FEEDBACK: … | APPROVED | HALT
(Or answer in the page, fill in your name, click Export review, save the file in brd-work/feedback/, then type FEEDBACK FILE.)
```

## 3. Taking feedback

Sources: the exported file (`brd-work/feedback/feedback-<step>-r<N>.json`, with `sections` and `items`, each item with `verdict`, `answer` and `answered_by`), chat, or both. If they contradict each other, ask which stands.

For each piece of feedback (`people-and-confirmations.md` explains names and Agree):
1. Apply it to the step's working files.
2. **Agree** on an item: the item is accepted as written → **Confirmed**, with the name in `answered_by` (or the reviewer's name if empty) and the date.
3. **Correct it** on an item, or a typed answer: record the answer or correction as **Confirmed** with the name and date, and update every place that used the old statement.
4. An answer that conflicts with evidence or with another person's answer: keep both, label **Conflicting** with both names, and ask once more which is right.
5. Section **Request a change:** redraft that section. Section **Agree:** leave it as it is.
6. Unclear answer: ask a short follow-up.
7. Items left as "none": stay open and come back in the next round.
8. Write the next round with a "What changed since round N" section, and stop.

If the feedback file is missing or unreadable, say so and ask the person to save it again or paste the feedback.

## 4. On APPROVED

- `STATUS.md`: APPROVED, round, signed off by (name), typed by (operator, if different), date, memory version used.
- Latest page: front matter `status:` becomes "Approved by <name> on <date>" (or "Approved by <operator>, sign-off pending" if no sign-off name was given for a document that has a named approver), and its HTML is rebuilt.
- BRD phases: copy the final content to `brd-work/brd/P<n>-<name>.md` with front matter `memory_version`, `round`, `approved_by`, `date`.
- BRD workspaces: any "Corrections the memory should receive" on the approved page are appended to `brd-work/memory-feedback.md` (`templates/memory-feedback.md`).
- Stop. Do not start the next step.

## 5. Re-running a step

- Re-running a step that was already closed creates the next round and needs closing again.
- Later steps that used it are marked `EARLIER-STEP-CHANGED` in `STATUS.md` and get a note on their next page. They are not changed automatically; the person decides what to revisit.

## 6. Long steps and resuming

- Long steps (the memory build above all) work in stages and batches with a checklist in `_progress.md`, a run budget and a heartbeat (`reading-protocol.md` §4). Each run stops cleanly after its budget; the user opens a **new chat** and runs the same command to continue. An interrupted run is detected from its heartbeat and resumed.
- After each stage, post one short progress line in chat ("Stage 2 of 8 done: 212 files read, 1,940 objects mapped").
- `/brd-status` reads `STATUS.md`, `MANIFEST.md` and `_progress.md` and shows the next command.
