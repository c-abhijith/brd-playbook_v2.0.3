# Environments and duplicates

## 1. Any environment
Dev, test, UAT or production: the agent uses whatever it is given in the same way. The environment is recorded as a note (on the evidence item, the data connection and the pages that use it), never as a reason to downgrade a label.

## 2. One copy of each database
The same database must not enter the work twice, for example production `Sales` and development `Sales_DEV`. Two copies would look like two independent sources confirming each other, or like conflicts, when they are one system.

### When the check runs
At `/brd-setup` (data connections), in stage 1 of `/brd-memory-build`, in `/brd-memory-update`, and whenever a metadata export, discovery package or connection is added.

### What counts as a likely duplicate
| Signal | Example |
|---|---|
| Same database or catalog name on a different server or workspace | `Sales` on SQLPROD01 and on SQLDEV01 |
| Same name apart from an environment marker | `Sales` / `Sales_DEV` / `SalesUAT`; `prod_sales` / `dev_sales`; markers: dev, test, tst, uat, qa, sit, stg, stage, staging, preprod, pre, prod, prd, live, copy, bak, old, archive, a date |
| Same structure under any name | 80% or more of `schema.object` names in common, and matching columns for the shared tables |

### What happens
1. Stop and show both copies side by side: names, servers, export dates, object counts, overlap.
2. Ask which copy to use (`### ITEM-` question). Suggest the one that looks most complete and recent; never decide alone.
3. The chosen copy is the **primary**. The other becomes a **comparison copy**:
   - kept and registered, marked "comparison copy of <primary> — never used as evidence"
   - never queried in normal work and never cited as support for anything
   - on request, the agent can list the differences between the copies (objects only in one, changed definitions) as information
4. If the user says they are **not** duplicates (two genuinely different systems that look alike), record that decision and use both normally.
5. All decisions go into `PROJECT.md` → *Data connections* and the evidence register.
