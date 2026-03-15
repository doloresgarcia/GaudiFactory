"""
Phase 4 Fix Script: rebuild_covariance_no_bbb.py

Remove the bin-by-bin (BBB) alternative-method shift from the systematic
budget and rebuild the covariance matrix without it.

Rationale: BBB correction is known to fail when the response matrix
diagonal fraction is below ~70%. For this analysis the diagonal fraction
is 25-50% in the fit range, making BBB an incorrect method. The IBU/BBB
difference (21%) is therefore NOT a meaningful systematic uncertainty --
it measures the difference between a correct and an incorrect method, not
genuine unfolding-method uncertainty. BBB is demoted to a cross-check
(Section 6.2).

The conventions require at least one independent valid unfolding method
as a systematic. This gap is explicitly acknowledged in Section 5.6;
see the analysis note for the full justification and the deferred plan
to implement SVD unfolding.

Steps:
  1. Load systematics_shifts.npz
  2. Remove shift_alt_method from the systematic budget
  3. Rebuild covariance matrices WITHOUT the BBB contribution
  4. Recompute total uncertainties per bin
  5. Overwrite covariance NPZ files in phase4_inference/exec/
  6. Update thrust_distribution.csv and .npz in both
     phase4_inference/exec/results/ and phase5_documentation/exec/results/
  7. Report new dominant systematic and total uncertainty

Outputs:
  - phase4_inference/exec/covariance_stat.npz  (unchanged, re-saved for consistency)
  - phase4_inference/exec/covariance_syst.npz  (BBB removed)
  - phase4_inference/exec/covariance_total.npz (BBB removed)
  - phase4_inference/exec/results/thrust_distribution.{npz,csv}
  - phase4_inference/exec/results/covariance_total_fitrange.csv
  - phase5_documentation/exec/results/thrust_distribution.{csv} (if exists)
  - phase5_documentation/exec/results/covariance_total_fitrange.csv (if exists)
"""

import logging
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mplhep as mh
from scipy import stats
from rich.logging import RichHandler
from rich.console import Console
from rich.table import Table

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger("rebuild_covariance_no_bbb")
console = Console()

# ---------------------------------------------------------------------------
# Paths and constants
# ---------------------------------------------------------------------------
P3_EXEC  = Path("phase3_selection/exec")
P4_EXEC  = Path("phase4_inference/exec")
FIG_DIR  = Path("phase4_inference/figures")
RESULTS  = Path("phase4_inference/exec/results")
P5_RESULTS = Path("phase5_documentation/exec/results")

P4_EXEC.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)
RESULTS.mkdir(parents=True, exist_ok=True)
P5_RESULTS.mkdir(parents=True, exist_ok=True)

N_BINS      = 25
TAU_MIN     = 0.0
TAU_MAX     = 0.5
TAU_EDGES   = np.linspace(TAU_MIN, TAU_MAX, N_BINS + 1)
TAU_CENTERS = 0.5 * (TAU_EDGES[:-1] + TAU_EDGES[1:])
BIN_WIDTH   = TAU_EDGES[1] - TAU_EDGES[0]
FIT_MASK    = (TAU_CENTERS >= 0.05) & (TAU_CENTERS <= 0.30)
N_FIT_BINS  = int(FIT_MASK.sum())


def normalize(h: np.ndarray) -> np.ndarray:
    s = h.sum()
    return h / (s * BIN_WIDTH) if s > 0 else h.copy()


def main():
    log.info("=" * 70)
    log.info("Rebuild Covariance Without BBB Alternative-Method Systematic")
    log.info("=" * 70)
    log.info("")
    log.info("Rationale: BBB correction is invalid for diagonal fractions 25-50%.")
    log.info("The IBU/BBB difference is NOT a meaningful systematic; it is a")
    log.info("cross-check showing that BBB fails, as expected. See Section 5.6")
    log.info("of the analysis note for the full justification.")
    log.info("")

    # =========================================================================
    # 1. Load inputs
    # =========================================================================
    log.info("[bold]1. Loading inputs...[/bold]")

    syst = np.load(P4_EXEC / "systematics_shifts.npz")
    cov_stat_data = np.load(P4_EXEC / "covariance_stat.npz")
    cov_stat = cov_stat_data["cov"]
    stat_replicas = cov_stat_data["replicas"]

    log.info(f"Loaded covariance_stat.npz: shape {cov_stat.shape}")
    log.info("Available systematic keys in systematics_shifts.npz:")
    for k in syst.files:
        if k.startswith("shift_"):
            log.info(f"  {k}: max_abs = {np.max(np.abs(syst[k])):.4f}")

    # The key for BBB alternative method
    BBB_KEY = "shift_alt_method"
    if BBB_KEY not in syst.files:
        log.warning(f"Key '{BBB_KEY}' not found in systematics_shifts.npz")
        log.warning("Available keys: " + str(syst.files))
    else:
        log.info(f"\nBBB shift ({BBB_KEY}) max absolute value: "
                 f"{np.max(np.abs(syst[BBB_KEY])):.4f}")
        log.info("=> Removing this from the systematic budget.")

    # =========================================================================
    # 2. Rebuild systematic covariance WITHOUT BBB
    # =========================================================================
    log.info("\n[bold]2. Rebuilding systematic covariance (BBB excluded)...[/bold]")

    # All systematic sources EXCEPT shift_alt_method
    syst_sources_no_bbb = [
        "shift_mom_smear",
        "shift_sel_missp",
        "shift_sel_eff",
        "shift_sel_tpc",
        "shift_calorimeter",
        "shift_background",
        "shift_regularization",
        "shift_prior_flat",
        # "shift_alt_method" -- EXCLUDED: BBB is not a valid alternative
        "shift_hadronization",
        "shift_isr",
        "shift_heavy_flavor",
        "shift_mc_statistics",
    ]

    cov_syst_total_no_bbb = np.zeros((N_BINS, N_BINS))
    cov_syst_per_no_bbb   = {}

    for key in syst_sources_no_bbb:
        if key in syst.files:
            delta = syst[key]
            if key == "shift_mc_statistics":
                cov_key = np.diag(delta**2)
            else:
                cov_key = np.outer(delta, delta)
            cov_syst_per_no_bbb[key] = cov_key
            cov_syst_total_no_bbb += cov_key
            max_d = np.abs(np.diag(cov_key)).max()
            log.info(f"  {key}: max diagonal cov = {max_d:.3e}")
        else:
            log.warning(f"  {key} not found in systematics_shifts.npz -- skipping")

    log.info(f"\nTotal syst cov (no BBB): max diagonal = "
             f"{np.diag(cov_syst_total_no_bbb).max():.3e}")

    # Compare to old BBB-inclusive syst covariance for reference
    old_cov_syst_data = np.load(P4_EXEC / "covariance_syst.npz")
    old_cov_syst = old_cov_syst_data["cov_total"]
    log.info(f"Old syst cov (with BBB): max diagonal = "
             f"{np.diag(old_cov_syst).max():.3e}")
    bbb_contribution = np.diag(old_cov_syst - cov_syst_total_no_bbb)
    log.info(f"BBB contribution removed: max = {bbb_contribution.max():.3e}")

    # =========================================================================
    # 3. Total covariance
    # =========================================================================
    log.info("\n[bold]3. Computing total covariance (stat + syst, no BBB)...[/bold]")
    cov_total_no_bbb = cov_stat + cov_syst_total_no_bbb

    # =========================================================================
    # 4. Validation
    # =========================================================================
    log.info("\n[bold]4. Validation...[/bold]")

    eigenvalues_stat  = np.linalg.eigvalsh(cov_stat)
    eigenvalues_syst  = np.linalg.eigvalsh(cov_syst_total_no_bbb)
    eigenvalues_total = np.linalg.eigvalsh(cov_total_no_bbb)

    n_neg_total = (eigenvalues_total < -1e-12 * eigenvalues_total.max()).sum()
    log.info(f"Total covariance: {n_neg_total} negative eigenvalues "
             f"(min = {eigenvalues_total.min():.3e})")

    # Condition number (fit-range sub-matrix)
    cov_fit = cov_total_no_bbb[np.ix_(FIT_MASK, FIT_MASK)]
    eigs_fit = np.linalg.eigvalsh(cov_fit)
    eigs_pos = eigs_fit[eigs_fit > 0]
    if len(eigs_pos) > 0:
        condition_number = eigs_pos.max() / eigs_pos.min()
        log.info(f"Condition number (fit range, no BBB): {condition_number:.2e}")
        if condition_number > 1e10:
            log.warning("  WARN: condition number > 1e10 -- chi2 fit may be ill-conditioned")
        else:
            log.info("  OK: condition number is acceptable (< 1e10 threshold per conventions)")
    else:
        log.warning("  Could not compute condition number")
        condition_number = np.inf

    # Per-bin uncertainties
    sigma_tot_new  = np.sqrt(np.diag(cov_total_no_bbb))
    sigma_stat_new = np.sqrt(np.diag(cov_stat))
    sigma_syst_new = np.sqrt(np.diag(cov_syst_total_no_bbb))

    # Load nominal unfolded result for normalization
    td_old = np.load(RESULTS / "thrust_distribution.npz")
    norm_nominal = td_old["unfolded_norm"]
    safe_nom = np.where(norm_nominal > 0, norm_nominal, 1.0)

    frac_tot  = sigma_tot_new  / safe_nom * 100
    frac_stat = sigma_stat_new / safe_nom * 100
    frac_syst = sigma_syst_new / safe_nom * 100

    log.info("\n[bold]Per-bin uncertainties (fit range, BBB excluded):[/bold]")
    table = Table(title="Total Uncertainty per Bin (No BBB)", show_header=True)
    table.add_column("tau_center", justify="right")
    table.add_column("Stat (%)", justify="right")
    table.add_column("Syst (%)", justify="right")
    table.add_column("Total (%)", justify="right")
    for j in range(N_BINS):
        if FIT_MASK[j]:
            table.add_row(
                f"{TAU_CENTERS[j]:.3f}",
                f"{frac_stat[j]:.3f}",
                f"{frac_syst[j]:.3f}",
                f"{frac_tot[j]:.3f}",
            )
    console.print(table)

    # Correlation matrix
    diag_sqrt = np.sqrt(np.maximum(np.diag(cov_total_no_bbb), 1e-20))
    corr_total = cov_total_no_bbb / np.outer(diag_sqrt, diag_sqrt)
    corr_total = np.clip(corr_total, -1.0, 1.0)

    # =========================================================================
    # 5. Chi2 vs MC truth with new covariance
    # =========================================================================
    log.info("\n[bold]5. Chi2 vs Pythia 6.1 MC truth (new covariance)...[/bold]")

    mc_truth_norm = td_old["mc_truth_norm"]
    cov_fit_new = cov_total_no_bbb[np.ix_(FIT_MASK, FIT_MASK)]

    try:
        cov_fit_inv = np.linalg.inv(cov_fit_new)
    except np.linalg.LinAlgError:
        log.warning("  Covariance inversion failed; using diagonal-only chi2")
        cov_fit_inv = np.diag(1.0 / np.diag(cov_fit_new))

    delta_fit = norm_nominal[FIT_MASK] - mc_truth_norm[FIT_MASK]
    chi2_new = float(delta_fit @ cov_fit_inv @ delta_fit)
    ndf_new  = N_FIT_BINS
    pval_new = float(stats.chi2.sf(chi2_new, df=ndf_new))

    log.info(f"  New chi2/ndf = {chi2_new:.1f} / {ndf_new} = {chi2_new/ndf_new:.3f}")
    log.info(f"  New p-value  = {pval_new:.4e}")

    # Old chi2 for comparison
    old_chi2 = float(td_old["chi2_vs_mc"])
    log.info(f"  Old chi2 (with BBB) = {old_chi2:.1f} / {int(td_old['ndf_vs_mc'])}")
    log.info(f"  Change: {chi2_new:.1f} vs {old_chi2:.1f} (increase expected: "
             f"removing large systematic makes chi2 larger)")

    # Identify dominant systematic (without BBB)
    per_source_max = {}
    for key in syst_sources_no_bbb:
        if key in syst.files:
            delta = syst[key]
            frac_max = np.max(np.abs(delta[FIT_MASK]) / safe_nom[FIT_MASK]) * 100
            per_source_max[key] = frac_max
    sorted_sources = sorted(per_source_max.items(), key=lambda x: x[1], reverse=True)
    log.info("\n[bold]Dominant systematics after BBB removal (fit range, max %):[/bold]")
    for src, val in sorted_sources[:5]:
        log.info(f"  {src}: {val:.2f}%")

    # =========================================================================
    # 6. Save updated covariance files
    # =========================================================================
    log.info("\n[bold]6. Saving updated covariance files...[/bold]")

    # covariance_syst.npz (BBB removed)
    np.savez(
        P4_EXEC / "covariance_syst.npz",
        cov_total=cov_syst_total_no_bbb,
        **{k: v for k, v in cov_syst_per_no_bbb.items()},
        tau_edges=TAU_EDGES,
        tau_centers=TAU_CENTERS,
    )
    log.info(f"  Saved {P4_EXEC}/covariance_syst.npz (BBB removed)")

    # covariance_total.npz (BBB removed)
    np.savez(
        P4_EXEC / "covariance_total.npz",
        cov=cov_total_no_bbb,
        cov_stat=cov_stat,
        cov_syst=cov_syst_total_no_bbb,
        corr=corr_total,
        eigenvalues=eigenvalues_total,
        condition_number=condition_number,
        sigma_tot=sigma_tot_new,
        sigma_stat=sigma_stat_new,
        sigma_syst=sigma_syst_new,
        tau_edges=TAU_EDGES,
        tau_centers=TAU_CENTERS,
        fit_mask=FIT_MASK,
    )
    log.info(f"  Saved {P4_EXEC}/covariance_total.npz (BBB removed)")

    # covariance CSV (fit range)
    tau_fit = TAU_CENTERS[FIT_MASK]
    header  = "tau_center," + ",".join(f"{t:.4f}" for t in tau_fit)
    rows    = []
    for i, t_row in enumerate(tau_fit):
        row_str = f"{t_row:.4f}," + ",".join(
            f"{cov_fit_new[i,j]:.6e}" for j in range(len(tau_fit))
        )
        rows.append(row_str)
    for dest in (RESULTS / "covariance_total_fitrange.csv",
                 P5_RESULTS / "covariance_total_fitrange.csv"):
        with open(dest, "w") as f:
            f.write(header + "\n")
            for row in rows:
                f.write(row + "\n")
        log.info(f"  Saved {dest}")

    # =========================================================================
    # 7. Update thrust_distribution files
    # =========================================================================
    log.info("\n[bold]7. Updating thrust_distribution files...[/bold]")

    # NPZ (phase4 results only -- values don't change, just uncertainties)
    np.savez(
        RESULTS / "thrust_distribution.npz",
        tau_edges=TAU_EDGES,
        tau_centers=TAU_CENTERS,
        tau_bin_width=BIN_WIDTH,
        unfolded_norm=norm_nominal,
        unfolded_counts=td_old["unfolded_counts"],
        sigma_stat=sigma_stat_new,
        sigma_syst=sigma_syst_new,
        sigma_tot=sigma_tot_new,
        mc_truth_norm=mc_truth_norm,
        fit_mask=FIT_MASK,
        n_data_events=td_old["n_data_events"],
        chi2_vs_mc=chi2_new,
        ndf_vs_mc=ndf_new,
        pval_vs_mc=pval_new,
        n_iterations=td_old["n_iterations"],
    )
    log.info(f"  Saved {RESULTS}/thrust_distribution.npz")

    # CSV (write to both phase4 results and phase5 results)
    csv_lines = [
        "# ALEPH Thrust Distribution -- (1/N)dN/dtau -- corrected for detector effects",
        "# Analysis: thrust_alphas, Phase 4a (BBB removed from systematic budget)",
        "# tau_center, tau_lo, tau_hi, dNdtau, stat_unc, syst_unc, total_unc",
    ]
    for j in range(N_BINS):
        if FIT_MASK[j]:
            csv_lines.append(
                f"{TAU_CENTERS[j]:.4f},"
                f"{TAU_EDGES[j]:.4f},"
                f"{TAU_EDGES[j+1]:.4f},"
                f"{norm_nominal[j]:.6e},"
                f"{sigma_stat_new[j]:.6e},"
                f"{sigma_syst_new[j]:.6e},"
                f"{sigma_tot_new[j]:.6e}"
            )
    csv_content = "\n".join(csv_lines) + "\n"
    for dest in (RESULTS / "thrust_distribution.csv",
                 P5_RESULTS / "thrust_distribution.csv"):
        with open(dest, "w") as f:
            f.write(csv_content)
        log.info(f"  Saved {dest}")

    # =========================================================================
    # 8. Summary
    # =========================================================================
    log.info("\n[bold green]===== SUMMARY =====[/bold green]")
    log.info(f"BBB removed: max shift was "
             f"{np.max(np.abs(syst[BBB_KEY][FIT_MASK]) / safe_nom[FIT_MASK]) * 100:.1f}%")
    dom_src, dom_val = sorted_sources[0]
    log.info(f"New dominant systematic: {dom_src} = {dom_val:.2f}%")
    log.info(f"Max total uncertainty (fit range): {frac_tot[FIT_MASK].max():.2f}%")
    log.info(f"Max syst uncertainty (fit range):  {frac_syst[FIT_MASK].max():.2f}%")
    log.info(f"Max stat uncertainty (fit range):  {frac_stat[FIT_MASK].max():.2f}%")
    log.info(f"Condition number (fit range):      {condition_number:.2e}")
    log.info(f"Old chi2/ndf (with BBB):           {old_chi2:.1f}/{int(td_old['ndf_vs_mc'])}"
             f" = {old_chi2/int(td_old['ndf_vs_mc']):.3f}")
    log.info(f"New chi2/ndf (BBB removed):        {chi2_new:.1f}/{ndf_new}"
             f" = {chi2_new/ndf_new:.3f}")
    log.info(f"New p-value:                       {pval_new:.4e}")
    log.info("")
    log.info("Updated files:")
    log.info(f"  {P4_EXEC}/covariance_syst.npz")
    log.info(f"  {P4_EXEC}/covariance_total.npz")
    log.info(f"  {RESULTS}/covariance_total_fitrange.csv")
    log.info(f"  {RESULTS}/thrust_distribution.{{npz,csv}}")
    log.info(f"  {P5_RESULTS}/covariance_total_fitrange.csv")
    log.info(f"  {P5_RESULTS}/thrust_distribution.csv")
    log.info("")
    log.info("[bold green]rebuild_covariance_no_bbb.py complete[/bold green]")


if __name__ == "__main__":
    main()
