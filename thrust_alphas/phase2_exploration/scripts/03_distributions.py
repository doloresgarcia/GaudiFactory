"""
Script 03: Produce key distributions for data and MC.
  - Track multiplicity, momentum, thrust (tau=1-T), sphericity
  - Cutflow table showing which events pass each selection cut
  - Year-by-year data consistency check for thrust
All figures saved to phase2_exploration/figures/.
"""
import logging
import numpy as np
import uproot
import awkward as ak
import hist
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
log = logging.getLogger("distributions")

DATA_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPH")
MC_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC")
FIGURES_DIR = Path("/n/home07/anovak/work/reslop/thrust_alphas/phase2_exploration/figures")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

DATA_FILES = {
    "1992": DATA_DIR / "LEP1Data1992_recons_aftercut-MERGED.root",
    "1993": DATA_DIR / "LEP1Data1993_recons_aftercut-MERGED.root",
    "1994P1": DATA_DIR / "LEP1Data1994P1_recons_aftercut-MERGED.root",
    "1994P2": DATA_DIR / "LEP1Data1994P2_recons_aftercut-MERGED.root",
    "1994P3": DATA_DIR / "LEP1Data1994P3_recons_aftercut-MERGED.root",
    "1995": DATA_DIR / "LEP1Data1995_recons_aftercut-MERGED.root",
}

MC_FILE = MC_DIR / "LEP1MC1994_recons_aftercut-001.root"

# Use passesAll for the full selection
SELECTION_BRANCHES = [
    "passesAll", "passesNTupleAfterCut",
    "passesTotalChgEnergyMin", "passesNTrkMin",
    "passesSTheta", "passesMissP", "passesISR",
    "Thrust", "Sphericity",
    "nChargedHadrons", "nChargedHadronsHP",
    "pmag", "nParticle", "missP",
]

mh.style.use("CMS")


def load_data_file(path: Path, label: str, entry_limit: int | None = None) -> ak.Array:
    """Load tree 't' from a ROOT file with selection branches."""
    log.info(f"  Loading {label}: {path.name}")
    with uproot.open(path) as f:
        tree = f["t"]
        avail = [b for b in SELECTION_BRANCHES if b in tree.keys()]
        arrays = tree.arrays(avail, entry_stop=entry_limit, library="ak")
    log.info(f"    {len(arrays):,} events loaded")
    return arrays


def apply_full_selection(events: ak.Array) -> ak.Array:
    """Apply full selection: passesAll == True."""
    mask = events["passesAll"]
    return events[mask]


def cutflow_table(events: ak.Array, label: str) -> None:
    """Print cutflow table."""
    log.info(f"\n  Cutflow for {label} ({len(events):,} input events):")
    n_total = len(events)

    flags = [
        ("NTupleAfterCut", "passesNTupleAfterCut"),
        ("TotalChgEnergyMin", "passesTotalChgEnergyMin"),
        ("NTrkMin", "passesNTrkMin"),
        ("STheta", "passesSTheta"),
        ("MissP", "passesMissP"),
        ("ISR", "passesISR"),
        ("ALL", "passesAll"),
    ]

    n_prev = n_total
    for name, flag in flags:
        if flag not in events.fields:
            continue
        n_pass = int(ak.sum(events[flag]))
        eff_abs = n_pass / n_total * 100
        eff_rel = n_pass / n_prev * 100 if n_prev > 0 else 0
        log.info(f"    {name:20s}: {n_pass:8,}  abs={eff_abs:.1f}%  rel={eff_rel:.1f}%")
        n_prev = n_pass


def compute_cutflow_full(entry_limit: int = 100000) -> None:
    """Compute cutflow on a larger sample."""
    log.info("\n=== Full Cutflow Analysis ===")
    # Use 1994P1 data (largest non-combined year)
    events = load_data_file(DATA_FILES["1994P1"], "DATA 1994P1", entry_limit=entry_limit)
    cutflow_table(events, "DATA 1994P1")

    events_mc = load_data_file(MC_FILE, "MC", entry_limit=entry_limit)
    cutflow_table(events_mc, "MC")


def plot_tau_distribution() -> None:
    """Plot thrust tau=1-T distribution: data vs MC with ratio."""
    log.info("\n=== Thrust tau distribution ===")

    # Load data: use combined 1994 period for comparison with 1994 MC
    tau_data_all = []
    for year, fpath in DATA_FILES.items():
        log.info(f"  Loading {year}...")
        events = load_data_file(fpath, year)
        sel = apply_full_selection(events)
        thrust = ak.to_numpy(sel["Thrust"])
        tau_data_all.append(1 - thrust)

    tau_data = np.concatenate(tau_data_all)
    log.info(f"  Total data events (passesAll): {len(tau_data):,}")

    # Load MC
    events_mc = load_data_file(MC_FILE, "MC (1 file)")
    sel_mc = apply_full_selection(events_mc)
    tau_mc = 1 - ak.to_numpy(sel_mc["Thrust"])
    log.info(f"  MC events (passesAll, 1 file): {len(tau_mc):,}")

    # Histogram
    bins = np.linspace(0, 0.5, 51)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    bin_widths = np.diff(bins)

    h_data, _ = np.histogram(tau_data, bins=bins)
    h_mc, _ = np.histogram(tau_mc, bins=bins)

    # Normalize to unit area
    n_data = np.sum(h_data)
    n_mc = np.sum(h_mc)
    h_data_norm = h_data / (n_data * bin_widths)
    h_mc_norm = h_mc / (n_mc * bin_widths)

    h_data_err = np.sqrt(h_data) / (n_data * bin_widths)

    # Plot
    fig, (ax, ax_ratio) = plt.subplots(
        2, 1, figsize=(10, 10),
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=True
    )

    ax.errorbar(bin_centers, h_data_norm, yerr=h_data_err, fmt="ko",
                markersize=4, label="Data (1992-1995)", zorder=5)
    ax.step(bins[:-1], h_mc_norm, where="post", color="royalblue",
            linewidth=1.5, label="Pythia 6.1 MC (1 file)")
    ax.set_ylabel(r"$(1/N)\,dN/d\tau$", fontsize=14)
    ax.set_yscale("log")
    ax.legend(fontsize="x-small")
    mh.label.exp_label(exp="ALEPH", data=True,
                       rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax)

    # Ratio
    ratio = np.where(h_mc_norm > 0, h_data_norm / h_mc_norm, np.nan)
    ratio_err = np.where(h_mc_norm > 0, h_data_err / h_mc_norm, np.nan)
    ax_ratio.errorbar(bin_centers, ratio, yerr=ratio_err, fmt="ko", markersize=4)
    ax_ratio.axhline(1.0, color="royalblue", linewidth=1)
    ax_ratio.axhline(1.1, color="gray", linewidth=0.8, linestyle="--")
    ax_ratio.axhline(0.9, color="gray", linewidth=0.8, linestyle="--")
    ax_ratio.set_ylim(0.5, 1.5)
    ax_ratio.set_ylabel("Data/MC", fontsize=12)
    ax_ratio.set_xlabel(r"$\tau = 1 - T$", fontsize=14)

    plt.tight_layout()
    for ext in ["pdf", "png"]:
        fig.savefig(FIGURES_DIR / f"thrust_tau_data_mc.{ext}",
                    bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("  Saved: thrust_tau_data_mc.{pdf,png}")


def plot_track_multiplicity() -> None:
    """Plot charged track multiplicity: data vs MC."""
    log.info("\n=== Track multiplicity distribution ===")

    events_data = load_data_file(DATA_FILES["1994P1"], "DATA 1994P1")
    sel_data = apply_full_selection(events_data)
    nch_data = ak.to_numpy(sel_data["nChargedHadrons"])

    events_mc = load_data_file(MC_FILE, "MC")
    sel_mc = apply_full_selection(events_mc)
    nch_mc = ak.to_numpy(sel_mc["nChargedHadrons"])

    bins = np.arange(0, 55, 1)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])

    h_data, _ = np.histogram(nch_data, bins=bins)
    h_mc, _ = np.histogram(nch_mc, bins=bins)

    n_data = np.sum(h_data)
    n_mc = np.sum(h_mc)
    h_data_norm = h_data / n_data
    h_mc_norm = h_mc / n_mc
    h_data_err = np.sqrt(h_data) / n_data

    fig, (ax, ax_ratio) = plt.subplots(
        2, 1, figsize=(10, 10),
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=True
    )

    ax.errorbar(bin_centers, h_data_norm, yerr=h_data_err, fmt="ko",
                markersize=4, label="Data 1994P1", zorder=5)
    ax.step(bins[:-1], h_mc_norm, where="post", color="royalblue",
            linewidth=1.5, label="Pythia 6.1 MC (1 file)")
    ax.set_ylabel("Event fraction", fontsize=14)
    ax.legend(fontsize="x-small")
    mh.label.exp_label(exp="ALEPH", data=True,
                       rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax)

    ratio = np.where(h_mc_norm > 0, h_data_norm / h_mc_norm, np.nan)
    ratio_err = np.where(h_mc_norm > 0, h_data_err / h_mc_norm, np.nan)
    ax_ratio.errorbar(bin_centers, ratio, yerr=ratio_err, fmt="ko", markersize=4)
    ax_ratio.axhline(1.0, color="royalblue", linewidth=1)
    ax_ratio.set_ylim(0.5, 1.5)
    ax_ratio.set_ylabel("Data/MC", fontsize=12)
    ax_ratio.set_xlabel(r"$N_{\rm charged}$", fontsize=14)

    plt.tight_layout()
    for ext in ["pdf", "png"]:
        fig.savefig(FIGURES_DIR / f"ncharged_data_mc.{ext}",
                    bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("  Saved: ncharged_data_mc.{pdf,png}")


def plot_momentum_distribution() -> None:
    """Plot track momentum distribution: data vs MC."""
    log.info("\n=== Track momentum distribution ===")

    TRACK_BRANCHES = ["pmag", "charge", "passesAll"]

    def load_pmag_selected(path, label):
        with uproot.open(path) as f:
            events = f["t"].arrays(
                [b for b in TRACK_BRANCHES if b in f["t"].keys()],
                library="ak"
            )
        sel = apply_full_selection(events)
        # charged tracks only (pwflag=0 equivalent: charge != 0)
        pmag_charged = sel["pmag"][sel["charge"] != 0]
        return ak.to_numpy(ak.flatten(pmag_charged))

    p_data = load_pmag_selected(DATA_FILES["1994P1"], "DATA 1994P1")
    p_mc = load_pmag_selected(MC_FILE, "MC")

    bins = np.logspace(np.log10(0.1), np.log10(50), 60)
    bin_centers = np.sqrt(bins[:-1] * bins[1:])
    bin_widths = np.diff(bins)

    h_data, _ = np.histogram(p_data, bins=bins)
    h_mc, _ = np.histogram(p_mc, bins=bins)

    n_data = np.sum(h_data)
    n_mc = np.sum(h_mc)
    h_data_norm = h_data / (n_data * bin_widths)
    h_mc_norm = h_mc / (n_mc * bin_widths)
    h_data_err = np.sqrt(h_data) / (n_data * bin_widths)

    fig, (ax, ax_ratio) = plt.subplots(
        2, 1, figsize=(10, 10),
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=True
    )

    ax.errorbar(bin_centers, h_data_norm, yerr=h_data_err, fmt="ko",
                markersize=4, label="Data 1994P1", zorder=5)
    ax.step(bins[:-1], h_mc_norm, where="post", color="royalblue",
            linewidth=1.5, label="Pythia 6.1 MC (1 file)")
    ax.set_ylabel(r"$(1/N)\,dN/d|p|$ [GeV$^{-1}$]", fontsize=14)
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.legend(fontsize="x-small")
    mh.label.exp_label(exp="ALEPH", data=True,
                       rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax)

    ratio = np.where(h_mc_norm > 0, h_data_norm / h_mc_norm, np.nan)
    ratio_err = np.where(h_mc_norm > 0, h_data_err / h_mc_norm, np.nan)
    ax_ratio.errorbar(bin_centers, ratio, yerr=ratio_err, fmt="ko", markersize=4)
    ax_ratio.axhline(1.0, color="royalblue", linewidth=1)
    ax_ratio.set_ylim(0.5, 1.5)
    ax_ratio.set_ylabel("Data/MC", fontsize=12)
    ax_ratio.set_xlabel(r"$|p|$ [GeV]", fontsize=14)

    plt.tight_layout()
    for ext in ["pdf", "png"]:
        fig.savefig(FIGURES_DIR / f"track_momentum_data_mc.{ext}",
                    bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("  Saved: track_momentum_data_mc.{pdf,png}")


def plot_sphericity() -> None:
    """Plot sphericity distribution: data vs MC."""
    log.info("\n=== Sphericity distribution ===")

    events_data = load_data_file(DATA_FILES["1994P1"], "DATA 1994P1")
    sel_data = apply_full_selection(events_data)
    sph_data = ak.to_numpy(sel_data["Sphericity"])

    events_mc = load_data_file(MC_FILE, "MC")
    sel_mc = apply_full_selection(events_mc)
    sph_mc = ak.to_numpy(sel_mc["Sphericity"])

    bins = np.linspace(0, 0.8, 41)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    bin_widths = np.diff(bins)

    h_data, _ = np.histogram(sph_data, bins=bins)
    h_mc, _ = np.histogram(sph_mc, bins=bins)

    n_data = np.sum(h_data)
    n_mc = np.sum(h_mc)
    h_data_norm = h_data / (n_data * bin_widths)
    h_mc_norm = h_mc / (n_mc * bin_widths)
    h_data_err = np.sqrt(h_data) / (n_data * bin_widths)

    fig, (ax, ax_ratio) = plt.subplots(
        2, 1, figsize=(10, 10),
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=True
    )

    ax.errorbar(bin_centers, h_data_norm, yerr=h_data_err, fmt="ko",
                markersize=4, label="Data 1994P1", zorder=5)
    ax.step(bins[:-1], h_mc_norm, where="post", color="royalblue",
            linewidth=1.5, label="Pythia 6.1 MC (1 file)")
    ax.set_ylabel(r"$(1/N)\,dN/dS$", fontsize=14)
    ax.legend(fontsize="x-small")
    mh.label.exp_label(exp="ALEPH", data=True,
                       rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax)

    ratio = np.where(h_mc_norm > 0, h_data_norm / h_mc_norm, np.nan)
    ratio_err = np.where(h_mc_norm > 0, h_data_err / h_mc_norm, np.nan)
    ax_ratio.errorbar(bin_centers, ratio, yerr=ratio_err, fmt="ko", markersize=4)
    ax_ratio.axhline(1.0, color="royalblue", linewidth=1)
    ax_ratio.set_ylim(0.5, 1.5)
    ax_ratio.set_ylabel("Data/MC", fontsize=12)
    ax_ratio.set_xlabel(r"Sphericity $S$", fontsize=14)

    plt.tight_layout()
    for ext in ["pdf", "png"]:
        fig.savefig(FIGURES_DIR / f"sphericity_data_mc.{ext}",
                    bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("  Saved: sphericity_data_mc.{pdf,png}")


def plot_year_consistency() -> None:
    """Plot year-by-year thrust distribution consistency."""
    log.info("\n=== Year-by-year tau consistency ===")

    bins = np.linspace(0, 0.5, 51)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    bin_widths = np.diff(bins)

    year_labels = {
        "1992": "1992",
        "1993": "1993",
        "1994P1": "1994 P1",
        "1994P2": "1994 P2",
        "1994P3": "1994 P3",
        "1995": "1995",
    }

    colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#a65628"]
    year_histos = {}

    for (year, path), color in zip(DATA_FILES.items(), colors):
        events = load_data_file(path, year)
        sel = apply_full_selection(events)
        tau = 1 - ak.to_numpy(sel["Thrust"])
        h, _ = np.histogram(tau, bins=bins)
        n = np.sum(h)
        h_norm = h / (n * bin_widths)
        year_histos[year] = (h_norm, np.sqrt(h) / (n * bin_widths))

    # Combined (reference)
    all_events = []
    for year, path in DATA_FILES.items():
        events = load_data_file(path, year)
        sel = apply_full_selection(events)
        all_events.append(1 - ak.to_numpy(sel["Thrust"]))
    tau_all = np.concatenate(all_events)
    h_all, _ = np.histogram(tau_all, bins=bins)
    n_all = np.sum(h_all)
    h_all_norm = h_all / (n_all * bin_widths)

    fig, (ax, ax_ratio) = plt.subplots(
        2, 1, figsize=(10, 10),
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=True
    )

    for (year, (h_norm, h_err)), color in zip(year_histos.items(), colors):
        ax.step(bins[:-1], h_norm, where="post",
                color=color, linewidth=1.2, label=year_labels[year])

    ax.step(bins[:-1], h_all_norm, where="post",
            color="black", linewidth=2.0, label="Combined", linestyle="--")
    ax.set_ylabel(r"$(1/N)\,dN/d\tau$", fontsize=14)
    ax.set_yscale("log")
    ax.legend(fontsize="x-small", ncol=2)
    mh.label.exp_label(exp="ALEPH", data=True,
                       rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax)

    # Ratio: each year / combined
    for (year, (h_norm, h_err)), color in zip(year_histos.items(), colors):
        ratio = np.where(h_all_norm > 0, h_norm / h_all_norm, np.nan)
        ax_ratio.step(bins[:-1], ratio, where="post",
                      color=color, linewidth=1.2, label=year_labels[year])

    ax_ratio.axhline(1.0, color="black", linewidth=1.5, linestyle="--")
    ax_ratio.set_ylim(0.85, 1.15)
    ax_ratio.set_ylabel("Year/Combined", fontsize=12)
    ax_ratio.set_xlabel(r"$\tau = 1 - T$", fontsize=14)

    plt.tight_layout()
    for ext in ["pdf", "png"]:
        fig.savefig(FIGURES_DIR / f"tau_year_consistency.{ext}",
                    bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("  Saved: tau_year_consistency.{pdf,png}")

    # Report chi2-like comparison for each year vs. combined
    log.info("\n  Year-vs-combined agreement (in tau 0-0.5):")
    for year, (h_norm, h_err) in year_histos.items():
        mask = h_all_norm > 0
        pull = (h_norm[mask] - h_all_norm[mask]) / np.sqrt(h_err[mask]**2 + 1e-20)
        rms_pull = np.sqrt(np.mean(pull**2))
        log.info(f"    {year}: RMS pull = {rms_pull:.2f}")


def main():
    log.info("=== Phase 2 Script 03: Key Distributions ===")

    compute_cutflow_full()
    plot_tau_distribution()
    plot_track_multiplicity()
    plot_momentum_distribution()
    plot_sphericity()
    plot_year_consistency()

    log.info("\n=== Done. All figures in: %s ===", FIGURES_DIR)


if __name__ == "__main__":
    main()
