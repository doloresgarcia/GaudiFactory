---
name: tool_preferences_reminder
description: Remind user to fill in Section 7 tool preferences (jet clustering, b-tagging, etc.) before running the full analysis
type: project
---

User needs to fill in Section 7.1 tool preferences in spec/methodology.md before running the analysis pipeline. Specifically: jet clustering algorithm, b-tagging approach, and any other experiment-specific tools. User has indicated they can synthesize this list.

**Why:** The spec has placeholder blanks for jet clustering and b-tagging that would cause agents to guess (possibly wrong, as the JADE/Durham test showed).

**How to apply:** Remind user before any attempt to run the full pipeline or Phase 1 for real.
