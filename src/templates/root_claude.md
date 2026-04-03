# GaudiFactory: {{name}}

**Goal:** Generate a Gaudi/k4FWCore algorithm from the user's prompt.

---

## Execution Model

**You are the orchestrator.** You do NOT write C++ code yourself. You
delegate to subagents. Your context stays small; heavy work happens in
subagent contexts.

**Progress tracking (mandatory).** Before any phase work, create a task list:

```
Phase 1: Design     — executor + 1-bot review
Phase 2: Implement  — executor + 1-bot review
Phase 3: Build/Run  — executor + 1-bot review
Phase 4: Validate   — executor + 1-bot review (critical + plot validator)
Phase 5: Document   — executor + 2-bot review
```

Mark each phase complete as it finishes.

**The orchestrator loop for each phase:**

```
1. EXECUTE  — spawn executor subagent with phase CLAUDE.md + upstream artifacts
2. REVIEW   — spawn reviewer(s) per review tier for this phase
3. CHECK    — read findings; if A/B items → fix agent → re-review; if only C → proceed
4. COMMIT   — commit phase output
5. ADVANCE  — next phase
```

**Anti-patterns:**
- Orchestrator writing C++ code directly
- Skipping the build step (Phase 3 must compile and run cleanly)
- Accepting a review PASS with unresolved A items
- Proceeding to Phase 4 if Phase 3 build/run fails

**First action:** Write the user's algorithm prompt to `prompt.md`.

---

## Methodology

| Topic | File | When |
|-------|------|------|
| Phase definitions | `methodology/03-phases.md` | Before each phase |
| Gaudi patterns | `conventions/gaudi_algorithm.md` | Phases 1 and 2 |
| Review protocol | `methodology/06-review.md` | Spawning reviewers |

---

## Phase Gates

Every phase must produce its artifact before the next phase begins.

| Phase | Required artifact | Review |
|-------|-------------------|--------|
| 1 | `phase1_design/outputs/DESIGN.md` | 1-bot (critical) |
| 2 | Source files: `src/components/*.{h,cpp}`, `options/*.py`, `CMakeLists.txt` | 1-bot (critical) |
| 3 | `phase3_build/outputs/BUILD_RUN.md` (clean build + run log) | 1-bot (critical) |
| 4 | `phase4_validation/outputs/VALIDATION.md` + figures | 1-bot (critical + plot validator) |
| 5 | Updated `README.md` + annotated header | 2-bot (critical + constructive) |

**Phase 3 is a hard gate.** If the build or run fails, fix it before
advancing — no exceptions.

---

## Review Classification

| Cat | Meaning | Action |
|-----|---------|--------|
| **A** | Blocks use (compile error, runtime crash, wrong output, non-existent API) | Fix + re-review |
| **B** | Weakens quality (compiler warning, missing docstring, undocumented property) | Fix before PASS |
| **C** | Style / clarity | Executor applies before commit |

---

## Conventions

Read `conventions/gaudi_algorithm.md` at Phases 1 and 2 (mandatory).
It specifies pattern selection, EDM4hep types, CMake targets, and
steering file structure.

---

## Git

Commit after each phase. Use conventional commit messages:
`feat(phase2): implement MyProducer algorithm`
