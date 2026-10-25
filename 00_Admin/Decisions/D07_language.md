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
