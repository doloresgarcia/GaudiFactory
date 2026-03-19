# Agent Definitions

Self-contained definitions for every agent role in the analysis pipeline.
Each file is a complete, auditable specification: role, inputs, outputs,
methodology references, and prompt template.

The orchestrator uses these definitions when spawning subagents.

## Executor agents

| Agent | File | Role |
|-------|------|------|
| Executor | `executor.md` | Phase execution — plan, code, figures, artifacts |
| Note writer | `note_writer.md` | AN prose — reads artifacts, writes the analysis note |
| Fixer | `fixer.md` | Targeted fixes for review findings and regression tickets |

## Reviewer agents

| Agent | File | Role |
|-------|------|------|
| Physics reviewer | `physics_reviewer.md` | Senior collaboration member review ("would I approve?") |
| Critical reviewer | `critical_reviewer.md` | Find all flaws in correctness and completeness |
| Constructive reviewer | `constructive_reviewer.md` | Strengthen the analysis — clarity, validation, presentation |
| Plot validator | `plot_validator.md` | Programmatic validation of plotting code and histogram data |
| BibTeX validator | `bibtex_validator.md` | Verify citations resolve to real, accurate bibliographic records |
| Rendering reviewer | `rendering_reviewer.md` | PDF compilation and rendering inspection |

## Adjudication agents

| Agent | File | Role |
|-------|------|------|
| Arbiter | `arbiter.md` | Adjudicate reviews — PASS / ITERATE / ESCALATE |
| Investigator | `investigator.md` | Regression investigation and scoped fix tickets |

## Specialist agents

| Agent | File | Role |
|-------|------|------|
| Typesetter | `typesetter.md` | LaTeX expert for PDF production |

## Phase activation

### Execution agents

| Agent | Ph1 | Ph2 | Ph3 | Ph4a | Ph4b | Ph4c | Ph5 |
|-------|-----|-----|-----|------|------|------|-----|
| Executor | strategy | explore | selection | stats | stats | stats | figures |
| Note writer | | | | | draft AN | update AN | final AN |
| Typesetter | | | | | compile draft | | final PDF |
| Fixer | on ITERATE | — | on ITERATE | on ITERATE | on ITERATE | on ITERATE | on ITERATE |

Phase 4b execution is three sequential steps: executor (statistical
analysis) → note writer (draft AN from artifacts) → typesetter (compile
PDF for human gate review). Phase 4c: executor → note writer. Phase 5:
executor (figures) → note writer (final AN) → typesetter (final PDF).

### Review agents

| Agent | Ph1 | Ph2 | Ph3 | Ph4a | Ph4b | Ph4c | Ph5 |
|-------|-----|-----|-----|------|------|------|-----|
| Physics reviewer | 4-bot | | | 4-bot | 4-bot | | 5-bot |
| Critical reviewer | 4-bot | | 1-bot | 4-bot | 4-bot | 1-bot | 5-bot |
| Constructive reviewer | 4-bot | | | 4-bot | 4-bot | | 5-bot |
| Plot validator | | self | 1-bot | 4-bot | 4-bot | 1-bot | 5-bot |
| BibTeX validator | | | | | 4-bot | | 5-bot |
| Rendering reviewer | | | | | | | 5-bot |
| Arbiter | 4-bot | | | 4-bot | 4-bot | | 5-bot |

**Plot validator** runs at every phase that produces figures (Phases 2-5).
At Phase 2 (self-review), it runs alongside the executor's self-check.
At Phase 1, it is skipped unless the executor produced figures.

**BibTeX validator** runs at phases that produce an AN with citations
(4b draft, 5 final). It verifies DOIs, arXiv IDs, and INSPIRE records
actually resolve to the expected papers — catching hallucinated entries.

**Rendering reviewer** runs only at Phase 5 where the final PDF is the
deliverable. At Phase 4b, the typesetter's compilation serves as the
rendering check.

## Review panel composition

| Review tier | Agents (parallel) | Then |
|-------------|-------------------|------|
| 4-bot | physics + critical + constructive + plot validator | arbiter |
| 4-bot+bib | physics + critical + constructive + plot validator + bibtex validator | arbiter |
| 5-bot | physics + critical + constructive + plot validator + rendering + bibtex validator | arbiter |
| 1-bot | critical + plot validator | (no arbiter — check findings directly) |
| Self | executor self-check + plot validator | (Phase 2 only) |

## Context assembly

Context assembly follows §3a.4 (three layers: bird's-eye framing,
relevant methodology sections, upstream artifacts). The phase CLAUDE.md
files (from `templates/`) are what agents read at runtime; these
definitions specify how the *orchestrator* launches agents that will
read those files.
