# Experiment Log

## Phase 1: Strategy

### 2026-03-15 — Strategy Development

**Corpus searches performed:**
- Thrust distribution and alpha_s extraction at LEP (ALEPH + DELPHI)
- Hadronic event selection criteria for ALEPH
- Systematic uncertainties for event shape measurements
- Archived ALEPH data samples and MC configurations
- Detector performance (tracking, calorimetry)
- Alpha_s extraction methods (NLO, resummed predictions)

**Key reference analyses identified:**
1. LEP QCD working group combination (hep-ex/0411006): Combined alpha_s from event shapes using all four LEP experiments. Result at Z pole: alpha_s(M_Z) = 0.1202 +/- 0.0003(stat) +/- 0.0007(exp) +/- 0.0012(hadr) +/- 0.0048(theo). Hadronization assessed using Pythia, Herwig, Ariadne.
2. DELPHI oriented event shapes (inspire:1661561): 1.4M events from 1994, 18 event shape distributions vs. thrust axis polar angle. Detailed systematic program including JETSET/Ariadne/Herwig comparison, Q0 variation, scale optimization.
3. Archived ALEPH QGP search (inspire:1793969): Uses the same archived dataset we have. Validated thrust distribution against published ALEPH results. Track selection: >= 4 TPC hits, |d0| < 2 cm, |z0| < 10 cm, |cos(theta)| < 0.95. Event selection: >= 5 charged tracks, E_ch > 15 GeV, >= 13 total tracks, |cos(theta_sph)| < 0.82.

**Material decisions:**
- Observable: Thrust tau = 1 - T, normalized distribution (1/N) dN/dtau
- Particle-level definition: All stable particles (c*tau > 10 mm) excluding neutrinos, full 4pi, ISR-exclusive
- Primary unfolding method: Iterative Bayesian unfolding (IBU)
- Alternative method: Bin-by-bin correction factors (cross-check)
- Response matrix MC: Pythia 6.1 reconstructed (40 files available)
- Hadronization systematic: Pythia 6.1 vs. Herwig 7 via particle-level reweighting (no alternative full-sim available)
- Alpha_s extraction: chi2 fit of O(alpha_s^2) + NLLA predictions to corrected distribution, fit range ~0.05 < tau < 0.30

**Data inventory:**
- Data: 6 files spanning 1992-1995, located at /n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPH/
- MC: 40 Pythia 6.1 reconstructed files, located at /n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC/
- Files are post-baseline-selection ("aftercut"). Exact applied cuts to be verified in Phase 2.

**Conventions check:**
- Read conventions/unfolding.md in full
- All required systematic sources enumerated in strategy with "Will implement" or justification
- No sources omitted silently
- Measurement is normalized shape -> normalization-only systematics excluded (documented)

**Open questions for Phase 2:**
- What cuts have already been applied in the "aftercut" files?
- What tree structure and branch names are in the ROOT files?
- How many events per data year and in MC?
- Is generator-level truth information stored in the MC files (needed for response matrix)?
- What is the MC/data agreement quality for input kinematic variables?

## Phase 2: Exploration

### 2026-03-15 — Data Format Discovery (scripts 01-04)

**File structure (script 01):**
- Main tree: `t` (detector-level, 151 branches). All data/MC files use same schema.
- Additional trees: `akR4ESchemeJetTree`, `akR8ESchemeJetTree`, `ktN2ESchemeJetTree`, `ktN3ESchemeJetTree` (pre-clustered jets), `BoostedWTAR8Evt`, `BoostedWTAktN2Evt` — jet/boosted analysis artifacts, not used for thrust.
- MC-only additional trees: `tgen` (generator-level matched to reco selection), `tgenBefore` (all generated events before selection), plus corresponding gen-jet trees.
- Thrust is **pre-computed** and stored as `Thrust`, `Thrust_charged`, `Thrust_neutral`, `ThrustCorr`, `ThrustCorrInverse`, `ThrustWithMissP`. All event shapes (Sphericity, Aplanarity, C/D parameters) pre-stored.
- Selection flags stored per event: `passesNTupleAfterCut`, `passesTotalChgEnergyMin`, `passesNTrkMin`, `passesSTheta`, `passesMissP`, `passesISR`, `passesAll`.
- Tracks stored as jagged arrays: `px`, `py`, `pz`, `pt`, `pmag`, `eta`, `theta`, `phi`, `charge`, `pwflag`, `pid`, `d0`, `z0`, `ntpc`, `highPurity`.

**Event counts:**
- LEP1Data1992: 551,474
- LEP1Data1993: 538,601
- LEP1Data1994P1: 433,947
- LEP1Data1994P2: 447,844
- LEP1Data1994P3: 483,649
- LEP1Data1995: 595,095
- TOTAL DATA: 3,050,610
- MC files 001-040: ~19,200 events each, TOTAL MC: 771,597

**"aftercut" discovery (script 02):**
- `passesNTupleAfterCut = 100%` for all events in files: files are pre-filtered to events passing the ALEPH NTuple aftercut (charged energy + N-track minimum).
- `passesTotalChgEnergyMin = 100%`, `passesNTrkMin = 100%`: these two cuts are pre-applied. The event-level charged energy (>15 GeV) and minimum tracks (≥5 good charged) have been applied upstream.
- Remaining cuts stored but NOT pre-applied: `passesSTheta` (97.7%), `passesMissP` (97.2%), `passesISR` (99.0%), `passesAll` (94.7%).
- **Implication for systematics:** The charged energy and NTrkMin cuts cannot be loosened below their thresholds; only tightening is possible. This was anticipated in the strategy; documented accordingly.

**pwflag encoding:**
- `pwflag=0`: good charged tracks (all have charge≠0), the primary charged-track category
- `pwflag=1,2,3`: charged tracks failing quality cuts (still charged, smaller populations)
- `pwflag=4`: neutral calorimeter clusters (photons, neutral hadrons) — no charged component
- `pwflag=5`: additional neutral objects
- `pwflag=-11` (gen tree only): likely ISR photons or neutrinos excluded from the thrust calculation

**Track/event kinematics (script 02):**
- Mean nParticle (all, reco): 29.0 (data), 29.7 (MC) — good agreement
- Mean nChargedHadrons: 18.8 (data and MC) — excellent agreement
- Track |p|: mean 2.76 GeV (data), 2.82 GeV (MC)
- Mean Energy (stored): 91.14 GeV data, 91.20 GeV MC — consistent with Z pole

**Selection cutflow (script 03, 100k events):**
Data 1994P1:
- NTupleAfterCut: 100% (pre-applied)
- TotalChgEnergyMin: 100% (pre-applied)
- NTrkMin: 100% (pre-applied)
- STheta: 97.7%
- MissP: 97.2%
- ISR: 99.0%
- ALL: 94.7%

MC:
- All same cuts: 94.6% pass passesAll — DATA/MC agreement on selection efficiency is excellent (<0.1% difference).

**Year-by-year consistency:**
- All 6 data periods show consistent tau distributions. Ratio to combined is flat to within ~2% across tau range 0.02-0.35. Low-statistics bins at large tau show more scatter. No evidence for year-to-year detector instabilities.

**MC truth / response matrix (script 04):**
- tgen has 19,158 entries, matched 1:1 with reco t tree (same events)
- tgenBefore has 24,360 entries (all generated events, before selection)
- Selection efficiency: 19,158/24,360 = 78.6% at generator level
- Detector smearing on tau: bias = -0.0067 (reco tau is lower than gen tau — detector sees slightly narrower jets), RMS = 0.013
- Tau resolution increases with tau: 0.008 at tau<0.05, 0.025 at tau~0.25
- Response matrix diagonal fractions: 89% at tau=[0,0.02] (2-jet region, dominated by single bin); 46-63% at tau=[0.02-0.10]; 25-40% at tau>0.10 — significant migration in intermediate-to-large tau region, confirming IBU is required (bin-by-bin is insufficient).
- Gen nParticle: mean 45.7 (vs. 29 reco) — large difference explains smearing and the need for acceptance corrections.
- bFlag in data: -1 (not b-tagged) vs. 4 (b-tagged). In MC: -999 (not set — MC b-flavor info is in bFlag but encoded differently; need to use pid or separate b-quark flag for b-fraction studies).

**Figures produced:**
- `thrust_tau_data_mc.{pdf,png}`: data (all years) vs. MC (1 file) tau distribution with ratio — good overall agreement, some data/MC differences in intermediate tau region (expected at 1-file MC statistics).
- `ncharged_data_mc.{pdf,png}`: charged multiplicity data/MC — good agreement.
- `track_momentum_data_mc.{pdf,png}`: track |p| spectrum data/MC.
- `sphericity_data_mc.{pdf,png}`: sphericity data/MC.
- `tau_year_consistency.{pdf,png}`: year-by-year consistency.
- `tau_gen_vs_reco_scatter.{pdf,png}`: 2D scatter tau_gen vs tau_reco.
- `response_matrix_prototype.{pdf,png}`: response matrix (normalized by gen row).
- `tau_reco_vs_gen.{pdf,png}`: reco/gen/tgenBefore tau comparison.

**Material decisions made in Phase 2:**
- Will use `passesAll` as the primary event selection (applies STheta, MissP, ISR cuts on top of pre-applied cuts).
- Charged-track selection: `pwflag=0` (primary good charged tracks). Neutral objects: `pwflag=4`.
- Response matrix will use `tgen` (matched to reco) for the numerator and `t` for the denominator.
- Will compute thrust from stored `Thrust` branch (not recompute from tracks) — it's pre-computed correctly.
- Generator-level target for unfolding: `tgenBefore["Thrust"]` after applying particle-level selection.
- bFlag in MC needs investigation — stored as -999 (no b-tagging applied). For b-flavor systematic, will use the `process` branch in tgen or pid of primary quarks.
- Binning: 25 bins in tau [0,0.5] appropriate given response matrix diagonal fractions of 25-90%. Will refine in Phase 4a.
- The low diagonal fractions (25-40%) at large tau confirm that bin-by-bin correction would be unreliable there; IBU is the correct choice.
