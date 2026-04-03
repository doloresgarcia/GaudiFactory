## 7. Tools and Paradigms

### 7.1 Core Tools

| Capability | Tool | Notes |
|-----------|------|-------|
| C++ framework | Gaudi / k4FWCore | See `conventions/gaudi_algorithm.md` |
| Event data model | EDM4hep | Header: `edm4hep/<Type>Collection.h` |
| Persistent I/O | PODIO + IOSvc | Configured in Python steering file |
| ROOT histograms | ROOT TH1/TH2 via `ITHistSvc` | Only for `Gaudi::Algorithm` pattern |
| Algorithm runner | `k4run` or `gaudirun.py` | `k4run options/myAlg.py` |
| Build system | CMake + Ninja | `cmake -G Ninja .. && ninja install` |
| Environment | Key4hep cvmfs stack | `source /cvmfs/sw.hsf.org/key4hep/setup.sh` |
| Plot reading | `uproot` | Read ROOT output files for validation plots |
| Plotting | `matplotlib` + `mplhep` | For diagnostic figures in Phase 4 |
| Logging (Python) | `logging` + `rich` | No bare `print()` |

### 7.2 Environment Setup

Always source the Key4hep environment before building or running:

```bash
source /cvmfs/sw.hsf.org/key4hep/setup.sh
```

This provides: `Gaudi`, `k4FWCore`, `EDM4hep`, `PODIO`, `ROOT`, `k4run`.

If cvmfs is not available, a local Key4hep install or Docker image provides
the same stack. See https://key4hep.github.io/key4hep-doc/ for alternatives.

### 7.3 Paradigms

- **Read the conventions first.** `conventions/gaudi_algorithm.md` has the
  authoritative pattern for every algorithm type. Do not invent alternatives.
- **Compile early.** After writing the skeleton (header + DECLARE_COMPONENT),
  attempt a build before filling in logic. Catch structural errors early.
- **One algorithm per file.** Each `.h`/`.cpp` pair contains exactly one
  algorithm class.
- **Properties for everything user-configurable.** Collection names,
  thresholds, flags — all as `Gaudi::Property<T>`. Hard-coded values that
  should be configurable are Category B at review.
- **Plots are evidence.** Every claim about algorithm behavior has a figure
  or table in `VALIDATION.md`.
- **Pin tool versions.** Record the Key4hep stack version used in `BUILD_RUN.md`
  (`echo $KEY4HEP_STACK` or `cat $KEY4HEP_STACK`).

### 7.4 Reading Output Files (Phase 4)

To read a ROOT file produced by the algorithm:

```python
import uproot
import matplotlib.pyplot as plt
import mplhep as mh

mh.style.use("CMS")

with uproot.open("output.root") as f:
    print(f.keys())           # explore contents
    hist = f["energy"]        # TH1 histogram
    values, edges = hist.to_numpy()

fig, ax = plt.subplots(figsize=(8, 6))
ax.stairs(values, edges, fill=True)
ax.set_xlabel("Energy [GeV]")
ax.set_ylabel("Entries")
fig.savefig("outputs/figures/energy.png", bbox_inches="tight", dpi=150)
plt.close()
```

For EDM4hep collections written via `IOSvc`, use podio's Python bindings
or `uproot` with the PODIO ROOT layout.
