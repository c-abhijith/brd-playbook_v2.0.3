# Genie Protocol (applies to every stage when Genie is in use)

> **Playbook 2.0:** direct read-only queries through the Databricks SQL and SQL Server connections (`query-protocol.md`) are the main way to check the data. Genie is optional. When a direct connection to the same data exists, use it for facts and use Genie only where its space adds curated context; the end-of-stage verification pass (§2b) applies only when Genie is the **only** data connection. Genie is never used against a comparison copy of a duplicate database.

**Is Genie in use?** Check `brd-work/PROJECT.md` (set at /brd-setup).
- **In use (read-only):** follow this whole protocol.
- **Not in use:** skip it. Never call a Genie tool, never present anything as a Genie finding, and show on every review page: "Genie: Not in use (no access details provided). Technical facts come only from the BRD files and your answers." Fact questions go straight to the human.
- **Connection fails mid-run:** say so plainly, mark the affected questions as escalated to the human, record the failure in `brd-work/PROJECT.md`, and do not retry in a loop.

**Labels for Genie findings.** A finding that is answered and SQL-verified is labelled **From evidence** and **Current state** (Genie reads what is running). It becomes **Confirmed** only when a person confirms it. A finding that is not SQL-verified is never used as evidence.


Some of the technical facts for this BRD (tables, columns, views, stored procedures, dependencies) live in metadata tables in Databricks. A Databricks Genie space sits on top of that data and is connected to Copilot as the `genie` tool. This protocol says how to use it.

## 0. Read-only guarantee (non-negotiable, every run, every rerun)
Nothing in this playbook may modify data, objects or permissions in Databricks. First runs and reruns alike. The guarantee is enforced in four layers, so no single layer has to be trusted on its own:

1. **Databricks permissions (the real lock).** The token or service principal used by the Genie connection is read-only: `USE CATALOG`, `USE SCHEMA`, `SELECT` on the listed metadata/data tables, `CAN RUN` on the Genie space, `CAN USE` on the SQL warehouse. It has no `MODIFY`, no `CREATE`, no `ALL PRIVILEGES`, no `MANAGE`, no rights to execute procedures. Even a bad query cannot write. (Set up at /brd-setup; recorded in `brd-work/genie-config.md`.)
2. **Agent rule on questions.** Ask only questions that read: look up, list, count, describe, compare. Never ask Genie to create, change, delete, load, refresh, optimize, grant or run anything. **Never ask for a stored procedure to be called or executed**; read its stored text only.
3. **Agent rule on SQL returned.** Before accepting any answer, read the SQL. It must be read-only: `SELECT` / `WITH ... SELECT` / `SHOW` / `DESCRIBE` / `EXPLAIN` only. Reject it if it contains or implies any of: `INSERT`, `UPDATE`, `DELETE`, `MERGE`, `DROP`, `TRUNCATE`, `ALTER`, `CREATE`, `REPLACE`, `COPY INTO`, `OPTIMIZE`, `VACUUM`, `REFRESH`, `GRANT`, `REVOKE`, `CALL`, `EXEC`/`EXECUTE`, `SET` on data, or `CTAS`/`INSERT OVERWRITE`. A rejected query is verdict `SQL-NOT-READ-ONLY`.
4. **Tool rule.** The agent's tools are read files, search, edit files inside `brd-work/`, ask the user, Genie, and the read-only query tools of `query-protocol.md`. No terminal. Every identity behind a connection is read-only.

If a `SQL-NOT-READ-ONLY` query ever appears:
- Do not run it again and do not "fix" it by re-asking in a way that might still write.
- Stop the Genie work for this stage, tell the human immediately (what was asked, what SQL came back), and mark that item escalated.
- Flag it as a possible Genie-space or permissions problem to check in Databricks (was it actually executed? with what rights?).

**Reruns.** Re-running a stage, or re-verifying with Genie, repeats the same read-only questions only. Reruns never "apply", "refresh" or "repair" anything in Databricks. Because data can change between runs, every Genie entry records an **as-of** timestamp, and if a rerun returns a different answer from the earlier one, the agent reports the difference and does not silently replace the old finding (it logs a new GQ entry and flags the old one as `SUPERSEDED-BY GQ-nnn`).

## 1. What Genie is for, and what it is not

| Ask Genie (facts in data or metadata) | Ask the human (intent and decisions) |
|---|---|
| Does table/view/procedure X exist? Its columns, types, keys | Why does the business want this? |
| What does stored procedure X contain? What does it read and write? | Which of two conflicting rules is correct? |
| What depends on view X? What feeds table Y? | Scope, priority, ownership, policy |
| What distinct values, null counts, row counts, date ranges does column Z have? | Anything the data cannot show (future plans, regulation) |
| Is a rule from the BRD actually reflected in the data? | Whether a Genie finding is acceptable to the business |

Genie answers are **evidence, never decisions**. A person confirms every Genie finding before it counts as fact.

## 2. Genie-first order
Whenever the agent has a doubt that could be a fact question:
1. Read `brd-work/genie-config.md` to know where the metadata lives and what each table holds.
2. Ask Genie first.
3. If Genie answers clearly, log it (section 4) as `PENDING-CONFIRM`. Do not ask the human the same question.
4. If Genie cannot answer, errors, returns nothing, or is ambiguous, log it as `ESCALATED` and ask the human in the normal question round.
5. If the doubt is about intent or a decision, skip Genie and ask the human.

## 2b. Mandatory verification pass at the end of every stage
Only when Genie is the only data connection: besides asking when in doubt, **every stage ends with a Genie verification pass** before the stage is presented. The agent takes the technical claims the stage has just produced (objects, columns, procedure behaviour, counts, rules) and verifies each against Genie. No stage is presented without it. If a stage has no technical claims, state that explicitly.

For each item verified, record two things:

**A. Did Genie answer?**
- `ANSWERED`: a clear answer to exactly what was asked
- `PARTIAL`: answers only part, or only with caveats (say which part)
- `NOT_ANSWERED`: error, empty result, refusal, off-topic, or "cannot determine"

**B. Is the answer supported by its SQL?** Genie writes prose and SQL; the prose can be wrong even when the SQL is right, and the SQL can answer a different question. Check every answered item against the SQL Genie returned:

| 0 | **Read-only** | The SQL is `SELECT`/`WITH...SELECT`/`SHOW`/`DESCRIBE`/`EXPLAIN` only (see section 0). If this fails, stop: verdict `SQL-NOT-READ-ONLY` and escalate immediately |
| 1 | Right objects | The SQL reads the table/view/column you asked about (not a look-alike) |
| 2 | Right scope | Filters match the question (schema, project filter, date range, status flags); no accidental filter hiding rows |
| 3 | Right logic | Joins, grouping, DISTINCT, aggregation and conditions match what the question means |
| 4 | Result matches prose | Numbers and names in the answer text equal the actual result returned |
| 5 | Complete, not truncated | No unintended `LIMIT`/"top N"/sample; if there is, say so |
| 6 | Second query agrees | For HIGH facts, a differently worded query (e.g. a count) gives a consistent result |

SQL verdict:
- `SQL-VERIFIED`: checks 1-5 pass (and 6 for HIGH)
- `SQL-MISMATCH`: any check fails; state which and why
- `SQL-NOT-AVAILABLE`: Genie returned no SQL (so it cannot be verified)
- `SQL-NOT-READ-ONLY`: the SQL contains something other than a read; never used, reported to the human at once

Rules:
- Only `ANSWERED` + `SQL-VERIFIED` findings may be presented as "answered by Genie".
- `SQL-MISMATCH` or `SQL-NOT-AVAILABLE` findings are treated as **not answered**: do not use them (not even provisionally) and escalate the question to the human. Show the mismatch so the human can see it.
- `PARTIAL` findings are used only for the part that is verified; the rest is escalated.
- The SQL check is done by reading the SQL and results Genie returns, plus the second-query cross-check. If a direct Databricks SQL connection is registered, the agent may also re-run Genie's SQL itself (read-only, logged as LQ) and say so; otherwise never claim the SQL was re-executed.

## 3. How to ask Genie
- One fact per question. Name the object exactly (`catalog.schema.object`).
- Ask for the SQL it used and for counts, not only for a prose answer.
- Prefer questions about metadata tables listed in `genie-config.md` over scanning large business tables.
- For HIGH-severity facts, check twice: ask a second, differently worded question (for example a count, or the same fact from another angle) and compare. If the two disagree, log both and escalate.
- Never ask for row-level personal or sensitive data. Ask for counts, distinct values, ranges and patterns.
- Do not paste BRD text or other confidential document content into Genie questions beyond object names and the minimum needed.

## 4. Recording: `brd-work/genie-log.md`
One entry per question, written **immediately** after the answer (before asking anything else):

```
### GQ-001 · Phase 5B · HIGH · PENDING-CONFIRM
Why asked: <the doubt or gap, with GAP-/INV- ids>
Question to Genie: "<exact text>"
Genie answered?: ANSWERED | PARTIAL (<which part>) | NOT_ANSWERED (<why>)
Genie answer (plain English): <what it said, faithfully>
SQL used: <as returned by Genie>
As of: <date-time the question was asked>
SQL verification: SQL-VERIFIED | SQL-MISMATCH | SQL-NOT-AVAILABLE | SQL-NOT-READ-ONLY
  0 read-only: pass/fail · 1 objects: pass/fail · 2 scope: pass/fail · 3 logic: pass/fail · 4 result=prose: pass/fail · 5 complete: pass/fail
  Notes: <what you checked, or what failed>
Evidence: <row counts, sample of non-sensitive values, objects found>
Cross-check (query 2): <second query, its SQL, result, consistent?> / not needed (not HIGH)
Affects: <requirement, rule, object or section of the BRD>
Compared with documents: consistent | conflicts with SRC-x <loc> (-> GAP-nnn)
Human verdict: (empty until confirmed)   Correction/comment:
```

Statuses: `PENDING-CONFIRM` → `CONFIRMED` | `CORRECTED` | `REJECTED`, or `ESCALATED` (Genie could not answer; the human is asked instead).

## 5. Using findings before confirmation
- A `PENDING-CONFIRM` finding may be used in working documents only if tagged `[GENIE-PROVISIONAL GQ-nnn]`.
- It is never recorded as a final decision (`DEC`) and never closes a gap by itself. Gaps it addresses move to `RESOLVED-PENDING-CONFIRM`.
- If a finding is later `REJECTED` or `CORRECTED`, find every place tagged with that GQ id and fix it. Tell the human what changed.

## 6. Genie versus documents
If Genie contradicts a BRD document, do not pick a side and do not overwrite. Create a `CON` gap citing both, and put it in the next question round.

## 7. Safety
- Read-only use only, always (section 0). Never ask Genie to create, change, delete, load, refresh or run anything, and never to call a stored procedure.
- No credentials, tokens or connection details in any file you write.
- Treat samples as samples: a sample or a "top N" is not the full picture. Say so in the evidence line.
- Do not copy personal or sensitive row-level data into `brd-work/` files. Summarise or mask.

## 8. If Genie is unavailable
If the `genie` tool is missing, errors, or times out repeatedly: say so plainly, do not invent answers, mark the doubts `ESCALATED`, and ask the human. Do not retry in a loop.

## 9. Report every stage
At the end of each stage, in the review message, show the **Genie verification table** (one row per item verified, HIGH first):

```
| GQ | What was verified | Genie answered? | SQL verified? | Result | Your confirmation |
|----|-------------------|-----------------|---------------|--------|-------------------|
| GQ-001 | Table X has 14 columns | ANSWERED | SQL-VERIFIED | 14 columns, matches SRC-C | pending |
| GQ-002 | SP Y writes table Z | ANSWERED | SQL-MISMATCH (scope: wrong schema) | not used, escalated | n/a |
```
and one line: `Genie: asked N · answered M (SQL-verified V) · partial P · not answered K · SQL mismatches X · pending your confirmation C`.
Never present a stage with the table missing. If nothing was verifiable, say "No technical claims in this stage" and why.

Confirmation happens on each stage's review page: important findings appear as `### GQ-nnn …` headings with an answer box (Agree / Correct it); the rest in a table that the human can agree or correct section by section. The human may also confirm in chat: `CONFIRM GQ-001, GQ-004`, `REJECT GQ-002: <reason>`, `CORRECT GQ-003: <text>`. A stage that relies on a finding cannot be approved while that finding is still unconfirmed (see `review-loop.md` section 3).
