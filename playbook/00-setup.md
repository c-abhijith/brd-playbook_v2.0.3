# Setup — `/brd-setup`

**Closes with:** APPROVED · **Writes:** `brd-work/PROJECT.md`, `STATUS.md`, `query-log.md`, `brd-work/memory/MANIFEST.md` (Memory workspaces, v0), `.vscode/mcp.json` (no secrets) · **Review page:** `reviews/setup-r<N>.html`

A short conversation. Use the ask-questions tool where it helps. Save each answer to `PROJECT.md` before the next. If `PROJECT.md` already exists (setup re-run, for example when a connection becomes available), show the current values and change only what the user asks.

## Step 1 — Workspace and operator
1. **Workspace type:** Memory (build and publish the memory) · BRD (load a published memory and build one BRD) · Memory + BRD (one person does both). Explain each in one line.
2. **Project name.**
3. **Who is running this workspace?** Name only (`people-and-confirmations.md`). No role, no job title.
4. Create `brd-work/` folders (`MASTER.md` §4); copy `templates/PROJECT.md`, `templates/STATUS.md`, `templates/query-log.md`; Memory workspaces also `templates/MANIFEST.md` into `brd-work/memory/`.

## Step 2 — Sources (Memory and Memory + BRD workspaces)
First ask the user to run `python tools/prepare-sources/prepare_sources.py` (it measures and, where needed, splits every source file and writes `brd-work/index/inventory.md`). Work only from the inventory: **never open a source file to measure it**. Report what is in each folder from the inventory. Do not read content in depth yet.

| Check | If not met |
|---|---|
| Files are Markdown, CSV or JSON | list the others; ask for Markdown/CSV versions (`tools/word-conversion/README.md`) |
| The inventory exists and lists no problems | if missing, ask the user to run the prepare script; list problems (`convert first`, `too large`); setup can still close, the build will stop at them |
| Metadata exports present in `sources/metadata/` (or discovery packages in `sources/agent-memory/`) | point to `tools/metadata-extraction/README.md`; they can come later through the inbox |
| Environment of each export | ask once and record as a note; any environment is fine |

**Scope from the metadata:** read only the object lists in the exports, using files or parts with status `read` in the inventory (SQL Server Q1: `database_name`, `schema_name`; Databricks D1: `table_catalog`, `table_schema`; discovery packages: their manifests) and propose the databases, catalogs and schemas found, with object counts. The user confirms or removes; **never ask for catalogs or schemas from scratch**. If no metadata exists yet, ask the user to name them or leave them to be filled in when metadata arrives.

## Step 3 — BRD documents (BRD and Memory + BRD workspaces)
- If `sources/template/` has client templates: ask the type of each (Functional, Technical, Summary) and who signs off each document (name, optional).
- **If there are none (the normal case):** register the three detailed default templates (`templates/default-functional-template.md`, `default-technical-template.md`, `default-summary-template.md`). Ask only whether all three documents are wanted (default: yes) and who signs off each (optional).
- Record in `PROJECT.md` → *BRD documents*.

## Step 4 — Data connections (all workspace types)
For each database or catalog in scope (from step 2, or named by the user), ask how it can be reached and test it **step by step**, reporting exactly which step failed (`query-protocol.md`):

**Databricks (Databricks SQL MCP server `dbsql`)**
1. `.vscode/mcp.json` has the `dbsql` server (write it from `.vscode/mcp.dbsql.example.json` with the workspace host; the token stays `${input:dbx_token}`). → if missing: "The connection file is missing; I've written it from the example."
2. The server is started (Command Palette → *MCP: List Servers* → `dbsql` → Start; VS Code asks for the token in its own box). → if the `dbsql` tools are not available: "The dbsql server is not running or its tools are not ticked for this agent."
3. `SELECT current_user()` answers. → if it fails: show the error in plain words (no access, token expired, MCP not allowed by your organisation).
4. Rights are read-only: `SELECT privilege_type FROM <catalog>.information_schema.catalog_privileges` shows only USE CATALOG, USE SCHEMA, SELECT, BROWSE. Anything that writes → **Blocked** until fixed.
5. The registered catalogs are visible (`SHOW SCHEMAS IN <catalog>`).

**SQL Server (MSSQL extension)**
1. The `mssql_*` tools are available. → if not: "Install the SQL Server (mssql) extension (VS Code offers it from `.vscode/extensions.json`), reload, and tick its tools for this agent."
2. A connection profile exists for the database (created by the user in the SQL Server view; never ask for passwords). `mssql_connect` succeeds.
3. `mssql_get_connection_details` shows the right server **and** database.
4. Rights are read-only: `SELECT permission_name FROM fn_my_permissions(NULL,'DATABASE')` shows nothing that writes (INSERT, UPDATE, DELETE, ALTER, CREATE, EXECUTE, CONTROL…). Otherwise **Blocked**.
5. Code is visible: `SELECT COUNT(*) FROM sys.sql_modules` > 0 (otherwise VIEW DEFINITION is missing: queries still work, code must come from the export).

**Genie (optional):** as before: space ID and host in `.vscode/mcp.json` from `.vscode/mcp.genie.example.json`, server started, one harmless question with the SQL check (`genie-protocol.md`), config in `brd-work/genie-config.md`.

**Azure DevOps (optional):** `devops-protocol.md` §2–3.

If a connection cannot be made, record **Relay** for it (`query-protocol.md` §7) and continue. Log every test query.

**Duplicates:** run the check in `environments-and-duplicates.md` across all registered databases, catalogs and exports; ask about any likely duplicate before closing.

## Step 5 — Anything else
Ask once: people who are likely to answer questions (names and what they know), known areas to exclude, deadlines.

## Review page
Workspace type, operator, sources inventory (Memory workspaces), large files waiting to be split, scope proposed from metadata, BRD documents and templates, every data connection with its test steps (✓ / ✗ and the plain reason), duplicates found, people, missing items as `### ITEM-n …`. Then `review-loop.md`. Closes with **APPROVED**.

Next command shown: Memory workspace → `/brd-memory-build`; BRD workspace → `/brd-memory-load`; Memory + BRD → `/brd-memory-build`.
