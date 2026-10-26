---
kind: review
title: <Step in plain words>
subtitle: <One sentence: what this page asks you to check>
project: <Project name>
stage: <Setup | Memory build | Memory update | Choose BRD | Template map | Phase 1 - Overview | ... | Phase 8A - Functional BRD>
brd_name: <once chosen>
round: <N>
memory_version: <vX.Y this step was built on>
memory_notice: <only if a newer memory exists>
status: Waiting for your review
date: <YYYY-MM-DD>
platform: <SQL Server | Databricks | ...>
connections: <for example "SQL Server Sales (live) · Databricks prod_sales (relay)" | none>
genie: <In use (read-only) | Not in use>
devops: <In use (read-only) | Not available yet>
playbook_version: 2.0.3
feedback_file: feedback-<step>-r<N>.json
feedback_folder: brd-work/feedback/
---

<!--
- Plain English. Every statement: label ([[Confirmed]] / [[From evidence]] / [[Inferred]] / [[Conflicting]]),
  state tag where relevant ([[Current state]] / [[Future state]] / [[State unclear]]), and its source (EV / OBJ / LQ id, or who confirmed).
- Least certain first.
- Items needing an answer: ### heading starting with an id (Q-, CLM-, PUR-, STU-, FS-, OBJ-, GAP-, GQ-, WI-, BR-, CD-, EXT-, REL-, R-, ASM-, ITEM-).
  Each gets Agree / Correct it, a text box and an "Answered by" field.
- Blocks: ```figures (Value | label), ```flow (Step | detail), ```layers (Name | note | part, part)
- Callouts: > [!NOTE] > [!DECISION] > [!RISK] > [!PROVISIONAL] > [!CONFIRMED]
-->

## 1. Summary

```figures
<n> | <what>
<n> | <what>
<n> | <what>
```

<3–5 sentences: what this step did, what it found, what it needs from you.>

## 2. <Step-specific content>

## 3. Needs your answer

### Q-001 <question in one line>
<context with sources> · options · suggested answer and why · who could probably answer · [[Inferred]]

## 4. Data checks

<Table: LQ id | purpose | connection (live / relay / Genie) | result | as of — or "No data checks in this step.">

## 5. What changed since the last round

<Round 1: "First round.">
