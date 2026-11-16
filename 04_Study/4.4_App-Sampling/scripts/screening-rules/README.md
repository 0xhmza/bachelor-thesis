# Screening rules

Codes each decision of `04_Study/4.4_App-Sampling/screening.csv` with the eligibility rule of
Methodology Table 4.2 (I1–I7, X1–X8), from the reason logged at screening (Decision D3). No
decision changes; the script stops on a reason it has no rule for.

## v001

```powershell
python 04_Study/4.4_App-Sampling/scripts/screening-rules/v001/recode.py 04_Study/4.4_App-Sampling/screening.csv
```
