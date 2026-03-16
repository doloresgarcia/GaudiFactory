# Phase 2: Exploration

> Read `methodology/03-phases.md` → "Phase 2" for full requirements.
> Read `methodology/appendix-plotting.md` for figure standards.

You are exploring the data and MC samples for a **{{analysis_type}}** analysis.

**Start in plan mode.** Before loading any data, produce a plan: which files
to inspect first, what variables to survey, what plots to make. Execute
after the plan is set.

## Output artifact

`exec/EXPLORATION.md` — sample inventory, data quality assessment, key
variable distributions, variable ranking, and preselection cutflow.

## Methodology references

- Phase requirements: `methodology/03-phases.md` → Phase 2
- Plotting: `methodology/appendix-plotting.md`
- Coding: `methodology/11-coding.md`

## RAG queries (mandatory)

Query the experiment corpus for:
1. Standard object definitions for this experiment (lepton ID, jet clustering, etc.)
2. Known data quality issues or detector effects relevant to the observables

Cite sources in the artifact.

## Data discovery

Expect to discover the data format at runtime. To avoid wasting time/memory:
1. **Metadata first.** Inspect tree names, branch names, types before loading.
2. **Small slice of scalars.** Load ~1000 events of scalar branches first.
3. **Identify jagged structure.** Determine which branches are variable-length
   before bulk loading.
4. **Document the schema.** The discovered structure is artifact content.

## PDF build test

At the end of this phase, run a stub PDF build to verify the toolchain:
1. Create a minimal `phase5_documentation/exec/ANALYSIS_NOTE.md` with a
   title, one section heading, and one figure reference
2. Run `pixi run build-pdf`
3. Fix any issues (missing packages, broken pandoc flags) now

This catches toolchain problems early — not in Phase 5.

## Rules

- Prototype on small subsets (~1000 events). Do not process full data to
  "see what's there."
- Append findings to experiment_log.md as you go.

## Review

**Self-review.** Explicitly check: sample inventory complete? Data quality
checked? Experiment log updated? Distributions look physical?
Write findings to `review/REVIEW_NOTES.md`.
