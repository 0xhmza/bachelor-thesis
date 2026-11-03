"""Polished file names for the reading PDFs: 'Author(s) Year - Title.pdf'."""
import re, unicodedata

INITIALS = re.compile(r'^[A-Za-z]\.(?:-?[A-Za-z]\.)*$')

# By source file name: (citation label, title). Used where the registry has none,
# is wrong for the file, or the file is not a plain article.
OVERRIDES = {
    '12_Polson_1992_Cognitive-walkthroughs-a-method-for-theory-based-evaluation-of-user-interfaces.pdf':
        ('Polson et al. 1992', 'Cognitive Walkthroughs: A Method for Theory-Based Evaluation of User Interfaces'),
    'N2_Wharton__Wharton-et-al-1994-The-Cognitive-Walkthrough-Method-A-Practitioner-s-Guide.pdf':
        ('Wharton et al. 1994', "The Cognitive Walkthrough Method: A Practitioner's Guide (chapter in Usability Inspection Methods, complete book)"),
    '70_Nissenbaum_2009_Privacy-in-Context_open-front-matter-and-introduction.pdf':
        ('Nissenbaum 2009', 'Privacy in Context: Technology, Policy, and the Integrity of Social Life (front matter and introduction)'),
    'X_Nissenbaum_2010_Privacy-in-Context_TOC-and-Introduction_OCR.pdf':
        ('Nissenbaum 2009', 'Privacy in Context: Technology, Policy, and the Integrity of Social Life (contents and introduction, OCR)'),
    'X_Hutton_2017_Popular-Apps-Evaluated_app-list.pdf':
        ('Hutton et al. 2017', 'Popular Apps Evaluated: App List (Appendix 2 of the heuristic evaluation)'),
    'X_Albrecht_2016_CHARISMHA-Gesamtbericht_BMG.pdf':
        ('Albrecht 2016', 'Chancen und Risiken von Gesundheits-Apps (CHARISMHA): Gesamtbericht'),
    'X_Amaral_2021_Completeness-checking-of-privacy-policies-GDPR.pdf':
        ('Amaral et al. 2021', 'AI-Enabled Automation for Completeness Checking of Privacy Policies'),
    'X_Carlo_2019_Ratings-and-utilization-of-behavioral-health-apps_npjDM.pdf':
        ('Carlo et al. 2019', 'By the Numbers: Ratings and Utilization of Behavioral Health Mobile Applications'),
    'X_Chew_2023_LLM-assisted-content-analysis-deductive-coding.pdf':
        ('Chew et al. 2023', 'LLM-Assisted Content Analysis: Using Large Language Models to Support Deductive Coding'),
    'X_Cui_2025_PoliGraph-journal-version-with-PoliGrapher-LM.pdf':
        ('Cui et al. 2025', 'PoliGraph: Automated Privacy Policy Analysis Using Knowledge Graphs (journal version)'),
    'X_Cummings_2021_User-expectations-for-differential-privacy_CCS.pdf':
        ('Cummings et al. 2021', 'I Need a Better Description: An Investigation Into User Expectations for Differential Privacy'),
    'X_Freiberger_2025_LLM-powered-interactive-privacy-policy-assessment.pdf':
        ('Freiberger et al. 2025', "You Don't Need a University Degree to Comprehend Data Protection This Way: LLM-Powered Interactive Privacy Policy Assessment"),
    'X_Gajavalli_2025_Measuring-privacy-as-shield-from-harms.pdf':
        ('Gajavalli et al. 2025', "What's Privacy Good For? Measuring Privacy as a Shield from Harms Due to Personal Data Use"),
    'X_Gligoric_2025_Unconfident-LLM-annotations-confident-conclusions_NAACL.pdf':
        ('Gligorić et al. 2025', 'Can Unconfident LLM Annotations Be Used for Confident Conclusions?'),
    'X_Hamid_2024_GenAIPABench_PoPETs.pdf':
        ('Hamid et al. 2024', 'GenAIPABench: A Benchmark for Generative AI-Based Privacy Assistants'),
    'X_Leitner_2025_Limits-of-LLMs-for-German-text-classification_JLCL.pdf':
        ('Leitner & Rehm 2025', 'Exploring the Limits of LLMs for German Text Classification: Prompting and Fine-Tuning Strategies Across Small and Medium-Sized Datasets'),
    'X_Schroeder_2025_LLMs-in-qualitative-research_CHI.pdf':
        ('Schroeder et al. 2025', 'Large Language Models in Qualitative Research: Uses, Tensions, and Intentions'),
    'X_Tang_2023_PolicyGPT.pdf':
        ('Tang et al. 2023', 'PolicyGPT: Automated Analysis of Privacy Policies with Large Language Models'),
    'X_Tang_2026_Decoding-the-legalese-corporate-privacy-policies.pdf':
        ('Tang et al. 2026', 'Decoding the Legalese: A Scalable and Quantitative Framework for Analyzing Corporate Privacy Policies'),
    'X_Xiang_2025_Google-Play-privacy-transparency-channels.pdf':
        ('Xiang et al. 2025', "Exploring the Effectiveness of Google Play Store's Privacy Transparency Channels"),
    'X_Xiao_2023_Codebook-plus-GPT-3-deductive-coding.pdf':
        ('Xiao et al. 2023', 'Supporting Qualitative Analysis with Large Language Models: Combining Codebook with GPT-3 for Deductive Coding'),
    'X_Zhang_2022_How-usable-are-iOS-privacy-labels_PoPETs.pdf':
        ('Zhang et al. 2022', 'How Usable Are iOS App Privacy Labels?'),
    'X_Ziems_2024_Can-LLMs-transform-computational-social-science.pdf':
        ('Ziems et al. 2024', 'Can Large Language Models Transform Computational Social Science?'),
    'X_Theis_2023_Fitness-tracker-privacy-information-requirements_CHI-EA.pdf':
        ('Theis et al. 2023', "Understanding Fitness Tracker Users' and Non-Users' Privacy Information Requirements"),
    'X_Zufferey_2023_Revoked-just-now-fitness-data-sharing-third-party-apps_PoPETs.pdf':
        ('Zufferey et al. 2023', 'Revoked Just Now! Users\' Behaviors Toward Fitness-Data Sharing with Third-Party Applications'),
    'N7_APA_App-Evaluation-Model_web-capture-2026-10-20.pdf':
        ('APA 2026', 'The App Evaluation Model (web capture, 20 October 2026)'),
    'N10_BfArM__BfArM-The-Fast-Track-Process-for-Digital-Health-Applications-DiGA.pdf':
        ('BfArM', 'The Fast-Track Process for Digital Health Applications (DiGA)'),
    'N8_Article-29-Working-Party-EDPB__Article-29-Working-Party-EDPB-Guidelines-on-transparency-under-Regulation-2016-679.pdf':
        ('Article 29 Working Party 2018', 'Guidelines on Transparency under Regulation 2016/679 (WP260 rev.01)'),
    'N9_Association-of-Internet-Researchers__Association-of-Internet-Researchers-Internet-Research-Ethical-Guidelines-3-0.pdf':
        ('franzke et al. 2020', 'Internet Research: Ethical Guidelines 3.0 (AoIR)'),
    'X_Aryal_2026_Traditional-policy-analysis-tools-vs-LLMs.pdf': ('Aryal et al. 2026', None),
    'X_Aydin_2024_Assessing-privacy-policies-with-AI-ethical-legal-technical.pdf': ('Aydin et al. 2024', None),
    'X_Chen_2025_LLMs-for-privacy-policy-analysis-prompting-fine-tuning-explainability.pdf': ('Chen et al. 2025', None),
    'X_Goknil_2024_Privacy-policy-analysis-through-prompt-engineering-PAPEL.pdf': ('Göknil et al. 2024', None),
    'X_Khatun_2026_Disclosure-divergence-policy-vs-Data-Safety.pdf': ('Khatun et al. 2026', None),
    'X_Lebanoff_2018_Vague-words-in-privacy-policies_EMNLP.pdf': ('Lebanoff & Liu 2018', None),
    'X_Lin_2024_Data-Safety-vs-App-Privacy-labels_PoPETs.pdf': ('Lin et al. 2024', None),
    'X_Mori_2025_LLMs-assessing-privacy-policy-understandability_USEC.pdf': ('Mori et al. 2025', None),
    'X_Saini_2024_Reproductive-health-apps-privacy-security.pdf': ('Saini & Saxena 2024', None),
    'X_Shvartzshnaider_2019_Contextual-integrity-privacy-policy-analysis_HCOMP.pdf': ('Shvartzshnaider et al. 2019', None),
    '22_Krippendorff_2019_Content-Analysis-4e.pdf':
        ('Krippendorff 2019', 'Content Analysis: An Introduction to Its Methodology (4th ed.)'),
}


def surname(name):
    toks = [t for t in name.replace(' ', ' ').split() if not INITIALS.match(t)]
    return ' '.join(toks) or name


def label(authors, year):
    if 'et al' in authors:
        return f"{authors.replace(' et al.', '').strip()} et al. {year}"
    names = [surname(a.strip()) for a in re.split(r',\s*|\s+and\s+', authors) if a.strip()]
    if len(names) == 1:
        a = names[0]
    elif len(names) == 2:
        a = f'{names[0]} & {names[1]}'
    else:
        a = f'{names[0]} et al.'
    return f'{a} {year}'


def clean_title(t):
    t = unicodedata.normalize('NFC', t).replace(chr(0xfffd), '')
    t = t.replace(chr(0x2018), "'").replace(chr(0x2019), "'").replace(chr(0x201c), '').replace(chr(0x201d), '').replace('"', '')
    t = t.replace("`Might'", 'Might').replace('`', '')
    t = re.sub(r'\?\s+', ' - ', t).rstrip('?')
    t = re.sub(r'[\/*<>|?]', '-', t)
    return re.sub(r'\s+', ' ', t).strip(' .')


def polished(lbl, title, limit=175):
    title = clean_title(title)
    stem = f'{lbl} - {title}'.replace(':', ' -')
    stem = re.sub(r'\.\s+-', ' -', re.sub(r'\s+', ' ', stem))
    if len(stem) > limit:
        stem = stem[:limit].rsplit(' ', 1)[0].rstrip(' -,:;') + '...'
    return stem + '.pdf'
