# Arbiter Decision: Phase 5 (Documentation) Review

**Arbiter:** Phase 5 final adjudicator
**Reviews considered:** Critical review, Constructive review
**Document:** `phase5_documentation/exec/ANALYSIS_NOTE.md`
**Conventions:** `conventions/unfolding.md`

---

## Verdict: ITERATE

Minimum fixes specified below. One documentation iteration is sufficient; no new analysis code is required.

---

## Category A Adjudication

### A1 (both reviewers): BBB systematic is not a valid alternative method

**Decision: UPHELD -- but the fix is a documentation change, not new code.**

Both reviewers correctly identify that comparing a correct method (IBU) to a known-incorrect method (BBB with 25-40% diagonal fractions) does not produce a meaningful uncertainty estimate. The note itself calls BBB "an incorrect method" in Section 5.6 and then uses the difference as the dominant systematic. This is internally contradictory.

However, implementing SVD or TUnfold would require substantial new analysis code and is disproportionate for this iteration. The practical fix:

1. **Demote BBB from a systematic to a cross-check.** Move the BBB comparison entirely to Section 6 (Cross-Checks). It is already documented there as Section 6.2. Remove it from Table 5.1 and the systematic covariance matrix.
2. **Recompute the covariance matrix and all downstream quantities** (total uncertainties, correlation matrix, chi-squared values, alpha_s uncertainty) without the BBB contribution. The scripts should already support dropping a systematic source; this is a re-run, not new code.
3. **Acknowledge the gap.** Add an explicit statement in Section 5.6 (or wherever the systematic table lives after the edit): "The conventions require at least one independent valid unfolding method as a systematic. This analysis does not implement a second valid method (e.g., SVD or TUnfold). The omission is justified because: (a) IBU closure at chi2/ndf = 0.924 demonstrates correct recovery of the truth spectrum, (b) the regularization variation (+/-1 iteration) already probes residual unfolding bias, and (c) the BBB cross-check (Section 6.2) confirms that the IBU result differs substantially from an inappropriate method, as expected. A genuine alternative-method systematic is deferred to future work alongside the NLO+NLL alpha_s extraction."
4. **Update the abstract** to reflect the new dominant systematic (track momentum smearing at 2.2%) and total uncertainty.

This is the correct resolution. Calling something both "incorrect" and "the dominant systematic" is not defensible. Demoting it to a cross-check with an honest justification for the gap is what a referee would accept.

### A2 (both reviewers): Stress test documentation incomplete

**Decision: UPHELD.**

The stress test was performed and a result exists (`stress_test_results.npz`), but the note gives only a single sentence with a suspicious chi2/ndf < 0.001. This needs a dedicated subsection. Required additions:

1. Add a subsection (Section 4.6.x or Section 6.x) titled "Stress Test" with:
   - The reweighting function applied (e.g., linear tilt, quadratic, specific functional form)
   - The stress chi2/ndf value with proper context
   - An explanation of the chi2/ndf < 0.001: if this is because the statistical uncertainties from the bootstrap are large relative to the reweighting-induced shift, say so explicitly. If the reweighting was too mild, document that as a limitation.
2. Reference the existing figure (`closure_chi2_vs_iter.pdf` already shows stress test results per line 590-591 of the note).

This is a documentation fix -- the data exists, it just needs to be written up properly.

### A3 (critical only): Reference comparison uses diagonal chi2

**Decision: DOWNGRADED to Category B.**

The conventions say to use the full covariance matrix for reference comparisons. However, the published ALEPH 2004 data points were obtained by digitization and no covariance matrix is available from the publication or HEPData for the specific binning used here. Using diagonal uncertainties when the reference covariance is genuinely unavailable is standard practice. The critical reviewer's suggestion to check HEPData is reasonable but not blocking.

**Recommended (not required) fix:** Add a sentence in Section 9.2 stating that the ALEPH 2004 covariance matrix was not available from HEPData or the publication, so diagonal uncertainties were used. Note this as a limitation. If the chi2/ndf = 2.33 investigation can identify which bins drive the tension (a few sentences), that would strengthen the section.

### A4 (critical only): Degenerate alpha_s result reported in the abstract

**Decision: UPHELD in part -- remove from abstract, keep in body.**

The note already documents the degeneracy honestly (Section 7.5). The problem is that the abstract reports $\alpha_s = 0.1066 \pm 0.0113$ without the degeneracy caveat, giving it unwarranted prominence. Required fix:

1. **Remove the specific alpha_s numerical value from the abstract.** Replace with a statement like: "An indicative alpha_s extraction is attempted using LO scaling; the method is shown to be degenerate for a normalized distribution, confirming that NLO+NLL theory predictions are required for a meaningful extraction."
2. **Keep Sections 7.5 and 8.3 as-is.** The methodological demonstration is valuable and the degeneracy is clearly documented in the body text. No need to remove those sections.
3. **In the Conclusions (Section 10),** ensure the alpha_s result is presented as a methodological finding (the method doesn't work) rather than a physics result.

### A3-constructive: Condition number threshold

**Decision: UPHELD -- trivial fix.**

Change the threshold in Table 7.1 from $10^6$ to $10^{10}$ to match conventions, or add a note explaining the stricter criterion. This is a one-line edit.

---

## Summary of Required Fixes for ITERATE

These are the **minimum changes** needed to pass the next review:

| # | Fix | Scope | Effort |
|---|-----|-------|--------|
| 1 | Demote BBB from systematic to cross-check; recompute covariance/uncertainties/chi2/alpha_s without BBB | Re-run existing scripts + edit note | Medium |
| 2 | Update abstract: remove specific alpha_s value, update dominant systematic | Edit note | Small |
| 3 | Add stress test subsection with reweighting description and chi2/ndf explanation | Edit note | Small |
| 4 | Fix condition number threshold ($10^6$ to $10^{10}$) or justify stricter criterion | Edit note | Trivial |
| 5 | Acknowledge alternative-method gap explicitly with justification | Edit note | Small |

Fix #1 is the only one requiring script re-execution. Fixes #2-5 are documentation edits.

---

## Category B Items -- Not Blocking but Recommended

The following items from both reviews are valid and should be addressed if time permits, but are not required for the next gate:

- **Hadronization floor:** Consider increasing from 2% to 3% (upper end of published range) for genuine conservatism. At minimum, change the note's claim from "conservative" to "moderate" if keeping 2%.
- **Per-bin flat-prior sensitivity table:** Conventions ask for it; add to appendix.
- **Normalization convention statement:** Add one paragraph in Section 5 confirming this is a normalized measurement and that luminosity/trigger efficiency cancel.
- **Chi2 consistency:** Use post-fix covariance values consistently in Table 9.1.
- **Response matrix condition number:** Report in Table 4.1 alongside other matrix properties.
- **Sphericity axis distribution:** Add figure reference or state available in supplementary material.
- **Year-by-year chi2 values:** Report actual pairwise values, not just "approximately 1."

---

## Process Notes

The underlying measurement appears sound: IBU closure at chi2/ndf = 0.924, well-defined particle-level target, comprehensive systematic program (excluding the BBB issue). The primary problems are in how uncertainties are assigned and reported, not in the measurement itself. After removing the BBB systematic, the total uncertainties will drop substantially (dominant systematic becomes track smearing at ~2.2%), and the data/MC chi2 will increase correspondingly -- this is the honest result and should be reported as such.

The alpha_s extraction was always flagged as indicative. Removing the numerical value from the abstract is the right call; keeping the methodological demonstration in the body is fine.

After the fixes above, this note will be ready for a final check (which should be fast -- the fixes are well-scoped).
