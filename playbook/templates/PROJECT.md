# Project

Written by /brd-setup; updated by later steps. Every command reads this first.

## Workspace
- Project name:
- Workspace type: Memory | BRD | Memory + BRD
- Operator (runs this workspace): <name>
- Playbook version: 2.0.3
- Set up on:

## Memory in use
- Path: brd-work/memory/ | shared-memory/memory-v<X.Y>/
- Version: v<X.Y> · owner: <name> · published: <date> · loaded: <date> by <name>
- Earlier loads: <version, date>

## Sources (Memory workspaces)
- Documents / metadata / pipelines / team BRDs / agent memory / discovery packages: <counts>
- Large files waiting to be split: <list or none>
- Query budget per build: 50
- Run budget: 150 KB of source text per run (about 3,000 lines); lower it if runs still stall

## Scope (proposed from metadata, confirmed at setup)
| Platform | Server or workspace | Database or catalog | Schemas | Objects | Environment (note) | Confirmed by |
|---|---|---|---|---|---|---|

## Data connections
| Name | Platform | Server / workspace | Database / catalog | Mode (Live / Relay / Genie) | Test result (step that failed, if any) | Status (OK / Blocked / Relay) | Duplicate group (primary / comparison copy of …) |
|---|---|---|---|---|---|---|---|

## Genie
- Status: In use (read-only) | Not in use
- Workspace host / space ID (no secrets):

## DevOps
- Status: Not available yet | In use (read-only)
- Organisation / project / mapping:

## BRD documents
| Document | Template | Sign-off (name, optional) | Latest version | Approved version |
|---|---|---|---|---|
| Functional | playbook/templates/default-functional-template.md | | | |
| Technical | playbook/templates/default-technical-template.md | | | |
| Summary | playbook/templates/default-summary-template.md | | | |

## The BRD (filled by /brd-choose; full definition in brd/00-brd-definition.md)
- BRD name:
- Chosen on memory version:

## People (names only; grows as answers come in)
| Name | Handle | Knows about |
|---|---|---|

## Exclusions and constraints
-

## Duplicate decisions
| Primary | Comparison copy | Decided by | Date |
|---|---|---|---|

## Notes
-
