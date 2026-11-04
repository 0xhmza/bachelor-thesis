# D7 — Which language version of a source is captured and coded?

- **Status:** confirmed (2026-10-13, supervisor meeting; adopted by the author 2026-10-23). The methodology states this choice.
- **Affects:** Methodology, Material and Language; [sampling protocol](../../04_Study/App-Sample/sampling_protocol.md); LLM prompts (D9); validation stratified by language
- **Options considered:**
  1. Proposal: German first, English when German is unavailable.
  2. **English first, German when no English version is available (chosen).**
  3. Capture both versions and code the German one (suggested in the [action plan](../Action-Plan_2026-10-13.md), §8).
- **Evidence:**
  - Supervisor meeting of 13 October: "we stick in English. English mainly else german as fallback" ([raw notes](../Meeting-Notes/2026-10-13_Supervisor-Meeting_Raw.md)); the organized notes ask to specify which materials the rule covers and when the fallback is used ([organized notes](../Meeting-Notes/2026-10-13_Supervisor-Meeting_Organized.md)).
  - The same meeting keeps the German market and asks for German and English search keywords. The language rule therefore concerns the captured text, not the search.
  - Counter-evidence: in the MAPP corpus, 14 of 59 apps acknowledged the GDPR only in their German policy, and 13 English–German policy pairs differed substantially (Arora et al. 2022, via the [gap search](../../01_Literature/Literature-Gap-Search_2026-10-23.md), §2).
- **Choice:** English text is primary for every captured source, including interface text; German is used when no English version is available. Where both versions exist, both are captured and their differences logged. Language is recorded per source, and the original wording is coded. Search keywords combine German and English terms, and the storefronts remain German.
- **Reason:** The supervisor set the rule. Capturing both versions where they exist keeps German-only content, such as the differences Arora et al. found, visible in the difference log instead of losing it.
- **Would change if:** the difference log shows that German versions often carry harm or protection content that the English version lacks; the supervisor revises the rule.

## Note 2026-11-04 — rule kept, justification stated

- The author kept English first (chat, 2026-11-04) after the methodology review raised German-market validity (M2). The methodology now states the cost (German users may meet German text; Arora et al. 2022, LREC, 59 semi-parallel pairs differ), keeps the difference log, and applies the existing "would change if": where the pilot shows German-only harm or protection content, the German version of that source is coded as well. A language limitation is added to the methodology.

## Note 2026-11-04 (evening) — audience check and log rule

- English first among the versions that apply to users in Germany (an English policy for another jurisdiction is not the English version; Arora et al. 2022; Linden et al. 2020). The capture record states product, territorial scope and regional sections. The difference log has a fixed record (pair, versions, matched state, spans, changed node or scope, materiality judgement) and reports compared/unavailable/material counts; any material difference, in the pilot or later, triggers coding of the German version and a recheck. The log documents observed differences; it does not measure every effect of the rule.
