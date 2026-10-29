# Germany download sampling - instance 2

Open `sampling_report.tex` for the complete report and reproduction procedure.
It is a standalone LaTeX document: references, all 19 keywords, data schemas,
commands, current evidence, and the full executable Python source are embedded.

**Status: incomplete final sampling.** There is no validated German download
dataset for both stores, no completed Play keyword-search frame, and no final
sample. The first trial's provisional 50 apps were not relabelled as final.

A fresh German Apple Search API collection was executed. Samsung Health was
checked directly in both stores as a user-requested coverage audit. Its absence
from keyword results and its presence in the catalog are separate observations.
The report documents the difference and the source access limit.

The proposed common download period is 1 October 2025 through 30 September 2026,
the last twelve complete calendar months before this collection. This is a
declared methodological choice, not a claim that those download data were obtained.

## Files

- `sampling_report.tex`: complete methods and execution report.
- `sampling.py`: executable copy of the source embedded in the LaTeX appendix.
- `raw/20261011T161853545650Z/`: original HTTP responses and SHA-256 sidecars.
- `processed/20261011T161853545650Z/`: fresh metadata and blank German-download input template.
- `evidence/`: transcribed public access observations and validation results.
- `build_document.py`: generates the standalone LaTeX report from this capture.

Raw responses are append-only and Git-ignored; back up the whole directory.
The unchanged proposal and the first sampling instance are separate artifacts.
No account was created and no purchase was made.

Run commands and input-file definitions are fully documented inside the LaTeX
document. A final download ranking can be generated only after comparable
German figures, complete discovery, identity checks and eligibility evidence
have been supplied. Missing iOS counts are never substituted with zero.
