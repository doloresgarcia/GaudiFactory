# Gaudi Algorithm Conventions

This directory contains accumulated knowledge about Gaudi/k4FWCore algorithm
development. These are **not** part of the methodology specification — the spec
describes process (phases, reviews, gates), while conventions encode what
experienced developers know about writing correct, idiomatic algorithms.

## Structure

| File | Contents |
|------|----------|
| `gaudi_algorithm.md` | Pattern selection, property declarations, data handles, CMake, steering files, EDM4hep types |

## Maintenance

- **Living documents.** Updated after each algorithm generation that
  encounters a new pattern or pitfall.
- **Empirically grounded.** Entries come from actual build/run experience
  and the k4-project-template reference implementation.
- **Consulted at Phases 1 and 2** (design and implementation).

## Adding new conventions

When an algorithm generation session discovers a new pattern not covered
by `gaudi_algorithm.md`:
1. Note it in `experiment_log.md` during the session.
2. After the phase completes, add it to the appropriate section of
   `gaudi_algorithm.md` with a concrete code example.
3. Patterns that apply to a specific EDM4hep type or service go in
   `appendix-heuristics.md` in the methodology directory.
