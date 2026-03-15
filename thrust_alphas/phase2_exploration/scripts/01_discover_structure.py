"""
Script 01: Discover ROOT file structure.
Prints tree names, branch names, types, and event counts
for one data file and one MC file.
"""
import logging
import sys
from pathlib import Path

import uproot
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger("discover")
console = Console()

DATA_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPH")
MC_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC")

DATA_FILES = sorted(DATA_DIR.glob("*.root"))
MC_FILES = sorted(MC_DIR.glob("*.root"))


def describe_file(path: Path, label: str) -> None:
    log.info(f"Opening {label}: {path.name}")
    with uproot.open(path) as f:
        # List all top-level keys
        keys = f.keys(cycle=False)
        log.info(f"  Top-level keys: {keys}")

        for key in keys:
            obj = f[key]
            obj_type = type(obj).__name__
            log.info(f"  Key '{key}': type={obj_type}")

            if hasattr(obj, "keys"):
                # It's a tree or something iterable
                try:
                    branches = obj.keys()
                    log.info(f"    Branches ({len(branches)}):")
                    table = Table(title=f"{key} branches")
                    table.add_column("Branch", style="cyan")
                    table.add_column("Type", style="green")
                    table.add_column("Interpretation", style="yellow")
                    for b in branches:
                        try:
                            branch = obj[b]
                            dtype = str(branch.dtype) if hasattr(branch, "dtype") else "N/A"
                            interp = str(branch.interpretation) if hasattr(branch, "interpretation") else "N/A"
                            table.add_row(b, dtype, interp[:80])
                        except Exception as e:
                            table.add_row(b, "ERROR", str(e)[:80])
                    console.print(table)
                except Exception as e:
                    log.warning(f"    Could not enumerate branches: {e}")

                if hasattr(obj, "num_entries"):
                    log.info(f"    Entries: {obj.num_entries:,}")


def count_all_files() -> None:
    """Count events in all data and MC files."""
    log.info("\n=== Event counts for all DATA files ===")
    total_data = 0
    data_counts = {}
    for f in DATA_FILES:
        with uproot.open(f) as root:
            keys = root.keys(cycle=False)
            for k in keys:
                obj = root[k]
                if hasattr(obj, "num_entries"):
                    n = obj.num_entries
                    data_counts[f.name] = n
                    total_data += n
                    log.info(f"  {f.name}: {n:,} events")
                    break

    log.info(f"  TOTAL DATA: {total_data:,} events")

    log.info("\n=== Event counts for all MC files ===")
    total_mc = 0
    for f in sorted(MC_FILES):
        with uproot.open(f) as root:
            keys = root.keys(cycle=False)
            for k in keys:
                obj = root[k]
                if hasattr(obj, "num_entries"):
                    n = obj.num_entries
                    total_mc += n
                    log.info(f"  {f.name}: {n:,} events")
                    break
    log.info(f"  TOTAL MC: {total_mc:,} events")


def main() -> None:
    log.info("=== Phase 2 Step 1: File Structure Discovery ===")

    # Describe first data file
    if DATA_FILES:
        describe_file(DATA_FILES[0], "DATA")
    else:
        log.error("No data files found!")

    # Describe first MC file
    if MC_FILES:
        describe_file(MC_FILES[0], "MC")
    else:
        log.error("No MC files found!")

    # Count all files
    count_all_files()


if __name__ == "__main__":
    main()
