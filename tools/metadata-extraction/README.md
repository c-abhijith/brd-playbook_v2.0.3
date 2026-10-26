# Metadata extraction: how to run and what to send back

These scripts collect the technical facts the agent needs to build the memory: what objects exist, their columns and keys, their code, what depends on what, and what actually runs. They are **read-only** (SELECT only). They return **no business data rows**: only metadata, counts and run history.

## Before you run
- **Environment:** any (dev, test or production); note which in the run notes. Do not send the same database from two environments: the agent flags duplicates and uses only one copy.
- **Account:** a read-only login. Needed rights:
  - SQL Server: `VIEW DEFINITION` on the databases. For Q6 and Q7, `VIEW SERVER STATE` (SQL Server 2022: `VIEW SERVER PERFORMANCE STATE`). For Q9 and Q10, read on `msdb` (for example `SQLAgentReaderRole`).
  - Databricks: `USE CATALOG` / `USE SCHEMA` / `SELECT` on the catalogs in scope. For D6 to D10, `SELECT` on the `system.access` and `system.lakeflow` schemas, which an admin must enable.
- Check with your client lead that exporting metadata (object names, code, run history) is allowed.

## SQL Server (SSMS): `sqlserver-metadata.sql`
1. Open the file in SSMS. Use **Results to Grid**.
2. Tick *Tools → Options → Query Results → SQL Server → Results to Grid → Quote strings containing list separators when saving .csv results*.
3. For each database in scope, run `USE [DatabaseName];` and then Q1 to Q8.
4. Once per server, run Q9 to Q11.
5. For each result: right-click the grid, choose **Save Results As…** → CSV, and use the file name shown in the query header (put the real database or server name in place of `<database>` / `<server>`).

## Databricks: `databricks-metadata.sql`
1. Open the file in the SQL editor on a SQL warehouse.
2. Replace `<catalog>` with your catalog name(s).
3. Run D1 to D10 one at a time, plus D11 if your team keeps procedure text or mappings in its own tables.
4. Download each result as CSV with the file name shown in the query header.

## Where to put the results
Put all CSV files in the workspace's sources folder under `sources/metadata/`. Next to them, add a short `metadata-run-notes.md` with:
- date and time of the run, environment (prod / copy), and who ran it
- databases, servers and catalogs covered
- any query that failed or was skipped, and why (for example "D6–D10: system tables not enabled")
- any database or catalog deliberately left out

The agent reads these files in `/brd-memory-build` (stage 2). Everything from them is marked **From evidence** and tagged **Current state**. Then run `python tools/prepare-sources/prepare_sources.py`: it splits large exports automatically.

## What each result is used for
| Result | Used for |
|---|---|
| Objects, columns, keys (Q1–Q3, D1–D2, D5) | The catalog of tables, views and procedures |
| Code (Q4, D3, D4, D11) | Business rules, logic, what each procedure reads and writes |
| Dependencies and lineage (Q5, D6, D7) | Data lineage from source to consumer |
| Usage, run history, jobs (Q6, Q7, Q9, Q10, D8–D10) | Which objects and jobs are active, inactive or unknown, and the run order |
| Row counts (Q8) | Volumes |
| Linked servers and synonyms (Q11) | Hints about upstream and downstream systems |

## Things to know
- **Dependencies (Q5)** miss dynamic SQL and don't say read vs write. The agent fills this in by reading the code.
- **Usage figures (Q6, Q7)** reset when the server restarts, and depend on the plan cache. A missing entry is not proof that something is unused, so the agent marks such objects **unknown**, not **inactive**.
- **Long code (Q4)** is split into numbered pieces so SSMS does not cut it off. Line breaks are replaced with ` \n `, which the agent restores.
- **Encrypted procedures** return no code. They still appear in Q1, and the agent will ask about them.
