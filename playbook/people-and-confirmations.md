# People and confirmations

There are **no roles** in this playbook and no weighting: every answer counts the same. What matters is **who** gave each answer, so a reader can see it and judge.

## 1. The operator
The person running the workspace (often a developer). Recorded at `/brd-setup` as `Operator: <name>` in `PROJECT.md`. The operator runs commands and relays answers from other people. The setup asks nothing else about them.

## 2. People
`PROJECT.md` → *People* lists anyone who has answered or may answer: name, what they know about (free text), and a short handle (`@anna`). The list grows by itself: whenever an answer comes from a new name, the agent adds it. No roles, no ranking.

## 3. Every answer carries a name
| How the answer arrives | Name recorded |
|---|---|
| Chat: `Q-012: monthly run, per @anna` or `… per Anna Weiss` | that person |
| Review page: the item's **Answered by** field | that person |
| Review page with Answered by empty | the reviewer name entered on the page |
| Chat with no name | the operator |

If several answers in one message have no name and the operator might be relaying, ask once: "Who gave these answers?" (options from the people list, plus "me").

**Confirmed** is written as: `Confirmed by Anna Weiss, 2026-10-26, phase 4 round 2` (name, date, where).

## 4. Agree, Correct it, Conflicting
- **Agree** on an item = accepted as written → Confirmed, with the name and date.
- **Correct it** or a typed answer = the person's statement → Confirmed, with the name and date; every place that used the old statement is updated.
- Two people disagree, or a person disagrees with the evidence → **Conflicting**, with every name and source. The agent asks the operator who should settle it; it never picks a side.

## 5. Approvals
- `APPROVED` records **who signs off**: `APPROVED for Anna Weiss` or `APPROVED by Anna Weiss`. Without a name, the operator is recorded.
- Each BRD document (Functional, Technical, Summary) may name its approver in `PROJECT.md` → *BRD documents*. If an approval of that document comes without that name, it is recorded as "approved by <operator>, sign-off pending", and the document's cover shows it.

## 6. Client validation list (phase 7 and every document)
1. Every important statement still **Inferred**, with what it is based on.
2. Every **Conflicting** statement, with all sides.
3. **Confirmed by**: a table of every confirmed statement grouped by the person who confirmed it, so the client sees at a glance who answered what (for example items answered only by the operator).

Nothing is hidden or ranked; the reader decides.
