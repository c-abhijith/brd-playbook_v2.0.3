# Object card format (memory files 10-catalog/<db>.<schema>.md)

```
### OBJ-0042 · Sales.sales.usp_calc_rebate · Stored procedure · Active
Source: EV-001 (part 07, chunks 1-3), EV-003 (dependencies), EV-006 (usage) · environment: prod
Reads: sales.invoice, sales.rate_card, ref.calendar
Writes: sales.rebate_calc · UPDATE sales.invoice (rebate_flag)
Calls: sales.usp_log_run · functions: dbo.fn_fiscal_period
Called by: SQL Agent job "Nightly rebate" step 3 (EV-008)
Parameters: @period_end DATE
What it does (From evidence):
  1. Selects invoices with status = 'PAID' for the period
  2. Applies tier thresholds from rate_card (units >= 5000 → tier 2)
  3. Subtracts credit notes where doc_type = 'CN'
  4. Writes one row per customer per period; sets rebate_flag = 1 on the invoices
Business rules: BR-21 (tier threshold), BR-22 (credit notes)
Hard-coded values: 'PAID', 'CN', 5000 → 35-reference-data.md
Edge handling: nulls in rate → default 0; no error handling on missing calendar rows
Dynamic SQL / outside references: none
Activity: Active — 92 executions since 2026-09-30, last 2026-10-17 (EV-006)
Data checks: LQ-0031 (3% of customers reach tier 2, 2026-10-26)
Purpose: PUR-007 (Inferred)
Open questions: Q-012
State: Current state
```

**Tables and views** add: columns (name, type, nullable, key, description), keys and links, rules in the design (checks, defaults, computed columns), row count and date range, and a **Where used** block:

```
Where used:
| Object | Reads / writes | Conditions it applies to this table |
|---|---|---|
| OBJ-0042 usp_calc_rebate | reads, updates rebate_flag | status = 'PAID'; invoice_date in period |
| OBJ-0215 vw_rebate_statement | reads | rebate_flag = 1 |
```

**Jobs and pipelines:** steps in order, what each runs, schedule, dependencies, last run, failures.
