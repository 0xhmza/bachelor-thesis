"""Code every screening decision with the eligibility rules of Methodology Table 4.2.

The screening of 23-25 October 2026 logged each exclusion with an E code (E1-E5) and a reason
taken from the store listing. Rules I1-I7 and X1-X8 restate E1-E5 (Decision D3), so no decision
changes: each excluded listing gets the rule that its logged reason names. An exclusion rule is
named where one applies; otherwise the inclusion rule that fails. The script adds or refreshes
the column `rule` of screening.csv and stops on any reason it has no rule for.

    python recode.py 04_Study/4.4_App-Sampling/screening.csv
"""
import csv
import sys
from collections import Counter

# Logged reason (text before the first ';') -> rule of Table 4.2.
RULES = {
    # X1: shows exercises or articles but records nothing (instructional or content-only app)
    'affirmation content': 'X1', 'anatomy reference (also not free)': 'X1',
    'bedtime stories for children': 'X1', 'drawing lessons': 'X1', 'driving-test training': 'X1',
    'greeting cards': 'X1', 'interactive training videos': 'X1', 'learning cards': 'X1',
    'meditation content': 'X1', 'pregnancy content': 'X1', 'reading platform': 'X1',
    'recipe collection': 'X1', 'recipes': 'X1', 'sleep sounds and stories': 'X1',
    'sports news': 'X1', 'workout video courses': 'X1',
    # X2: a game, a shop or a general-purpose app
    'game': 'X2', 'casino game': 'X2', 'shop': 'X2', 'supermarket app': 'X2',
    'loyalty programme': 'X2', 'meal kits and recipes': 'X2', 'browser': 'X2', 'search app': 'X2',
    'e-mail': 'X2', 'messaging': 'X2', 'social network': 'X2', 'office software': 'X2',
    'general-purpose assistant': 'X2', 'calendar': 'X2', 'general-purpose diary': 'X2',
    'photo editor': 'X2', 'video editor': 'X2', 'design tool': 'X2', 'photo sharing': 'X2',
    'home-screen themes': 'X2', 'home-screen widgets': 'X2', 'business communication': 'X2',
    'decision wheel': 'X2', 'party tool': 'X2', 'weather thermometer': 'X2',
    'weather (also not free)': 'X2',
    # X3: tracks a child or another person instead of the user
    'baby development': 'X3', 'baby sleep schedule': 'X3', 'baby tracker': 'X3', 'baby monitor': 'X3',
    # X4: records only other self-tracking data
    'brain training': 'X4', 'habit and routine planner': 'X4', 'meditation and sleep content': 'X4',
    # X6: no tracking or predictive feature
    'interval timer only': 'X6', 'pill reminder': 'X6', 'product ingredient scanner': 'X6',
    # I1.2 fails: the data are not about the user's own health or body
    'pet health': 'I1.2', 'job portal': 'I1.2', 'dating': 'I1.2', 'beauty bookings': 'I1.2',
    'restaurant bookings': 'I1.2', 'ride hailing': 'I1.2', 'hotel partner management': 'I1.2',
}
# The other E codes map one to one (D3).
BY_CODE = {'E2': 'X7', 'E3': 'I6', 'E4': 'I7', 'E5': 'X8'}


def rule(row):
    if row['decision'] == 'eligible':
        return ''
    if row['criterion'] in BY_CODE:
        return BY_CODE[row['criterion']]
    key = row['reason'].split(';')[0].strip()
    if key not in RULES:
        raise SystemExit(f"no rule for reason {key!r} ({row['store']} {row['id']})")
    return RULES[key]


def main(path):
    with open(path, encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f))
    fields = [k for k in rows[0] if k != 'rule']
    fields.insert(fields.index('criterion') + 1, 'rule')
    for r in rows:
        r['rule'] = rule(r)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(dict(Counter(r['rule'] or 'eligible' for r in rows)))


if __name__ == '__main__':
    main(sys.argv[1])
