## Agent Prompt Templates

Full agent definitions — role, inputs/outputs, methodology references, and
prompt templates — live in `../agents/*.md`. See `../agents/README.md` for
the index and phase activation matrix.

This appendix provides a summary of roles and context assembly rules.

Context assembly follows §3a.4 (three layers: bird's-eye framing,
relevant methodology sections, upstream artifacts). The phase CLAUDE.md
files (from `../templates/`) are what agents read at runtime; the agent
definitions in `../agents/` specify how the *orchestrator* launches agents
that will read those files.

### Agent summary

**Executor agents:**

| Role | Definition | Context | Writes |
|------|-----------|---------|--------|
| Executor | `agents/executor.md` | Full methodology + RAG | `outputs/` artifacts, `../src/` code, `outputs/figures/` |
| Note writer | `agents/note_writer.md` | Phase artifacts + conventions | `outputs/ANALYSIS_NOTE.md` |
| Fixer | `agents/fixer.md` | Arbiter verdict or regression ticket + existing code | Updated artifact + code |

**Reviewer agents:**

| Role | Definition | Context | Writes |
|------|-----------|---------|--------|
| Physics reviewer | `agents/physics_reviewer.md` | Physics prompt + artifact only | `review/physics/` |
| Critical reviewer | `agents/critical_reviewer.md` | Full methodology + RAG | `review/critical/` |
| Constructive reviewer | `agents/constructive_reviewer.md` | Full methodology + RAG | `review/constructive/` |
| Plot validator | `agents/plot_validator.md` | Plotting scripts + histogram data | `review/validation/` |
| BibTeX validator | `agents/bibtex_validator.md` | references.bib + web access | `review/validation/` |
| Rendering reviewer | `agents/rendering_reviewer.md` | Compiled PDF only | `review/rendering/` |

**Adjudication and specialist agents:**

| Role | Definition | Context | Writes |
|------|-----------|---------|--------|
| Arbiter | `agents/arbiter.md` | All reviews + artifact + conventions | `review/arbiter/` |
| Investigator | `agents/investigator.md` | Review output + origin phase | `REGRESSION_TICKET.md` |
| Typesetter | `agents/typesetter.md` | LaTeX + figures only | `outputs/ANALYSIS_NOTE.{tex,pdf}` |

### Review panel composition

| Review tier | Phases | Parallel agents | Sequential |
|-------------|--------|----------------|------------|
| 4-bot | 1, 4a | physics + critical + constructive + plot validator | arbiter |
| 4-bot+bib | 4b | physics + critical + constructive + plot validator + bibtex | arbiter |
| 5-bot | 5 | physics + critical + constructive + plot validator + rendering + bibtex | arbiter |
| 1-bot | 3, 4c | critical + plot validator | (check findings directly) |
| Self | 2 | executor self-check + plot validator | — |

### Execution pipeline by phase

| Phase | Step 1 | Step 2 | Step 3 |
|-------|--------|--------|--------|
| 1–3, 4a | executor | | |
| 4b | executor (stats) | note writer (draft AN) | typesetter (compile) |
| 4c | executor (stats) | note writer (update AN) | |
| 5 | executor (figures) | note writer (final AN) | typesetter (final PDF) |
