# Rules for every BRD phase (1–8)

1. **Gate.** The BRD definition is approved (`brd/00-brd-definition.md` with a complete summary and a confirmed fence), the template map is approved, and the previous phase is APPROVED in `STATUS.md`. Otherwise say what is missing and stop.
2. **Inputs.** The memory in use (`<memory>`, version from its `MANIFEST.md`), the BRD definition, the template map, the approved outputs of earlier phases (`brd/P*.md`), and the evidence they cite. Use `<memory>/05-index.md` and the summaries first; open detailed memory files only where needed, and read whatever you open in full (the whole file, or the whole card or section, never a first slice; `reading-protocol.md`).
3. **Inside the fence.** Work on the **core** in full; **supporting** items only as far as the core uses them; **interface** items as hand-overs (what, to or from whom, how); nothing from **out**. Something outside the fence that seems to matter becomes a question, never silent scope growth.
4. **Current state only.** Use only Current state statements. Future-state material is never described (phase 2 adds one line noting it exists). State-unclear items that matter become questions.
5. **Labels everywhere.** Every statement shows its label and source. Never write an Inferred statement as fact.
6. **Sources, then data, then people.** For every gap: look in the memory and sources; if the data can settle it, run a read-only query (`query-protocol.md`; a few per phase, more than 10 asked first); only then ask a person. Results are From evidence with their LQ id and time.
7. **Ask well.** Questions in rounds of at most 8, each with context, evidence, options, a suggested answer and who could probably answer. Answers are recorded with the **name** of the person who gave them (`people-and-confirmations.md`).
8. **Template map.** Cover every section `brd/template-map.md` assigns to this phase, for every document, and ask the extra questions it lists. The page shows "Template sections fed by this phase" with status (covered / partly / still open).
9. **Memory version.** Stamp the page and output with the memory version used. If an earlier phase was approved on an older version, show that. Change nothing because of it.
10. **Memory feedback.** A correction to something that is also in the memory (a purpose, a rule, a relationship) is recorded in this phase as Confirmed and listed under "Corrections the memory should receive"; on APPROVED it is appended to `brd-work/memory-feedback.md` (BRD workspaces). The memory itself is never changed from a BRD workspace.
11. **Batches.** Long lists (rules, steps, objects) are written in batches until complete. Never cut a list short.
12. **Exit.** Before accepting APPROVED, state "I have no further questions for this phase" or list what is still open (`review-loop.md` §1).
13. **Output.** On APPROVED, save the phase content to `brd/P<n>-<name>.md` with front matter: memory_version, round, approved_by, date.
14. **Genie and DevOps.** If in use, they may be consulted in any phase for a specific doubt (read-only, logged). Phases 5B and 5C are the systematic passes.
