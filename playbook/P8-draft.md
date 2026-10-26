# Phase 8 — Write the BRD documents (shared rules)

**Follow:** `P0-phase-rules.md` · **Closes with:** APPROVED, per document

| Step | Command | File | Needs |
|---|---|---|---|
| 8A Functional BRD | `/brd-p8a-functional` | `P8A-functional.md` | P7 approved |
| 8B Technical BRD | `/brd-p8b-technical` | `P8B-technical.md` | P7 approved |
| 8C Summary BRD | `/brd-p8c-summary` | `P8C-summary.md` | 8A **and** 8B approved (whichever are registered) |

8A and 8B in either order. `/brd-p8-draft` asks which document to write and then follows that file. Only the documents registered in `PROJECT.md` → *BRD documents* are written.

## Templates
- Use each document's template exactly: section order, headings, numbering, tables, required fields. Normally these are the **detailed defaults** (`templates/default-functional-template.md`, `default-technical-template.md`, `default-summary-template.md`); a client template replaces a default if one was registered.
- Map content with `brd/template-map.md`.
- **Very detailed:** every section is filled completely from the approved phases; lists are never shortened; long documents are written in batches, section by section, until complete.
- A section with no content: fill from the memory where possible (labelled); otherwise "To be completed" with the question, and it appears in the risks / open questions.
- Template instruction text ("describe here…") is removed once the section is filled.

## Content rules (all documents)
- Built only from the approved BRD definition, phases P1–P7 and P6 answers (and, for the Summary, only from the approved Functional and Technical documents). **No new facts.**
- **Current state only.** Scope carries the future-state line from phase 2.
- Every statement keeps its label and source; Confirmed items show who confirmed them. Pills in the HTML: `[[Confirmed]]`, `[[From evidence]]`, `[[Inferred]]`, `[[Conflicting]]`.
- **Same facts, same words.** A rule, figure, process step or object appearing in more than one document uses the same id (BR-, PUR-, OBJ-, R-) and the same statement; documents differ in depth and audience, never in facts.
- The cover shows the BRD name and the approved summary, the fence in one line (core count, interfaces), and the sign-off name.

## Files and versions
- `brd/functional/BRD-F_v<n>.md|.html` · `brd/technical/BRD-T_v<n>.md|.html` · `brd/summary/BRD-S_v<n>.md|.html`; one `CHANGELOG.md` per folder. First draft v1; each redraft v2, v3 … Never overwrite.
- Front matter: `kind: brd`, `document_type`, `brd_name`, `brd_version`, `memory_version`, `playbook_version: 2.0.3`, `approved_by` (sign-off name or "Pending"), the table **"Memory version per phase"**, and for the Summary `based_on: Functional vX, Technical vY`.
- Memory notice on the cover if any phase was approved on an older memory version.

## Keeping the documents in step
- A new version of one document after another was approved → `STATUS.md` marks the others **may need revisiting**, shown on their next page. Nothing changes by itself.
- Functional or Technical moving past the versions the Summary was based on → Summary **out of date** in `STATUS.md`; `/brd-p8c-summary` makes its next version.
- A correction in one document that affects shared facts is listed on the page as "Also affects: Technical 8.2, Summary 5" for the user to apply in that document's next round.

## Build (every document)
1. Write the `.md` (in batches for long documents; checklist in `brd-work/_progress-brd.md`).
2. Copy `templates/viewer.html` to the same name `.html` with the identical Markdown between the marker comments, front matter `kind: brd`.
3. The HTML is the review page. Feedback creates the next version.

## Before presenting
Optionally run `/brd-check` for this document. Self-check: every template section present or marked; everything the template map assigned is present; only fence content; no future-state description; labels on every statement; ids and statements identical to the other documents; stamps correct.

## Word and PDF
`tools/word-conversion/README.md` converts approved documents to Word (pandoc). PDF: print the HTML page.
