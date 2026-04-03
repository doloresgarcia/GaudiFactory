# GaudiFactory: Methodology Specification

## 1. Scope and Principles

This spec defines *what* each phase must produce when generating a Gaudi
algorithm package from a user prompt. The agent selects patterns, writes
code, builds, and validates within these constraints.

**Quality bar: compilable, runnable, correct code.** Every phase must meet
the standard: would a Gaudi/key4hep developer accept this as a well-written
algorithm? Not "compiles somehow" — correct, idiomatic, documented code.

**Default posture: strongest achievable implementation.** The goal is not
the first working sketch but the cleanest, most maintainable solution. When
multiple patterns exist (e.g., functional vs. traditional Algorithm), prefer
the modern k4FWCore functional approach unless the use case genuinely
requires traditional Gaudi::Algorithm. When a requirement is ambiguous,
prefer the more general, composable solution.

**Design principles:**

- **Artifacts over memory.** Each phase produces self-contained output
  files. Subsequent phases read those files, not conversation history.
- **Compile before proceeding.** Code that does not compile is not an
  artifact. Build and fix before advancing phases.
- **Review at every level.** Design, code, build output, and runtime
  behavior all reviewed before advancing.
- **Conventions over ad-hoc patterns.** Gaudi/k4FWCore idioms are in
  `conventions/gaudi_algorithm.md`. Consult at every implementation phase.
- **Downscope as last resort, don't block.** If a full implementation is
  genuinely infeasible given available dependencies, fall back gracefully
  and document the constraint.
