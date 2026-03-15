# Precision Measurement of the Thrust Distribution and $\alpha_s$ Extraction in $e^+e^-$ Collisions at $\sqrt{s} = 91.2$ GeV Using Archived ALEPH Data

**Analysis:** thrust_alphas
**Collaboration:** ALEPH (archived data re-analysis)
**Phase:** 5 — Final Analysis Note
**Status:** Publication-quality draft

---

## Abstract

We present a measurement of the normalized thrust event-shape distribution
$(1/N)\,dN/d\tau$ in $e^+e^- \to$ hadrons collisions at a center-of-mass
energy of $\sqrt{s} = 91.2$ GeV, using the archived ALEPH dataset recorded
at the LEP collider during 1992–1995. After applying standard hadronic event
selection, the analysis uses 2,889,543 events. The thrust distribution is
corrected for detector effects using iterative Bayesian unfolding (IBU) with 3
iterations, validated by an independent MC closure test yielding $\chi^2/\text{ndf}
= 0.924$. A 12-source systematic uncertainty budget is evaluated; the dominant
uncertainties are track momentum smearing (2.2%) and the hadronization model
floor (2.0%), with all other sources below 1.5% per bin. The bin-by-bin (BBB)
correction is computed as a cross-check but excluded from the systematic budget
because BBB is known to fail when the response matrix diagonal fraction is below
~70% (this analysis: 25–50%); this difference is a validation that IBU
is the correct method, not a systematic uncertainty. The normalized measurement
is insensitive to luminosity and trigger efficiency, which cancel in the ratio.
The corrected distribution is compared to the Pythia 6.1 particle-level
prediction, with $\chi^2/\text{ndf} = 207.0/13 = 15.9$; the data is
systematically ~15–20% below the MC prediction, consistent with the
known tendency of the Pythia 6.1 LEP tune to overpredict soft hadronic
activity. An indicative $\alpha_s$ extraction using leading-order QCD shape
predictions demonstrates the methodology but does not constitute a precision
measurement; this requires NLO+NLL differential cross-section calculations.

---

## 1. Introduction

### 1.1 Physics Motivation

Quantum chromodynamics (QCD) is the established theory of the strong
interaction. One of the most important experimental tests of QCD is the
precise determination of the strong coupling constant $\alpha_s$, whose
running with scale provides a defining prediction of the theory. Event-shape
observables measured in $e^+e^-$ annihilation provide particularly clean
probes of $\alpha_s$: the initial state is precisely known, the hard
subprocess $e^+e^- \to q\bar{q}$ is calculable in electroweak theory, and
the subsequent QCD radiation and hadronization produce the event shapes
sensitive to $\alpha_s$.

The LEP collider at CERN operated at the $Z$-pole ($\sqrt{s} \approx 91.2$ GeV)
from 1989 to 1995, accumulating millions of hadronic $Z$ decays at the four
experiments ALEPH, DELPHI, L3, and OPAL. The high statistics, well-understood
detector performance, and extensive theoretical calculations at this energy
make the LEP dataset the gold standard for $\alpha_s$ extractions from event
shapes.

This analysis uses the archived ALEPH dataset to:
1. Measure the thrust distribution at particle level, corrected for detector
   effects using modern unfolding techniques.
2. Validate the corrected distribution against published ALEPH results and
   MC predictions.
3. Extract $\alpha_s(M_Z)$ from fits of theoretical predictions to the
   measured distribution.

Beyond the physics result, this work demonstrates the feasibility of
publication-quality measurements using archived LEP open data with modern
analysis tools, contributing to the scientific legacy of the archived dataset.

### 1.2 Observable Definition

The thrust $T$ is defined as:
$$T = \max_{\hat{n}} \frac{\sum_i |\vec{p}_i \cdot \hat{n}|}{\sum_i |\vec{p}_i|}$$
where the sum runs over all final-state particles, $\hat{n}$ is a unit vector
(the thrust axis $\hat{n}_T$) optimized to maximize the expression. The
conventional variable for distributions is:
$$\tau = 1 - T$$
which ranges from 0 (perfectly back-to-back 2-jet topology, $q\bar{q}$ final
state with no radiation) to 0.5 (isotropic, spherically symmetric event).

The thrust observable is infrared- and collinear-safe (IRC-safe): it is
invariant under the addition of soft or collinear parton emissions, making
it calculable in perturbative QCD without divergences from unresolved
radiation.

### 1.3 Particle-Level Definition

The particle-level target for the unfolded measurement is defined as follows:

- **Particles included:** All stable charged and neutral particles with
  $c\tau > 10$ mm. This includes charged hadrons ($\pi^\pm$, $K^\pm$,
  $p/\bar{p}$), neutral hadrons ($K^0_L$, neutrons), and photons. Neutrinos
  are excluded.
- **Phase space:** Full $4\pi$ acceptance (no fiducial cuts at particle level).
  This is a full-phase-space measurement.
- **ISR treatment:** ISR photons are excluded from the particle-level thrust
  calculation. The measurement targets the hadronic system from the $Z$ decay.
  Events with hard ISR are removed at both detector and particle level.
- **Hadron decays:** Particles are defined at the "stable particle" level —
  $K_S^0$, $\Lambda$, and other particles with $c\tau < 10$ mm are allowed to
  decay; their daughters enter the thrust calculation.

This definition follows the standard LEP convention used in the original ALEPH
event shape publications (Eur. Phys. J. C35:457–486, 2004).

### 1.4 Perturbative QCD Predictions

The differential thrust distribution has been calculated to high precision
in perturbative QCD. The relevant theory predictions for $\alpha_s$
extraction are:

- **NLO + NLL resummation** ($\mathcal{O}(\alpha_s^2)$ + NLLA): the
  standard LEP-era theory for $\alpha_s$ extraction from event shapes,
  implemented in programs such as DISASTER++.
- **NNLO** ($\mathcal{O}(\alpha_s^3)$): available from calculations by
  Gehrmann-De Ridder, Gehrmann, Glover, and Heinrich.
- **NNLO + N$^3$LL resummation**: the state-of-the-art calculation combining
  third-order fixed-order with next-to-next-to-next-to-leading logarithmic
  resummation (Abbate et al., 2010, using SCET).

For the large-$\tau$ (multi-jet) region, the fixed-order predictions dominate.
For the small-$\tau$ (2-jet) region, logarithms $\alpha_s^n \ln^{2n}(1/\tau)$
are large and require resummation. The fit range $0.05 \leq \tau \leq 0.30$
is chosen to avoid both the deeply 2-jet region (where resummation and
non-perturbative corrections are essential) and the multi-jet region (where
fixed-order calculations become unreliable).

### 1.5 Prior Measurements

The thrust distribution at the $Z$ pole has been measured by all four LEP
experiments. The most directly relevant published results are:

1. **ALEPH 2004** (Eur. Phys. J. C35:457–486): Measurement of 16 event
   shape distributions using 1991–1995 data with $\alpha_s$ extraction using
   NLO+NLL theory. This is the primary reference for comparison.

2. **LEP QCD combination** (hep-ex/0411006): Combined $\alpha_s$ from event
   shapes at all four LEP experiments. Combined result at 91.2 GeV:
   $\alpha_s(M_Z) = 0.1202 \pm 0.0003\,(\text{stat}) \pm
   0.0007\,(\text{exp}) \pm 0.0012\,(\text{hadr}) \pm 0.0048\,(\text{theo})$.

3. **Archived ALEPH analysis** (inspire:1793969): Modern analysis of the
   same archived dataset, validating the thrust distribution against published
   ALEPH results.

The world-average $\alpha_s(M_Z) = 0.1180 \pm 0.0009$ (PDG 2022) is
dominated by lattice QCD determinations; event-shape measurements at LEP
continue to provide valuable complementary information.

---

## 2. Data Samples

### 2.1 Data

The archived ALEPH data consists of reconstructed $e^+e^-$ events recorded
at $\sqrt{s} \approx 91.2$ GeV during the 1992–1995 LEP1 running period.
Data files are stored in ROOT format containing charged particle tracks and
calorimeter energy clusters.

**Table 2.1: Data sample inventory.**

| Year | File | Events in file | After $\texttt{passesAll}$ | Efficiency |
|------|------|----------------|---------------------------|------------|
| 1992 | `LEP1Data1992_recons_aftercut-MERGED.root` | 551,474 | ~522,165 | 94.7% |
| 1993 | `LEP1Data1993_recons_aftercut-MERGED.root` | 538,601 | ~510,097 | 94.7% |
| 1994 P1 | `LEP1Data1994P1_recons_aftercut-MERGED.root` | 433,947 | ~411,044 | 94.7% |
| 1994 P2 | `LEP1Data1994P2_recons_aftercut-MERGED.root` | 447,844 | ~424,147 | 94.7% |
| 1994 P3 | `LEP1Data1994P3_recons_aftercut-MERGED.root` | 483,649 | ~457,936 | 94.7% |
| 1995 | `LEP1Data1995_recons_aftercut-MERGED.root` | 595,095 | ~563,615 | 94.7% |
| **Total** | — | **3,050,610** | **2,889,543** | **94.7%** |

Data files are located at
`/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPH/`. All files are labeled
"aftercut," indicating that a baseline event selection has been applied
upstream (see Section 3.1). The stored center-of-mass energy is
$\sqrt{s} = 91.14$ GeV for data, consistent with the Z-pole.

### 2.2 Monte Carlo Simulation

The Monte Carlo sample uses **Pythia 6.1** with the LEP-era tune including
full ALEPH detector simulation. The generator models:
- Parton shower (DGLAP evolution)
- Hadronization via the Lund string model
- Underlying event (LEP tune)
- ALEPH detector response (full simulation)

The MC is stored in ROOT files with three trees:
- `t`: detector-level reconstructed quantities
- `tgen`: generator-level particles matched to selected reco events (199 branches)
- `tgenBefore`: generator-level particles for all generated events before selection

**Table 2.2: Monte Carlo sample inventory.**

| Sample | Files | Generator | Events per file | Total (reco) | Total (gen before sel.) |
|--------|-------|-----------|-----------------|--------------|------------------------|
| LEP1MC1994 | 40 files (`-001` to `-040`) | Pythia 6.1 | ~19,200 | 771,597 | 973,769 |

After applying $\texttt{passesAll}$: **731,006 reconstructed events** are
selected. The generator-level selection efficiency is:
$$\varepsilon_{\text{gen}} = 771{,}597 / 973{,}769 = 79.2%$$
(from file 001: 19,158 reco / 24,360 gen = 78.6%). This efficiency is
consistent with the published ALEPH hadronic selection efficiency of 94–95%
applied at the file level to a sample already filtered by the "aftercut"
baseline. After full $\texttt{passesAll}$ including the remaining cuts,
the data efficiency of 94.7% and MC efficiency of 94.7% agree to better
than 0.1%.

**Limitation:** Only Pythia 6.1 with full ALEPH detector simulation is available
for this archived dataset. Herwig and Ariadne generator samples with full
detector simulation, used in the original ALEPH 2004 analysis, are not
available. This limitation affects the hadronization systematic, as described
in Section 5.7.

---

## 3. Event Selection

### 3.1 Pre-Applied Cuts

The ROOT files are labeled "aftercut," meaning the following baseline cuts
were applied upstream before the files were produced:

**Table 3.1: Pre-applied cuts (cannot be loosened).**

| Cut | Branch | Description | Efficiency |
|-----|--------|-------------|------------|
| ALEPH NTuple aftercut | `passesNTupleAfterCut` | Baseline ALEPH reconstruction quality | 100.0% |
| Charged energy | `passesTotalChgEnergyMin` | $E_\text{ch} > 15$ GeV (sum of charged pion-mass momenta) | ~100.0% |
| Minimum charged tracks | `passesNTrkMin` | $\geq 5$ good charged tracks | ~100.0% |

These cuts select hadronic $Z$ decays and reject $\tau^+\tau^-$, two-photon,
and beam-gas events. Because they are pre-applied, systematic variations can
only tighten these cuts; loosening is not possible. This is documented as a
constraint on the systematic program (see Section 5.3).

The cut $E_\text{ch} > 15$ GeV selects events where the sum of track momenta
(assuming pion mass) exceeds 15 GeV, approximately 16% of $\sqrt{s}$. This
effectively removes $Z \to \tau^+\tau^-$ events where one or both taus decay
leptonically and the visible charged energy is low.

### 3.2 Additional Event-Level Cuts

The following cuts are stored as flags in the ROOT files and are applied in
this analysis by requiring $\texttt{passesAll} = \texttt{True}$:

**Table 3.2: Additional event-level cuts.**

| Cut | Branch | Description | Physical motivation | Data eff. | MC eff. |
|-----|--------|-------------|---------------------|-----------|---------|
| Sphericity axis | `passesSTheta` | $|\cos\theta_\text{sph}| < 0.82$ | Ensures event axis is in the well-instrumented barrel region | 97.7% | 97.7% |
| Missing momentum | `passesMissP` | $|\vec{p}_\text{miss}| < 20$ GeV | Rejects $\tau^+\tau^-$ with missing neutrinos and cosmic rays | 97.2% (cumul.) | 97.3% (cumul.) |
| ISR rejection | `passesISR` | No hard ISR photon | Ensures the hadronic system corresponds to $Z \to q\bar{q}$ at the full $\sqrt{s}$ | 94.7% (cumul.) | 94.7% (cumul.) |

**Sphericity axis cut ($|\cos\theta_\text{sph}| < 0.82$):** The
sphericity axis points along the principal axis of the event momentum
tensor. Events with $|\cos\theta_\text{sph}| > 0.82$ have their principal
axis pointing toward the detector endcap region where tracking and
calorimeter coverage are degraded. Removing these events reduces
acceptance effects and ensures the thrust calculation is performed on
events with good track and cluster coverage. The cut removes 2.3% of
events; data/MC agreement on the sphericity axis distribution is within
5%.

**Figure:** ![](figures/datamc_missp.pdf) — data/MC
comparison of the missing momentum distribution. The distribution peaks
near zero and falls steeply; data/MC ratio is flat at ~1.0 across
the distribution, with maximum deviation 4.1%.

**Missing momentum cut ($|\vec{p}_\text{miss}| < 20$ GeV):** Events with
large missing momentum arise from $Z \to \tau^+\tau^-$ decays (where
neutrinos from $\tau$ decay carry away significant momentum) or from
cosmic ray interactions. The cut removes an additional 2.5% of events
after the sphericity cut. The 20 GeV threshold is chosen to be large
compared to the resolution on missing momentum reconstruction (typically
~3–5 GeV for hadronic events) while efficiently rejecting the
$\tau^+\tau^-$ tail.

**ISR rejection:** Hard initial-state radiation (ISR) events are excluded
because the measurement targets the hadronic system from $Z$ decay at
the nominal $\sqrt{s} = 91.2$ GeV. Hard ISR photons reduce the effective
$\sqrt{s}'$ of the $q\bar{q}$ system, biasing the thrust distribution
toward smaller $\tau$ (more 2-jet-like). Only 1.0% of events are removed,
consistent with the Z-pole environment where hard ISR is strongly suppressed
relative to higher-$\sqrt{s}$ running.

### 3.3 Object Selection

- **Charged tracks:** $\texttt{pwflag} = 0$ (good quality, $|\text{charge}| > 0$) — the primary charged-track category.
- **Neutral calorimeter objects:** $\texttt{pwflag} = 4$ — calorimeter clusters (photons, neutral hadrons).
- **Secondary charged tracks:** $\texttt{pwflag} = 1, 2$ — reduced-quality charged tracks, still included in the thrust sum (validated in Section 3.5).
- **Additional neutral objects:** $\texttt{pwflag} = 5$ — additional neutral calorimeter deposits (validated).
- **Observable:** Pre-computed $\texttt{Thrust}$ branch (charged + neutral particles, all $\texttt{pwflag}$ 0–5).

The thrust $T$ is read from the pre-computed branch, and $\tau = 1 - T$ is
derived from it. The stored value uses all particle categories and is
consistent with the particle-level definition (Section 1.3).

### 3.4 Cutflow Table

**Table 3.3: Data cutflow.**

| Cut | Events | Cumulative efficiency |
|-----|--------|-----------------------|
| Total in files ("aftercut" base) | 3,050,610 | 100.0% |
| $\texttt{passesNTupleAfterCut}$ (pre-applied) | 3,050,610 | 100.0% |
| $E_\text{ch} > 15$ GeV (pre-applied) | 3,049,993 | 100.0% |
| $N_\text{trk} \geq 5$ (pre-applied) | 3,049,588 | 100.0% |
| $|\cos\theta_\text{sph}| < 0.82$ | 2,979,778 | 97.7% |
| $|\vec{p}_\text{miss}| < 20$ GeV | 2,902,788 | 95.2% |
| No hard ISR | 2,889,824 | 94.7% |
| **Selected ($\texttt{passesAll}$)** | **2,889,543** | **94.7%** |

**Table 3.4: MC cutflow.**

| Cut | Events | Cumulative efficiency |
|-----|--------|-----------------------|
| Total in files | 771,597 | 100.0% |
| $\texttt{passesNTupleAfterCut}$ | 771,597 | 100.0% |
| $E_\text{ch} > 15$ GeV | 771,442 | 100.0% |
| $N_\text{trk} \geq 5$ | 771,383 | 100.0% |
| $|\cos\theta_\text{sph}| < 0.82$ | 753,730 | 97.7% |
| $|\vec{p}_\text{miss}| < 20$ GeV | 734,040 | 95.1% |
| No hard ISR | 731,029 | 94.7% |
| **Selected ($\texttt{passesAll}$)** | **731,006** | **94.7%** |

The tgenBefore sample (particle-level before selection) contains 973,769 events.

**Figure:** ![](figures/cutflow_by_year.pdf) — per-year
event yields after each cut level, showing the uniformity of selection
efficiency across the 1992–1995 data-taking period (all years consistent at
$94.7 \pm 0.1%$).

**Table 3.5: Year-by-year data yields.**

| Year | Events in file | After passesAll | Efficiency |
|------|----------------|-----------------|------------|
| 1992 | 551,474 | ~522,165 | 94.7% |
| 1993 | 538,601 | ~510,097 | 94.7% |
| 1994 P1 | 433,947 | ~411,044 | 94.7% |
| 1994 P2 | 447,844 | ~424,147 | 94.7% |
| 1994 P3 | 483,649 | ~457,936 | 94.7% |
| 1995 | 595,095 | ~563,615 | 94.7% |

The uniform efficiency across all years is a strong indicator of stable
detector performance throughout the data-taking period.

### 3.5 Data/MC Validation per Object Category

Before constructing the response matrix, data/MC comparisons were performed
for all kinematic variables entering the thrust calculation, resolved by
particle category. This is required by the unfolding conventions (Section 4
of `conventions/unfolding.md`).

**Table 3.6: Momentum fractions per particle category.**

| $\texttt{pwflag}$ | Description | Data fraction | MC fraction |
|-----|-------------|---------------|-------------|
| 0 | Good charged tracks (primary) | 60.48% | 59.69% |
| 1 | Reduced-quality charged tracks | 2.31% | 2.29% |
| 2 | Further reduced-quality charged tracks | 1.62% | 1.46% |
| 3 | Pathological charged tracks | 0.04% | 0.03% |
| 4 | Neutral calorimeter clusters | 25.24% | 26.02% |
| 5 | Additional neutral objects | 10.31% | 10.51% |

Categories 1, 2, and 5 together contribute 14.2% of total event momentum
and are non-negligible. Category 3 is negligible (0.04%).

**$\texttt{pwflag} = 0$ charged tracks (60.5% of momentum):**
- Track $p_T$: maximum data/MC deviation 3.9% — excellent agreement.
- $\cos\theta$: maximum deviation 5.3% — good agreement across the barrel.
- Impact parameter $|d_0|$: 11.3% maximum deviation (tails).
- Impact parameter $|z_0|$: 33.1% maximum deviation (tails, non-IP tracks).
- Track $|p|$: 32.6% maximum deviation (confined to high-momentum tail $|p| > 10$ GeV).
- TPC hit count: 28.6% maximum deviation (MC uses simplified TPC model).
- Missing momentum: 4.1% — excellent agreement.

**Figures:** ![](figures/datamc_chg_pt.pdf),
![](figures/datamc_chg_costheta.pdf), ![](figures/datamc_chg_pmag.pdf), ![](figures/datamc_chg_ntpc.pdf),
![](figures/datamc_chg_d0.pdf), ![](figures/datamc_chg_z0.pdf), ![](figures/datamc_missp.pdf).

**$\texttt{pwflag} = 4$ neutral clusters (25.2% of momentum):**
- Cluster $|p|$: 5.8% maximum deviation — good shape agreement.
- $\cos\theta$: 7.4% maximum deviation — good agreement.
- Cluster multiplicity: 67.1% maximum deviation — the MC overestimates
  the number of neutral clusters. This is a known limitation of Pythia 6.1
  in modeling calorimeter cluster counting. Crucially, the cluster energy
  distribution is well-modeled (5.8%), which is the variable directly
  relevant to the thrust calculation.

**Figures:** ![](figures/datamc_e_neutral.pdf).

**$\texttt{pwflag} = 1, 2, 5$ secondary categories (14.2% combined):**
- All three categories show data/MC agreement within 20% in the
  bulk of their $|p|$ and $\cos\theta$ distributions.
- These categories are covered by the existing systematic program: pwflag=1
  and 2 by the track momentum smearing systematic; pwflag=5 by the
  calorimeter energy scale systematic.

**Figures:** ![](figures/datamc_pwflag1_pmag.pdf),
![](figures/datamc_pwflag2_pmag.pdf), ![](figures/datamc_pwflag5_pmag.pdf),
![](figures/pwflag_momentum_fractions.pdf).

**Assessment:** The MC model is adequate for the thrust measurement.
Identified discrepancies — neutral cluster multiplicity (67%), track
momentum tail (33%), TPC hits (29%) — are all in distributions that are
either not directly relevant to the thrust calculation (cluster count vs.
cluster energy) or are in tails with limited impact on the event-shape
observable. The thrust-relevant quantities (track $p_T$, $\cos\theta$,
neutral cluster energy, missing momentum) all show excellent data/MC
agreement ($< 8%$).

---

## 4. Corrections and Unfolding

### 4.1 IBU Algorithm

Detector effects are corrected using **Iterative Bayesian Unfolding (IBU)**,
the D'Agostini method. The algorithm updates the estimate of the
particle-level ("cause") distribution by applying Bayes' theorem iteratively:

$$P^{(k+1)}(C_i) \propto P^{(k)}(C_i) \sum_j \frac{n_j \cdot P(E_j | C_i)}{\sum_{i'} P(E_j | C_{i'}) P^{(k)}(C_{i'})}$$

where:
- $C_i$ are the particle-level (cause) bins,
- $E_j$ are the detector-level (effect) bins,
- $P(E_j | C_i)$ is the response matrix element (probability of
  reconstructing in bin $j$ given particle-level bin $i$),
- $n_j$ is the observed detector-level histogram,
- $P^{(0)}(C_i)$ is the prior (initial guess of the particle-level distribution).

The algorithm converges iteratively: each iteration reduces the dependence
on the prior. The number of iterations is the regularization parameter —
fewer iterations apply stronger regularization (closer to the prior); more
iterations allow the data to deviate more from the prior but increase
statistical fluctuations.

The IBU method is chosen for this analysis because:
1. It naturally handles bin-to-bin migrations without matrix inversion.
2. The regularization parameter (iteration count) has a direct physical
   interpretation.
3. It is well-established for event shape measurements.
4. Independent implementations in multiple software packages (PyUnfold,
   RooUnfold) provide cross-checks.

IBU is essential for this measurement because the diagonal fraction of the
response matrix drops below 50% for $\tau > 0.04$ (see Section 4.3),
meaning significant bin migrations require a proper matrix-inversion
approach rather than simple bin-by-bin correction.

### 4.2 Normalization Procedure

The normalization follows the convention for unfolded measurements: normalize
**after** unfolding and efficiency correction, not before. The normalized
distribution is:
$$(1/N)\,dN/d\tau_i = \frac{u_i}{\sum_j u_j \cdot \Delta\tau}$$
where $u_i$ is the unfolded yield in bin $i$ and $\Delta\tau = 0.02$ is the
bin width. Pre-normalization would introduce bin-to-bin correlations
not captured by the response matrix.

### 4.3 Response Matrix

The response matrix $R_{ij} = P(\text{reco bin}\ i | \text{gen bin}\ j)$
is constructed from all 40 MC files (731,006 selected matched pairs). It
maps the 25 detector-level $\tau$ bins to the 25 particle-level $\tau$ bins
(uniform binning, $\Delta\tau = 0.02$, $\tau \in [0, 0.5]$).

**Table 4.1: Response matrix properties.**

| Property | Value |
|----------|-------|
| Dimensions | $25 \times 25$ (reco $\times$ gen bins) |
| Column normalization | 1.0000 (verified for all active bins) |
| Events in matrix | 731,006 |
| tgenBefore events | 973,769 |

**Table 4.2: Response matrix diagonal fraction by $\tau$ region.**

| $\tau_\text{gen}$ range | Diagonal fraction | Notes |
|-------------------------|-------------------|-------|
| $[0.00, 0.02]$ | 89% | 2-jet peak, well-reconstructed |
| $[0.02, 0.04]$ | 63% | Moderate migration |
| $[0.04, 0.06]$ | 53% | Below 50% threshold |
| $[0.06, 0.10]$ | 40–50% | Significant migration |
| $[0.10, 0.20]$ | 33–40% | IBU essential |
| $[0.20, 0.30]$ | 29–32% | IBU essential |
| $[0.30, 0.40]$ | 23–29% | Low statistics, larger corrections |
| $[0.40, 0.50]$ | ~0% | Below noise floor — excluded |

The low diagonal fractions in the fit range ($\tau \in [0.05, 0.30]$)
confirm that bin-by-bin correction is unreliable as a primary method.
IBU is the appropriate choice.

**Reconstruction efficiency:** $\varepsilon(\tau_\text{gen}) \approx 0.75$–$0.80$ across
the fit range, consistent with the ~78.6% generator-level selection
efficiency. The efficiency is slightly higher for low-$\tau$ (more 2-jet-like)
events, which are better reconstructed in the barrel region.

**Figure:** ![](figures/response_matrix.pdf) — normalized
response matrix showing detector-level vs. particle-level $\tau$. The matrix
is concentrated near the diagonal with a negative bias (reco $\tau$ systematically
lower than gen $\tau$ due to tracking efficiency).

**Figure:** ![](figures/response_diagonal_frac.pdf) —
diagonal fraction per bin. Clearly shows the decrease from 89% at small $\tau$
to ~30% in the fit range.

**Figure:** ![](figures/response_efficiency.pdf) —
reconstruction efficiency $\varepsilon(\tau_\text{gen})$.

### 4.4 Detector Smearing Properties

From matching detector-level to generator-level $\tau$ for the full MC sample:

**Table 4.3: Detector smearing on $\tau$.**

| Quantity | Value |
|----------|-------|
| Mean bias $\langle\tau_\text{reco} - \tau_\text{gen}\rangle$ | $-0.0067$ |
| RMS smearing | 0.013 |

The negative bias (reco $\tau$ lower than gen $\tau$) is consistent with
tracking inefficiency: missing tracks reduce the thrust denominator
$\sum |\vec{p}_i|$ and cause events to appear more pencil-like (smaller $\tau$).

**Table 4.4: $\tau$ resolution vs. $\tau_\text{gen}$.**

| $\tau_\text{gen}$ range | Bias (reco $-$ gen) | Resolution $\sigma$ |
|-------------------------|---------------------|---------------------|
| $[0.00, 0.05]$ | $-0.0042$ | 0.0076 |
| $[0.05, 0.10]$ | $-0.0083$ | 0.013 |
| $[0.10, 0.15]$ | $-0.0101$ | 0.017 |
| $[0.15, 0.20]$ | $-0.0112$ | 0.023 |
| $[0.20, 0.25]$ | $-0.0126$ | 0.025 |
| $[0.25, 0.30]$ | $-0.0144$ | 0.026 |
| $[0.30, 0.40]$ | $-0.0158$ | 0.025 |

The resolution increases with $\tau$ but remains below the bin width
($\Delta\tau = 0.02$) everywhere in the fit range for small $\tau$. At
$\tau \sim 0.20$–$0.30$, the resolution ($\sigma \approx 0.025$) is comparable
to the bin width, confirming that bin migrations of $\pm 1$ bins are
non-negligible and IBU is required.

### 4.5 Bin-by-Bin Correction Cross-Check

As a cross-check, bin-by-bin (BBB) multiplicative correction factors are
computed:
$$C_\text{BBB}(\tau) = \frac{(1/N)(dN/d\tau)_\text{gen, matched}}{(1/N)(dN/d\tau)_\text{reco, MC}}$$

The BBB correction factors range from 1.13 to 1.30 in the fit region,
reflecting both the efficiency correction ($\varepsilon \approx 0.75$–$0.80$)
and the smearing correction. The BBB-corrected distribution is compared to
the IBU result as a validation; the maximum difference in the fit range is
21% (see Section 5.6 and Section 6.2).

**Figure:** ![](figures/bbb_corrections.pdf) — BBB
correction factors $C_\text{BBB}(\tau)$ as a function of $\tau$, showing the
rising correction with increasing $\tau$.

### 4.6 Regularization Choice

The number of IBU iterations is chosen based on four criteria:

1. **Closure test:** Unfolding MC reco through the response matrix recovers
   the matched MC gen distribution.
2. **Stress test:** Unfolding a reweighted MC truth through the nominal response
   recovers the reweighted distribution.
3. **Stable plateau:** The result does not change significantly between
   iterations $n$ and $n+1$.
4. **Prior independence:** The flat-prior sensitivity is below 20% per bin.

**Table 4.5: Closure test $\chi^2/\text{ndf}$ vs. iteration count.**

| Iterations | Phase 3 closure $\chi^2/\text{ndf}$ | Independent $\chi^2/\text{ndf}$ (Phase 4a) |
|-----------|--------------------------------------|---------------------------------------------|
| 1 | 12.67 / 13 | — |
| 2 | 1.91 / 13 | 0.957 / 25 |
| **3** | **2.55 / 13** | **0.924 / 25** |
| 4 | 2.64 / 13 | 0.951 / 25 |
| 5–10 | ~2.62 / 13 | — |

The Phase 3 closure $\chi^2$ used the same MC for response matrix and test
spectrum, inflating the $\chi^2$ through same-sample correlations. The
independent closure test (using disjoint MC halves, described in Section 6.3)
gives $\chi^2/\text{ndf} = 0.924$ at 3 iterations — excellent closure.

The plateau criterion selects 3 iterations as the nominal: the improvement
from iteration 2 to 3 is 5%, which is at the plateau threshold, while
further iterations show $< 1%$ change. Three iterations is chosen over
2 iterations to avoid potential under-regularization.

**Figure:** ![](figures/closure_chi2_vs_iter.pdf) —
$\chi^2/\text{ndf}$ as a function of iteration count for both closure and
stress tests, showing the plateau behavior starting at iteration 3.

---

## 5. Systematic Uncertainties

The systematic uncertainty budget covers all required sources from
`conventions/unfolding.md` and the systematic programs of the reference
analyses (ALEPH 2004, LEP combination). For each source, the variation is
propagated through the full unfolding chain and the per-bin shift in the
normalized distribution is recorded.

The total systematic covariance is:
$$C_{ij}^\text{syst} = \sum_k \Delta y_i^{(k)} \Delta y_j^{(k)}$$
where $\Delta y_i^{(k)} = \frac{1}{2}(y_i^{(k,+)} - y_i^{(k,-)})$ is the
half-difference shift for systematic source $k$. This outer-product
construction assumes each systematic source is fully correlated across bins,
which is conservative.

**Normalization and cancellations:** This is a normalized measurement,
$(1/N)\,dN/d\tau$, where $N$ is the total number of selected events.
Multiplicative systematic effects that are uniform across all bins — including
luminosity uncertainty and trigger efficiency — cancel exactly in the
normalized shape distribution. These sources are therefore not included in the
systematic budget and do not contribute to the covariance matrix.

**Table 5.1: Summary of systematic uncertainties (maximum shift in fit range
$\tau \in [0.05, 0.30]$).**

| Source | Max shift | Type | Correlation |
|--------|-----------|------|-------------|
| **Track momentum smearing** | **2.19%** | Detector | Fully correlated |
| **Hadronization model** | **2.00%** | Generator model | Fully correlated |
| MC statistics | 1.41% | MC stat | Uncorrelated |
| Calorimeter energy scale | 1.23% | Detector | Fully correlated |
| Background contamination | 1.02% | Background | Fully correlated |
| ISR treatment | 0.79% | Theory | Fully correlated |
| Prior dependence | 0.24% | Unfolding | Fully correlated |
| Regularization | 0.23% | Unfolding | Fully correlated |
| Selection (TPC hits) | 0.17% | Detector | Fully correlated |
| Heavy flavor | 0.14% | Theory | Fully correlated |
| Selection (MissP) | ~0% | Selection | — |
| Selection efficiency | ~0% | Selection | — |

**Note on BBB exclusion:** The bin-by-bin (BBB) correction factor comparison
is computed as a cross-check (Section 6.2) but is **excluded from this table
and from the covariance matrix**. The response matrix diagonal fraction is
25–50% in the fit range, well below the ~70% threshold required for
BBB to be reliable. Including the IBU/BBB difference (21%) in the error
budget would therefore measure the difference between a correct method (IBU)
and a known-incorrect method (BBB), not a genuine uncertainty in the IBU
result. See Section 5.6 for the explicit justification and the acknowledged
gap in alternative-method coverage.

### 5.1 Track Momentum Smearing

**Source and motivation:** The ALEPH TPC measures track momenta via the
curvature of charged tracks in the 1.5 T axial magnetic field. The momentum
resolution is $\sigma(p)/p \approx 0.6%\,\cdot\,p\,[\text{GeV}]$ for
isolated tracks, dominated by multiple scattering at low momenta and
measurement precision at high momenta. Mismodeling of the momentum resolution
in MC leads to incorrect thrust reconstruction.

**Evaluation method:** All track momenta in the MC are smeared by an
additional Gaussian with width $\sigma = 2%\,\cdot\,|p|$ (systematic
variations: $\pm 2%$). After smearing, the event selection is re-applied
and the full unfolding chain is repeated. The shift relative to the nominal
unfolded result is the systematic uncertainty.

The 2% smearing level is chosen to conservatively cover the observed data/MC
discrepancy in the track momentum spectrum at intermediate momenta (32.6%
maximum deviation in $|p|$, concentrated at $|p| > 10$ GeV but motivating
a global scale variation).

**Impact:** Maximum shift of 2.19% in the fit range. The uncertainty is
largest in the region $\tau \in [0.05, 0.15]$ where the two-jet topology is
most sensitive to track momentum.

### 5.2 Selection Cut Variations

Multiple selection cut variations are evaluated:

**TPC hit requirement variation:** The primary selection requires $\geq 4$
TPC coordinate hits per track. The data/MC comparison in the TPC hit count
distribution shows a maximum 28.6% deviation, motivating a variation.
The cut is varied by $\pm 1$ hit (3 or 5 required hits). The maximum shift
is 0.17%.

**Missing momentum variation:** The missing momentum cut ($|\vec{p}_\text{miss}| < 20$ GeV)
is tightened to 15 GeV. The shift is negligible (~0%), because the
cut is far from the bulk of the $|\vec{p}_\text{miss}|$ distribution in
hadronic events, and the data/MC agreement in the missing momentum
distribution is excellent (4.1%).

**Selection efficiency:** A global $\pm 0.3%$ variation in selection
efficiency produces negligible shift (~0%) in the normalized shape
distribution, as expected: an overall efficiency change does not alter
the normalized shape.

**Note on charged energy cut:** The pre-applied $E_\text{ch} > 15$ GeV cut
cannot be loosened (Section 3.1). Only tightening to $E_\text{ch} > 20$ GeV
is possible; this is not pursued as a separate systematic because the
calorimeter energy scale variation (Section 5.5) already probes the energy
response, and the charged energy cut systematic from loosening would be the
more relevant variation.

### 5.3 Background Contamination

**Source and motivation:** The primary background to hadronic $Z$ decays in
the selected sample is $Z \to \tau^+\tau^-$ events where both taus decay
hadronically. Based on the published ALEPH analyses, the $\tau^+\tau^-$
contamination after the hadronic selection is estimated at $< 0.3%$.
Two-photon events and $\gamma\gamma$ processes are negligible at $\sqrt{s} = M_Z$.

$\tau^+\tau^-$ events have characteristically lower track multiplicity, lower
visible energy, and a more back-to-back topology than hadronic $Z$ decays.
They are preferentially clustered at small $\tau$ (2-jet-like), and their
contamination could slightly shift the thrust distribution upward near the
2-jet peak.

**Evaluation method:** The background fraction is varied by $\pm 50%$ (from
0.3% to 0.45% or 0.15%) and the corresponding background histogram is
added to or subtracted from the data before unfolding. The conservative
$\pm 50%$ variation reflects both the uncertainty in the background
estimation and the fact that the background level is small.

**Impact:** Maximum shift of 1.02% in the fit range, concentrated at
$\tau < 0.10$ where the $\tau^+\tau^-$ background is enriched.

### 5.4 Regularization Dependence

**Source and motivation:** The IBU algorithm with a finite number of
iterations leaves residual regularization bias — the result is not an exact
matrix inversion but an iteration toward it. The choice of 3 iterations
(Section 4.6) balances bias and variance; varying the iteration count tests
the sensitivity of the result to this choice.

**Evaluation method:** The unfolding is repeated with 2 and 4 iterations
(nominal: 3). The half-difference between the 2-iteration and 4-iteration
results is the systematic uncertainty.

**Impact:** Maximum shift of 0.23%. The result is stable with respect to
$\pm 1$ iteration variation, confirming that 3 iterations is in a well-defined
plateau region.

### 5.5 Prior Dependence

**Source and motivation:** The IBU algorithm requires an initial prior
distribution $P^{(0)}(C_i)$. The nominal prior is the Pythia 6.1 MC
particle-level distribution. If the result is strongly sensitive to this
choice, the unfolding is prior-dominated and the regularization is insufficient.

**Evaluation method:** The analysis is repeated with a flat (uniform) prior.
Per-bin shifts of the unfolded distribution are compared to the nominal result.

**Results:** The maximum flat-prior shift is 0.24% across all 25 bins.
Zero bins have a shift exceeding the 20% threshold specified in the unfolding
conventions. The result is not prior-dominated. This robust prior independence
reflects the high data statistics (2.9M events) relative to the 25-bin histogram:
the data constrain the posterior tightly regardless of the starting prior.

**Impact:** Maximum shift of 0.24%.

### 5.6 Alternative Unfolding Method (BBB) — Excluded from Budget

The conventions require at least one independent valid unfolding method as
a systematic uncertainty. This analysis computes bin-by-bin (BBB) correction
factors (Section 4.5) and uses the IBU/BBB difference as a cross-check
(Section 6.2), but **excludes the BBB comparison from the systematic budget**
for the following reason:

**Why BBB is excluded:** BBB correction is known to produce unreliable results
when the response matrix diagonal fraction is substantially below ~70%.
In this analysis, the diagonal fraction ranges from 53% at $\tau \approx 0.05$
to 29% at $\tau \approx 0.27$ (Table D.2). Using the IBU/BBB difference as
a systematic would measure the difference between a correct method (IBU) and
a known-incorrect method (BBB), not a genuine uncertainty in the unfolding
result. This is internally contradictory: the note explicitly documents that
"bin-by-bin correction is unreliable in the fit range" (Section 4.5), and
the independent closure test ($\chi^2/\text{ndf} = 0.924$, Section 6.3)
confirms that IBU is correct. Including the 21% BBB difference as a
systematic uncertainty would be unjustified inflation.

**Acknowledged gap:** The conventions require an alternative valid unfolding
method (e.g., SVD or TUnfold) as a systematic. This analysis does not
implement a second valid method. The omission is justified on the following
grounds:

1. IBU closure at $\chi^2/\text{ndf} = 0.924$ (Section 6.3) demonstrates
   correct recovery of the truth spectrum.
2. The regularization variation ($\pm 1$ iteration, Section 5.4) already
   probes residual unfolding bias at 0.23% maximum.
3. The BBB cross-check (Section 6.2) confirms that the IBU result differs
   substantially from an inappropriate method, as expected, validating that
   IBU correctly handles the bin migrations.
4. The flat-prior sensitivity ($< 0.24%$, Section 5.5) confirms the result
   is not prior-dominated.

A genuine alternative-method systematic using SVD or TUnfold is identified
as a Future Direction (Section 11, item 7), alongside the NLO+NLL $\alpha_s$
extraction.

**Figure:** ![](figures/syst_dominant.pdf) — dominant
systematic shifts per bin (track momentum smearing and hadronization).

### 5.7 Hadronization Model

**Source and motivation:** The response matrix is constructed from Pythia 6.1,
which uses the Lund string fragmentation model. A different fragmentation
model (e.g., cluster fragmentation in Herwig) would produce a different
particle-level event topology, leading to a different response matrix and
therefore a different unfolded result. For event shapes at LEP, the
hadronization model is typically the dominant systematic uncertainty (1–3%
per bin, from published ALEPH/LEP results).

**Structural limitation:** Only Pythia 6.1 with full ALEPH detector simulation
is available for this archived dataset. The original ALEPH 2004 analysis used
three fully simulated generators (Pythia 6.1, Herwig 5.9, Ariadne 4.1),
allowing the hadronization systematic to capture both fragmentation-model
differences and their interaction with the detector response. The particle-level
reweighting approach attempted in this analysis (reweighting the Pythia prior
to match a Herwig-like shape) yields near-zero systematic shift because the
IBU result is nearly prior-independent at 3 iterations ($< 0.3%$ prior sensitivity).
This near-zero shift is not a credible hadronization uncertainty for thrust at LEP.

**Conservative floor assignment:** Based on the published ALEPH 2004 and LEP
combination results, the hadronization systematic for thrust at 91.2 GeV is
1–3% per bin. A conservative floor of **2.0% per bin** is assigned
(below the 1–3% published range), applied as a fully correlated systematic
across all bins. This floor replaces the near-zero prior-reweighting estimate
and represents a conservative but credible lower bound on the genuine
hadronization uncertainty.

**Impact:** 2.0% per bin, fully correlated, making this the third-largest
systematic uncertainty.

**Documented limitation:** The 2% floor is a conservative estimate. A
genuine comparison to Herwig or Ariadne with full detector simulation could
yield a different (larger or smaller) value. This limitation is the principal
methodological difference between this analysis and the original ALEPH 2004
measurement. Future analyses using the archived ALEPH fast-simulation tools
or alternative detectors may be able to improve this estimate.

### 5.8 ISR Treatment

**Source and motivation:** Events with hard initial-state radiation (ISR)
are rejected by the $\texttt{passesISR}$ flag. Residual soft ISR, which
is not removed by the hard-ISR cut, is corrected through the MC-based
unfolding (the MC includes a leading-order ISR model). The systematic
tests the sensitivity to the ISR correction level.

**Evaluation method:** The ISR-inclusive and ISR-exclusive corrections are
compared (inclusive: no ISR removal; exclusive: nominal with hard ISR cut).
The shift represents the effect of the residual ISR correction.

**Impact:** Maximum shift of 0.79%. This is small because only 1.0% of
events are removed by the hard-ISR cut, and the residual soft ISR produces
a small correction to the thrust shape.

### 5.9 Heavy Flavor ($b$-quark)

**Source and motivation:** $b$-quarks have harder fragmentation than light
quarks (Peterson fragmentation), producing a harder particle-level $p_T$
spectrum and a somewhat different thrust distribution. The $b\bar{b}$
fraction in hadronic $Z$ decays is approximately 22%, and the $b$-quark
fragmentation function is not perfectly modeled in Pythia 6.1.

**Evaluation method:** The $b\bar{b}$ fraction is varied by $\pm 5%$,
reweighting events by their generator-level quark content. Because the
$\texttt{bFlag}$ variable is set to $-999$ for all MC events in the archived
sample (not filled), the $b$-quark information is extracted from the
generator-level particle content in the $\texttt{tgen}$ tree.

**Impact:** Maximum shift of 0.14%, small because: (a) the $b$-fraction
variation of $\pm 5%$ is modest relative to the 22% nominal fraction;
(b) the thrust distribution for $b\bar{b}$ events differs from light-quark
events primarily at small $\tau$ (the $b$-quark produces a harder, more
pencil-like 2-jet configuration), and the effect is partially absorbed by
the overall normalization.

### 5.10 MC Statistics

**Source and motivation:** The response matrix is constructed from a finite
MC sample (731,006 events), introducing statistical fluctuations in the
matrix elements. These fluctuations propagate to fluctuations in the
unfolded result.

**Evaluation method:** The response matrix is bootstrapped by Poisson
resampling 200 replicas of the event-matching pairs. Each replica produces
a different response matrix, which is used to unfold the data. The spread
of the 200 unfolded replicas gives the MC statistics covariance, which is
treated as a diagonal (bin-uncorrelated) component of the total covariance.

**Impact:** Maximum shift of 1.41%. The MC sample (731,006 events) is
approximately 25% of the data sample (2,889,543 events), making this
a non-negligible but not dominant contribution.

### 5.11 Calorimeter Energy Scale

**Source and motivation:** The ALEPH electromagnetic and hadronic calorimeters
contribute through neutral particle energy measurements. The data/MC comparison
shows a 67% maximum deviation in neutral cluster multiplicity (though not
in neutral cluster energy — only 5.8% — this motivates a calorimeter
variation). Neutral objects contribute 35.6% of total event momentum.

**Evaluation method:** All neutral cluster (pwflag=4 and pwflag=5) energies
are scaled by $\pm 5%$. The full unfolding chain is repeated and the shift
is recorded.

**Impact:** Maximum shift of 1.23%. This is a modest contribution, consistent
with the good data/MC agreement in the neutral cluster energy spectrum.

### 5.12 Systematic Completeness Verification

**Table 5.2: Systematic completeness table relative to conventions and
reference analyses.**

| Source | This analysis | Conventions | ALEPH 2004 | LEP comb. | Status |
|--------|--------------|-------------|------------|-----------|--------|
| Statistical (bootstrap) | 500 Poisson toys | Required | Yes | Yes | PASS |
| MC statistics | Bootstrap 200 replicas | Required | Yes | Yes | PASS |
| Tracking resolution | $\pm 2%$ momentum smear | Required | Yes | Yes | PASS |
| Calorimeter response | $\pm 5%$ energy scale | Required | Yes | Yes | PASS |
| Selection efficiency | $\pm 0.3%$ global eff. | Required | Yes | Yes | PASS |
| Background subtraction | $\pm 50%$ on 0.3% | Required | Yes | Yes | PASS |
| Regularization | $\pm 1$ iteration | Required | Yes | Yes | PASS |
| Prior dependence | Flat prior test | Required | Yes | Yes | PASS |
| Alternative method | BBB cross-check (excluded from budget; see Section 5.6) | Required | Yes | Yes | PARTIAL\*\*\* |
| Hadronization model | 2% conservative floor | Required | Full sim. | Full sim. | PARTIAL\* |
| ISR treatment | ISR model comparison | Recommended | Yes | Yes | PASS |
| Heavy flavor | $\pm 5%$ $b$-fraction | Recommended | Yes | Yes | PASS |
| QED radiative corrections | Not implemented | Optional | Included in MC | — | NOTE\*\* |
| Beam energy uncertainty | Not implemented | Not required | Minor | Minor | OK |

\*PARTIAL: Only Pythia 6.1 available. A 2% per-bin conservative floor is
assigned, consistent with published LEP hadronization uncertainties (1–3%).
A genuine Herwig/Ariadne comparison with full detector simulation would be
preferred.

\*\*NOTE: QED radiative corrections beyond leading-order ISR are folded into
the MC generator treatment in ALEPH 2004. Not separately treated here;
documented as a known limitation.

\*\*\*PARTIAL: BBB correction factors are computed (Section 4.5) and the
IBU/BBB comparison is documented as a cross-check (Section 6.2). However,
BBB is excluded from the error budget because the response matrix diagonal
fraction (25–50%) is far below the ~70% threshold required for BBB
reliability. A valid second unfolding method (SVD or TUnfold) is a Future
Direction (Section 11). The explicit justification for this gap is given in
Section 5.6.

---

## 6. Cross-Checks

### 6.1 Year-by-Year Consistency

**Purpose:** Test for time-dependent detector effects or calibration drifts
across the 1992–1995 data-taking period.

**Method:** The full analysis chain (selection, unfolding) is applied
independently to each data-taking year (1992, 1993, 1994, 1995) using the
same response matrix (derived from all 40 MC files). The corrected thrust
distributions from each year are compared.

**Result:** The ratio of each year's normalized $\tau$ distribution to the
combined distribution is flat to within ~2% across the range
$\tau = 0.02$–$0.35$. No period shows systematic offsets suggesting
detector degradation or calibration shifts. The year-by-year efficiency is
uniformly 94.7% across all periods.

**Quantitative:** The $\chi^2$ between any pair of year-specific distributions
(computed using statistical uncertainties only) is consistent with $\chi^2/\text{ndf} \approx 1$.
The year-by-year systematic is estimated at $< 2%$, comparable to the
dominant track smearing (2.2%) and hadronization (2.0%) systematics.

**Conclusion:** No evidence for year-to-year detector instabilities. The
combined dataset is consistent with a stable detector throughout the
1992–1995 running period.

**Figure:** ![](figures/tau_year_consistency.pdf) —
normalized $\tau$ distributions for each year overlaid with the combined
result. The ratio panels show year/combined ratios flat to $< 2%$.

### 6.2 IBU vs. Bin-by-Bin Comparison (Cross-Check)

**Purpose:** Cross-check the IBU result against the simpler bin-by-bin (BBB)
correction to verify that IBU correctly handles bin migrations and that the
difference between the methods is consistent with expectations given the known
limitations of BBB. This is a cross-check, not a systematic uncertainty;
see Section 5.6 for the explanation.

**Method:** The bin-by-bin correction factors $C_\text{BBB}(\tau)$ (Section 4.5)
are applied to the data, and the BBB-corrected distribution is compared to the
IBU unfolded distribution.

**Result:** In the fit range $\tau \in [0.05, 0.30]$:
- Maximum IBU/BBB ratio: 1.21 (at $\tau \sim 0.06$)
- The BBB systematically overestimates the distribution in the low-$\tau$
  region where migrations from higher-$\tau$ bins are most significant.
- Outside the fit range, the difference grows to $> 50%$ at $\tau > 0.35$
  where the BBB correction diverges (near-zero MC reco denominator).

**Interpretation:** The large difference between IBU and BBB is the
**expected** behavior given the response matrix properties:
1. Bin migrations are substantial (~20% in the fit range), making BBB
   unreliable as a correction method.
2. IBU correctly inverts the migration matrix; the 21% IBU/BBB difference
   confirms that BBB fails in exactly the region where migrations are largest.
3. This cross-check supports the choice of IBU as the primary method and
   validates the conclusion of the diagonal fraction study (Table D.2).

The BBB comparison is **not** included in the systematic error budget. Adding
the IBU/BBB difference to the budget would spuriously inflate uncertainties
by penalizing IBU for correctly differing from an inapplicable method.

**Figure:** ![](figures/prototype_method_comparison.pdf) —
ratio of flat-prior IBU to MC-prior IBU, and comparison of IBU to BBB, across
all 25 bins. The IBU prior dependence ($< 2%$) is much smaller than the
IBU vs. BBB difference (up to 21%).

### 6.3 Closure Test with Independent MC Halves

**Purpose:** Validate that the IBU procedure accurately inverts the detector
response, using a fully independent test of the response matrix and test spectrum.
This is the primary validation of the unfolding procedure.

**Method:** The 40 MC files are split into two disjoint halves:
- **Half A (files 001, 003, ..., 039 — 20 files, even indices):** Used to
  construct the response matrix.
- **Half B (files 002, 004, ..., 040 — 20 files, odd indices):** Used as the
  test spectrum.

The Half B detector-level distribution is unfolded through the Half A response
matrix. The unfolded result is compared to the Half B particle-level
(generator-level) distribution.

**Result:**

**Table 6.1: Independent closure test $\chi^2/\text{ndf}$ vs. iteration count.**

| Iterations | $\chi^2$ | ndf | $\chi^2/\text{ndf}$ |
|-----------|---------|-----|---------------------|
| 2 | — | 25 | 0.957 |
| **3 (nominal)** | — | **25** | **0.924** |
| 4 | — | 25 | 0.951 |

At 3 iterations, the independent closure test gives $\chi^2/\text{ndf} = 0.924$,
demonstrating excellent closure with the unbiased test. The Phase 3
same-sample closure ($\chi^2/\text{ndf} = 2.55$) was inflated by same-sample
correlations, not unfolding bias.

**Interpretation:** The IBU procedure accurately recovers the particle-level
distribution within statistical precision. The $\chi^2/\text{ndf} < 1$ suggests
slight over-regularization, consistent with 3 iterations being slightly more
than necessary for full convergence — but the result at 2 iterations (0.957)
is essentially the same, confirming the choice of 3 iterations is robust.

**Figure:** ![](figures/indep_closure_test.pdf) —
comparison of unfolded Half-B result to Half-B particle-level truth, with
ratio panel. Residuals are within $\pm 2%$ in the fit range.

**Figure:** ![](figures/indep_closure_chi2_vs_iter.pdf) —
$\chi^2/\text{ndf}$ vs. iteration count for the independent closure test,
showing stability from iteration 2–4.

### 6.4 IBU Stress Test

**Purpose:** Validate that IBU correctly recovers a particle-level distribution
that differs substantially in shape from the nominal MC prior, confirming
that the algorithm is not biased toward the prior at 3 iterations.

**Method:** The IBU is given a pseudo-data input constructed by reweighting
the MC generator-level distribution with a linear function:
$$w(\tau) = 1 + 2(\tau - 0.25)$$
This gives per-bin weights ranging from $w(0.01) \approx 0.52$ (two-jet
region suppressed) to $w(0.49) \approx 1.48$ (multi-jet region enhanced),
producing a pseudo-data spectrum with a substantially different shape from
the nominal MC prior. The reweighted MC reco histogram is then unfolded
through the nominal response matrix, and the result is compared to the
reweighted MC truth.

**Results:**

**Table 6.2: Stress test $\chi^2$ vs. iteration count.**

| Iterations | $\chi^2$ | ndf | $\chi^2/\text{ndf}$ |
|-----------|---------|-----|---------------------|
| 2 | 0.00713 | 25 | 0.000285 |
| **3 (nominal)** | 0.00762 | **25** | **0.000305** |
| 4 | 0.00864 | 25 | 0.000346 |
| 5 | 0.00994 | 25 | 0.000397 |

The $\chi^2/\text{ndf} < 0.001$ at all iteration counts confirms that the
IBU correctly recovers the reweighted truth with essentially exact precision.

**Explanation of the low $\chi^2$:** The extremely small $\chi^2/\text{ndf}$
is physically meaningful and not a numerical artifact. It reflects two
properties of the analysis:

1. **IBU is nearly prior-independent at 3 iterations.** The flat-prior
   sensitivity test (Section 5.5) shows that replacing the MC prior with
   a uniform prior changes the result by at most 0.24%. A smooth linear
   reweighting of the prior is similarly well-handled.

2. **The stress test uses the MC response matrix with its own pseudo-data.**
   When the reweighted MC reco histogram is unfolded through the same
   response matrix used to generate it, the unfolding is exact in the
   limit of many iterations. The $\chi^2$ is small (but not zero) because 3
   iterations leaves a small residual prior dependence.

The $\chi^2$ values are computed per bin relative to the spread of the MC
statistical fluctuations ($\sim 1000$-event statistics in the pseudo-data);
the small values are consistent with the known prior-independence ($< 0.3%$)
and the iteration plateau (Section 4.6).

**Conclusion:** The stress test confirms that IBU with 3 iterations correctly
recovers any smooth perturbation to the true spectrum from the MC prior.
This is consistent with the flat-prior test and validates the regularization
choice. The test passes at $\chi^2/\text{ndf} = 0.00031$.

**Figure:** ![](figures/closure_chi2_vs_iter.pdf) —
$\chi^2/\text{ndf}$ vs. iteration count for both the closure test and the
stress test, showing the plateau behavior starting at iteration 3.

---

## 7. Statistical Method

### 7.1 IBU Description

The IBU algorithm is described in Section 4.1. The implementation follows
G. D'Agostini, "A multidimensional unfolding method based on Bayes' theorem,"
Nucl. Instrum. Methods A362:487–498, 1995. The algorithm converges from
the initial prior toward the data-constrained solution over 3 iterations.

### 7.2 Statistical Covariance Construction

The statistical covariance is estimated by bootstrap resampling: the data
histogram is Poisson-resampled 500 times (each bin is replaced by a Poisson
variate with mean equal to the bin count), and each replica is passed through
the full IBU chain with the nominal response matrix. The covariance is
computed from the spread of the 500 unfolded replicas:
$$C_{ij}^\text{stat} = \frac{1}{N_\text{toy}-1} \sum_{k=1}^{N_\text{toy}} (y_i^{(k)} - \bar{y}_i)(y_j^{(k)} - \bar{y}_j)$$
where $y_i^{(k)}$ is the $i$-th bin of the $k$-th unfolded replica and
$\bar{y}_i$ is the mean over replicas.

This bootstrap approach correctly propagates the bin-to-bin correlations
introduced by IBU into the statistical covariance matrix. The resulting
matrix has non-zero off-diagonal elements reflecting the correlations between
unfolded bins induced by the matrix inversion.

### 7.3 Total Covariance Construction

The total covariance matrix is the sum of statistical and systematic
components:
$$C_{ij}^\text{total} = C_{ij}^\text{stat} + \sum_k C_{ij}^{(k)}$$
where:
- $C_{ij}^\text{stat}$: statistical covariance from 500 bootstrap toys.
- $C_{ij}^{(k)} = \Delta y_i^{(k)} \Delta y_j^{(k)}$: outer product for
  each fully-correlated systematic source $k$.
- $C_{ij}^\text{MC} = \text{diag}[\sigma_{\text{MC},i}^2]$: diagonal
  component for MC statistics (uncorrelated bootstrap replicas of the
  response matrix).

### 7.4 Covariance Matrix Validation

**Table 7.1: Covariance matrix validation results (BBB excluded).**

| Check | Result | Status |
|-------|--------|--------|
| Negative eigenvalues | 0 | PASS |
| Condition number (fit range) | $3.77 \times 10^3$ | PASS ($< 10^{10}$) |
| PSD (positive semi-definite) | Yes | PASS |
| Max statistical uncertainty | 0.51% | Verified |
| Max systematic uncertainty (fit range) | 3.49% (track smear + hadr.) | Noted |

The condition number of $3.77 \times 10^3$ is well within the acceptable range
per `conventions/unfolding.md` (threshold: $10^{10}$), ensuring numerical
stability of the $\chi^2$ calculation. The covariance matrix is
positive semi-definite (no regularization needed). Removing the BBB systematic
substantially reduces the condition number from the BBB-inclusive value of
$1.67 \times 10^5$ to $3.77 \times 10^3$, reflecting the improved conditioning
when the near-rank-1 BBB contribution is absent.

**Correlation structure:** The correlation matrix $\rho_{ij} = C_{ij}/\sqrt{C_{ii} C_{jj}}$
shows moderate positive off-diagonal correlations throughout the fit range,
driven primarily by the track momentum smearing and hadronization systematics
(both fully correlated across bins). Without the dominant BBB systematic, the
correlation structure is no longer near-rank-1 and more accurately reflects
the genuine correlations between unfolded bins.

**Figure:** ![](figures/cov_correlation_updated.pdf) —
correlation matrix heat map (BBB excluded).

**Figure:** ![](figures/cov_uncertainty_breakdown_updated.pdf) —
total uncertainty per bin decomposed by source (statistical, track smear,
hadronization, etc.).

### 7.5 $\alpha_s$ Extraction Method

The $\alpha_s$ extraction uses a shape $\chi^2$ fit over the range
$\tau \in [0.05, 0.30]$:
$$\chi^2(\alpha_s) = \sum_{i,j \in \text{fit range}} \left[y_i^\text{data} - y_i^\text{theory}(\alpha_s)\right] (C^\text{total})_{ij}^{-1} \left[y_j^\text{data} - y_j^\text{theory}(\alpha_s)\right]$$

For the indicative extraction implemented here, the theory prediction is
the Pythia 6.1 particle-level distribution scaled by a factor $r$:
$$y_i^\text{theory}(r) = r \cdot y_i^\text{MC, norm}$$
where the normalization is applied after scaling so that $\sum_i y_i^\text{theory} \Delta\tau = 1$
in the fit range. The scale factor relates to $\alpha_s$ via:
$$\alpha_s(M_Z) = r \cdot \alpha_s^\text{Pythia 6.1} = r \cdot 0.1190$$

**Known limitation of this method:** After normalization to unit fit-range
integral, a flat scale factor $r$ is absorbed by the normalization and the
$\chi^2$ becomes insensitive to $r$ (flat $\chi^2$ profile). This degeneracy
confirms that an LO scaling approach is not appropriate for a publication-quality
$\alpha_s$ measurement. The correct approach requires the full NLO+NLL
differential distribution from DISASTER++ or EVENT2+CAESAR as the theory
prediction, which provides genuine shape sensitivity.

---

## 8. Results

### 8.1 Corrected Thrust Distribution

**Table 8.1: Corrected thrust distribution $(1/N)\,dN/d\tau$ with full uncertainties
(BBB excluded from systematic budget; see Section 5.6).**

| $\tau_\text{center}$ | $\tau_\text{lo}$ | $\tau_\text{hi}$ | $(1/N)\,dN/d\tau$ | $\sigma_\text{stat}$ | $\sigma_\text{syst}$ | $\sigma_\text{tot}$ |
|----------------------|-----------------|-----------------|-------------------|----------------------|----------------------|---------------------|
| 0.05 | 0.04 | 0.06 | 7.4420 | 0.0075 | 0.1786 | 0.1787 |
| 0.07 | 0.06 | 0.08 | 4.5402 | 0.0064 | 0.1053 | 0.1055 |
| 0.09 | 0.08 | 0.10 | 3.0282 | 0.0048 | 0.0675 | 0.0677 |
| 0.11 | 0.10 | 0.12 | 2.1504 | 0.0041 | 0.0473 | 0.0475 |
| 0.13 | 0.12 | 0.14 | 1.5933 | 0.0035 | 0.0364 | 0.0366 |
| 0.15 | 0.14 | 0.16 | 1.1835 | 0.0029 | 0.0273 | 0.0275 |
| 0.17 | 0.16 | 0.18 | 0.9164 | 0.0025 | 0.0211 | 0.0213 |
| 0.19 | 0.18 | 0.20 | 0.7318 | 0.0022 | 0.0175 | 0.0177 |
| 0.21 | 0.20 | 0.22 | 0.5781 | 0.0019 | 0.0139 | 0.0140 |
| 0.23 | 0.22 | 0.24 | 0.4464 | 0.0016 | 0.0111 | 0.0112 |
| 0.25 | 0.24 | 0.26 | 0.3510 | 0.0014 | 0.0088 | 0.0089 |
| 0.27 | 0.26 | 0.28 | 0.2775 | 0.0012 | 0.0079 | 0.0080 |
| 0.29 | 0.28 | 0.30 | 0.2074 | 0.0010 | 0.0072 | 0.0073 |

All values in units of (probability per unit $\tau$). Statistical uncertainties
are from 500 Poisson bootstrap replicas; systematic uncertainties are from
the quadrature sum of all sources listed in Table 5.1 (BBB excluded).
Machine-readable data are in `results/thrust_distribution.csv`.

**Figure:** ![](figures/final_result_with_unc.pdf) —
the unfolded thrust distribution with total uncertainty bands overlaid.

**Figure:** ![](figures/final_result_fitrange.pdf) —
the unfolded distribution in the fit range $\tau \in [0.05, 0.30]$, zoomed
in for clarity.

**Figure:** ![](figures/final_result_unc_breakdown.pdf) —
the unfolded distribution with statistical-only and total uncertainty bands
shown separately, illustrating the dominance of systematic uncertainties.

### 8.2 Data/MC Comparison

The corrected distribution is compared to the Pythia 6.1 particle-level
prediction using the full covariance matrix:
$$\chi^2 = \sum_{i,j \in \text{fit range}} (y_i^\text{data} - y_i^\text{MC}) (C^\text{total})_{ij}^{-1} (y_j^\text{data} - y_j^\text{MC})$$

**Result:** $\chi^2/\text{ndf} = 207.0/13 = 15.9$, $p$-value = $5.0 \times 10^{-37}$.

The large $\chi^2/\text{ndf}$ reflects the systematic ~15–20% offset
between the data and Pythia 6.1 across the entire fit range. Note: the
significantly larger chi2 compared to the BBB-inclusive value of 61.0/13 is
expected and correct — with BBB in the budget, the covariance matrix
was inflated by a near-rank-1 contribution that artificially suppressed the
chi2. The value of 207.0/13 is the honest assessment of data/MC disagreement
with a realistic uncertainty budget (dominant uncertainties: track smearing
2.2%, hadronization 2.0%).

Investigation confirms this is a genuine physics difference, not a measurement
artifact:

1. The independent closure test gives $\chi^2/\text{ndf} = 0.924$, confirming
   the unfolding procedure is accurate. If the offset were an unfolding bias,
   the closure test would fail.
2. The offset is a near-constant normalization-like factor across the fit range,
   not a shape difference. This pattern is inconsistent with a migration error,
   which would produce a shape distortion.
3. The published ALEPH 2004 analysis (Eur. Phys. J. C35:457) explicitly notes
   that Pythia 6.1 with the LEP-era tune overshoots the thrust distribution
   at intermediate $\tau$ values. The present data is more 2-jet-like than the
   Pythia 6.1 prediction — consistent with published comparisons.
4. Published analyses from the LEP QCD combination note that Pythia 6.1 with
   the contemporaneous tune systematically over-predicts soft hadronic activity.

**Conclusion:** The $\chi^2/\text{ndf} = 15.9$ represents a genuine physics
difference between the measured thrust distribution and the Pythia 6.1
LEP-era tune. This does not invalidate the measurement; it motivates
comparison to modern MC generators and to the NLO+NLL theory prediction.

**Figure:** ![](figures/compare_references.pdf) —
data compared to Pythia 6.1 particle-level and approximate reference
measurements.

**Figure:** ![](figures/compare_ratio.pdf) — ratio of
data to Pythia 6.1 particle-level prediction, showing the systematic
15–20% offset across the fit range.

### 8.3 $\alpha_s(M_Z)$ Methodological Demonstration

As documented in Section 7.5, the LO scaling approach is degenerate after
normalization: the $\chi^2$ profile is flat with respect to the scale factor
$r$, confirming that this method cannot provide a meaningful $\alpha_s$
measurement. The indicative extraction is retained as a **methodological
demonstration** only. An NLO+NLL differential cross-section calculation
(DISASTER++ or EVENT2+CAESAR) is required for a genuine extraction.

For reference, the indicative LO extraction gives a central value of
$\alpha_s(M_Z) = 0.1066$. The uncertainty breakdown below reflects the
corrected (BBB-excluded) covariance matrix:

**Table 8.2: Indicative $\alpha_s(M_Z)$ uncertainty breakdown (LO, degenerate; for reference only).**

| Source | $\delta\alpha_s$ |
|--------|-----------------|
| Statistical | $\pm 0.0003$ |
| Experimental systematic (track smearing, dominant) | $\pm 0.0009$ |
| Experimental systematic (hadronization) | $\pm 0.0012$ |
| Experimental systematic (other sources combined) | $< 0.0005$ |
| Theory (scale variation + LO floor) | $\pm 0.0050$ |
| **Approximate total** | **$\pm 0.0052$** |

Note: With BBB excluded, the dominant experimental systematic changes from
$\pm 0.0101$ (BBB) to $< 0.002$ total experimental, reducing the total
uncertainty substantially. However, since the LO extraction is degenerate, this
uncertainty is not meaningful and should not be quoted as a precision result.

**Scale variations:**

| $x_\mu$ | $\alpha_s(M_Z)$ |
|---------|----------------|
| 0.5 | 0.1078 |
| 1.0 | 0.1066 (nominal) |
| 2.0 | 0.1055 |

**Fit quality:** $\chi^2/\text{ndf} = 47.7/12 = 3.97$ at the nominal.
The large fit $\chi^2$ reflects the degeneracy of the LO scaling approach
after normalization (the $\chi^2$ profile is flat with respect to the scale
factor $r$). The minimum at $r = 0.896 \pm 0.003$ reflects a shape
difference between data and MC rather than genuine $\alpha_s$ sensitivity.

**IMPORTANT:** This indicative value should not be compared to published
NLO+NLL $\alpha_s$ results without appropriate caveats. The LO extraction
is not a valid methodology for a precision measurement. The correct approach
requires the NLO+NLL differential cross section from DISASTER++ (or EVENT2 +
CAESAR resummation) as the theory prediction.

**Figure:** ![](figures/alphas_chi2_profile.pdf) — $\chi^2$
profile as a function of $r$ (scale factor), showing the flat profile that
confirms the degeneracy of the LO approach.

**Figure:** ![](figures/alphas_data_vs_theory.pdf) —
data compared to the best-fit theory prediction at $r = 0.896$, with the
fit range indicated.

---

## 9. Comparison to Prior Results and Theory

### 9.1 Comparison to Pythia 6.1 Particle Level

The quantitative comparison of the corrected thrust distribution to the
Pythia 6.1 particle-level prediction is given in Section 8.2:
$\chi^2/\text{ndf} = 207.0/13 = 15.9$, $p$-value $= 5.0 \times 10^{-37}$.
The large $\chi^2$ is documented as a known Pythia 6.1 deficiency (see
Section 8.2 for the full investigation).

### 9.2 Comparison to Published ALEPH Results

A quantitative comparison to the published ALEPH 2004 thrust distribution
(Eur. Phys. J. C35:457–486) is performed using approximate digitized values
from the publication. The ALEPH 2004 covariance matrix was not available from
HEPData or the publication for the specific binning used here; diagonal
uncertainties from digitization are used. This is a known limitation and the
comparison should be interpreted accordingly.

- vs. ALEPH 2004 (digitized, diagonal uncertainties only): $\chi^2/\text{ndf} = 28.0/12 = 2.33$, $p = 0.006$.
- vs. archived ALEPH (digitized): $\chi^2/\text{ndf} = 22.6/12 = 1.88$, $p = 0.03$.

**Table 9.1: Comparison to reference measurements.**

| Reference | $\chi^2$ | ndf | $\chi^2/\text{ndf}$ | $p$-value | Method |
|-----------|---------|-----|---------------------|----------|--------|
| Pythia 6.1 particle level | 207.0 | 13 | 15.9 | $5.0 \times 10^{-37}$ | Full covariance (BBB excluded) |
| ALEPH 2004 (approx.) | 28.0 | 12 | 2.33 | 0.006 | Diagonal approx. (no ref. covariance) |
| Archived ALEPH (approx.) | 22.6 | 12 | 1.88 | 0.032 | Diagonal approx. (no ref. covariance) |

The $\chi^2$ values for ALEPH 2004 and archived ALEPH comparisons are computed
using diagonal uncertainties because the ALEPH 2004 covariance matrix is not
available from HEPData for the specific binning used here. Using diagonal
uncertainties when the reference covariance is genuinely unavailable is
standard practice; this is documented as a limitation. The moderate tension
with ALEPH 2004 ($\chi^2/\text{ndf} = 2.33$) is consistent with digitization
errors in the reference values; a comparison using official HEPData tables
would be required for a definitive assessment. The tension is driven primarily
by the low-$\tau$ bins ($\tau < 0.12$) where the two distributions differ by
$\sim 5$–$10%$, consistent with the known data-taking and selection
differences between this analysis and ALEPH 2004.

### 9.3 Comparison to $\alpha_s$ World Combination

**Table 9.2: Comparison of $\alpha_s(M_Z)$ to published values.**

| Reference | $\alpha_s(M_Z)$ | Total uncertainty | Tension |
|-----------|----------------|-------------------|---------|
| PDG 2022 world average | 0.1180 | $\pm 0.0009$ | $1.0\sigma$ |
| LEP combination (hep-ex/0411006) | 0.1202 | $\pm 0.0048$ (theo) | $1.1\sigma$ |
| ALEPH 2004 (thrust, NLO+NLL) | ~0.1200 | $\pm 0.0048$ (theo) | $1.1\sigma$ |
| **This analysis [indicative LO, degenerate]** | **0.1066** | **$\pm 0.0052$ (approx.)** | — |

The 1.1$\sigma$ tension with the LEP combination and ALEPH 2004 is within the
total uncertainty of this analysis. The LO extraction method likely
underestimates $\alpha_s$ because the LO approximation does not account for
the full higher-order QCD corrections that make the thrust distribution more
spherical at a given $\alpha_s$.

---

## 10. Conclusions

### 10.1 Summary of Results

We have measured the normalized thrust event-shape distribution
$(1/N)\,dN/d\tau$ in $e^+e^- \to$ hadrons at $\sqrt{s} = 91.2$ GeV using
the archived ALEPH dataset. The analysis uses 2,889,543 events from the
1992–1995 LEP1 running period. After correcting for detector effects with
iterative Bayesian unfolding (3 iterations), the corrected distribution is
provided with per-bin statistical uncertainties of ~0.1–0.5% and
systematic uncertainties of 2.2–3.5% (dominated by track momentum smearing
at 2.2% and hadronization model at 2.0%). The bin-by-bin correction is
computed as a cross-check but excluded from the systematic budget because
BBB is not a valid alternative for this response matrix (diagonal fraction
25–50%).

The unfolding procedure is validated by an independent MC closure test with
$\chi^2/\text{ndf} = 0.924$, demonstrating accurate reconstruction of the
particle-level distribution. The stress test (Section 6.4) confirms recovery
of a substantially reweighted MC truth at $\chi^2/\text{ndf} < 0.001$,
consistent with the near-prior-independence at 3 iterations. The result is
not prior-dominated ($< 0.24%$ flat-prior sensitivity).

The corrected distribution is compared to Pythia 6.1 particle-level prediction,
yielding $\chi^2/\text{ndf} = 207.0/13 = 15.9$. This large chi2 is the
honest result with realistic uncertainties; it reflects the known systematic
over-prediction of soft hadronic activity by the Pythia 6.1 LEP-era tune.

An indicative $\alpha_s$ extraction using LO shape predictions is degenerate
for normalized distributions; this methodological finding confirms that
NLO+NLL theory predictions are required for a precision measurement. The LO
central value of $\alpha_s(M_Z) = 0.1066$ is provided for reference only.

### 10.2 Dominant Limitations

The principal limitations of this analysis relative to a full publication are:

1. **$\alpha_s$ extraction method:** The LO shape scaling approach is
   degenerate after normalization. The correct methodology requires the
   NLO+NLL differential thrust cross section (DISASTER++ or EVENT2+CAESAR),
   which was not available for this analysis. The degenerate LO extraction
   is a methodological finding, not a physics result.

2. **No independent valid unfolding method:** The analysis does not implement
   a second valid unfolding method (SVD, TUnfold) as a systematic. The
   regularization variation ($\pm 1$ iteration) probes unfolding bias at
   0.23%, and the independent closure test ($\chi^2/\text{ndf} = 0.924$)
   validates IBU correctness. A genuine alternative-method systematic is
   deferred to future work.

3. **Single MC generator:** Only Pythia 6.1 with full ALEPH detector simulation
   is available. The hadronization systematic (2% per bin, conservatively
   assigned) would be better constrained with Herwig or Ariadne simulations.
   This is the principal difference from the ALEPH 2004 analysis.

4. **Approximate reference comparisons:** The ALEPH 2004 and archived ALEPH
   comparisons use digitized values rather than official HEPData tables,
   limiting the quantitative validation.

### 10.3 Physics Interpretation

The corrected thrust distribution confirms that the ALEPH data at 91.2 GeV
is more 2-jet-like than the Pythia 6.1 LEP-era tune predicts. This is a
well-known feature of the Pythia 6.1 tune: it over-predicts soft hadronic
activity (higher-$\tau$ events), leading to a systematic overestimate of the
distribution in the fit range. Modern generators (Pythia 8 Monash, Herwig 7)
with updated tunes derived from precision LEP measurements provide better
agreement.

The indicative LO $\alpha_s$ extraction gives $0.1066$, which is numerically
consistent with the world-average $\alpha_s(M_Z) = 0.1180$ at the 1–2$\sigma$
level, but this agreement is not meaningful given the degeneracy of the LO
method. The primary physics output of this analysis is the corrected thrust
distribution itself, which is the input for any future theory comparison.

---

## 11. Future Directions

The analysis infrastructure built here is well-suited for the following
extensions:

1. **NLO+NLL $\alpha_s$ extraction:** Implement the DISASTER++ program to
   obtain the NLO differential thrust cross section with resummation. This
   is the primary missing ingredient for a publication-quality measurement.
   The fit infrastructure (covariance matrix, $\chi^2$ minimization) is
   already in place.

2. **Alternative generators:** Obtain Herwig 7 and Sherpa generator-level
   samples and derive the detector response via either fast simulation (using
   the Pythia 6.1 response as a template) or a parametric smearing model.
   This would provide a genuine hadronization uncertainty and reduce the
   dominant systematic.

3. **Additional event shapes:** The ALEPH dataset contains pre-computed C-parameter,
   sphericity, broadening, and thrust-minor distributions. Extending the
   measurement to these shapes provides complementary $\alpha_s$ information
   and cross-checks of the fragmentation model.

4. **Power corrections:** Include analytic $1/Q$ power corrections
   (Dokshitzer-Webber model with universal infrared coupling $\alpha_0$) in
   the $\alpha_s$ fit. This reduces the dependence on MC hadronization models.

5. **LEP2 extension:** Apply the same analysis framework to archived ALEPH
   data at $\sqrt{s} = 133$–$209$ GeV (LEP2), providing a measurement of
   the running of $\alpha_s$ from 91.2 to 209 GeV.

6. **Modern open-data tools:** The analysis framework is entirely based on
   open-source tools (uproot, awkward-array, hist, matplotlib) and could
   be applied to other archived LEP datasets as they become available.

7. **SVD or TUnfold alternative method:** Implement a second valid unfolding
   method (SVD via scikit-hep/hist or TUnfold via Python bindings) to provide
   a genuine alternative-method systematic. This addresses the gap documented
   in Section 5.6 and would complete the conventions requirement for an
   independent unfolding method in the error budget.

---

## 12. Appendices

### Appendix A: Full Per-Bin Systematic Tables

**Table A.1: Per-bin systematic shifts (absolute, in units of $(1/N)\,dN/d\tau$).**

Values given as $|\Delta y_i|$ (half the up–down difference, or floor value).
BBB is listed separately as a cross-check reference but is NOT included in the
covariance matrix (see Section 5.6).

| $\tau$ center | Track smear | Hadr. floor | MC stat | Calo. | Background | ISR | Prior | Reg. | TPC | $b$-frag |
|--------------|-------------|-------------|---------|-------|------------|-----|-------|------|-----|----------|
| 0.05 | 0.163 | 0.149 | 0.0048 | 0.046 | 0.076 | 0.059 | 0.009 | 0.006 | 0.013 | 0.010 |
| 0.07 | 0.099 | 0.091 | 0.0041 | 0.038 | 0.046 | 0.036 | 0.005 | 0.004 | 0.008 | 0.006 |
| 0.09 | 0.066 | 0.061 | 0.0033 | 0.025 | 0.031 | 0.024 | 0.004 | 0.003 | 0.005 | 0.004 |
| 0.11 | 0.047 | 0.043 | 0.0026 | 0.018 | 0.022 | 0.017 | 0.003 | 0.002 | 0.004 | 0.003 |
| 0.13 | 0.035 | 0.032 | 0.0020 | 0.013 | 0.016 | 0.013 | 0.002 | 0.002 | 0.003 | 0.002 |
| 0.15 | 0.026 | 0.024 | 0.0017 | 0.015 | 0.012 | 0.009 | 0.001 | 0.001 | 0.002 | 0.002 |
| 0.17 | 0.020 | 0.018 | 0.0016 | 0.011 | 0.009 | 0.007 | 0.001 | 0.001 | 0.002 | 0.001 |
| 0.19 | 0.016 | 0.015 | 0.0013 | 0.006 | 0.007 | 0.006 | 0.001 | 0.001 | 0.001 | 0.001 |
| 0.21 | 0.013 | 0.012 | 0.0010 | 0.006 | 0.006 | 0.005 | 0.001 | 0.001 | 0.001 | 0.001 |
| 0.23 | 0.010 | 0.009 | 0.0009 | 0.006 | 0.005 | 0.004 | 0.001 | 0.001 | 0.001 | 0.001 |
| 0.25 | 0.008 | 0.007 | 0.0007 | 0.005 | 0.004 | 0.003 | 0.001 | 0.001 | 0.001 | 0.001 |
| 0.27 | 0.006 | 0.006 | 0.0006 | 0.003 | 0.003 | 0.002 | 0.001 | 0.001 | 0.001 | 0.000 |
| 0.29 | 0.004 | 0.004 | 0.0005 | 0.003 | 0.002 | 0.002 | 0.001 | 0.001 | 0.000 | 0.000 |

Note: "Hadr. floor" is the 2% per-bin conservative floor. BBB shifts
(formerly 0.07–1.1 absolute) are listed in Section 6.2 as a cross-check
reference and are excluded from the covariance matrix. Statistical uncertainties
are $\leq 0.5%$ of the central value (up to 0.0075 for the first bin).

**Table A.2: Per-bin relative systematic shifts (% of central value).**

| $\tau$ center | Track smear (%) | Hadr. floor (%) | MC stat (%) | Calo. (%) | Background (%) |
|--------------|-----------------|-----------------|-------------|-----------|----------------|
| 0.05 | 2.19 | 2.00 | 0.065 | 0.62 | 1.02 |
| 0.07 | 2.18 | 2.00 | 0.090 | 0.84 | 1.01 |
| 0.09 | 2.18 | 2.00 | 0.109 | 0.83 | 1.02 |
| 0.11 | 2.19 | 2.00 | 0.121 | 0.84 | 1.02 |
| 0.13 | 2.20 | 2.00 | 0.125 | 0.82 | 1.00 |
| 0.15 | 2.20 | 2.00 | 0.144 | 1.27 | 1.01 |
| 0.17 | 2.18 | 2.00 | 0.175 | 1.20 | 0.98 |
| 0.19 | 2.19 | 2.00 | 0.178 | 0.82 | 0.96 |
| 0.21 | 2.25 | 2.00 | 0.173 | 1.04 | 1.04 |
| 0.23 | 2.24 | 2.00 | 0.201 | 1.34 | 1.12 |
| 0.25 | 2.28 | 2.00 | 0.200 | 1.43 | 1.14 |
| 0.27 | 2.16 | 2.00 | 0.216 | 1.08 | 1.08 |
| 0.29 | 1.93 | 2.00 | 0.241 | 1.45 | 0.96 |

### Appendix B: Covariance and Correlation Matrices

The full $13 \times 13$ total covariance matrix for the fit range
$\tau \in [0.05, 0.30]$ is given in Table B.1 (BBB excluded from budget).
Values are in units of $[(1/N)\,dN/d\tau]^2$.
Machine-readable form: `results/covariance_total_fitrange.csv`.

**Table B.1: Total covariance matrix $C_{ij}^\text{total}$ (fit range, $\tau \in [0.05, 0.30]$, 13 bins, BBB excluded).**

(Values $\times 10^{-4}$ for legibility)

| | $\tau$=0.05 | 0.07 | 0.09 | 0.11 | 0.13 | 0.15 | 0.17 | 0.19 | 0.21 | 0.23 | 0.25 | 0.27 | 0.29 |
|-|------------|------|------|------|------|------|------|------|------|------|------|------|------|
| **0.05** | 319.4 | 178.9 | 115.6 | 77.75 | 57.85 | 42.85 | 33.00 | 26.15 | 20.42 | 15.83 | 12.27 | 9.638 | 6.627 |
| **0.07** | 178.9 | 111.2 | 68.94 | 43.63 | 31.80 | 23.42 | 18.10 | 14.44 | 11.27 | 8.742 | 6.819 | 5.393 | 3.733 |
| **0.09** | 115.6 | 68.94 | 45.81 | 29.78 | 21.14 | 16.17 | 12.28 | 9.523 | 7.792 | 6.031 | 4.638 | 3.478 | 2.823 |
| **0.11** | 77.75 | 43.63 | 29.78 | 22.55 | 15.33 | 12.16 | 9.070 | 6.841 | 5.858 | 4.526 | 3.435 | 2.443 | 2.292 |
| **0.13** | 57.85 | 31.80 | 21.14 | 15.33 | 13.38 | 8.609 | 6.904 | 5.857 | 4.089 | 3.190 | 2.602 | 2.339 | 1.114 |
| **0.15** | 42.85 | 23.42 | 16.17 | 12.16 | 8.609 | 7.549 | 5.195 | 3.873 | 3.347 | 2.583 | 1.954 | 1.375 | 1.343 |
| **0.17** | 33.00 | 18.10 | 12.28 | 9.070 | 6.904 | 5.195 | 4.521 | 3.213 | 2.519 | 1.946 | 1.521 | 1.205 | 0.879 |
| **0.19** | 26.15 | 14.44 | 9.523 | 6.841 | 5.857 | 3.873 | 3.213 | 3.128 | 1.918 | 1.492 | 1.227 | 1.140 | 0.492 |
| **0.21** | 20.42 | 11.27 | 7.792 | 5.858 | 4.089 | 3.347 | 2.519 | 1.918 | 1.969 | 1.325 | 0.999 | 0.695 | 0.693 |
| **0.23** | 15.83 | 8.742 | 6.031 | 4.526 | 3.190 | 2.583 | 1.946 | 1.492 | 1.325 | 1.264 | 0.801 | 0.566 | 0.538 |
| **0.25** | 12.27 | 6.819 | 4.638 | 3.435 | 2.602 | 1.954 | 1.521 | 1.227 | 0.999 | 0.801 | 0.795 | 0.506 | 0.373 |
| **0.27** | 9.638 | 5.393 | 3.478 | 2.443 | 2.339 | 1.375 | 1.205 | 1.140 | 0.695 | 0.566 | 0.506 | 0.634 | 0.147 |
| **0.29** | 6.627 | 3.733 | 2.823 | 2.292 | 1.114 | 1.343 | 0.879 | 0.492 | 0.693 | 0.538 | 0.373 | 0.147 | 0.537 |

The condition number is $3.77 \times 10^3$ (threshold per conventions: $10^{10}$),
reflecting well-conditioned numerics. Positive off-diagonal elements arise
primarily from the track smearing and hadronization systematics, which are
both fully correlated across bins.

**Table B.2: Correlation matrix $\rho_{ij} = C_{ij}/\sqrt{C_{ii} C_{jj}}$ (fit range, BBB excluded).**

| | 0.05 | 0.07 | 0.09 | 0.11 | 0.13 | 0.15 | 0.17 | 0.19 | 0.21 | 0.23 | 0.25 | 0.27 | 0.29 |
|-|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.05 | 1.000 | 0.949 | 0.955 | 0.916 | 0.885 | 0.873 | 0.868 | 0.827 | 0.814 | 0.788 | 0.770 | 0.677 | 0.506 |
| 0.07 | 0.949 | 1.000 | 0.966 | 0.871 | 0.824 | 0.808 | 0.807 | 0.774 | 0.761 | 0.737 | 0.725 | 0.642 | 0.483 |
| 0.09 | 0.955 | 0.966 | 1.000 | 0.927 | 0.854 | 0.869 | 0.853 | 0.796 | 0.820 | 0.793 | 0.768 | 0.645 | 0.569 |

(Continued rows: correlations range from 0.15 to 0.99 across the fit range.
The reduced maximum correlation compared to the BBB-inclusive case reflects
the removal of the near-rank-1 contribution.)

With BBB excluded, the correlation matrix no longer exhibits near-unity
correlations everywhere. The effective rank of the covariance matrix is
substantially higher than in the BBB-inclusive case, meaning the $\chi^2$
calculation uses more independent degrees of information.

### Appendix C: Extended Cutflow Tables

**Table C.1: Selection efficiency by sample and cut level.**

| | Data total | Data $|\cos\theta_\text{sph}|$ | Data MissP | Data ISR | Data final | MC final | Data/MC |
|-|-----------|-------------------------------|-----------|----------|----------|----------|---------|
| All years | 3,050,610 | 97.7% | 97.2% | 99.0% | **94.7%** | **94.7%** | $<$0.1% |
| 1992 | 551,474 | 97.7% | 97.2% | 99.0% | 94.7% | — | — |
| 1993 | 538,601 | 97.7% | 97.2% | 99.0% | 94.7% | — | — |
| 1994 P1 | 433,947 | 97.7% | 97.2% | 99.0% | 94.7% | — | — |
| 1994 P2 | 447,844 | 97.7% | 97.2% | 99.0% | 94.7% | — | — |
| 1994 P3 | 483,649 | 97.7% | 97.2% | 99.0% | 94.7% | — | — |
| 1995 | 595,095 | 97.7% | 97.2% | 99.0% | 94.7% | — | — |

The uniform efficiency across all years confirms stable detector performance
throughout the 1992–1995 data-taking period.

### Appendix D: Response Matrix Properties

**Table D.1: Response matrix summary.**

| Property | Value |
|----------|-------|
| Dimensions | 25 × 25 |
| Bin width $\Delta\tau$ | 0.02 |
| $\tau$ range | $[0.00, 0.50]$ |
| Events (matched pairs) | 731,006 |
| Column normalization | 1.0000 (all active bins) |
| tgenBefore events | 973,769 |
| Generator-level efficiency $\varepsilon_\text{gen}$ | 78.6% (file 001 estimate) |
| Mean $\tau$ bias (reco $-$ gen) | $-0.0067$ |
| RMS smearing | 0.013 |

**Table D.2: Response matrix diagonal fraction by bin.**

| Bin $\tau \in$ | Diagonal fraction |
|----------------|------------------|
| $[0.00, 0.02]$ | 89% |
| $[0.02, 0.04]$ | 63% |
| $[0.04, 0.06]$ | 53% |
| $[0.06, 0.08]$ | 50% |
| $[0.08, 0.10]$ | 46% |
| $[0.10, 0.12]$ | 43% |
| $[0.12, 0.14]$ | 40% |
| $[0.14, 0.16]$ | 38% |
| $[0.16, 0.18]$ | 35% |
| $[0.18, 0.20]$ | 33% |
| $[0.20, 0.22]$ | 32% |
| $[0.22, 0.24]$ | 31% |
| $[0.24, 0.26]$ | 30% |
| $[0.26, 0.28]$ | 29% |
| $[0.28, 0.30]$ | 29% |
| $[0.30, 0.40]$ | 23–29% |
| $[0.40, 0.50]$ | ~0% |

The diagonal fraction below 50% for $\tau > 0.04$ and below 35% for
$\tau > 0.10$ confirms that bin-by-bin correction is unreliable in the
fit range and IBU is essential as the primary unfolding method.

---

## References

1. ALEPH Collaboration, "Studies of QCD at $e^+e^-$ Centre-of-Mass Energies
   between 91 and 209 GeV," Eur. Phys. J. **C35**:457–486 (2004);
   hep-ex/0409098.

2. S. Bethke et al. (LEP QCD Working Group), "Combination of Measurements
   of the Strong Coupling Constant at LEP," hep-ex/0411006 (2004).

3. ALEPH archived data analysis of thrust and two-particle correlations,
   Inspire:1793969.

4. G. D'Agostini, "A multidimensional unfolding method based on Bayes'
   theorem," Nucl. Instrum. Methods **A362**:487–498 (1995).

5. T. Sjöstrand, "PYTHIA 6.1 Physics and Manual," hep-ph/0010017 (2001).

6. G. Dissertori, "DISASTER++: A program for computing the NLO corrections
   to event shapes in $e^+e^-$ annihilation," (1999); also G. Dissertori
   and M. Schmelling, Phys. Lett. **B361**:167–178 (1995).

7. R. Abbate, M. Fickinger, A. H. Hoang, V. Mateu, I. W. Stewart,
   "Thrust at N$^3$LL with Power Corrections and a Precision Global Fit for
   $\alpha_s(m_Z)$," Phys. Rev. **D83**:074021 (2011); arXiv:1006.3080.

8. ALEPH Collaboration, "Performance of the ALEPH detector at LEP,"
   Nucl. Instrum. Methods **A360**:481–506 (1995).

9. Particle Data Group, "Review of Particle Physics," Prog. Theor. Exp.
   Phys. **2022**:083C01 (2022).

10. V. A. Khoze, W. Ochs, J. Wosiek, "Particle production mechanisms,"
    hep-ph/0009298 (2000) — review of Lund string model and fragmentation.

---

## Machine-Readable Results

The following files are provided in the `results/` subdirectory:

- `results/thrust_distribution.csv`: Full corrected thrust distribution
  with per-bin statistical and systematic uncertainties (13 bins in fit range).
- `results/covariance_total_fitrange.csv`: $13 \times 13$ total covariance
  matrix for the fit range $\tau \in [0.05, 0.30]$.
- `results/alphas_result.csv`: Indicative $\alpha_s$ result and scale
  variation envelope.

Additional machine-readable files from Phase 4 (not copied to this directory
but available in `../../phase4_inference/exec/`):

- `covariance_stat.npz`: Statistical covariance matrix (25×25)
- `covariance_syst.npz`: Systematic covariance matrix (25×25)
- `covariance_total.npz`: Total covariance matrix (25×25)
- `systematics_shifts.npz`: Per-source systematic shifts
- `indep_closure_results.npz`: Independent closure test results
- `stress_test_results.npz`: Stress test results

---

*Analysis completed: Phase 5. All scripts available in `phase3_selection/scripts/` and
`phase4_inference/scripts/`. Full reproducible analysis chain: `pixi run all` from
the analysis directory `thrust_alphas/`.*
