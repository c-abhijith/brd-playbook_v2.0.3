---
kind: brd
title: <BRD name> — Summary BRD
subtitle: The current state in brief, for decision makers
project: <Project name>
brd_name: <BRD name>
document_type: Summary
based_on: Functional v<x>, Technical v<y>
brd_version: v<n>
memory_version: <vX.Y>
status: Draft for review
date: <YYYY-MM-DD>
playbook_version: 2.0.3
prepared_by: <operator> with the BRD Reconstruction agent
approved_by: Pending
feedback_file: brd-summary-review-v<n>.json
feedback_folder: brd-work/feedback/
---

<!-- Default Summary BRD template (playbook 2.0). Built ONLY from the approved Functional and Technical BRDs at the versions in based_on.
Every statement points to the sections it summarises (→ F 6.2, T 8.1) and keeps its label. About 3–6 pages, complete enough
for a decision maker to understand the area, its risks and what is still open without reading the other two documents. -->

## 1. At a glance
The BRD name and approved summary.

```figures
<n> | <key figure, e.g. customers per month>
<n> | <key figure, e.g. business rules documented>
<n> | <key figure, e.g. open risks>
```

## 2. Business purpose and value
What the area does, for whom, and why it matters (→ F 1–2)

## 3. Scope
In · supporting · hand-overs · out, in one view (→ F 3)

## 4. Main processes
A few lines per process, and one ```flow picture (→ F 5)

## 5. Key rules and controls
The rules and controls that matter most, in plain words (→ F 6, F 9, T 8)

## 6. Systems and data
One paragraph and one picture: where it runs and the main data (→ T 2–5)

## 7. Dependencies
Hand-overs and interfaces that matter (→ F 10, T 10)

## 8. Top risks, gaps and decisions needed
| Item | Why it matters | Who must act | By when (if known) |
|---|---|---|---|

## 9. Confirmation status
What is confirmed and by whom · what is still Inferred or Conflicting · what the client still needs to validate (→ F 13)

## 10. Document set and next steps
Functional v<x>, Technical v<y> (this summary is based on them) · memory v<X.Y> · next steps
