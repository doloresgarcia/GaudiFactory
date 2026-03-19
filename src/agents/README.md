# Agent Definitions

Self-contained definitions for every agent role in the analysis pipeline.
Each file is a complete, auditable specification: role, inputs, outputs,
methodology references, and prompt template.

The orchestrator uses these definitions when spawning subagents.

| Agent | File | Role |
|-------|------|------|
| Executor | `executor.md` | Phase execution — code, figures, artifacts |
| Physics reviewer | `physics_reviewer.md` | Senior collaboration member review ("would I approve?") |
| Critical reviewer | `critical_reviewer.md` | Find all flaws in correctness and completeness |
| Constructive reviewer | `constructive_reviewer.md` | Strengthen the analysis — clarity, validation, presentation |
| Arbiter | `arbiter.md` | Adjudicate reviews — PASS / ITERATE / ESCALATE |
| Typesetter | `typesetter.md` | LaTeX expert for Phase 5 PDF production |
| Investigator | `investigator.md` | Regression investigation and scoped fix tickets |

## Context assembly

Context assembly follows §3a.4 (three layers: bird's-eye framing,
relevant methodology sections, upstream artifacts). The phase CLAUDE.md
files (from `templates/`) are what agents read at runtime; these
definitions specify how the *orchestrator* launches agents that will
read those files.
