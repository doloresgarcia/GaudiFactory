# Primary Lund Jet Plane Density — ALEPH at √s = 91.2 GeV

Type: measurement

Start a new claude instance at the reslop repo root and paste one of
the prompts below.

---

## Short prompt

````text
Scaffold and run a measurement analysis of the primary Lund jet plane
density in hadronic Z decays using archived ALEPH data at √s = 91.2 GeV.

Setup: scaffold analyses/lund_plane as a measurement, set
data_dir=/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ in
.analysis_config, install the pixi environment, then begin orchestrating.

Observable: The 2D density of primary Cambridge/Aachen declusterings
in each thrust hemisphere, mapped to coordinates
(ln 1/Δθ, ln k_t/GeV), where Δθ is the emission angle and
k_t = E_soft sin Δθ. Use charged particles only (pwflag == 0,
highPurity == 1). One jet = one hemisphere.

Deliverables:
1. 2D density ρ(ln 1/Δθ, ln k_t) corrected to charged-particle level,
   ~10–15 × 10–15 bins at least - as fine as it makes sense
2. 1D projections (k_t spectrum, angular spectrum) with covariance
3. Number of primary declusterings vs. minimum k_t threshold
4. Comparison to PYTHIA 6 MC
5. Machine-readable results (CSV/NPY)

Data:
- Data: /n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPH/
  (LEP1Data{1992..1995}_recons_aftercut-MERGED.root, 6 files)
- MC:   /n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC/
  (LEP1MC1994_recons_aftercut-{001..041}.root, 41 files)

This is the first Lund plane measurement in e⁺e⁻ collisions.
````
