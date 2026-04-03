# Agent Definitions

Self-contained definitions for every agent role in the algorithm generation
pipeline. Each file is a complete, auditable specification: role, inputs,
outputs, and prompt template.

The orchestrator uses these definitions when spawning subagents.

## Executor agents

| Agent | File | Role |
|-------|------|------|
| Executor | `executor.md` | Phase execution — design, code, build, validation |
| Fixer | `fixer.md` | Targeted fixes for review findings |

## Reviewer agents

| Agent | File | Role |
|-------|------|------|
| Critical reviewer | `critical_reviewer.md` | Find all flaws in correctness and completeness |
| Constructive reviewer | `constructive_reviewer.md` | Strengthen the result — clarity, best practices |
| Plot validator | `plot_validator.md` | Visual inspection of output plots |

## Adjudication agents

| Agent | File | Role |
|-------|------|------|
| Arbiter | `arbiter.md` | Adjudicate reviews — PASS / ITERATE / ESCALATE |
| Investigator | `investigator.md` | Regression investigation and scoped fix tickets |

---

## Phase activation

### Execution pipeline

| Phase | Step 1 |
|-------|--------|
| Ph1 | executor (design) |
| Ph2 | executor (implementation) |
| Ph3 | executor (build + run) |
| Ph4 | executor (validation + plots) |
| Ph5 | executor (documentation) |

The fixer replaces the executor during ITERATE cycles at any phase.

### Review panel by phase

"x" = agent is active at that phase's review gate.

| Agent | Ph1 | Ph2 | Ph3 | Ph4 | Ph5 |
|-------|-----|-----|-----|-----|-----|
| Critical reviewer | x | x | x | x | x |
| Constructive reviewer | | | | | x |
| Plot validator | | | | x | |
| Arbiter | | | | | x |

**Critical reviewer** runs at every phase — the most important check
is always correctness (correct API, clean build, correct output).

**Plot validator** runs at Phase 4 to verify diagnostic plots have
axis labels, units, readable content, and no empty panels.

**Constructive reviewer** runs at Phase 5 to ensure documentation is
clear, complete, and usable by a new developer.

**Arbiter** runs at Phase 5 where two reviewers produce potentially
conflicting findings.

## Review panel composition

| Review tier | Phases | Parallel agents | Then |
|-------------|--------|----------------|------|
| 1-bot | 1, 2, 3 | critical | (no arbiter) |
| 1-bot+plt | 4 | critical + plot validator | (no arbiter) |
| 2-bot | 5 | critical + constructive | arbiter |

## Context assembly

Each executor subagent receives:
1. The phase CLAUDE.md (from `templates/`)
2. The user's algorithm prompt (from `prompt.md`)
3. Paths to upstream phase artifacts
4. `conventions/gaudi_algorithm.md`

Reviewer subagents receive:
1. The phase artifact to review
2. `conventions/gaudi_algorithm.md`
3. Review criteria from the phase CLAUDE.md
