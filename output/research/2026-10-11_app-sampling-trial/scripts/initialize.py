"""Freeze trial inputs before collection. Run once; existing files are protected."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[2]

def write(name, data):
    path = BASE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

fitness = ['Fitness', 'Fitness Tracker', 'Schrittzähler', 'Aktivitätstracker',
           'Schlaf-Tracker', 'Herzfrequenz', 'Kalorienzähler', 'Ernährungstagebuch', 'Workout']
fertility = ['Periode', 'Zyklus', 'Zyklustracker', 'Menstruation', 'Eisprung',
             'Fruchtbarkeit', 'Kinderwunsch', 'period tracker', 'ovulation', 'fertility']
keywords = [{'id': f'{prefix}{i}', 'term': term, 'domain': domain}
            for prefix, domain, terms in [('F', 'fitness', fitness), ('P', 'fertility', fertility)]
            for i, term in enumerate(terms, 1)]
proposal = ROOT / '03_Thesis/proposal/proposal.tex'
write('config/protocol.json', {
    'protocol_id': 'app-sampling-trial-v1', 'frozen_utc': datetime.now(timezone.utc).isoformat(),
    'authority': 'Current proposal.tex Sampling; older protocol supplies keyword list only',
    'proposal_path': str(proposal.relative_to(ROOT)),
    'proposal_sha256': hashlib.sha256(proposal.read_bytes()).hexdigest(),
    'purpose': 'Feasibility trial and candidate register, not a frozen thesis analysis sample',
    'storefront': 'de', 'play_language': 'de', 'apple_api_language': 'en_us',
    'per_query_limit': 20, 'minimum_ratings_per_listing': 1000,
    'targets': {'fitness': 30, 'fertility': 20}, 'keywords': keywords,
    'ranking': ['rating_count_weighted_mean_desc', 'eligible_rating_count_sum_desc', 'canonical_app_id_asc'],
    'tie_note': 'Stable canonical ID is a trial operational choice; proposal leaves exact ties unspecified.',
    'secondary_metric': 'Play embedded install count; no country-specific or unique-user interpretation',
    'delay_seconds': 3.5, 'timeout_seconds': 30, 'retries': 0,
    'inclusion': ['German store availability', 'health/body tracking, including device companions displaying tracking',
                  'free installation', 'German or English interface', 'reachable privacy policy', 'at least one listing with >=1000 ratings'],
    'exclusion': ['no relevant tracking', 'paid installation', 'neither German nor English interface',
                  'policy unavailable after verification', 'DiGA', 'duplicate product'],
    'unknown_rule': 'Unknown is pending, never silently treated as eligible or excluded',
    'discovery_modes': {'apple': 'official_search_api_trial', 'play': 'documented_web_discovery_seed'},
    'final_gate': 'All eligibility checks, identity resolution, both-store discovery completion and store-UI membership must be verified.'
})
# IDs observed in primary Play pages returned by web discovery in this session.
groups = {
    'fitness': ['co.pacetech.dietx', 'io.schritte.moveup', 'com.google.android.apps.fitness',
                'com.gen.workoutme', 'com.sirvendor.lensnutra', 'com.tayu.tau.pedometer',
                'com.zumba.consumerapp', 'step.pedometer.stepcounter.walking',
                'com.stepsappgmbh.stepsapp', 'com.peakd.app',
                'com.maxxnation.workout_for_men', 'com.ty.stepfit'],
    'fertility': ['org.iggymedia.periodtracker', 'caculator.period.tracker',
                  'com.periodtracker.ovulation.periodcycle', 'com.period.tracker.lite',
                  'de.cyclotest.mysense', 'com.wachanga.womancalendar',
                  'com.periodtracker.periodcalendar.ovulation.periodcycle',
                  'com.granitedigital.velle', 'com.lbrc.PeriodCalendar',
                  'com.kunpitech.bloomperiodtracker', 'com.ovulation.Period.tracker', 'com.clue.android']}
write('config/play_seeds.json', [
    {'app_id': app, 'domain_hint': domain,
     'evidence_url': 'https://play.google.com/store/apps/details?id=' + app,
     'discovery': 'prior direct Clue fetch' if app == 'com.clue.android' else 'web search result linking to primary Play listing',
     'store_search_rank': None, 'in_proposal_search_frame': 'pending'}
    for domain, ids in groups.items() for app in ids])
write('config/discovery_log.json', {
    'date': '2026-10-11', 'method': 'Assistant web search; URLs used only as feasibility seeds, not ranked store results',
    'queries': ['site:play.google.com/store/apps/details fitness tracker Schrittzähler workout',
                'site:play.google.com/store/apps/details Periode Zyklus Eisprung period tracker',
                'site:play.google.com/store/apps/details Kalorienzähler Schlaf Herzfrequenz',
                'site:play.google.com/store/apps/details fertility ovulation Kinderwunsch',
                'site:play.google.com/store/apps/details "Fitness" "Schritte"',
                'site:play.google.com/store/apps/details "Kalorienzähler" "Schlaf"'],
    'limitation': 'Search service selected results; no exhaustive or ordered web-search corpus is claimed.'})
with (BASE / 'config/proposal_snapshot.tex').open('xb') as f:
    f.write(proposal.read_bytes())
print('Frozen protocol, 19 keywords, 24 Play seeds and proposal snapshot.')
