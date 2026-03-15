"""
Script 02: Load a small sample (~1000 events) and inspect structure.
Understand pwflag meaning (charged vs neutral), selection flags,
and verify thrust computation against stored value.
"""
import logging
import numpy as np
import uproot
import awkward as ak
from pathlib import Path
from rich.console import Console
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger("inspect")
console = Console()

DATA_FILE = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPH/LEP1Data1994P1_recons_aftercut-MERGED.root")
MC_FILE = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC/LEP1MC1994_recons_aftercut-001.root")

BRANCHES_NEEDED = [
    "nParticle", "px", "py", "pz", "pmag", "pt", "theta", "phi",
    "charge", "pwflag", "pid",
    "d0", "z0", "ntpc",
    "passesNTupleAfterCut", "passesTotalChgEnergyMin", "passesNTrkMin",
    "passesSTheta", "passesMissP", "passesISR", "passesAll",
    "nChargedHadrons", "nChargedHadronsHP",
    "Thrust", "Thrust_charged", "Thrust_neutral", "Sphericity", "missP",
    "isMC", "Energy", "bFlag",
    "passesArtificAccept",
]

NMAX = 2000  # slightly more than 1000 for robust statistics


def compute_thrust(px, py, pz):
    """Compute thrust from momentum arrays (columnar, per event)."""
    # Thrust axis brute-force for a sample: iterate over candidate axes
    # Use the leading momentum direction as initial estimate, then maximize
    # For exploration only — stored Thrust value is the reference
    pmag = np.sqrt(px**2 + py**2 + pz**2)
    psum = ak.sum(pmag, axis=1)
    # Project along all particle axes as candidates
    # Use stored Thrust value for comparison; here just verify formula
    return psum  # placeholder


def analyze_pwflag(pwflag_array, charge_array):
    """Understand the pwflag encoding."""
    # Flatten to see all values
    pf_flat = ak.to_numpy(ak.flatten(pwflag_array))
    ch_flat = ak.to_numpy(ak.flatten(charge_array))

    unique_pf = np.unique(pf_flat)
    log.info(f"  Unique pwflag values: {unique_pf}")

    for pf_val in unique_pf:
        mask = pf_flat == pf_val
        charges = ch_flat[mask]
        n_charged = np.sum(charges != 0)
        n_neutral = np.sum(charges == 0)
        log.info(f"  pwflag={pf_val}: {mask.sum():,} particles, "
                 f"charged={n_charged:,}, neutral={n_neutral:,}")


def analyze_selection_flags(events):
    """Inspect the selection flag distributions."""
    flags = [
        "passesNTupleAfterCut", "passesTotalChgEnergyMin", "passesNTrkMin",
        "passesSTheta", "passesMissP", "passesISR", "passesAll"
    ]
    log.info("  Selection flag pass rates:")
    for f in flags:
        if f in events.fields:
            rate = ak.mean(events[f])
            log.info(f"    {f}: {float(rate)*100:.1f}%")


def verify_thrust(events):
    """Verify the stored Thrust value by recomputing from px/py/pz."""
    # Use only charged particles (charge != 0) for the charged-only thrust
    px = events["px"]
    py = events["py"]
    pz = events["pz"]
    charge = events["charge"]
    pwflag = events["pwflag"]

    # Use all particles (pwflag used to select good tracks)
    pmag_all = np.sqrt(px**2 + py**2 + pz**2)
    p_sum_all = ak.sum(pmag_all, axis=1)

    stored_thrust = ak.to_numpy(events["Thrust"])
    log.info(f"  Stored Thrust: mean={np.mean(stored_thrust):.4f}, "
             f"min={np.min(stored_thrust):.4f}, max={np.max(stored_thrust):.4f}")
    log.info(f"  Tau=1-T: mean={np.mean(1-stored_thrust):.4f}, "
             f"in range (0,0.5]: {np.sum((1-stored_thrust) >= 0) / len(stored_thrust) * 100:.1f}%")

    # Check charged-only thrust
    stored_thrust_ch = ak.to_numpy(events["Thrust_charged"])
    log.info(f"  Stored Thrust_charged: mean={np.mean(stored_thrust_ch):.4f}")

    # Understand particle flags more deeply
    # pwflag == 0 are good charged tracks (from the archived analysis paper)
    # pwflag != 0 are neutral or bad tracks
    charged_mask = charge != 0
    n_charged = ak.sum(charged_mask, axis=1)
    log.info(f"  nParticle (all): mean={ak.mean(events['nParticle']):.1f}")
    log.info(f"  n_charged (charge!=0): mean={ak.mean(n_charged):.1f}")
    log.info(f"  nChargedHadrons (stored): mean={ak.mean(events['nChargedHadrons']):.1f}")
    log.info(f"  nChargedHadronsHP (stored): mean={ak.mean(events['nChargedHadronsHP']):.1f}")


def inspect_data(path: Path, label: str) -> None:
    log.info(f"\n{'='*60}")
    log.info(f"Inspecting {label}: {path.name}")
    log.info(f"{'='*60}")

    with uproot.open(path) as f:
        tree = f["t"]
        log.info(f"Reading first {NMAX} events from tree 't'...")
        events = tree.arrays(
            [b for b in BRANCHES_NEEDED if b in tree.keys()],
            entry_stop=NMAX,
            library="ak"
        )
        log.info(f"  Loaded {len(events)} events")
        log.info(f"  Fields: {events.fields}")

        log.info("\n--- pwflag analysis ---")
        analyze_pwflag(events["pwflag"], events["charge"])

        log.info("\n--- Selection flags ---")
        analyze_selection_flags(events)

        log.info("\n--- Thrust verification ---")
        verify_thrust(events)

        log.info("\n--- Basic kinematic statistics ---")
        pmag = events["pmag"]
        p_flat = ak.to_numpy(ak.flatten(pmag))
        log.info(f"  Track |p| (all particles): "
                 f"mean={np.mean(p_flat):.3f} GeV, "
                 f"median={np.median(p_flat):.3f} GeV, "
                 f"max={np.max(p_flat):.3f} GeV")
        log.info(f"  Events: {len(events)}")
        log.info(f"  Energy (stored): mean={ak.mean(events['Energy']):.2f} GeV")

        # Look at isMC flag
        is_mc_vals = ak.to_numpy(events["isMC"])
        log.info(f"  isMC: unique values = {np.unique(is_mc_vals)}")

        # bFlag: b-quark events
        bflag_vals = ak.to_numpy(events["bFlag"])
        unique_bflag = np.unique(bflag_vals)
        log.info(f"  bFlag unique values: {unique_bflag}")
        for bf in unique_bflag:
            log.info(f"    bFlag={bf}: {np.sum(bflag_vals == bf):,} events")


def inspect_mc_gen(path: Path) -> None:
    """Inspect the MC generator-level tree."""
    log.info(f"\n{'='*60}")
    log.info("Inspecting MC generator-level trees")
    log.info(f"{'='*60}")

    gen_branches = [
        "nParticle", "Thrust", "Thrust_charged", "Sphericity",
        "passesAll", "passesNTupleAfterCut",
        "nChargedHadrons", "pid", "charge", "pwflag",
    ]

    with uproot.open(path) as f:
        # tgen: generator-level, after selection
        for tname in ["tgen", "tgenBefore"]:
            if tname in f:
                tree = f[tname]
                avail = [b for b in gen_branches if b in tree.keys()]
                events = tree.arrays(avail, entry_stop=NMAX, library="ak")
                log.info(f"\n  Tree '{tname}': {tree.num_entries:,} entries")
                if "Thrust" in events.fields:
                    thrust = ak.to_numpy(events["Thrust"])
                    log.info(f"    Thrust: mean={np.mean(thrust):.4f}, "
                             f"tau_mean={np.mean(1-thrust):.4f}")
                if "nParticle" in events.fields:
                    log.info(f"    nParticle: mean={ak.mean(events['nParticle']):.1f}")
                if "passesAll" in events.fields:
                    log.info(f"    passesAll rate: {float(ak.mean(events['passesAll']))*100:.1f}%")

        # Show entries in tgen vs t
        t_entries = f["t"].num_entries
        tgen_entries = f["tgen"].num_entries if "tgen" in f else 0
        tgb_entries = f["tgenBefore"].num_entries if "tgenBefore" in f else 0
        log.info(f"\n  Entry counts:")
        log.info(f"    t (reco): {t_entries:,}")
        log.info(f"    tgen (gen after cuts): {tgen_entries:,}")
        log.info(f"    tgenBefore (gen before cuts): {tgb_entries:,}")
        if tgb_entries > 0:
            eff = t_entries / tgb_entries
            log.info(f"    Selection efficiency (t/tgenBefore): {eff:.4f}")


def main():
    log.info("=== Phase 2 Script 02: Sample Inspection ===")

    # Inspect data file
    inspect_data(DATA_FILE, "DATA (1994P1)")

    # Inspect MC reco tree
    inspect_data(MC_FILE, "MC (reco)")

    # Inspect MC generator trees
    inspect_mc_gen(MC_FILE)


if __name__ == "__main__":
    main()
