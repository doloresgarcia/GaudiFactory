# Critical Review: Phase 5 Analysis Note

**Reviewer role:** Journal referee (reading only the analysis note)
**Document reviewed:** `phase5_documentation/exec/ANALYSIS_NOTE.md`
**Conventions consulted:** `conventions/unfolding.md`

---

## Summary Assessment

The analysis note is a thorough document covering a measurement of the
normalized thrust distribution at $\sqrt{s} = 91.2$ GeV using archived
ALEPH data, with an indicative $\alpha_s$ extraction. The particle-level
definition, event selection, response matrix construction, IBU unfolding,
and systematic uncertainty program are all described in detail. However,
several issues require resolution before this could pass journal review.

---

## Category A: Must Resolve

### A1. The BBB "alternative method" systematic is not a legitimate systematic uncertainty

The 21% BBB systematic dominates the entire uncertainty budget and inflates
the total uncertainty by roughly an order of magnitude beyond what a genuine
uncertainty estimate would produce. As the note itself acknowledges
(Section 5.6), BBB is "an incorrect method" for this measurement because
diagonal fractions are 29-40% in the fit range. Comparing a correct method
(IBU) to a known-incorrect method does not yield a credible uncertainty
estimate -- it yields the bias of the incorrect method.

The conventions (`conventions/unfolding.md`) require "at least one
independent unfolding method" as a cross-check. This means a second
*valid* method (e.g., SVD unfolding, TUnfold, or matrix inversion with
regularization), not comparison to an invalid one. BBB with diagonal
fractions of 30-40% is not a valid alternative -- it is a sanity check
at best.

**Impact:** The entire covariance matrix is nearly rank-1 (all correlations
>0.98) because the BBB systematic dominates everything. The $\alpha_s$
uncertainty is inflated from ~0.002 (experimental systematics ex-BBB) to
~0.011. The $\chi^2/\text{ndf}$ for the data/MC comparison drops from
what would be O(100) (with genuine uncertainties) to 4.7, masking potential
issues.

**Resolution required:** Either (a) implement a genuine alternative
unfolding method (SVD or TUnfold) as the "alternative method" systematic,
or (b) demote the BBB comparison to a cross-check (Section 6) and remove
it from the systematic budget. If (b), the note must acknowledge that the
"alternative method" systematic from conventions is not covered and justify
the omission. The current treatment -- calling BBB both "incorrect" and
using it as the dominant systematic -- is internally contradictory.

### A2. Stress test has no dedicated subsection or quantitative result

The conventions require: "Show closure chi2/ndf and stress chi2/ndf vs.
regularization strength." The stress test is mentioned in three places
(Sections 4.6, 10.1, and the file list) but has no dedicated cross-check
subsection, no table of results, no figure showing the reweighted truth
recovery, and the only quantitative value given ($\chi^2/\text{ndf} < 0.001$
in Section 10.1) is suspiciously small -- a chi2/ndf of essentially zero
suggests either a bug or an overestimated uncertainty, not a passing test.
A proper stress test with reweighted truth should give $\chi^2/\text{ndf}
\approx 1$ if the uncertainties are correct.

**Resolution required:** Add a dedicated stress test subsection (in
Section 6 or Section 4.6) with: (a) description of the reweighting function
used, (b) chi2/ndf with proper uncertainties, (c) figure showing the
recovery. Investigate the $\chi^2 < 0.001$ value -- if real, explain why.

### A3. No comparison to published ALEPH results using full covariance

The conventions state: "Use the full covariance matrix (not diagonal
uncertainties only)" for reference comparisons. Section 9.2 explicitly
notes the ALEPH 2004 and archived ALEPH comparisons use "diagonal
uncertainties only" and "digitized values." The $\chi^2/\text{ndf} = 2.33$
for ALEPH 2004 exceeds the 1.5 threshold that conventions say requires
investigation, and the investigation consists only of blaming digitization
errors.

**Resolution required:** Either (a) obtain the published ALEPH 2004
values from HEPData (they are available: the ALEPH 2004 paper
hep-ex/0409098 has HEPData entries) and redo the comparison with proper
covariances, or (b) if truly unavailable, document the search for HEPData
entries explicitly and provide a more rigorous investigation of the
$\chi^2 = 2.33$ tension (e.g., which bins drive it, is the pattern
consistent with a normalization offset vs. a shape difference).

### A4. The $\alpha_s$ extraction method is acknowledged as degenerate

Section 7.5 states that the LO scaling approach produces a flat $\chi^2$
profile after normalization, making the extraction meaningless. Section 8.3
reports $\chi^2/\text{ndf} = 47.7/12 = 3.97$ at the minimum. This is not
an "indicative" result -- it is a non-result from a method that cannot
extract $\alpha_s$ from a normalized distribution.

**Resolution required:** Either (a) remove the $\alpha_s$ extraction
entirely and present this as a thrust distribution measurement only, or
(b) clearly delineate the $\alpha_s$ section as a methodological
demonstration that does not produce a physics result, and remove it from
the abstract and conclusions. The current framing -- reporting
$\alpha_s = 0.1066 \pm 0.0113$ and comparing it to the world average --
gives false legitimacy to a number that comes from a degenerate fit.

---

## Category B: Should Address

### B1. Hadronization systematic floor lacks rigorous justification

The 2% per-bin floor is assigned by fiat based on "published LEP
hadronization uncertainties (1-3%)." This is reasonable as a stopgap, but:
- The note says 2% is "below the 1-3% published range" and then calls it
  "conservative." Choosing the low end of a published range is not
  conservative -- it is optimistic.
- The floor is applied as fully correlated across all bins. Published
  hadronization uncertainties from ALEPH 2004 show bin-dependent shape
  variations (not flat percentage), so the correlation structure is wrong.
- The conventions say: "reweighting at particle level is acceptable but
  must be documented as a limitation." The note does document this, but
  the near-zero reweighting result suggests the reweighting was done
  incorrectly (reweighting the IBU prior, which has no effect at 3
  iterations, rather than reweighting the response matrix).

**Suggested fix:** (a) Increase the floor to 3% (the upper end of the
published range) to be genuinely conservative. (b) Note that the flat
correlation structure is an approximation. (c) Clarify whether the
particle-level reweighting was applied to the prior or to the response
matrix -- if only the prior, try reweighting the response matrix entries
to simulate a Herwig-like particle-level distribution.

### B2. Response matrix condition number not reported

The conventions require reporting the condition number of the response
matrix itself (Section "Matrix properties to report"). The note reports
the condition number of the *covariance matrix* ($1.67 \times 10^5$) but
not of the response matrix. For a 25x25 matrix with diagonal fractions
dropping to 23%, the condition number could be large enough to matter.

**Suggested fix:** Report the response matrix condition number in
Table 4.1 or Appendix D.

### B3. Efficiency as a function of particle-level observable not shown in detail

The conventions require "Efficiency as a function of the particle-level
observable." Section 4.3 mentions efficiency is ~0.75-0.80 and there is
a figure reference, but no per-bin efficiency table is provided. Given
that the efficiency enters the unfolding correction, per-bin values should
be tabulated.

**Suggested fix:** Add a per-bin efficiency table in Appendix D, alongside
Table D.2.

### B4. Inconsistent chi2 values for Pythia comparison

Table 9.1 reports $\chi^2 = 67.9/13 = 5.22$ for Pythia 6.1, while
Section 8.2 reports $\chi^2 = 61.0/13 = 4.7$. The note explains this is
pre-fix vs. post-fix covariance, but having two different values for the
same comparison in the same document is confusing and suggests incomplete
editing.

**Suggested fix:** Update Table 9.1 to use the post-fix (final) covariance
values consistently. Remove or footnote the pre-fix value.

### B5. Per-cut distributions not shown for all cuts

The phase instructions require "per-cut event selection with individual
distributions and efficiencies." The note shows the missing momentum
distribution (Figure reference in Section 3.2) but does not show figures
for the sphericity axis $\cos\theta$ distribution or the ISR flag
distribution. These are referenced implicitly but not explicitly shown.

**Suggested fix:** Add figure references for data/MC comparisons of the
sphericity axis and ISR variables, or state they are available in the
supplementary figures.

### B6. Normalization formula has an error

Section 4.2 gives:
$$(1/N)\,dN/d\tau_i = \frac{u_i}{\sum_j u_j \cdot \Delta\tau}$$

This normalizes to unit integral over the full range, but the denominator
should be $(\sum_j u_j) \cdot \Delta\tau$ only if all bins have the same
width $\Delta\tau$. More precisely, the normalization should be
$u_i / (N_\text{total} \cdot \Delta\tau_i)$ where
$N_\text{total} = \sum_j u_j$. The formula as written divides each bin by
$\Delta\tau$ times the total, which would give units of $1/\tau^2$ rather
than $1/\tau$.

**Suggested fix:** Clarify the normalization formula. If all bins have
equal width, the formula should be $u_i / (\sum_j u_j \cdot \Delta\tau)$
with the product in the denominator being $N \times \Delta\tau$, giving
$(1/N)(dN/d\tau)$. Make the grouping explicit.

### B7. Flat-prior sensitivity per bin not shown

The conventions require: "Show the flat-prior sensitivity per bin."
Section 5.5 states the maximum is 0.24% but does not show a per-bin
table or figure. The conventions specifically ask for per-bin values to
identify any bins that might be prior-dominated.

**Suggested fix:** Add a per-bin flat-prior sensitivity table or figure.

---

## Category C: Suggestions

### C1. Figure cosmetics cannot be verified from the note alone

All figure references point to relative paths (`../../phase3_selection/
figures/...`). Without viewing the figures, the cosmetic checklist cannot
be fully evaluated. From the figure descriptions:
- $\sqrt{s}$ labels: mentioned in the text but unclear if on figures.
- Experiment name: should say "ALEPH" on all data plots.
- Figure titles: methodology says "No figure titles" -- cannot verify.
- Axis labels with units: cannot verify.

**Suggestion:** Ensure all figures follow the cosmetic checklist. Consider
embedding critical figures directly in the note or providing a figure
appendix.

### C2. The `results/` directory path in the note is ambiguous

The note says "in the `results/` subdirectory" but the actual path is
`phase5_documentation/exec/results/`. A reader of the standalone note
would not know where to find these files.

**Suggestion:** Use absolute paths relative to the analysis root, e.g.,
`phase5_documentation/exec/results/`.

### C3. The covariance matrix in Table B.1 uses inconsistent scaling

Table B.1 says "Values $\times 10^{-2}$ for legibility" but the values
shown (e.g., 132.74 for the (0.05, 0.05) entry) would imply the actual
covariance is 1.3274. Given that $(1/N)\,dN/d\tau \approx 7.44$ at
$\tau = 0.05$ and the total uncertainty is 1.16, the variance should be
$1.16^2 = 1.35$. So the scaling factor appears correct, but the notation
"$\times 10^{-2}$" is confusing -- it means the displayed values should
be multiplied by $10^{-2}$ to get the actual covariance. State this
more clearly.

### C4. Correlation matrix table is truncated

Table B.2 shows only 3 rows of the 13x13 matrix, with a note saying
"Continued rows follow the same pattern; all entries exceed 0.98." The
full matrix should be provided if claiming to give it. Alternatively,
since it is nearly rank-1, simply state this fact and refer to the
machine-readable file.

### C5. The abstract reports too many significant figures on some quantities

The hadronization floor (2.0%) and the data/MC offset ("~15-20%") are
rough estimates, but the BBB systematic is reported as "up to 21%" which
is appropriate. The $\alpha_s$ result $0.1066 \pm 0.0113$ has 4 significant
figures on the central value but only 3 on the uncertainty -- standard
practice would round to $0.107 \pm 0.011$.

### C6. No discussion of luminosity or trigger efficiency

The note correctly identifies this as a normalized measurement where
luminosity cancels, but does not explicitly state that trigger efficiency
cancels in the normalized shape. A brief sentence would satisfy a referee
who checks for this.

---

## Depth Requirements Checklist

| Requirement | Status | Notes |
|---|---|---|
| One subsection per systematic source | PASS | 11 subsections covering 13 sources |
| One subsection per cross-check | PARTIAL | Year-by-year (6.1), IBU vs BBB (6.2), closure (6.3) present; stress test missing dedicated subsection |
| Per-cut event selection with distributions and efficiencies | PARTIAL | Cutflow tables present; only missing momentum figure explicitly shown |
| Full covariance matrix in appendix (table) | PASS | Table B.1 with full 13x13 matrix |
| Machine-readable results directory | PASS | `results/` with CSV files present |
| LaTeX math throughout | PASS | Consistent $\LaTeX$ notation |
| `pixi.toml` has `all` task | PASS | Verified; chains all scripts |
| Experiment log non-empty | PASS | 420 lines |

---

## Conventions Compliance (`conventions/unfolding.md`)

| Convention requirement | Status | Finding |
|---|---|---|
| Particle-level definition | PASS | Section 1.3, complete |
| Response matrix input validation | PASS | Section 3.5, per-category |
| Matrix properties (dimension, diagonal, column norm, condition number, efficiency) | PARTIAL | Missing response matrix condition number (B2), per-bin efficiency table (B3) |
| Regularization: closure, stress, plateau, flat-prior | PARTIAL | Closure: PASS. Stress: mentioned but no subsection or result (A2). Plateau: PASS. Flat-prior: summary only, no per-bin (B7) |
| Required systematics: detector response | PASS | Track smear + calo scale |
| Required systematics: selection cuts | PASS | TPC hits, MissP, efficiency |
| Required systematics: background | PASS | |
| Required systematics: regularization | PASS | |
| Required systematics: prior dependence | PASS | |
| Required systematics: alternative method | FAIL | BBB is not a valid alternative method (A1) |
| Required systematics: hadronization model | PARTIAL | Floor assigned, not a genuine comparison (B1) |
| Required systematics: ISR treatment | PASS | |
| Required systematics: heavy flavor | PASS | |
| Covariance: construction, PSD, condition number, correlation viz | PASS | |
| Reference comparison with full covariance | FAIL | Diagonal only (A3) |
| Normalized vs absolute: document reasoning | PARTIAL | Implicit but not stated explicitly for trigger/lumi (C6) |

---

## Summary of Findings

**4 Category A findings** that must be resolved before this note could
pass journal review. The most impactful are A1 (BBB systematic inflating
the entire error budget by an order of magnitude) and A4 (degenerate
$\alpha_s$ fit presented as a result).

**7 Category B findings** that should be addressed to bring the note to
publication standard.

**6 Category C suggestions** for polish and clarity.

The underlying measurement (thrust distribution corrected by IBU with
independent closure at $\chi^2/\text{ndf} = 0.924$) appears sound. The
issues are primarily in the interpretation of uncertainties (A1), missing
validation detail (A2, A3), and the $\alpha_s$ extraction framing (A4).
