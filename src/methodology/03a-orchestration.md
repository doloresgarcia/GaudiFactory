## 3a. Orchestration and Agent Architecture

---

### 3a.1 Orchestrator Architecture

The orchestrator is a **thin coordinator** — it spawns subagents, reads
summaries, makes phase-transition decisions, and commits. It never writes
C++ code, builds, or debugs. Subagent contexts are discarded after each
phase; the orchestrator stays small.

**The orchestrator loop** is EXECUTE → REVIEW → CHECK → COMMIT → ADVANCE.

**Review is always by subagent.** The orchestrator does not self-review code.

**Anti-patterns:**
- Orchestrator writing C++ code directly
- Skipping the build/run phase (Phase 3 is mandatory)
- Accepting a PASS with unresolved Category A items
- Proceeding to Phase 4 if Phase 3 failed

---

### 3a.2 Subagent Roles and Context

Subagents are **executors** or **reviewers**. Each receives curated context
(§3a.4). See `agents/README.md` for the phase activation matrix.

**Executors** receive the phase CLAUDE.md, upstream artifacts, and
`conventions/gaudi_algorithm.md`. They work plan-then-code: design or
implementation plan first, then code, then artifact.

**Reviewers:**

| Role | Context | Goal |
|------|---------|------|
| Critical reviewer | Phase artifact + conventions | Find all correctness and completeness flaws |
| Constructive reviewer | Phase artifact + conventions | Strengthen clarity, best practices |
| Plot validator | Phase 4 figures | Empty plots, missing labels — Category A |
| Arbiter | All reviews + artifact + conventions | PASS / ITERATE / ESCALATE |

---

### 3a.3 Health Monitoring

- **Commit before spawning** each subagent (checkpoint).
- **Monitor agent progress.** If an agent produces no output for a sustained
  period, check logs before respawning.
- **Session logs survive crashes.** Every agent writes an incremental session
  log to `phase*/logs/`. If an agent is terminated, check the log to
  understand progress before respawning.

---

### 3a.4 Context Management

**Artifacts are the only handoff.** No conversation history, no shared
variables. Each session starts from artifacts + instructions.

**Three context layers per agent:**

1. **Framing (~0.5 page):** the algorithm prompt, current phase, end goal
   (compilable, validated Gaudi algorithm).
2. **Relevant methodology sections:**

| Role | Sections to include |
|------|---------------------|
| Phase 1 executor | §1, §2, §3 Phase 1, `conventions/gaudi_algorithm.md` |
| Phase 2 executor | §3 Phase 2, §5, §11, `conventions/gaudi_algorithm.md` |
| Phase 3 executor | §3 Phase 3, §5, §7 |
| Phase 4 executor | §3 Phase 4, §5, §7 |
| Phase 5 executor | §3 Phase 5, §5 |
| Critical reviewer | §6, applicable phase from §3, `conventions/gaudi_algorithm.md` |
| Plot validator | §6.4 |
| Arbiter | §6, `conventions/gaudi_algorithm.md` |

3. **Upstream artifacts:** prior phase artifacts. Pass paths — subagent
   reads from disk.

---

### 3a.5 Parallelism

The five phases are sequential — each depends on the prior. Within Phase 4,
plot generation for multiple output types can be parallelised (separate
subagent per output collection). Within review, multiple reviewer roles run
in parallel before the arbiter.
