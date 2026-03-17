## Analysis Note Specification

The AN is a single evolving document across Phases 4b, 4c, and 5. Phase 4b
writes the complete AN with 10% results. Phase 4c updates numbers. Phase 5
polishes and renders. Structure is written in 4b; later phases update results.

The AN is the complete record — not a journal paper. Every detail needed to
reproduce the analysis from scratch must be present. ~50-100 rendered pages
for a typical measurement. **Under 30 pages means detail is missing** —
this is a Category A finding at Phase 5 review. Common causes of thin ANs:
missing per-cut distribution plots, missing per-systematic impact figures,
missing cross-check result plots, summary tables without supporting figures.
The rule of thumb: every selection cut needs a before/after distribution
plot, every systematic needs an impact figure, every cross-check needs a
comparison plot.

---

### Required sections

1. **Introduction** — motivation, observable definition, prior measurements
2. **Data samples** — experiment, √s, luminosity, MC generators, event counts
3. **Event selection** — every cut with motivation, distribution plot,
   efficiency (per-cut and cumulative)
4. **Corrections / unfolding** (measurements) — full procedure, closure/stress
   tests, response matrix, regularization
5. **Systematic uncertainties** — one subsection per source: what, how
   evaluated, impact (table + figure), correlation info. Summary table.
6. **Cross-checks** — each as a subsection within the section it validates
   (not a standalone section). Comparison plots, chi2/p-value, interpretation.
   Large cross-checks → appendix with forward reference.
7. **Statistical method** — likelihood, fit validation, GoF
8. **Results** — full uncertainties, per-bin tables, summary figures
9. **Comparison to prior results and theory** — quantitative (chi2 with full
   covariance). "Qualitative consistency" insufficient when data exist.
10. **Conclusions** — result, precision, dominant limitations
11. **Future directions** — concrete roadmap (§12)
12. **Appendices** — per-bin systematic tables, covariance matrices (as
    tables), extended cutflow, auxiliary plots. Appendices are where the
    bulk of detail lives.

---

### Requirements

- Self-contained: all results inline, publication-quality figures
- **Machine-readable results** in `results/` (CSV/JSON for spectra,
  covariance matrices)
- **Completeness test:** a physicist unfamiliar with the analysis should
  reproduce every number from the AN alone
- **BibTeX:** `[@key]` with `references.bib`. Entries must include `doi`,
  `url`, `eprint`. Use `unsrt`-style. Use `get_paper` for RAG papers.

---

### LaTeX compilation

Markdown → PDF via **pandoc** (≥3.0) + tectonic (or xelatex). The
`build-pdf` pixi task runs pandoc with
`--number-sections --toc --filter pandoc-crossref --citeproc`, default
figure width `0.45\linewidth`. Do not use an LLM for conversion.

### Table formatting

Pipe tables in markdown become `longtable` in LaTeX. To avoid overflow:

- **Keep columns narrow.** Use abbreviations, symbols, and short headers.
  Move long descriptions to footnotes or prose.
- **Avoid monospace text in tables.** File paths, code identifiers, and
  other long monospace strings will overflow. Use short labels and
  reference a lookup table in an appendix if needed.
- **Split wide tables.** If a table exceeds 6 columns, split into two
  tables or rotate content (rows ↔ columns).
- **Numeric precision.** Use consistent significant figures: 2-3 digits
  for uncertainties, match precision for central values. Don't typeset
  `91.17930000` when `91.179` suffices.
- **Test with `build-pdf`.** Overfull hbox warnings in the TeX log indicate
  table overflow. Fix before submitting for review.

---
