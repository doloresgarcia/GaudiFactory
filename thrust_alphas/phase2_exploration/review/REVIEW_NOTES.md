# Phase 2 Self-Review Notes

**Reviewer:** Self-review (per Phase 2 CLAUDE.md rules)
**Date:** 2026-03-15
**Artifact reviewed:** `exec/EXPLORATION.md`

---

## Checklist: Required Deliverables

### Sample Inventory (files, trees, branches, event counts)
- [x] All 6 data files listed with event counts. Total: 3,050,610.
- [x] All 40 MC files counted. Total: 771,597.
- [x] Tree names documented: `t`, `tgen`, `tgenBefore`, jet trees.
- [x] 151 branches in `t` enumerated; key branches tabulated.
- [x] pwflag encoding documented with all 7 values.

### Data Quality Assessment
- [x] Selection efficiency: data 94.7%, MC 94.6% — quantitatively compared.
- [x] Year-by-year consistency: 6 periods assessed, consistent.
- [x] "Aftercut" definition discovered: E_ch > 15 GeV and N_tracks ≥ 5 pre-applied.
- [x] Implication for systematics documented (cannot loosen E_ch cut).

### Key Variable Distributions with Figures
- [x] Thrust tau=1-T: data/MC comparison (Figure 1)
- [x] Charged multiplicity: data/MC comparison (Figure 2)
- [x] Track momentum spectrum: data/MC comparison (Figure 3)
- [x] Sphericity: data/MC comparison (Figure 4)
- [x] Year-by-year tau consistency (Figure 5)
- [x] Generator vs. reco tau scatter (Figure 6)
- [x] Response matrix prototype (Figure 7)
- [x] Reco/gen/tgenBefore comparison (Figure 8)
- Total: 8 figures (16 files: PDF + PNG each)

### Variable Ranking
- [x] Table of variables and roles provided in Section 7.

### Preselection Cutflow
- [x] Full cutflow table provided in Section 8 for data and MC.
- [x] Pre-applied cuts identified and documented.
- [x] Remaining cuts to be applied in Phase 3 quantified.

---

## Correctness Assessment

### Findings confirmed as correct:
1. **"Aftercut" definition**: confirmed by 100% pass rates on NTupleAfterCut, TotalChgEnergyMin, NTrkMin. This is consistent with the upstream filtering described in inspire:1793969 (archived ALEPH analysis paper).
2. **Thrust pre-computed**: confirmed by reading Thrust branch directly — values in [0.59, 0.999], tau=1-T in [0, 0.41] range, consistent with expected hadronic Z decay kinematics.
3. **tgen matched to t**: entry counts match (19,158 each in file -001). Tau_gen > tau_reco on average (gen has more particles, wider jets, higher tau).
4. **Response matrix needs IBU**: diagonal fractions below 50% for tau > 0.04 — confirmed numerically.
5. **Data/MC selection efficiency agreement**: 94.7% vs 94.6% — matches published ALEPH values (~94-95%).

### Potential concerns (noted but assessed as non-blocking):
1. **bFlag in MC = -999**: This will require investigation in Phase 3/4 to identify b-quark events for the heavy-flavor systematic. Documented in Section 9, item 2.
2. **One-file MC statistics**: The data/MC comparison uses only 1/40 MC files for plotting efficiency. This is appropriate for exploration. Full comparison with all 40 files is scheduled for Phase 3.
3. **Gen pwflag=-11 interpretation**: Identified as likely ISR photons/neutrinos but not definitively confirmed from pid values alone. Impact: the stored Thrust in tgen already excludes these particles (consistent with particle-level measurement definition), so this is not a blocker.

---

## Completeness Assessment

### Against Phase 2 CLAUDE.md requirements:
- [x] Sample inventory: complete
- [x] Data quality assessment: complete
- [x] Key variable distributions with data/MC comparisons: complete (8 figures)
- [x] Variable ranking: complete
- [x] Preselection cutflow: complete
- [x] Artifact on disk before Phase 3: complete

### Against strategy Phase 2 gate condition:
- [x] "Aftercut" discovery: exactly which cuts are pre-applied is now documented
- [x] Impact on systematic program documented (E_ch loosening not possible)
- [x] Strategy update required: systematic plan will substitute track energy scale variation for E_ch loosening. This is documented in Section 9, item 1 of EXPLORATION.md and in the experiment_log.

### Against convention requirements for Phase 2 (unfolding.md):
Phase 2 conventions check is not required (conventions check is required at Phase 1, Phase 4a, Phase 5). However, the response matrix characterization performed here is directly relevant to unfolding.md requirements:
- Response matrix diagnostic fractions computed: range 16-89% by tau bin (documented)
- Diagonal dominance: not achieved in most bins (< 50% for tau > 0.04) — this is expected and documented, and confirms IBU is necessary

---

## Findings: Category A (must fix before Phase 3)

None identified.

---

## Findings: Category B (should address in Phase 3 or 4a)

1. **bFlag not set in MC**: Need to find alternative b-quark identifier in MC for heavy-flavor systematic. Recommend checking `process` branch in `tgen` or generator-level quark pid.

2. **MC statistics for data/MC comparison**: Full 40-file MC comparison not yet done. Should be performed at start of Phase 3 to validate all selection variables before applying cuts.

3. **Charged energy systematic**: The pre-application of the E_ch cut must be formally documented in the Phase 3 strategy and systematic plan updated. The alternative probe (track energy scale variation) must be specified.

---

## Conclusion

The Phase 2 artifact is **complete** and meets all required deliverables. The key Phase 2 gate condition (characterizing the "aftercut" definition) is satisfied. The systematic program update required by this discovery (E_ch cut cannot be loosened) is documented. Phase 3 may proceed.
