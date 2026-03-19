## Agent Prompt Templates

Full agent definitions — role, inputs/outputs, methodology references, and
prompt templates — live in `../agents/*.md`. See `../agents/README.md` for
the index.

This appendix provides a summary of roles and context assembly rules.

Context assembly follows §3a.4 (three layers: bird's-eye framing,
relevant methodology sections, upstream artifacts). The phase CLAUDE.md
files (from `../templates/`) are what agents read at runtime; the agent
definitions in `../agents/` specify how the *orchestrator* launches agents
that will read those files.

### Agent summary

| Role | Definition | Context | Writes |
|------|-----------|---------|--------|
| Executor | `agents/executor.md` | Full methodology + RAG | `outputs/` artifacts, `../src/` code, `outputs/figures/` |
| Physics reviewer | `agents/physics_reviewer.md` | Physics prompt + artifact only | `review/physics/` |
| Critical reviewer | `agents/critical_reviewer.md` | Full methodology + RAG | `review/critical/` |
| Constructive reviewer | `agents/constructive_reviewer.md` | Full methodology + RAG | `review/constructive/` |
| Arbiter | `agents/arbiter.md` | All reviews + artifact + conventions | `review/arbiter/` |
| Typesetter | `agents/typesetter.md` | LaTeX + figures only | `outputs/ANALYSIS_NOTE.{tex,pdf}` |
| Investigator | `agents/investigator.md` | Review output + origin phase | `REGRESSION_TICKET.md` |
