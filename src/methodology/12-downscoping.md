## 12. Scope Management and Downscoping

Downscoping is a last resort when the full implementation is genuinely
infeasible — not merely difficult. Every downscope weakens the result and
must be documented.

### When to downscope

Justified only when the stronger approach has been **attempted and failed**
or is **demonstrably infeasible**:

- Required EDM4hep type genuinely does not exist in the available stack
- Required Gaudi service unavailable in the current environment
- Algorithm requires dependencies not in the Key4hep stack (and cannot be added)
- Build system constraint prevents implementation of a specific pattern

"It would be harder" or "it might not compile" are not justifications.
Try first, document failure, then downscope.

### How

1. **Attempt the full approach first.** Document the attempt and specific
   failure reason in `experiment_log.md`.
2. **Choose best achievable alternative.** Examples:
   - Functional pattern not compiling → fall back to `Gaudi::Algorithm`
     (document why functional failed)
   - EDM4hep type missing → use the nearest available type with a comment
   - `ITHistSvc` unavailable → write histogram data to a text file instead
3. **Label the downscope** in the artifact: `[D] <original approach>:
   downscoped to <alternative> because <specific reason>`.
4. **Evaluate impact.** Is the downscoped version still useful? If the
   fallback fundamentally cannot meet the prompt requirements, escalate to
   the user rather than silently delivering something different.

### What is NOT a downscope

- Choosing `Gaudi::Algorithm` when the design determined it was the right
  pattern → correct implementation, not a downscope
- Simplifying a steering file that was over-engineered → correct
- Removing a property that was redundant → correct

Downscoping is specifically when the original design intent cannot be met
and you fall back to a weaker alternative.
