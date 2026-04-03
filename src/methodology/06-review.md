## 6. Review Protocol

Review is mandatory at every phase gate. Skipping review is a process failure.

### 6.1 Classification

- **(A) Must resolve** — blocks advancement. Compile error, runtime crash,
  non-existent API, empty output, wrong behavior.
- **(B) Should address** — weakens quality. Compiler warning, missing property
  docstring, undocumented assumption, plot without units.
- **(C) Suggestions** — style, clarity, naming. Applied before commit; no re-review.

### 6.2 Review Tiers

| Phase | Type | Reviewer(s) |
|-------|------|-------------|
| 1: Design | 1-bot | Critical reviewer |
| 2: Implementation | 1-bot | Critical reviewer |
| 3: Build/Run | 1-bot | Critical reviewer |
| 4: Validation | 1-bot+plt | Critical reviewer + plot validator |
| 5: Documentation | 2-bot | Critical + constructive → arbiter |

**1-bot:** Critical reviewer only. Category A → fixer agent → re-submit.
No arbiter needed for a single reviewer.

**1-bot+plt:** Critical reviewer + plot validator in parallel. Plot validator
auto-flags empty plots and missing axis labels as Category A.

**2-bot:** Critical + constructive in parallel, then arbiter adjudicates.

### 6.3 Critical Reviewer Checklist

At every phase the critical reviewer checks:

**Phase 1 (Design):**
- [ ] Pattern choice justified against alternatives
- [ ] All collections have explicit EDM4hep types
- [ ] All properties have defaults and docstrings
- [ ] No invented API (every class/method in `conventions/gaudi_algorithm.md`)
- [ ] CMake target and link libraries specified

**Phase 2 (Implementation):**
- [ ] `DECLARE_COMPONENT` present
- [ ] No `std::cout` — Gaudi `info()`/`debug()` used
- [ ] No raw `new`/`delete`
- [ ] Data handles consistent between header and source
- [ ] All includes resolve to real headers
- [ ] CMakeLists.txt uses `gaudi_add_module`

**Phase 3 (Build/Run):**
- [ ] Zero compiler errors
- [ ] Zero unaddressed compiler warnings
- [ ] Zero ERROR/FATAL in run log
- [ ] `EvtMax` events actually processed

**Phase 4 (Validation):**
- [ ] All expected outputs present and non-empty
- [ ] At least one numeric cross-check performed
- [ ] Property variation verified

**Phase 5 (Documentation):**
- [ ] Every property has a doxygen comment
- [ ] Class-level doxygen comment present
- [ ] README covers: purpose, pattern, collections, properties, build, run

### 6.4 Plot Validator Checklist (Phase 4)

Auto-flags as Category A:
- Empty histogram (zero entries)
- Missing x-axis or y-axis label
- Missing units on axis with physical quantity
- Figure file missing from `outputs/figures/`

Flags as Category B:
- No title or overly terse filename
- Legend missing when >1 series plotted

### 6.5 Iteration Limits

- 1-bot: warn after 3 fix cycles, escalate to orchestrator after 5.
- 2-bot: warn after 3 cycles, hard cap at 7.

When the cap is reached, the orchestrator reviews the remaining issues
and decides whether to accept with documented caveats or escalate to the user.

### 6.6 Regression Protocol

If a reviewer at Phase N finds an issue traceable to Phase M < N:
1. Spawn Investigator to assess scope and create `REGRESSION_TICKET.md`.
2. Fix origin phase (Phase M) — new artifact versions, not overwrites.
3. Re-run affected downstream phases.
4. Resume review at Phase N.

Write review findings to `phase*/review/{role}/` using timestamped filenames.
