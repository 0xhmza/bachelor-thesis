# D12 — What is the harm tree built on (the supervisor's "best app")?

- **Status:** proposed (2026-11-01, author's instruction in chat). The supervisor has not confirmed that this reading matches the phrase "best app".
- **Affects:** RQ1, RQ3 · [`reference_model_v1.yaml`](../../04_Study/Reference-Model/reference_model_v1.yaml) · codebook v5 · Methodology, Reference Model and Reference Harm Trees
- **Author's instruction:** first make a model of a generic health app that has all the capabilities a health app can have, then apply that tree to apps on the basis of their privacy policy and the cognitive walkthrough.
- **Options considered:**
  1. Pick one real app as "best" (most popular, most complete policy). Needs a criterion for "best", and misses functions that app lacks.
  2. Build trees per app category. Rejected by [D15](D15_health-tracker-domain.md): categories do not select separate reference trees.
  3. **Build one generic health tracker that holds every function a tracker can have; a real app is a subset of it (chosen).**
- **Evidence:**
  - Knabenhans et al. 2026, §4 (p. 6): harms cannot be judged from the abstract functionality alone; §3–4 model one ideal functionality that covers many applications, then study concrete use cases. §4.2, Fig. 5: common sub-trees are reused across harms. §4.3 (p. 8): trees apply verbatim to another use case where the pathways match.
  - De & Le Métayer 2017, *A Refinement Approach for the Reuse of Privacy Risk Analysis Results*, doi:10.1007/978-3-319-67280-9_4: a generic analysis based on the system specification yields generic harm trees, which are then refined. **Only a search-engine summary of the opening of the method was seen; the paper's full text was not reachable (HAL bot protection, CORE 403). The author must read it before the thesis relies on it.**
  - Deng et al. 2011, Sec. 2 (p. 2): a system is modelled as data flows, stores, processes and external entities before threats are elicited. Iwaya et al. 2023, Sec. 2.3 (p. 6): LINDDUN used on mental-health apps.
  - Meeting 2026-10-13, §6: identify capabilities through the literature review and synthesise a harm tree.
- **Choice:** one reference model. A function enters it if the review evidence or a cited source documents it for health trackers. Components are stated as features that can be checked on a real app. Capabilities K1–K8 keep the numbers of the review's capability table; K3 is excluded (connected device). K9, K10 and I1–I3 are added, each with a source. Every pathway states whether its link is documented or argued. No completeness is claimed (Knabenhans et al. §4.1, p. 7).
- **Reason:** A generic model needs no criterion for "best", treats all 50 apps alike, and turns "does this harm apply?" into a checkable question about features. A superset errs towards listing a pathway that an app lacks, which the applicability record then closes; a single real app would err towards missing harms silently.
- **Would change if:** the supervisor meant a specific app; the pilot shows components that cannot be checked from the available material; De & Le Métayer 2017, once read, contradicts this use.

## Update 2026-11-04 — independent check of the trees

- **Status:** proposed (2026-11-04, methodology review M5).
- **Choice:** before the instrument freeze, the D8 second coder checks every pathway against its cited source; objections and resolutions are logged. Reason: "missing harm" is measured against a model built by the author, so the yardstick needs a check by someone else.

## Update 2026-11-04 (evening) — OR+, actor access, coverage matching, wording

- **Status:** proposed (submission review R3, R4; privacy card W1–W5).
- **Choice:** (1) OR+ is not evaluated as OR; each OR+ is rewritten as an OR of explicitly sufficient AND-combinations (attack-tree set semantics, Mauw & Oostdijk 2005); unsupported combinations stay uncertain. Each combination names the actor and the access component. (2) Proposed rewrite of K10 for v2, to be argued from sources and checked by the second person: OR( AND(CO2, IM2) provider holds derived scores; AND(IM4, CX3) advertising partner receives identifiers or events; IM7 tracked data drives offers ). (3) IM12 defined by the absence of any usable route (in app or by request), deletion and export judged separately. (4) A named harm credits a pathway only if consequence and data/actor/access match (contextual-integrity parameters, Shvartzshnaider et al. 2019); otherwise a category-level mention. (5) Denials count as mentions with negative polarity (PolicyLint, Andow et al. 2019). (6) "Every function a tracker can have" replaced by "functions the included evidence documents". (7) De 2017 anchored to §§3, 4.6, 5.4 of the HAL author manuscript.
- **Needs:** reference model v2, re-run of the evaluator and the instrument test.
