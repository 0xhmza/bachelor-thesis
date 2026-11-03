"""Shared helpers of the v002 literature search (D14): term groups, their translation for each platform, and the
local Boolean match used where a platform offers no search (venue enumerations, the ACL Anthology file).

Matching rules of the local Boolean: text and terms are lower-cased and reduced to letters and digits separated by
single spaces (so "m-health" and "m health" match the same term); a trailing * matches any word ending; a term matches
only at word boundaries. Standard library only.
"""
import html, json, re, unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_config(path=None):
    return json.loads(Path(path or HERE / 'config.json').read_text(encoding='utf-8'))


def norm_text(text):
    text = html.unescape(text or '')
    text = re.sub(r'<[^>]+>', ' ', text)  # Crossref JATS abstracts
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode().lower()
    return ' ' + re.sub(r'[^a-z0-9*]+', ' ', text).strip() + ' '


def term_regex(term):
    words = norm_text(term).split()
    parts = [re.escape(w.rstrip('*')) + (r'[a-z0-9]*' if w.endswith('*') else '') for w in words]
    return re.compile(r' ' + r' '.join(parts) + r'(?= )')


_CACHE = {}


def group_regexes(config, group):
    key = (id(config), group)
    if key not in _CACHE:
        _CACHE[key] = [term_regex(t) for t in config['groups'][group]['terms']]
    return _CACHE[key]


def group_match(config, group, text):
    """The terms of the group found in the text (empty list if none)."""
    norm = norm_text(text).replace('*', ' ')
    return [t for t, rx in zip(config['groups'][group]['terms'], group_regexes(config, group)) if rx.search(norm)]


def strand(config, strand_id):
    return next(s for s in config['strands'] if s['id'] == strand_id)


def strand_match(config, strand_id, text):
    return all(group_match(config, g, text) for g in strand(config, strand_id)['groups'])


def rule_match(config, rule, text):
    """A venue rule: a strand id (S1), a group (D) or groups joined with & (D&P)."""
    if rule.startswith('S'):
        return strand_match(config, rule, text)
    return all(group_match(config, g, text) for g in rule.split('&'))


# --- Platform translations ------------------------------------------------------------------------------------------

def pubmed_term(term):
    return f'"{term}"[tiab]'


def pubmed_query(config, strand_id):
    return ' AND '.join('(' + ' OR '.join(pubmed_term(t) for t in config['groups'][g]['terms']) + ')'
                        for g in strand(config, strand_id)['groups'])


def arxiv_term(term):
    """arXiv stems words and accepts * only on single words; phrases lose their trailing * (the stem covers plurals)."""
    t = term.replace('ä', 'a')
    if ' ' in t or '-' in t:
        t = '"' + t.rstrip('*') + '"'
    return f'ti:{t} OR abs:{t}'


def arxiv_query(config, strand_id, start, until):
    groups = ' AND '.join('(' + ' OR '.join(arxiv_term(t) for t in config['groups'][g]['terms']) + ')'
                          for g in strand(config, strand_id)['groups'])
    return f"{groups} AND submittedDate:[{start.replace('-', '')}0000 TO {until.replace('-', '')}2359]"


# --- Identifiers and duplicates -------------------------------------------------------------------------------------

def norm_doi(doi):
    if not doi:
        return ''
    doi = doi.strip().lower()
    return re.sub(r'^(https?://(dx\.)?doi\.org/|doi:)', '', doi)


def norm_title(title):
    return norm_text(title).strip()


def arxiv_id(value):
    match = re.search(r'(\d{4}\.\d{4,5})', value or '')
    return match.group(1) if match else ''


def ieee_term(term):
    """IEEE Xplore command search: no stemming, * allowed inside quoted phrases; title and abstract fields."""
    t = term.replace('ä', 'a')
    t = f'"{t}"' if (' ' in t or '-' in t) else t
    return f'"Document Title":{t} OR "Abstract":{t}'


def ieee_query(config, strand_id):
    return ' AND '.join('(' + ' OR '.join(ieee_term(t) for t in config['groups'][g]['terms']) + ')'
                        for g in strand(config, strand_id)['groups'])
