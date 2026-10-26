# Choose the BRD — `/brd-choose`

**Closes with:** APPROVED, only when the summary is complete and the fence is confirmed · **Needs:** a memory in use (loaded release, or approved memory in a Memory + BRD workspace) · **Writes:** `brd/00-brd-definition.md` (`templates/brd-definition.md`), `PROJECT.md` (BRD name), `STATUS.md` (phase rows) · **Review page:** `reviews/choose-brd-r<N>.html`

## One BRD per workspace
If a BRD has already been chosen here, say so and stop. A different BRD needs a new BRD workspace (it can load the same memory release).

## Part A — Name and summary (mandatory)
1. Ask for the **BRD name** and a **short summary** (3–6 sentences) covering:

   | Part | Required? | Asks |
   |---|---|---|
   | **What** | required | the business area or process |
   | **Why** | required | the business outcome it supports |
   | **Who** | required | the main users or teams |
   | **Where** | must be stated; "not known yet" allowed | systems, databases, tables already known |
   | **Not included** | must be stated; "not known yet" allowed | what is known to be out of scope |

   Show this example: *"Rebate settlement. Calculates the monthly rebate each customer earns from paid invoices and the rebate rate card, and produces the statements Finance sends out. Used by Finance and Sales Operations. Runs on the Sales database (usp_calc_rebate, rebate_calc) and the prod_sales gold layer. Does not cover invoice creation or payment collection."*
2. **If the user cannot write one:** propose 2–6 candidate BRDs from `<memory>/50-relationships.md` and `80-summaries.md` (name, what it covers, boundaries, coverage strong / partial / thin, main unknowns). The user picks one; the agent **drafts the summary** for the user to correct and confirm. A name alone is never accepted.
3. **Check the summary** part by part: present, missing, or too vague. For each missing part, **suggest it from the memory** (using the seeds of what was written), with the evidence, and ask only about the gaps (options: accept, edit, or "not known yet" where allowed).
4. **Special cases:**
   | Situation | Do |
   |---|---|
   | Too vague ("sales stuff") | offer 2–4 concrete readings from the memory and ask the user to pick |
   | Too broad (the fence would cover a large part of the system) | show the size; suggest splitting into several BRDs, each with its own summary |
   | Too narrow (one table or one report) | ask whether that is the whole BRD; show the process around it |
   | Disagrees with the memory | show both with the evidence; ask which is right; never override silently |
   | Matches nothing in the memory | warn; offer: check the name and terms · add sources (memory owner updates the memory) · go ahead with thin coverage |
   | What or Why still unknown after options | keep the step open; suggest asking someone who knows, or picking a candidate BRD |
5. Record the summary in `brd/00-brd-definition.md`, each part marked **written by <name>**, **suggested and accepted by <name>** (with evidence), or **not known yet**. Every "not known yet" becomes an open question (`Q-`) for phase 2 and, if still open in phase 7, a risk or assumption (`P7-risks.md`).

## Part B — Logical fence
Build the fence from the summary and the memory:
1. **Seeds:** key words and names from the summary (terms, processes, teams, systems, objects) matched against the memory: purposes, processes, glossary, object and column names, code values, document sections, candidate BRD areas (use `<memory>/05-index.md`).
2. **Follow the relationships** out from each seed: procedures called and calling, jobs that run them, tables read and written, views on top, upstream and downstream lineage, rules and code values used.
3. **Stop at hubs:** objects used by many unrelated areas (store master, calendar, logging, shared lookups; listed as hubs in `50-relationships.md`) are recorded but not walked through.
4. **Place everything in a ring:**
   | Ring | Meaning |
   |---|---|
   | **Core** | does this BRD's work directly |
   | **Supporting** | shared data the core needs; described only as far as it is used |
   | **Interface** | where this area hands over to another area, or receives from one |
   | **Out** | reached only through a hub, or belongs to another area |
   Inactive objects and future-state items inside the fence are listed separately.
5. For each item: **why** it is in that ring (seed, link, evidence). Borderline items become questions (`### Q-…`: "Is store re-opening after renovation in scope?").
6. Show **coverage** of the core (strong / partial / thin).
7. Optional: up to 10 read-only queries to settle borderline membership (for example whether a table still changes), logged.

## Review page
Name and summary (with where each part came from), questions on missing parts, the fence (four rings with reasons, a ```layers picture), borderline questions, coverage, connections to other areas. Then `review-loop.md`.

## Closing
- `APPROVED` is refused while What, Why or Who is missing, or a part is unanswered, or the fence has not been shown: say exactly what is missing.
- On APPROVED: save `brd/00-brd-definition.md` (name, summary, fence, memory version, approved by), the BRD name in `PROJECT.md`, phase rows in `STATUS.md`. Next command: `/brd-template-map`.

## Changing the summary or fence later
Allowed in any later step on request: record the change in the *Change log* of `00-brd-definition.md` (date, who, what, why). Pages built on the older definition show a notice; approved phases are not changed by themselves.
