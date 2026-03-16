# Phase 4: Inference

> Read `methodology/03-phases.md` → "Phase 4" for full requirements.
> Read `methodology/appendix-plotting.md` for figure standards.
> Read `methodology/04-blinding.md` for the blinding protocol.

You are building the statistical model and computing results for a
**{{analysis_type}}** analysis.

**Start in plan mode.** Before writing any code, produce a plan: what
systematics you will evaluate, what validation checks you will run, what
the artifact structure will be. Execute after the plan is set.

## Output artifacts and flow

**Both measurements and searches follow the same 4a → 4b → 4c structure:**
- **4a:** Statistical analysis — systematics, expected results. Artifact: `INFERENCE_EXPECTED.md`. No AN draft here.
- **4b:** 10% data validation. Compare to expected. Write full AN draft with 10% results. Review + PDF render. Human gate after review passes.
- **4c:** Full data. Compare to 10% and expected. Update AN with full results.

| Sub-phase | Artifact | Review |
|-----------|----------|--------|
| 4a | `exec/INFERENCE_EXPECTED.md` | 4-bot |
| 4b | `exec/INFERENCE_PARTIAL.md` + `ANALYSIS_NOTE_DRAFT.md` | 4-bot → human gate |
| 4c | `exec/INFERENCE_OBSERVED.md` | 1-bot |

## Methodology references

- Phase requirements: `methodology/03-phases.md` → Phase 4
- Technique-specific requirements: `methodology/03-phases.md` → §3.3/§3.4
- Blinding: `methodology/04-blinding.md`
- Review protocol: `methodology/06-review.md` → §6.2 (4-bot / 1-bot), §6.4
- Goodness-of-fit: `methodology/03-phases.md` → Phase 4 GoF requirements
- Plotting: `methodology/appendix-plotting.md`

## RAG queries (mandatory)

Query the experiment corpus for:
1. Systematic evaluation methods used in reference analyses
2. Published measurements for comparison (use `compare_measurements` for
   cross-experiment results)
3. Theory predictions or MC generator comparisons for the observable

Cite sources in the artifact.

## Completeness requirements (critical)

**Systematic completeness table.** Compare your implemented sources
against the reference analyses from Phase 1 and the conventions
(read all applicable files in `conventions/`).

Format:
```
| Source | Conventions | Ref 1 | Ref 2 | This analysis | Status |
```
Any MISSING source without justification is a blocker. The reviewer
will check this table row by row.

## Extraction measurement requirements

For extraction / counting measurements (double-tag, ratio, branching fraction):

- **Independent closure test (Category A if fails).** Apply the full
  extraction procedure to a statistically independent MC sample. Extract
  the quantity and compare to MC truth. The pull must be < 2sigma.
- **Parameter sensitivity table.** For each MC-derived input parameter,
  compute |dResult/dParam| x sigma_param. Flag any contributing > 5x
  the data statistical uncertainty.
- **Operating point stability.** Scan the result vs. the primary operating
  point over a range spanning at least 2x the optimized region. The
  extracted quantity should be flat within uncertainties.
- **Expected results from MC pseudo-data, not real data.** The Phase 4a
  "expected result" must be computed on MC pseudo-data — never on actual
  data counts.

## Review

**4-bot review** (4a, 4b) / **1-bot review** (4c) — see `methodology/06-review.md`
for protocol. Write findings to `review/REVIEW_NOTES.md`.
