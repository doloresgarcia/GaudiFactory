# Phase 4: Validation & Plots

> Read `methodology/03-phases.md` → "Phase 4" for full requirements.

**Goal:** Verify the algorithm produces correct, meaningful output and
generate diagnostic plots.

**Prerequisite:** Phase 3 must have PASS status for both build and run.

## Validation steps

### 1. Run on data

Run the steering file on suitable input:
- Real events if available (specify path in `IOSvc.Input`)
- Generated events from a Producer algorithm
- A minimal synthetic dataset if no other data is available

Increase `EvtMax` to a meaningful sample (≥ 1000 events for plots).

### 2. Inspect output

For each expected output, verify it exists and has sensible content:

| Output type | Check |
|-------------|-------|
| ROOT histogram | Non-empty, fill count > 0, range physically reasonable |
| Output collection | Exists in output file, size consistent with input |
| Log messages | Algorithm prints expected `info()` messages |
| Event counter | Matches `EvtMax` |

**An empty histogram is a bug, not a result.** Investigate and fix before
advancing.

### 3. Generate plots

For each ROOT histogram or output collection:
- Read the ROOT file with `uproot` (Python) or ROOT macros
- Plot with `matplotlib` + `mplhep`
- Every plot must have:
  - X-axis label with units
  - Y-axis label
  - Title or descriptive filename
  - Saved as PNG to `outputs/figures/`

Typical plots for common algorithm types:
- **Producer:** energy spectrum, pT spectrum, multiplicity per event
- **Consumer:** same as Producer inputs
- **Transformer:** before vs. after comparison, efficiency vs. cut value
- **Gaudi::Algorithm with histograms:** all booked histograms

### 4. Cross-check

Verify at least one numeric result against an expectation:
- Multiplicity per event consistent with `EvtMax` × expected rate
- Histogram mean / peak consistent with physics expectation
- Output collection size ≤ input collection size (for filters)
- Properties affect output as expected (vary one property, re-run, check effect)

## Artifact

Write `VALIDATION.md` to `phase4_validation/outputs/VALIDATION.md`:

```markdown
## Output Summary

| Output | Type | Fill count / Size | Status |
|--------|------|-------------------|--------|

## Cross-checks

| Check | Expected | Observed | Pass? |
|-------|----------|----------|-------|

## Figures

- `outputs/figures/energy_spectrum.png` — [description]
- `outputs/figures/multiplicity.png`    — [description]
```

Save all figures to `phase4_validation/outputs/figures/`.

## Self-check before review

- [ ] All expected outputs present and non-empty
- [ ] At least one numeric cross-check performed and documented
- [ ] Every plot has axis labels with units
- [ ] No empty figures
- [ ] Property effect verified (varied at least one property)

## Review

1-bot: critical reviewer + plot validator.
- Critical: checks cross-check values are physically reasonable, all
  outputs present and non-empty.
- Plot validator: checks axis labels, units, readability, no empty panels.
