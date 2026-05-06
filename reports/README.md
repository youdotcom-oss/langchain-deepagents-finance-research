# Reports

This directory contains outputs from local agent runs.

Each run creates a timestamped subdirectory (`YYYYMMDD_HHMMSS/`) with:

- `research_request.md` — The user's original research question
- `workpapers/` — Intermediate outputs from each subagent
  - `landscape_scan.md` — GDP, inflation, current account data tables for all countries
  - `anomaly_analysis.md` — Statistical analysis, flagged outliers, investigation targets (includes a fenced JSON block)
  - `expenditure_decomposition.md` — Expenditure-side GDP contributions (C, I, G, NX)
  - `sector_decomposition.md` — Sector GVA growth by NACE section
  - `country_<name>.md` — Per-country qualitative deep dives (one per anomalous country)
- `final_report.md` — The synthesized final report with unified citations

These files are generated automatically by the agent's `FilesystemBackend` when running locally via `examples/eu_gdp_analysis.py` or the programmatic API.
