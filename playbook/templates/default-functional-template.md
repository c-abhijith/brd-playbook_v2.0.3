---
kind: brd
title: <BRD name> — Functional BRD
subtitle: How the business process works today, reconstructed from existing systems, documents and data
project: <Project name>
brd_name: <BRD name>
document_type: Functional
brd_version: v<n>
memory_version: <vX.Y>
memory_notice: <only if a newer memory exists>
status: Draft for review
date: <YYYY-MM-DD>
platform: <platforms>
playbook_version: 2.0.3
prepared_by: <operator> with the BRD Reconstruction agent
approved_by: Pending
feedback_file: brd-functional-review-v<n>.json
feedback_folder: brd-work/feedback/
---

<!-- Default Functional BRD template (playbook 2.0). Fill every section completely from the approved phases; never shorten lists.
Every statement carries its label ([[Confirmed]] / [[From evidence]] / [[Inferred]] / [[Conflicting]]) and source. Current state only.
Write long sections in batches. Remove these instruction comments as sections are filled. -->

## 0. Document control
- Document versions table: version · date · what changed · memory version · approved by
- Memory version per phase: P1 … P7, each with the version it was approved on
- Related documents: Technical BRD v<x>, Summary BRD v<y>
- Confirmed-by summary: number of confirmed statements per person

## 1. Overview
- BRD name and the approved summary (What, Why, Who, Where, Not included)
- Purpose of this document and who should read it
- How it was produced (sources, memory version, data checks), in three or four lines

## 2. Business context and objectives
- The business area and what it exists to do
- The business problem or need it serves
- Objectives and measures seen in the evidence (volumes, deadlines, service levels), each with its source

## 3. Scope
### 3.1 In scope (core)
Processes, flows, data and reports covered, in business words
### 3.2 Supporting data
Shared data the process uses, and which part of it
### 3.3 Hand-overs (interfaces)
Where the process hands over to, or receives from, other areas
### 3.4 Out of scope
What is excluded and why
### 3.5 Current-state statement
"This document describes the process as it runs today." · Future-state line from phase 2

## 4. Stakeholders and users
| Team or group | What they do in the process | What they use or receive | Source |
|---|---|---|---|

## 5. Business processes
### 5.1 End-to-end view
One ```flow picture of the whole process
### 5.2 Process list
| Process | Purpose | Trigger | Frequency | Owner (if known) |
|---|---|---|---|---|
### 5.3 Process details (one sub-section per process)
| Step | Actor | Trigger | Input | What happens | Output | Timing | System step (→ Technical BRD) | Label |
|---|---|---|---|---|---|---|---|---|

Variants (month-end, corrections, reruns, late data) · Exceptions and how they are handled · Manual steps (clearly marked)

## 6. Business rules and calculations
One entry per rule, grouped by process:
```
BR-21 · Tier threshold · [[Confirmed]] by <name>, <date>
Rule: Customers buying 5,000 units or more in a month earn the tier-2 rebate rate.
Condition and values: units in the month >= 5,000 → tier 2; otherwise tier 1
Worked example: 5,240 units × 3.5% tier-2 rate on €48,200 = €1,687
Exceptions: credit notes are subtracted before the tier is decided (BR-22)
Source: procedure step (→ Technical BRD 8.1), Rebate guide §2.3, data check LQ-0031
```

## 7. Business data
### 7.1 Business entities
| Entity | Meaning | Key attributes | Where it comes from |
|---|---|---|---|
### 7.2 Code values
| Code list | Value | Meaning | How often used (data check) |
|---|---|---|---|

## 8. Reports and outputs
| Output | Content | Audience | Frequency | Produced by (process step) |
|---|---|---|---|---|

## 9. Controls
| Control | What it checks | Protects rule | When | Who acts on it |
|---|---|---|---|---|
Rules without a control, and controls without a clear rule

## 10. Hand-overs to other areas
| Direction | Other area or team | What is passed | When | Agreed owner of the data |
|---|---|---|---|---|

## 11. Business issues observed
Gaps, inconsistencies between documents and the system, manual workarounds, data quality issues that affect the business (with evidence)

## 12. Assumptions, risks and open questions
### 12.1 Risks
| R | Risk | Gap behind it | Impact | Likelihood | Affected sections | Who could resolve | Suggested action |
|---|---|---|---|---|---|---|---|
### 12.2 Assumptions
| ASM | We assume | Evidence | If wrong | Who could confirm |
|---|---|---|---|---|
### 12.3 Open questions
| Q | Question | Who could answer |
|---|---|---|

## 13. Client validation list
### 13.1 Important statements still Inferred
### 13.2 Conflicting statements
### 13.3 Confirmed by
| Person | Statements confirmed (ids) |
|---|---|

## 14. Glossary
| Term | Meaning | Used in |
|---|---|---|

## Appendix A. Traceability matrix
| Process step | Business rule(s) | Technical object(s) | Technical BRD section |
|---|---|---|---|

## Appendix B. Evidence index
| Id | Source | Used in sections |
|---|---|---|
