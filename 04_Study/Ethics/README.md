# Ethics

## Does this study need a review?

Two parts of the project have different answers, and the answer depends on which
scope is finally agreed (see the open question in
`00_Admin/Meeting-Notes/2026-09-04_Proposal-Meeting.md`, §8):

| Part | Human subjects? | Likely needs review |
|---|---|---|
| App-store / policy document analysis | No — public material | Usually not, but confirm |
| Manual app walkthroughs | No, if you use your own throwaway accounts | Usually not |
| Scenario-based user survey | **Yes** | **Yes — apply early** |

**Action:** ask the advisor and the RUB/MPI-SP ethics contact in writing, and put
the answer in this folder. Do it before recruiting anyone. An ethics application
can take weeks; it is the single most common reason a thesis timeline slips.

## Files to keep here

- `application.pdf` — the submitted application
- `approval.pdf` — the decision
- `information_sheet.md` — what participants are told
- `consent_form.md` — what participants agree to
- `data_protection_note.md` — GDPR information for participants

## Practical rules regardless of review

- Use throwaway accounts and synthetic data for walkthroughs. Never enter your
  real name, address, health data, or payment details into a studied app.
- Do not create accounts that require real identity verification.
- Store any participant data pseudonymised, in `05_Data/raw/`, which is gitignored.
- Check each store's terms before automated collection; prefer manual or
  officially permitted access over scraping that violates the terms.
