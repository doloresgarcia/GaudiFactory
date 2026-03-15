"""
Script 04: MC truth (generator-level) inspection and response matrix prototype.
- Compare detector-level vs generator-level thrust
- Show tau migration: scatter plot and response matrix prototype
- Verify tgen vs tgenBefore (generator efficiency)
- Check MC truth particle content (pid, pwflag encoding in gen level)
"""
import logging
import numpy as np
import uproot
import awkward as ak
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mplhep as mh
from pathlib import Path
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger("mc_truth")

MC_FILE = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC/LEP1MC1994_recons_aftercut-001.root")
FIGURES_DIR = Path("/n/home07/anovak/work/reslop/thrust_alphas/phase2_exploration/figures")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

mh.style.use("CMS")


def load_mc_trees():
    """Load all MC trees from one file."""
    log.info("Loading MC trees from: %s", MC_FILE.name)
    with uproot.open(MC_FILE) as f:
        # Reco (detector-level)
        reco_branches = ["Thrust", "Thrust_charged", "Sphericity",
                         "nChargedHadrons", "passesAll", "uniqueID",
                         "nParticle", "Energy", "bFlag"]
        t_reco = f["t"].arrays(
            [b for b in reco_branches if b in f["t"].keys()],
            library="ak"
        )

        # Generator-level (after selection applied to gen)
        gen_branches = ["Thrust", "Thrust_charged", "Sphericity",
                        "nChargedHadrons", "passesAll", "uniqueID",
                        "nParticle", "pid", "pwflag", "charge",
                        "ThrustWithReco", "ThrustWithGenIneff",
                        "Energy", "bFlag"]
        t_gen = f["tgen"].arrays(
            [b for b in gen_branches if b in f["tgen"].keys()],
            library="ak"
        )

        t_gen_before = f["tgenBefore"].arrays(
            [b for b in gen_branches if b in f["tgenBefore"].keys()],
            library="ak"
        )

    log.info(f"  t (reco): {len(t_reco):,} events")
    log.info(f"  tgen: {len(t_gen):,} events")
    log.info(f"  tgenBefore: {len(t_gen_before):,} events")

    return t_reco, t_gen, t_gen_before


def analyze_gen_particle_content(t_gen):
    """Analyze what particles are in the generator-level tree."""
    log.info("\n=== Generator-level particle content ===")

    # Check pwflag in gen tree
    if "pwflag" in t_gen.fields:
        pf_flat = ak.to_numpy(ak.flatten(t_gen["pwflag"]))
        unique_pf = np.unique(pf_flat)
        log.info(f"  Gen pwflag values: {unique_pf}")
        for pf_val in unique_pf:
            n = np.sum(pf_flat == pf_val)
            log.info(f"    pwflag={pf_val}: {n:,}")

    # pid distribution
    if "pid" in t_gen.fields:
        pid_flat = ak.to_numpy(ak.flatten(t_gen["pid"]))
        unique_pid, counts = np.unique(pid_flat, return_counts=True)
        top_idx = np.argsort(counts)[::-1][:20]
        log.info(f"\n  Top 20 PIDs in gen tree:")
        for i in top_idx:
            log.info(f"    PID={unique_pid[i]:6d}: {counts[i]:8,}")

    log.info(f"  nParticle (gen): mean={float(ak.mean(t_gen['nParticle'])):.1f}")


def plot_det_vs_gen_tau():
    """Plot detector-level vs generator-level tau with response matrix."""
    log.info("\n=== Detector vs Generator tau comparison ===")

    t_reco, t_gen, t_gen_before = load_mc_trees()

    # Apply passesAll to reco
    mask_reco = t_reco["passesAll"]
    reco_sel = t_reco[mask_reco]
    tau_reco = 1 - ak.to_numpy(reco_sel["Thrust"])

    # Generator-level: tgen has same event count as reco (matched)
    # Apply the same mask - since entries are matched 1:1
    gen_sel = t_gen[mask_reco]
    tau_gen = 1 - ak.to_numpy(gen_sel["Thrust"])

    log.info(f"  Events passing passesAll: {len(tau_reco):,}")
    log.info(f"  tau_reco: mean={np.mean(tau_reco):.4f}, std={np.std(tau_reco):.4f}")
    log.info(f"  tau_gen:  mean={np.mean(tau_gen):.4f}, std={np.std(tau_gen):.4f}")
    log.info(f"  Detector smearing (reco-gen): mean={np.mean(tau_reco-tau_gen):.4f}, "
             f"std={np.std(tau_reco-tau_gen):.4f}")

    # Scatter: tau_gen vs tau_reco
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.hist2d(tau_gen, tau_reco, bins=50, range=[[0, 0.5], [0, 0.5]],
              cmap="Blues", density=True)
    ax.plot([0, 0.5], [0, 0.5], "r--", linewidth=1.5, label="$\\tau_{\\rm reco} = \\tau_{\\rm gen}$")
    ax.set_xlabel(r"$\tau_{\rm gen}$", fontsize=14)
    ax.set_ylabel(r"$\tau_{\rm reco}$", fontsize=14)
    ax.legend(fontsize="x-small")
    mh.label.exp_label(exp="ALEPH", rlabel=r"Pythia 6.1 MC (1 file)", ax=ax)
    plt.tight_layout()
    for ext in ["pdf", "png"]:
        fig.savefig(FIGURES_DIR / f"tau_gen_vs_reco_scatter.{ext}",
                    bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("  Saved: tau_gen_vs_reco_scatter.{pdf,png}")

    # Response matrix (prototype: 2D histogram)
    bins = np.linspace(0, 0.5, 26)
    response, _, _ = np.histogram2d(tau_gen, tau_reco, bins=[bins, bins])
    # Normalize row by row (generator bin = row)
    row_sums = response.sum(axis=1, keepdims=True)
    response_norm = np.where(row_sums > 0, response / row_sums, 0)

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.imshow(response_norm.T, origin="lower", aspect="auto",
                   extent=[0, 0.5, 0, 0.5], cmap="viridis",
                   vmin=0, vmax=response_norm.max())
    plt.colorbar(im, ax=ax, label="P(reco bin | gen bin)")
    ax.set_xlabel(r"$\tau_{\rm gen}$", fontsize=14)
    ax.set_ylabel(r"$\tau_{\rm reco}$", fontsize=14)
    ax.plot([0, 0.5], [0, 0.5], "r--", linewidth=1.5)
    mh.label.exp_label(exp="ALEPH", rlabel=r"Pythia 6.1 MC (1 file)", ax=ax)
    plt.tight_layout()
    for ext in ["pdf", "png"]:
        fig.savefig(FIGURES_DIR / f"response_matrix_prototype.{ext}",
                    bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("  Saved: response_matrix_prototype.{pdf,png}")

    # Check diagonal fraction
    diag_frac = np.diag(response_norm)
    log.info(f"\n  Response matrix diagonal fractions (per bin):")
    for i in range(len(diag_frac)):
        lo = bins[i]
        hi = bins[i+1]
        log.info(f"    tau [{lo:.3f}, {hi:.3f}]: diag = {diag_frac[i]:.3f}")

    # Compare reco tau vs gen tau distributions
    bins_plot = np.linspace(0, 0.5, 51)
    bin_centers = 0.5 * (bins_plot[:-1] + bins_plot[1:])
    bin_widths = np.diff(bins_plot)

    h_reco, _ = np.histogram(tau_reco, bins=bins_plot)
    h_gen, _ = np.histogram(tau_gen, bins=bins_plot)
    h_gen_before = None

    # Also compare tgenBefore thrust
    tau_gen_before = 1 - ak.to_numpy(t_gen_before["Thrust"])
    h_gen_before, _ = np.histogram(tau_gen_before, bins=bins_plot)

    n_reco = np.sum(h_reco)
    n_gen = np.sum(h_gen)
    n_gb = np.sum(h_gen_before)

    h_reco_norm = h_reco / (n_reco * bin_widths)
    h_gen_norm = h_gen / (n_gen * bin_widths)
    h_gen_before_norm = h_gen_before / (n_gb * bin_widths)

    fig, (ax, ax_ratio) = plt.subplots(
        2, 1, figsize=(10, 10),
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=True
    )

    ax.step(bins_plot[:-1], h_reco_norm, where="post", color="royalblue",
            linewidth=1.5, label="MC reco (passesAll)")
    ax.step(bins_plot[:-1], h_gen_norm, where="post", color="darkorange",
            linewidth=1.5, label="MC gen (tgen, matched to reco)", linestyle="--")
    ax.step(bins_plot[:-1], h_gen_before_norm, where="post", color="green",
            linewidth=1.5, label="MC gen (tgenBefore, all gen)", linestyle=":")
    ax.set_ylabel(r"$(1/N)\,dN/d\tau$", fontsize=14)
    ax.set_yscale("log")
    ax.legend(fontsize="x-small")
    mh.label.exp_label(exp="ALEPH", rlabel=r"Pythia 6.1 MC (1 file)", ax=ax)

    ratio_det_gen = np.where(h_gen_norm > 0, h_reco_norm / h_gen_norm, np.nan)
    ax_ratio.step(bins_plot[:-1], ratio_det_gen, where="post",
                  color="royalblue", linewidth=1.5)
    ax_ratio.axhline(1.0, color="black", linewidth=1)
    ax_ratio.set_ylim(0.5, 1.5)
    ax_ratio.set_ylabel("Reco/Gen", fontsize=12)
    ax_ratio.set_xlabel(r"$\tau = 1 - T$", fontsize=14)

    plt.tight_layout()
    for ext in ["pdf", "png"]:
        fig.savefig(FIGURES_DIR / f"tau_reco_vs_gen.{ext}",
                    bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("  Saved: tau_reco_vs_gen.{pdf,png}")


def analyze_tau_resolution():
    """Quantify tau resolution as function of tau_gen."""
    log.info("\n=== Tau resolution vs tau_gen ===")

    t_reco, t_gen, _ = load_mc_trees()
    mask_reco = t_reco["passesAll"]
    tau_reco = 1 - ak.to_numpy(t_reco["Thrust"][mask_reco])
    tau_gen = 1 - ak.to_numpy(t_gen["Thrust"][mask_reco])

    delta_tau = tau_reco - tau_gen

    # Profile in gen bins
    gen_bins = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]
    log.info("\n  tau_gen bin | <delta_tau> | sigma(delta_tau)")
    for i in range(len(gen_bins) - 1):
        lo, hi = gen_bins[i], gen_bins[i+1]
        mask = (tau_gen >= lo) & (tau_gen < hi)
        if mask.sum() > 10:
            mean_dt = np.mean(delta_tau[mask])
            std_dt = np.std(delta_tau[mask])
            log.info(f"  [{lo:.2f}, {hi:.2f}]:  bias={mean_dt:+.4f}  res={std_dt:.4f}  N={mask.sum():,}")


def main():
    log.info("=== Phase 2 Script 04: MC Truth and Response Matrix ===")

    t_reco, t_gen, t_gen_before = load_mc_trees()

    analyze_gen_particle_content(t_gen)
    plot_det_vs_gen_tau()
    analyze_tau_resolution()

    log.info("\n=== Done ===")


if __name__ == "__main__":
    main()
