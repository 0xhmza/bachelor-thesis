## Contract Paraphrase

D1 (methodology_rigor, mandatory, owned by methodology): The study design, the way data are collected and handled, the reporting of counts and any statistics, and the material that lets others repeat the work must reach the bar that peer review in this field expects. For a measurement study that builds a sample from app-store data, I read this as follows. The sampling frame, the inclusion and exclusion rules, the stopping points and the screening steps are stated explicitly. They are fixed before the data are seen, or any later change is disclosed and justified. Each stage reports its counts with denominators, the date of collection and the conditions of collection. Text plus appendix give enough detail that another researcher could rebuild the same selection or explain why their result differs.

D2 (domain_accuracy, mandatory, owned by domain): Claims must match current evidence in the domain, prior work must be represented correctly, and domain terms and results must be stated without factual error. From a methodology standpoint, this matters wherever a procedural choice is justified by citing earlier work. The cited work must actually support that procedure. I do not plan a score for this dimension.

D3 (argumentative_coherence, mandatory, owned by da, methodology eligible): The core thesis must be internally consistent, the evidence must support the claims, and no fallacy may undermine the central argument. From a methodology standpoint, conclusions must not go beyond what the design can show. Validation steps must be independent of the procedure they validate. Generalisations must stay within the population the sampling frame covers. Counts, rules and terms must stay the same across the methods, the results and the conclusions.

D4 (cross_disciplinary_relevance, high, owned by perspective): Framing, definitions and implications should be accessible to readers in adjacent fields, and interdisciplinary claims should be backed up. From a methodology standpoint, method terms and procedures should be defined so that readers outside the subfield can follow them and judge them. I do not plan a score for this dimension.

D5 (writing_and_structure, normal, owned by eic): The organisation of the manuscript, clear exposition, good figures and tables, and adherence to the conventions of the venue. From a methodology standpoint, the order of the method description and the design of its tables should make each step checkable. I do not plan a score for this dimension.

D6 (venue_fit_and_contribution, mandatory, owned by eic): The manuscript should fit the configured venue and make an original, significant contribution for its readers. From a methodology standpoint, a contribution counts only as far as the method behind it is sound. No venue binding is supplied, so I make no claim about venue fit, and I do not plan a score for this dimension.

## Scoring Plan

### D1: methodology_rigor
dimension_id: D1
what_to_look_for: A sampling frame and selection pipeline stated before the data are seen (stores, the full query set, result depth or other stopping rule, collection dates, locale and device conditions); a validity argument or check for any popularity proxy used to rank or filter apps; handling of non-deterministic store search (repeat runs, snapshots or a stated bound); screening rules with reliability evidence (a second coder, an agreement measure, or an explicit mitigation if one coder screens alone) and disclosure of any decisions carried over from one store's listings to another's; any concentration of one developer or publisher in the sample, reported and discussed; counts at every stage with denominators; and enough material (query lists, frozen raw collection, scripts, exclusion log) in the text and appendix to reproduce the selection.
what_triggers_block: A defect that keeps the selection from being reproduced or trusted as reported but can be fixed in a revision, such as a missing query list, depth cut-off or collection date, a popularity proxy used with no validity argument at all, a single coder screening with no reliability check or mitigation, decisions reused across stores without disclosure, or selection rules or stopping points changed after seeing the data without saying so.
what_triggers_warn: Choices that are disclosed but weakly justified, such as proxy validity argued only by assertion or citation without its own check, search non-determinism acknowledged but not measured, single-coder screening with only partial mitigation, developer concentration or other skew in the sample noted but not analysed, or small gaps in the stage counts that a reader can still reconstruct.
what_triggers_fatal: The reported sample or counts cannot be derived from the described procedure even in principle (the counts contradict the pipeline, or the data cannot be traced to any described collection), or the design is structurally unable to answer the stated research question, so that no revision of the reporting can repair it.

### D3: argumentative_coherence
dimension_id: D3
what_to_look_for: Whether claims about the sample's coverage, popularity or representativeness stay within what the selection procedure supports; whether any validation check is independent of the procedure it validates (a check against a reference list picked by the same researcher, or a procedure adjusted after seeing the check's misses, is circular unless disclosed and supplemented); whether limitations stated in the methods carry through to the results and the conclusions; and whether counts, rules and terms stay consistent across sections.
what_triggers_block: A central claim about the sample (for example that it covers the most popular or a representative set of apps) rests on a circular check or on evidence that does not support it, or the methods and results contradict each other on counts or rules, in a way that reframing the claim or adding an independent check in a revision can fix.
what_triggers_warn: Claims mildly overstate completeness or generality, a limitation is acknowledged in one place but not carried through, or it is unclear whether a validation step is independent, without evidence that it is compromised.
what_triggers_fatal: The core thesis contradicts itself, or the paper's own reported data directly refute its central conclusion, so that the argument cannot stand without a different study.

criteria_binding_unavailable

[CONTRACT-ACKNOWLEDGED]
