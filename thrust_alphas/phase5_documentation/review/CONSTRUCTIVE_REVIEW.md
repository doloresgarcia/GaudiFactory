# Constructive Review: Phase 5 Analysis Note

**Reviewer role:** Constructive reviewer (clarity, presentation, completeness, reproducibility)
**Document reviewed:** `phase5_documentation/exec/ANALYSIS_NOTE.md`
**Conventions consulted:** `conventions/unfolding.md`

---

## Overall Assessment

The analysis note is well-structured, thorough, and broadly meets the standard expected for a journal-quality document. The particle-level definition is precise, the event selection is well-documented with per-cut efficiencies, the systematic program is complete relative to conventions (with documented limitations), and machine-readable results are provided. The note is honest about its limitations (single MC generator, LO alpha_s extraction, digitized reference comparisons) and does not overstate its results.

Several issues need attention, ranging from a potential methodological concern about the dominant systematic to presentation improvements that would strengthen the document for external review.

---

## Findings

### (A) Must Resolve

**A1. The BBB "alternative method" systematic is methodologically questionable and dominates the entire error budget.**

The BBB vs. IBU difference (up to 21%) is taken as a systematic uncertainty on the unfolding method. However, as the note itself acknowledges (Section 5.6), BBB is the *wrong* method for this measurement given the off-diagonal migration structure. Using the difference between a correct method and a known-incorrect method as a systematic uncertainty is not standard practice -- it inflates the uncertainty without probing a genuine source of ignorance. The conventions (`conventions/unfolding.md`) require "at least one independent unfolding method" as a cross-check, but the intent is to compare two *valid* methods (e.g., IBU vs. SVD, or IBU vs. TUnfold matrix inversion), not a valid method vs. an inapplicable one.

The consequence is severe: the BBB systematic drives the correlation matrix to near-rank-1 (all correlations > 0.98), which artificially deflates the effective degrees of freedom in the chi-squared fit and makes the covariance matrix difficult to interpret physically. The alpha_s uncertainty is also dominated by this single source.

**Recommendation:** Either (a) replace the BBB comparison with a genuine alternative method (SVD unfolding via a different package, or IBU with a substantially different implementation), or (b) retain BBB as a *cross-check* (Section 6) but remove it from the systematic budget, replacing it with a more targeted unfolding uncertainty (e.g., variation of the number of iterations beyond +/-1, or response matrix reweighting). If neither is feasible, the note must clearly state that the total uncertainty is a conservative upper bound and provide a "without BBB" uncertainty column in Table 5.1 and Table 8.1 so readers can assess the measurement precision excluding this inflated contribution.

**A2. Stress test result is not adequately documented.**

Section 10.1 mentions a stress test with chi-squared/ndf < 0.001, which is suspiciously small -- a value this low suggests the test may be trivial (e.g., reweighting by a factor close to 1.0) or that the chi-squared was computed incorrectly. The conventions require showing "closure chi2/ndf and stress chi2/ndf vs. regularization strength" (Section on Reporting under Regularization). The stress test is mentioned in passing in Section 4.6 (listed as a criterion) but no dedicated results are shown: no table of stress chi-squared vs. iteration count, no description of what reweighting was applied, no figure. A referee would flag this omission.

**Recommendation:** Add a dedicated stress test subsection (or expand Section 4.6) with: the reweighting function applied, the stress chi-squared vs. iteration count, and at least one figure showing the reweighted truth recovery. A chi-squared/ndf of 0.001 needs explanation -- if the reweighting is very mild, that should be stated, and a more aggressive reweighting should also be tested.

**A3. Condition number reporting uses wrong threshold.**

Table 7.1 reports the condition number as $1.67 \times 10^5$ and evaluates it as "PASS (< 10^6)." However, `conventions/unfolding.md` specifies that a condition number > $10^{10}$ should be flagged for the fit sub-matrix. The note uses a stricter threshold ($10^6$) without justification. This is not wrong per se (being stricter is fine), but it creates a discrepancy with the conventions that a reviewer would notice. More importantly, given that the correlation matrix is near-rank-1 due to the BBB systematic, the condition number of the *inverse* covariance (which enters the chi-squared) should be reported, not just the condition number of the covariance itself.

**Recommendation:** Report the condition number threshold from conventions ($10^{10}$) and note that the analysis uses a stricter criterion. Also report the condition number of the inverse covariance matrix used in the chi-squared fit.

---

### (B) Should Address

**B1. The normalization formula has a potential inconsistency.**

Section 4.2 defines:
$(1/N)\,dN/d\tau_i = u_i / (\sum_j u_j \cdot \Delta\tau)$

This divides each bin by the sum times the bin width, but $\Delta\tau$ appears once (not per-bin). If all bins have the same width (they do: 0.02), this is fine. But the formula as written is ambiguous -- it could be read as dividing by $(\sum_j u_j) \times \Delta\tau$ (correct for uniform bins) or as $\sum_j (u_j \times \Delta\tau_j)$ (correct in general). Clarify the formula for non-expert readers.

**B2. Table 2.1 "after passesAll" values are approximate ("~") but Table 3.3 gives exact values.**

Table 2.1 uses approximate values (e.g., "~522,165") while Table 3.3 gives the exact cutflow. This creates ambiguity about whether the numbers are consistent. Either use exact values in both places or explain the approximation.

**B3. The data/MC chi-squared in Table 9.1 is inconsistent with Section 8.2.**

Section 8.2 reports chi-squared/ndf = 61.0/13 = 4.7 for the Pythia comparison using the full covariance. Table 9.1 reports chi-squared/ndf = 67.9/13 = 5.22 for the same comparison. The note explains the difference (pre-fix vs. post-fix covariance) in the text after the table, but having two different numbers for nominally the same comparison is confusing. Table 9.1 should use the final (post-fix) value consistently.

**B4. No individual cut-efficiency distributions are shown for the sphericity axis cut.**

Section 3.2 describes the sphericity axis cut in detail but no data/MC comparison figure for $|\cos\theta_\text{sph}|$ is referenced. A figure for the missing momentum distribution is shown, and detailed per-category kinematic plots are listed in Section 3.5, but the sphericity axis distribution -- which defines the fiducial acceptance boundary -- is absent. Given that this cut removes 2.3% of events, the distribution should be shown.

**B5. The `results/` directory referenced in Section 12 ("Machine-Readable Results") points to a relative path that is ambiguous.**

The note says files are in `results/` but relative to what? Relative to the note itself, it would be `phase5_documentation/exec/results/`. But the note also references `../../phase4_inference/exec/` for additional files. State absolute paths relative to the analysis root, or clarify the convention.

**B6. Flat-prior sensitivity is reported but the per-bin table is missing.**

Section 5.5 reports a maximum flat-prior shift of 0.24% and states zero bins exceed 20%. However, `conventions/unfolding.md` requires "Show the flat-prior sensitivity per bin." A per-bin table of flat-prior shifts should be included (in the appendix if not in the main text). The per-bin systematic table (A.1) includes a "Prior" column, but these values are absolute shifts -- the relative (%) prior sensitivity per bin is what the conventions ask for.

**B7. No explicit mention of the normalization convention for systematics in a normalized measurement.**

`conventions/unfolding.md` (Section "Normalized vs. absolute measurements") requires the agent to explicitly document which type of measurement is being performed and explain why normalization-only systematics are included or excluded. The note measures $(1/N)\,dN/d\tau$ (normalized) and implicitly excludes luminosity, but this reasoning is never explicitly stated. A brief paragraph in Section 5 confirming this would satisfy the convention.

**B8. Year-by-year cross-check lacks explicit chi-squared values.**

Section 6.1 says "The chi-squared between any pair of year-specific distributions ... is consistent with chi-squared/ndf approximately 1" but does not give the actual values. A table of pairwise chi-squared/ndf (or at least the range) would strengthen this cross-check.

---

### (C) Suggestions

**C1. The abstract could benefit from stating the particle-level definition concisely.**

The abstract describes the measurement but does not specify whether it is fiducial or full-phase-space, nor whether it is charged-only or charged+neutral. Adding one clause ("full-phase-space, charged and neutral particles") would help readers immediately understand what was measured.

**C2. Section 7 (Statistical Method) partly duplicates Section 4.**

Section 7.1 says "The IBU algorithm is described in Section 4.1" and adds only a reference. Consider merging Section 7.1 into Section 4.1 (or removing it) to reduce redundancy. Section 7 could then focus exclusively on the covariance construction and alpha_s fit.

**C3. The response matrix condition number is not reported.**

Table 4.1 reports column normalization and event counts but not the condition number of the response matrix itself, which `conventions/unfolding.md` lists under "Matrix properties to report" ("Condition number (if matrix inversion is involved)"). While IBU does not perform explicit matrix inversion, reporting the condition number provides useful context on the difficulty of the unfolding problem.

**C4. Consider providing the full 25-bin result table, not just the 13 fit-range bins.**

Table 8.1 reports only the 13 bins in the fit range. The note mentions 25 bins total. Providing the full 25-bin table (with appropriate caveats for bins outside the fit range) would be more useful for theorists who may want to compare to predictions in different tau ranges. The machine-readable CSV may already contain this; if so, state that explicitly.

**C5. Figure references use relative paths with `../../` which will break if the note is rendered outside its directory.**

Consider either embedding figures or using paths relative to the analysis root (e.g., `phase3_selection/figures/...`).

**C6. The references section could include DOIs or arXiv identifiers more consistently.**

Some references have arXiv numbers (e.g., hep-ex/0409098) while others have only partial information. Adding DOIs where available would improve citability.

**C7. The efficiency value of 78.6% from "file 001 estimate" in Table D.1 vs. the 79.2% quoted in Section 2.2 should be reconciled or explained more clearly.**

Both numbers appear correct for different denominators, but a reader may be confused by the discrepancy.

---

## Conventions Compliance Checklist (`conventions/unfolding.md`)

| Convention requirement | Status | Note |
|---|---|---|
| Particle-level definition (particles, phase space, ISR, decays) | PASS | Section 1.3, complete |
| Response matrix input validation (per-category data/MC) | PASS | Section 3.5, thorough |
| Matrix properties (dimensions, diagonal fraction, column norm, efficiency) | PASS | Table 4.1, 4.2; condition number missing (C3) |
| Regularization choice with closure + stress + plateau + flat-prior | PARTIAL | Closure and plateau shown; stress test inadequately documented (A2); flat-prior shown |
| Flat-prior sensitivity per bin | PARTIAL | Maximum reported; per-bin table missing (B6) |
| Systematic: object-level response | PASS | Track smearing (5.1), calorimeter scale (5.11) |
| Systematic: selection cuts | PASS | TPC hits, MissP, efficiency (5.2) |
| Systematic: background contamination | PASS | Section 5.3 |
| Systematic: regularization | PASS | Section 5.4 |
| Systematic: prior dependence | PASS | Section 5.5 |
| Systematic: alternative method | PARTIAL | BBB used; methodological concern (A1) |
| Systematic: hadronization model | PARTIAL | 2% floor assigned; structural limitation documented |
| Systematic: ISR treatment | PASS | Section 5.8 |
| Systematic: heavy flavor | PASS | Section 5.9 |
| Normalized vs. absolute documentation | MISSING | Not explicitly stated (B7) |
| Covariance: stat + syst construction | PASS | Sections 7.2, 7.3 |
| Covariance: PSD, condition number, correlation | PASS | Table 7.1 |
| Reference comparison with full covariance + chi2/p-value | PARTIAL | Pythia uses full cov; ALEPH 2004 uses diagonal only (digitization limitation) |
| chi2/ndf > 1.5 investigation | PASS | Section 8.2, thorough investigation |

---

## Summary

The note is substantial and largely complete. The three must-resolve items are:
1. The BBB systematic methodology and its outsized impact on the total uncertainty (A1)
2. The missing stress test documentation (A2)
3. The condition number threshold inconsistency (A3, minor but easy to fix)

Items B1-B8 are presentation and completeness improvements that would strengthen the document for external review. None are blocking but several address explicit requirements from the unfolding conventions.
