# Genie configuration (filled at /brd-setup; no secrets)

The agent reads this to know where the technical metadata lives. Fill what you know; the agent asks about the rest during /brd-setup.

## Genie space
- Space name:
- Workspace host:
- MCP server name in `.vscode/mcp.json`: `genie`
- Genie space owner / contact:

## Access (read-only is mandatory)
The identity behind the Genie connection must be read-only. Record it here (names only, never secrets) and tick when confirmed in Databricks:
- [ ] Identity used (service principal / user): 
- [ ] Unity Catalog: `USE CATALOG`, `USE SCHEMA`, `SELECT` on the tables listed below, and nothing else
- [ ] No `MODIFY`, `CREATE`, `ALL PRIVILEGES`, `MANAGE`, or rights to run procedures
- [ ] Genie space: `CAN RUN` only (not `CAN MANAGE` / `CAN EDIT`)
- [ ] SQL warehouse: `CAN USE` only
- [ ] A write test was tried and failed (for example, an attempt to create a table in a scratch schema was refused)
- [ ] Confirmed by / date:

## Metadata tables (where tables, views and stored procedures are described)
| Purpose | Table (catalog.schema.table) | Key columns | Notes |
|---------|------------------------------|-------------|-------|
| Registry of tables | | | |
| Columns (name, type, nullability, description) | | | |
| Views (name, definition) | | | |
| Stored procedures (name, full text/definition) | | | |
| Dependencies / lineage | | | |
| Business glossary / descriptions (if any) | | | |

## Project scope filter
How to limit questions to this project's objects (schema names, naming prefix, a project/module column):

## Business data tables the agent may profile (counts, distinct values, ranges)
| Table | Allowed use | Sensitive columns to never sample |
|-------|-------------|-----------------------------------|

## Known quirks
(e.g. procedure text is split across several rows; deleted objects stay in the table with a flag; last-refresh date of the metadata)
