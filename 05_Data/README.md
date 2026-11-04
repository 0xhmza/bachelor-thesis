# Data

```
raw/        Untouched, exactly as collected. Read-only. NOT in version control.
processed/  Cleaned and structured data produced by scripts from raw/.
analysis/   Scripts, notebooks, and outputs (tables, figures).
```

## Rules

- **`raw/` is append-only.** Never edit a file in it. Every transformation is a
  script in `analysis/` that reads from `raw/` and writes to `processed/`.
- **`raw/` is gitignored.** Scraped store content and any participant data stay
  off the repository. Back it up separately.
- **Figures for the thesis** are written to `../03_Thesis/figures/` by the scripts
  that generate them, so they are never out of date by hand.
- **Note the collection date** in a sidecar file for every batch you collect.
