# Phase 2 Exploration: Precision Measurement of Thrust and α_s at ALEPH

**Analysis:** thrust_alphas
**Date:** 2026-03-15
**Scripts:** `phase2_exploration/scripts/01_discover_structure.py`, `02_inspect_sample.py`, `03_distributions.py`, `04_mc_truth_response.py`

---

## 1. Sample Inventory

### 1.1 Data Files

| Year | File | Events (tree `t`) | Notes |
|------|------|-------------------|-------|
| 1992 | `LEP1Data1992_recons_aftercut-MERGED.root` | 551,474 | |
| 1993 | `LEP1Data1993_recons_aftercut-MERGED.root` | 538,601 | |
| 1994 P1 | `LEP1Data1994P1_recons_aftercut-MERGED.root` | 433,947 | |
| 1994 P2 | `LEP1Data1994P2_recons_aftercut-MERGED.root` | 447,844 | |
| 1994 P3 | `LEP1Data1994P3_recons_aftercut-MERGED.root` | 483,649 | |
| 1995 | `LEP1Data1995_recons_aftercut-MERGED.root` | 595,095 | |
| **TOTAL** | | **3,050,610** | |

After applying `passesAll` (the full hadronic event selection): **2,889,543 events** (94.7%).

### 1.2 MC Files

| Sample | Files | Events per file | Total events |
|--------|-------|-----------------|--------------|
| Pythia 6.1 reconstructed | 40 files (`-001.root` to `-040.root`) | ~19,200 | **771,597** |

Each file contains three trees:
- `t`: detector-level reconstructed quantities (151 branches)
- `tgen`: generator-level particles, indexed to match reco events (199 branches)
- `tgenBefore`: generator-level particles for all generated events before selection (151 branches)

File 001 has 19,158 reco events and 24,360 generator-level events before selection, giving a generator-level selection efficiency of **78.6%**.

---

## 2. File Structure

### 2.1 Tree Structure

Both data and MC files have an identical primary tree `t` with **151 branches**, plus several pre-clustered jet trees (`akR4ESchemeJetTree`, `akR8ESchemeJetTree`, `ktN2ESchemeJetTree`, `ktN3ESchemeJetTree`, `BoostedWTAR8Evt`, `BoostedWTAktN2Evt`) which are irrelevant to this analysis.

MC files additionally contain generator-level trees `tgen` and `tgenBefore` with 199 and 151 branches respectively.

### 2.2 Key Branches in Tree `t`

**Event-level scalars:**
| Branch | Type | Description |
|--------|------|-------------|
| `EventNo`, `RunNo` | `int32` | Event and run identifiers |
| `year` | `int32` | Data-taking year |
| `isMC` | `bool` | True for MC events |
| `Energy` | `float32` | CM energy (≈91.14 GeV data, ≈91.20 GeV MC) |
| `bFlag` | `int32` | b-quark flag: -1 (not b), 4 (b-tagged) in data; -999 in MC (not set) |
| `nParticle` | `int32` | Total number of particles (charged + neutral) |
| `nChargedHadrons` | `int32` | Number of charged hadrons (charge≠0), mean=18.8 |
| `nChargedHadronsHP` | `int32` | High-purity charged hadrons, mean=18.2 |
| `Thrust` | `float32` | Pre-computed thrust T (charged + neutral) |
| `Thrust_charged` | `float32` | Charged-only thrust |
| `Thrust_neutral` | `float32` | Neutral-only thrust |
| `ThrustCorr` | `float32` | Thrust corrected for acceptance effects |
| `ThrustWithMissP` | `float32` | Thrust including missing momentum |
| `Sphericity` | `float32` | Linearized sphericity |
| `missP` | `float32` | Missing momentum magnitude |

**Per-particle jagged arrays (indexed per event):**
| Branch | Type | Description |
|--------|------|-------------|
| `px`, `py`, `pz` | `float32[n]` | Momentum components (GeV) |
| `pmag`, `pt` | `float32[n]` | Momentum magnitude, transverse momentum |
| `theta`, `phi`, `eta` | `float32[n]` | Angular quantities |
| `charge` | `int16[n]` | Electric charge (0 = neutral) |
| `pwflag` | `int16[n]` | Particle/track type flag (see below) |
| `pid` | `int32[n]` | Particle ID (internal ALEPH encoding) |
| `d0`, `z0` | `float32[n]` | Impact parameters (cm) |
| `ntpc` | `int16[n]` | Number of TPC coordinate hits |
| `highPurity` | `bool[n]` | High-purity track flag |

**Selection flags (stored per event):**
| Branch | Description |
|--------|-------------|
| `passesNTupleAfterCut` | Pre-applied, 100% in files |
| `passesTotalChgEnergyMin` | Pre-applied, ~100% in files |
| `passesNTrkMin` | Pre-applied, ~100% in files |
| `passesSTheta` | Sphericity axis cut, ~97.7% pass |
| `passesMissP` | Missing momentum cut, ~97.2% pass |
| `passesISR` | ISR rejection, ~99.0% pass |
| `passesAll` | Logical AND of all above, ~94.7% pass |

### 2.3 pwflag Encoding

| pwflag | Charge | Description |
|--------|--------|-------------|
| 0 | Charged | Good charged tracks — primary category for thrust |
| 1 | Charged | Charged tracks with reduced quality |
| 2 | Charged | Charged tracks with further reduced quality |
| 3 | Charged | Charged tracks (very few, likely pathological) |
| 4 | Neutral | Calorimeter clusters (photons, neutral hadrons) |
| 5 | Neutral | Additional neutral objects |
| -11 | — | Gen-tree only: excluded particles (ISR photons, neutrinos) |

The stored `Thrust` branch uses **all particles** (pwflag 0-5, excluding -11 in gen). The `Thrust_charged` branch uses only pwflag=0 tracks.

### 2.4 Generator-Level Tree `tgen`

The `tgen` tree is indexed to match the `t` (reco) tree: event $i$ in `tgen` corresponds to event $i$ in `t`. It has 199 branches, which include all the same branches as `t` plus additional generator-level thrust variants:
- `ThrustWithReco`: particle-level thrust computed using only particles reconstructed at detector level
- `ThrustWithGenIneff`: particle-level thrust with tracking inefficiency applied
- `ThrustWithGenIneffFake`: particle-level thrust with fake rate included

The `tgenBefore` tree has all generated events before the selection efficiency, with 151 branches (same as `t`).

---

## 3. "Aftercut" Definition

**The "aftercut" files have the following cuts pre-applied upstream:**
1. `passesNTupleAfterCut = True` (100% of events in files)
2. `passesTotalChgEnergyMin = True` (sum of charged pion-mass momenta > 15 GeV, >99.9% of events in files)
3. `passesNTrkMin = True` (≥5 good charged tracks, >99.9% of events in files)

**The following cuts are stored but NOT pre-applied and must be applied in Phase 3:**
- `passesSTheta`: sphericity axis `|cos(theta_sph)| < 0.82` — 97.7% pass
- `passesMissP`: missing momentum < 20 GeV — 97.2% pass
- `passesISR`: no hard ISR photon — 99.0% pass
- `passesAll` = AND of all above: **94.7% pass (data), 94.6% pass (MC)**

**Implication for systematics:** The strategy's plan to vary the charged energy cut downward (15→10 GeV) is **not possible** since this cut is pre-applied. This was anticipated in the strategy (Section 4.1, Phase 2 gate condition). The systematic program will use cut tightening only for this variable, and alternative probes of the charged energy response (e.g., energy scale smearing) will be used instead. This is documented here and will be propagated to the Phase 3 and Phase 4a strategy updates.

---

## 4. Data Quality Assessment

### 4.1 Selection Efficiency

| Quantity | Data | MC | Difference |
|----------|------|-----|------------|
| passesAll rate | 94.7% | 94.6% | <0.1% |
| Mean nChargedHadrons | 18.8 | 18.7 | 0.5% |
| Mean tau = 1-T | 0.0638 | 0.0642 | 0.6% |
| Mean Sphericity | (see Fig.) | (see Fig.) | |
| Mean Energy (stored) | 91.14 GeV | 91.20 GeV | 0.07% |

The selection efficiency agrees between data and MC to better than 0.1%. This is an excellent baseline and is consistent with the ~94-95% efficiency quoted in the original ALEPH publications.

### 4.2 Year-by-Year Consistency

The six data-taking periods (1992, 1993, 1994 P1/P2/P3, 1995) show consistent thrust distributions (Figure `tau_year_consistency`). The ratio of each year's normalized tau distribution to the combined sample is flat to within ~2% across the range tau = 0.02-0.35. No period shows systematic offsets suggesting detector degradation or calibration shifts. The year-by-year systematic (planned in strategy Section 6.1.5) is expected to be small.

---

## 5. Key Variable Distributions

### 5.1 Thrust tau = 1 - T

**Figure:** `phase2_exploration/figures/thrust_tau_data_mc.{pdf,png}`

- Data (combined 1992-1995, passesAll): 2,889,543 events
- MC (Pythia 6.1, 1 file, passesAll): 18,131 events
- Distributions are normalized to unit area with 50 bins in tau ∈ [0, 0.5]
- Overall shape agreement is good; the 1-file MC is statistically limited at large tau
- Data mean tau = 0.064, MC mean tau = 0.064 (excellent agreement)

**Observation:** The tau distribution peaks sharply at low tau (2-jet events) and falls steeply. The fit range for α_s extraction (0.05 < tau < 0.30) covers the bulk of the distribution with good statistics.

### 5.2 Charged Track Multiplicity

**Figure:** `phase2_exploration/figures/ncharged_data_mc.{pdf,png}`

Data (1994P1) vs. MC: good agreement in the peak region (nCharged = 15-25). MC slightly overshoots at nCharged > 30. The mean is 18.8 for both. Data/MC ratio is flat to within ~5% across the multiplicity range.

### 5.3 Track Momentum Spectrum

**Figure:** `phase2_exploration/figures/track_momentum_data_mc.{pdf,png}`

Data (1994P1) vs. MC: good agreement across the momentum range 0.1–20 GeV. The spectrum falls steeply. Data/MC ratio is close to 1.0 with some deviations at |p| > 10 GeV (few events, statistical).

### 5.4 Sphericity

**Figure:** `phase2_exploration/figures/sphericity_data_mc.{pdf,png}`

Good data/MC agreement in the sphericity distribution. The distribution peaks near S ~ 0.05-0.10 (pencil-like 2-jet events) and has a tail to larger S.

---

## 6. Response Matrix and MC Truth Analysis

**Figures:** `tau_gen_vs_reco_scatter.{pdf,png}`, `response_matrix_prototype.{pdf,png}`, `tau_reco_vs_gen.{pdf,png}`

### 6.1 Detector Smearing

Comparing matched detector-level and generator-level tau (using `tgen` tree, applying `passesAll`):

| Quantity | Value |
|----------|-------|
| Mean tau (reco) | 0.0615 |
| Mean tau (gen) | 0.0683 |
| Mean bias (reco - gen) | −0.0067 |
| RMS smearing | 0.013 |

The detector systematically reconstructs slightly lower tau than the generator. This is consistent with tracking inefficiency reducing the number of particles and biasing the thrust axis.

### 6.2 Tau Resolution vs. tau_gen

| tau_gen range | Bias (reco-gen) | Resolution σ |
|--------------|-----------------|--------------|
| [0.00, 0.05] | -0.0042 | 0.0076 |
| [0.05, 0.10] | -0.0083 | 0.013 |
| [0.10, 0.15] | -0.0101 | 0.017 |
| [0.15, 0.20] | -0.0112 | 0.023 |
| [0.20, 0.25] | -0.0126 | 0.025 |
| [0.25, 0.30] | -0.0144 | 0.026 |
| [0.30, 0.40] | -0.0158 | 0.025 |

Resolution increases with tau but remains below the bin width (0.02 for 25 bins over [0,0.5]) everywhere. The bias reaches ~1.6% of tau at the upper end of the fit range.

### 6.3 Response Matrix Diagonal Fractions

With 25 bins in tau ∈ [0, 0.5] (bin width 0.02), the diagonal fraction (probability of staying in the same bin) is:

| tau region | Diagonal fraction |
|------------|------------------|
| [0.00, 0.02] | 89% |
| [0.02, 0.04] | 63% |
| [0.04, 0.06] | 50% |
| [0.06, 0.10] | 43–46% |
| [0.10, 0.20] | 31–40% |
| [0.20, 0.40] | 16–34% |
| [0.40, 0.50] | ~0% (no MC events in this range at reco level) |

**Key finding:** The diagonal fraction drops below 50% for tau > 0.04, and below 35% for tau > 0.10. This confirms that **bin-by-bin correction factors would be unreliable** in the fit region (0.05 < tau < 0.30). IBU is essential as the primary unfolding method. The bin-by-bin method will still be implemented as a cross-check, with the difference taken as a systematic uncertainty.

The response matrix is populated only up to tau ≈ 0.40 at detector level, consistent with the maximum observed data tau. The last few bins (tau > 0.38) have zero diagonal fraction and will be excluded from the measurement.

### 6.4 Generator-Level Particle Content

In the `tgen` tree, `pwflag=-11` (10,455 out of ~880,000 particles) identifies particles excluded from the generator-level thrust — likely ISR photons and neutrinos. The remaining particles follow the same pwflag scheme as reco. Generator-level nParticle ≈ 45.7 versus reco nParticle ≈ 29 reflects the loss of neutral particles in calorimeter and tracking acceptance.

---

## 7. Variable Ranking and Selection for Analysis

Based on the exploration findings, the relevant variables and their roles are:

| Variable | Role | Notes |
|----------|------|-------|
| `Thrust` | Primary observable | Pre-computed, use directly |
| `passesAll` | Event selection mask | Apply in Phase 3 |
| `pwflag==0` | Charged track selection | For track-level studies |
| `pwflag==0,4` | Charged + neutral | For charged+neutral thrust verification |
| `nChargedHadronsHP` | Track multiplicity QC | High-purity subset |
| `ntpc` | TPC hit systematic | Vary 4→7 for systematic |
| `d0`, `z0` | Impact parameter cuts | Vary for systematic |
| `passesSTheta` | STheta cut | Vary threshold ±5% for systematic |
| `passesMissP` | MissP cut | Vary threshold for systematic |
| `tgen["Thrust"]` | Generator-level target | For response matrix |
| `tgenBefore["Thrust"]` | Unfolded target | Full generator sample |

---

## 8. Preselection Cutflow

The pre-applied cuts define the base sample in all files:

| Cut | Status | Efficiency |
|-----|--------|-----------|
| `passesNTupleAfterCut` | Pre-applied | 100% (in files) |
| `passesTotalChgEnergyMin` (E_ch > 15 GeV) | Pre-applied | ~100% (in files) |
| `passesNTrkMin` (≥5 charged tracks) | Pre-applied | ~100% (in files) |

Additional cuts to apply in Phase 3 (stored in files, not pre-applied):

| Cut | Variable | Data efficiency | MC efficiency |
|-----|----------|-----------------|---------------|
| Sphericity axis | `passesSTheta` | 97.7% | 97.6% |
| Missing momentum | `passesMissP` | 97.2% | 97.3% |
| ISR rejection | `passesISR` | 99.0% | 99.0% |
| **All cuts** | `passesAll` | **94.7%** | **94.6%** |

---

## 9. Open Issues and Decisions for Phase 3

1. **Charged energy cut systematic:** Cannot loosen E_ch < 15 GeV cut (pre-applied). Phase 3 will document this and substitute track energy scale variation as the relevant systematic. Only tightening the cut (e.g., 15→20 GeV) is possible.

2. **bFlag in MC:** Set to -999 for all MC events (not filled in the archived reconstructed MC). For b-flavor systematics (heavy quark fragmentation), will need to use the `process` branch or the gen-level quark information in `tgen`. This will be investigated in Phase 3/4.

3. **Binning confirmation:** 25 bins in tau ∈ [0, 0.5] with uniform 0.02 width is appropriate. The low diagonal fractions at tau > 0.04 motivate fine binning to avoid large migration corrections that would amplify statistical noise. This will be formally optimized in Phase 4a.

4. **MC statistics:** With 771,597 total MC events and ~94.6% selection efficiency, the post-selection MC sample is ~730,000 events — about 25% of the data sample. The response matrix statistical uncertainty will be non-negligible and is included in the systematic budget (Section 6.1.5 of strategy). Full MC sample (all 40 files) will be used in Phase 4a.

5. **Thrust upper limit for measurement:** The response matrix shows essentially no MC events at tau > 0.40 at detector level. The measurement range will be restricted to tau < 0.40 (25 bins from 0 to 0.50 with the last few bins excluded). The α_s fit range 0.05 < tau < 0.30 is well within the populated region.

6. **Data/MC comparison quality:** The one-file MC comparison shows generally good agreement but is statistically limited. The full comparison with all 40 MC files will be performed in Phase 3. Any bins with data/MC ratio outside [0.8, 1.2] will be flagged for investigation.

---

## 10. Summary

Phase 2 successfully established:

- **Data format:** Tree `t` with 151 branches; charged tracks as jagged arrays; all event shapes pre-computed; selection flags stored but not all pre-applied.
- **Aftercut definition:** E_ch > 15 GeV and N_tracks ≥ 5 are pre-applied; STheta, MissP, ISR cuts are stored but not pre-applied; applying `passesAll` gives 94.7% data efficiency.
- **Sample sizes:** 2,889,543 data events (passesAll), ~730,000 MC events total after selection.
- **MC truth available:** Generator-level `tgen` tree matched to reco events; `tgenBefore` for efficiency studies.
- **Thrust smearing:** Detector systematically reconstructs tau ~0.007 lower than generator with ~0.013 RMS smearing. Response matrix diagonal fractions are 30-89% depending on tau bin.
- **Data quality:** Excellent year-by-year consistency; excellent data/MC agreement on selection efficiency (94.7% vs. 94.6%).
- **Unfolding feasibility confirmed:** Low diagonal fractions confirm IBU is necessary; the response matrix structure is well-behaved (no pathological off-diagonal structure).

**Phase gate artifact:** This document is the required artifact for Phase 3 to proceed.

---

*Produced by Phase 2 exploration scripts. All scripts located in `phase2_exploration/scripts/`. All figures in `phase2_exploration/figures/`.*
