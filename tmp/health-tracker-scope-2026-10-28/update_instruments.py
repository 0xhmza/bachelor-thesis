from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
source=ROOT/'04_Study/Codebook/codebook_v3.md'
dest=ROOT/'04_Study/Codebook/codebook_v4.md'
assert not dest.exists(), 'Do not overwrite an existing codebook version'
text=source.read_text(encoding='utf-8')
edits=[
 ('version: 3\ndate: 2026-10-05\nstatus: draft — definitions aligned with the proposal; examples to be filled from the pilot\nsource: 03_Thesis/proposal/proposal.tex (Reference harm trees, Harm categories, Coding A–C, LLM assistance, Validation); harm model from Knabenhans et al. (2026), ePrint 2026/867, version of 4 May 2026\nsupersedes: codebook_v2.md',
  'version: 4\ndate: 2026-10-28\nstatus: draft — one health-tracker study domain (D15); examples to be filled from the pilot\nsource: current 03_Thesis/chapters/04_methodology.tex; author clarification recorded in 00_Admin/Decisions/D15_health-tracker-domain.md; harm model from Knabenhans et al. (2026), ePrint 2026/867, version of 4 May 2026\nsupersedes: codebook_v3.md'),
 ('# Codebook v3','# Codebook v4'),
 ('**The proposal is authoritative.** Where this file and the proposal disagree,\nthe proposal wins and this file gets a new version.',
  '**Current authority:** the thesis methodology, the supervisor guidance of 13 October and the author\'s confirmed clarification in D15 govern this instrument. The 5 October proposal and codebook v3 are historical versions. The study domain is health trackers overall; source-paper categories inform the scope and search vocabulary, and app features determine pathway applicability.'),
 ('Origin is **not** coded from provider text. It is fixed in advance, per domain,\nin `harm_trees_v1.md` (to be built before the pilot) from the sources named in\nthe proposal (fitness: Salehzadeh Niksirat et al. 2024, Gabriele & Chiasson\n2020; fertility: Shipp & Blasco 2020, Malki et al. 2024, Hudig & Singh 2025,\nCao et al. 2024), extended by the logged literature search with a recorded\nreason.',
  'Origin is **not** coded from provider text. It is fixed in advance for each pathway\nin `harm_trees_v1.md` (to be built before the pilot) for health trackers overall.\nSources include Salehzadeh Niksirat et al. 2024, Gabriele & Chiasson 2020,\nShipp & Blasco 2020, Malki et al. 2024, Hudig & Singh 2025 and Cao et al. 2024,\nextended by the logged literature search with a recorded reason. App categories\ndo not select separate reference trees; applicability is assessed per app and pathway.'),
 ('| Domain | fitness · fertility (selects the reference tree) |','| App category / relevant features | descriptive metadata; reference-pathway applicability is assessed separately |'),
 ("As in the proposal's *Validation and missed mentions* paragraph, summarised:",
  'Aligned with the current methodology and D15:'),
 ('- **Validation set:** ten apps, five per domain, drawn at random with a\n  recorded seed from providers and documents **not used in the pilot**,',
  '- **Pilot:** five apps drawn at random with a recorded seed from the full health-tracker sample, without category quotas; recoded with the frozen instruments and excluded from validation.\n- **Validation set:** ten apps drawn at random from the health-tracker sample with a\n  recorded seed from providers and documents **not used in the pilot**,')]
for old,new in edits:
 assert text.count(old)==1, old
 text=text.replace(old,new,1)
text+='\n| 4 | 2026-10-28 | One health-tracker study domain; feature-based pathway applicability; descriptive category metadata; five pilot and ten independent validation apps across the sample, without category allocations | Author clarification D15; retain existing coding axes, totals and validation safeguards |\n'
dest.write_text(text,encoding='utf-8')

p=ROOT/'04_Study/Instrument/walkthrough_protocol.md'
text=p.read_text(encoding='utf-8')
assert text.count('(codebook v3)')==2
p.write_text(text.replace('(codebook v3)','(codebook v4)'),encoding='utf-8')

# The restored old sampling protocol is an uncommitted historical document.
# Prepend the current operative scope without overwriting its historical body.
p=ROOT/'04_Study/App-Sample/sampling_protocol.md'
text=p.read_text(encoding='utf-8')
assert text.startswith('# Sampling Protocol\n')
current='''# Sampling Protocol — current scope amendment

**Version:** 3 (scope amendment) · **Date:** 2026-10-28 · **Authority:** author's confirmed clarification in [D15](../../00_Admin/Decisions/D15_health-tracker-domain.md), read with the current thesis methodology and D1–D7.

The study domain is health trackers overall. Categories from the source papers explain the domain definition and the [49 search queries](keywords.csv) and describe the apps; they do not define separate study strata or analysis groups.

- Sampling remains one combined ranking of eligible health trackers, with no category quotas; the present target is 47 ranked plus three preinstalled apps (D1/D2/D6).
- The pilot draws five apps at random from the whole sample, with a recorded seed and no category allocation.
- Validation draws ten apps at random from providers and documents not used in the pilot, with a recorded seed and policy-language stratification where both languages occur. Pilot apps do not enter validation.
- Walkthroughs inspect twelve distinct apps across the sample, six on Android and six on iOS, alternating platform slots in rank order. Existing access exclusions and reporting of unfilled slots remain.
- The reference harm trees concern health trackers; applicability follows each app's features and the pathway's data, access and context conditions.
- Codebook v4 and walkthrough protocol v3 implement this scope. This amendment changes no collected query, raw record, eligibility judgment, ranking or selected app. It does not settle other open methodological decisions.

The text below is the preserved version-1 historical draft. Its sampling/ranking rules and category-specific allocations do not govern current work. Use the current methodology and decision records for the operative procedure.

---

'''
p.write_text(current+text,encoding='utf-8')
print('Created codebook v4; updated active instrument references and sampling scope amendment.')
