"""Plan the new 01_Literature layout: one library file per distinct PDF, named Author_Year_ShortTitle.pdf.

Reads a sha256 listing of every PDF under 01_Literature/ and literature_new/ (argument 1) and writes plan.csv
(argument 2): hash, new name, kept source, other copies to remove. Nothing is moved here.
"""
import collections, csv, json, re, sys
from pathlib import Path
import names

ROOT = Path(__file__).resolve().parents[3]
listing, out = sys.argv[1], sys.argv[2]
groups = collections.defaultdict(list)
for line in open(listing, encoding='utf-8', errors='replace'):
    h, p = line.rstrip('\n').split('  ', 1)
    groups[h].append(p)

LN_INDEX = {r['File']: r for r in csv.DictReader(open(ROOT / 'literature_new/references index.csv', encoding='utf-8'))}

# Names that stay exactly as the core reading list already uses them (README rule: keep, the key never changes).
CORE = {'Cao_2024_PeriodTrackingApps-PostRoe.pdf', 'Citron_2022_PrivacyHarms.pdf',
        'Gabriele_2020_FitnessTrackerUsers-KnowledgeAttitudes.pdf', 'Hudig_2025_IntimateDataSharing-FertilityTracking.pdf',
        'Knabenhans_2026_PrivacyHarms-EUDigitalIdentity.pdf', 'Malki_2024_PrivacyPractices-FemaleMHealthApps.pdf',
        'Martin_2025_NoCookiesForYou.pdf', 'SalehzadehNiksirat_2024_WearableActivityTrackers-Survey.pdf',
        'Nielsen_1994_UsabilityInspectionMethods-Book.pdf'}

# Files outside the numbered corpus, named by hand (identified from their first page / the audit README).
MANUAL = {
    'The Boundaries of Privacy Harm.pdf': 'Calo_2011_BoundariesOfPrivacyHarm.pdf',
    'popets-2019-0037.pdf': 'Zimmeck_2019_MAPS-ScalingPrivacyCompliance.pdf',
    'Harm Tree sS3-P2-SouryaJoyeeDe.pdf': 'De_2016_PrivacyHarmAnalysis-SmartGrids_manuscript.pdf',
    'angelopoulos2023prediction.pdf': 'Angelopoulos_2023_PredictionPoweredInference.pdf',
    'apple2022itunessearch_web-capture_2026-11-04.pdf': 'Apple_2022_ITunesSearchAPI_web-capture.pdf',
    'de2016privacy_published.pdf': 'De_2016_PrivacyHarmAnalysis-SmartGrids.pdf',
    'de2017refinement_author_manuscript.pdf': 'De_2017_RefinementApproachPrivacyRiskAnalysis_manuscript.pdf',
    'hu2018studying_author_manuscript.pdf': 'Hu_2018_ConsistencyStarRatingsComplaints_manuscript.pdf',
    'iwaya2023privacy_published.pdf': 'Iwaya_2023_PrivacyMentalHealthApps_published.pdf',
    'kim2025correlated.pdf': 'Kim_2025_CorrelatedErrorsLLMs.pdf',
    'priem2022openalex.pdf': 'Priem_2022_OpenAlex.pdf',
    'rodriguez2024llm_published.pdf': 'Rodriguez_2024_LargeLanguageModelsPrivacyPolicyAnalysis_published.pdf',
    'schroeder2025just.pdf': 'Schroeder_2025_LLMsQualitativeResearch_preprint.pdf',
    'schroeder2025just_published.pdf': 'Schroeder_2025_LLMsQualitativeResearch_published.pdf',
    'statcounter2026os_web-capture_2026-11-04.pdf': 'StatCounter_2026_MobileOSGermany_web-capture.pdf',
    'statcounter2026vendor_web-capture_2026-11-04.pdf': 'StatCounter_2026_MobileVendorGermany_web-capture.pdf',
    'statcounter_methodology_supplement_web-capture_2026-11-04.pdf': 'StatCounter_2026_Methodology_web-capture.pdf',
    'steinboeck2024comparing.pdf': 'Steinboeck_2024_ComparingAppStoreRatings.pdf',
}
# Hand-fixes for numbered/LN names whose automatic short title is poor or ambiguous.
FIX = {
    'Krippendorff_2019_ContentAnalysis.pdf': 'Krippendorff_2019_ContentAnalysis.pdf',
    'Habib_2020_SScavengerHuntUsabilityWebsites.pdf': 'Habib_2020_ScavengerHunt-OptOutDeletionChoices.pdf',
    'Franzke_2020_InternetResearch.pdf': 'Franzke_2020_InternetResearchEthics-AoIRGuidelines3.pdf',
    'Article29WP_2018_GuidelinesTransparencyUnderRegulation2016.pdf': 'Article29WP_2018_TransparencyGuidelinesWP260.pdf',
    'Iwaya_2023_PrivacyMentalHealthAppsEmpirical.pdf': 'Iwaya_2023_PrivacyMentalHealthApps.pdf',
    'Rodriguez_2024_LargeLanguageModelsApproachPrivacy.pdf': 'Rodriguez_2024_LargeLanguageModelsPrivacyPolicy.pdf',
    'Rodriguez_2024_LargeLanguageModelsPrivacyPolicyAnalysis_published.pdf': 'Rodriguez_2024_LargeLanguageModelsPrivacyPolicy_published.pdf',
    'Schroeder_2025_LLMsQualitativeResearch_preprint.pdf': 'Schroeder_2025_JustPutHumanInLoop_preprint.pdf',
    'Schroeder_2025_LLMsQualitativeResearch_published.pdf': 'Schroeder_2025_JustPutHumanInLoop_published.pdf',
    'Hutton_2018_AssessingPrivacymHealthAppsSelf.pdf': 'Hutton_2018_AssessingPrivacyMHealthApps.pdf',
    'Page_2021_PRISMA2020StatementUpdatedGuideline.pdf': 'Page_2021_PRISMA2020.pdf',
    'Rethlefsen_2021_PRISMASExtensionPRISMAStatement.pdf': 'Rethlefsen_2021_PRISMA-S.pdf',
    'Tricco_2018_PRISMAExtensionScopingReviewsPRISMA.pdf': 'Tricco_2018_PRISMA-ScR.pdf',
    'Nissenbaum_2009_PrivacyContext_excerpt.pdf': 'Nissenbaum_2009_PrivacyInContext_excerpt.pdf',
    'Nissenbaum_2010_PrivacyContext_excerpt.pdf': 'Nissenbaum_2010_PrivacyInContext_toc-excerpt.pdf',
    'UNNAMED': 'BfArM_2023_DiGAFastTrackGuide.pdf',
}
VOLUMES = lambda p: 'AI Literature Analysis' in p or 'literature methodology analysis' in p
CACHE = lambda p: '/pdf-cache/' in p or '/private/' in p or p.startswith('01_Literature/.tex/')
DROP = {'01_Literature/PDFs/Methods-Reading/04_Coding/74_Braun_2006_Using-thematic-analysis-in-psychology.pdf'}  # wrong paper (HAL, 2 pp.)

MR = re.compile(r'(?:N?\d+|X)_(?P<a>[^_]+)_(?P<y>\d{4})_(?P<t>.+)\.pdf$')


def mr_name(base):
    m = MR.match(base)
    if not m:
        return None
    a, y, t = m.group('a'), m.group('y'), m.group('t')
    parts = t.split('_')
    title, extra = parts[0], ' '.join(parts[1:])
    suffix = ''
    low = (title + ' ' + extra).lower()
    if re.search(r'additional-file|multimedia-appendix|app-list|scoring-criteria|rating-form|instrument', low):
        suffix = '_supplement'
    elif 'web-capture' in low:
        suffix = '_web-capture'
    elif re.search(r'excerpt|front-matter|toc|ocr', low):
        suffix = '_excerpt'
    elif 'manuscript' in low:
        suffix = '_manuscript'
    a = re.sub(r"^T-rnberg$", 'Tornberg', a)
    return f"{names.author_token(a.replace('-', ' ') if a != 'Salehzadeh-Niksirat' else 'Salehzadeh Niksirat')}_{y}_{names.short_title(title)}{suffix}.pdf"


def ln_name(file):
    r = LN_INDEX.get(file)
    f = file[:-4]
    m = re.match(r'(.+?) (\d{4})(?:, [^-]+?)? - (.*)$', f)
    if not m:
        return None
    a, y, t = m.groups()
    return f"{names.author_token(a)}_{y}_{names.short_title(t)}.pdf"


rows, taken = [], collections.Counter()
for h, paths in sorted(groups.items(), key=lambda kv: sorted(kv[1])[0]):
    paths = sorted(paths)
    if any(VOLUMES(p) for p in paths) or all(CACHE(p) for p in paths):
        continue
    if any(p in DROP for p in paths):
        rows.append((h, '', '', '|'.join(paths), 'wrong paper')); continue
    base = [Path(p).name for p in paths]
    new = None
    for b in base:
        if b in CORE: new = b
    if not new:
        for b in base:
            if b in MANUAL: new = MANUAL[b]
    mr = [Path(p).name for p in paths if 'Methods-Reading' in p]
    ln = [Path(p).name for p in paths if p.startswith('literature_new/references/')]
    if not new and mr:
        new = mr_name(mr[0])
    if not new and ln:
        new = ln_name(ln[0])
    if not new and any(b.startswith('N10_') for b in base):
        new = 'UNNAMED'
    new = FIX.get(new, new)
    if not new:
        new = 'UNNAMED_' + h[:8] + '.pdf'
    # keep one source: prefer a tracked-looking file under 01_Literature/PDFs, then Methods-Reading, then literature_new
    def rank(p):
        return (0 if p.startswith('01_Literature/PDFs/') and 'Methods-Reading' not in p else 1 if 'Methods-Reading' in p else 2, p)
    if new.startswith('Krippendorff_2019'):
        paths = [p for p in paths if '/.tex/' not in p]
    keep = sorted(paths, key=rank)[0]
    rows.append((h, new, keep, '|'.join(p for p in paths if p != keep), ''))
    taken[new] += 1

with open(out, 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh); w.writerow(['sha256', 'new_name', 'keep', 'remove', 'note']); w.writerows(rows)
print(len(rows), 'works;', 'collisions:', [k for k, v in taken.items() if v > 1])
