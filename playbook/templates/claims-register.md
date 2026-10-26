# Claims, purposes, future state and relationships — formats

## Claim (`40-claims.md`)
```
### CLM-018 · Conflicting · Current state
Statement: Rebate cut-off is the 5th working day.
Sources: EV-021 Rebate guide §2.3 says 5th working day · EV-030 Operations runbook §4 says 3rd working day
Code / data check: job "Nightly rebate" runs daily; no cut-off logic found in code (EV-001) — not checkable
Question: Q-019
```

## Purpose (`30-business-map.md`)
```
### PUR-007 · Inferred · Current state
Flow / object: sales.usp_calc_rebate and job "Nightly rebate"
What it does (From evidence): calculates rebate per customer per period from paid invoices (OBJ-0042)
Why it likely exists: to pay volume rebates to customers monthly (clues: table name, Rebate guide EV-021, finance report consumer)
Confirmed by: —
```

## Future-state item (`60-future-state.md`)
```
### FS-002 · From evidence · Future state
Planned: rebates paid monthly instead of quarterly
Source: EV-044 Target design deck, slide 9
Would change: PUR-007, OBJ-0042, job "Nightly rebate"
Status: held for later stage; excluded from the BRD
```

## Relationship (`50-relationships.md`)
```
### REL-004 · From evidence · Current state
Between: rebate settlement area → finance reporting area
What: rebate_calc feeds the monthly finance extract (EV-009 lineage)
Keys: customer_id, period
Notes: candidate BRD boundary
```

## Open question (`70-open-questions.md`)
| Q | Question | Raised in | Related | Status |
|---|---|---|---|---|
