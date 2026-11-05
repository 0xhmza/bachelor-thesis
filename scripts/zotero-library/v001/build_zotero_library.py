"""Build a Zotero library file (Zotero RDF) from the thesis bibliography.

    python scripts/zotero-library/v001/build_zotero_library.py            # writes _shared/references-zotero.rdf
    python scripts/zotero-library/v001/build_zotero_library.py --check    # exit 1 if that file is out of date

Run it (and commit the result) every time `_shared/references.bib` changes, and
after compiling the thesis whenever the citations in the thesis change: the
reference numbers move with them.

What goes into the file, one Zotero item per BibTeX entry:
  * every field of the .bib entry, mapped to the Zotero field of the same meaning
    (what has no Zotero field is kept as a line in Extra); the comment block above
    the entry in the .bib becomes a child note;
  * the citation key (Zotero's Citation Key field);
  * the reference number `[n]` as printed in the thesis, in Rights and Call Number
    (both can be shown as columns and sort numerically); uncited works get none and
    the tag `thesis:uncited`;
  * the literature catalogue: reading status, priority, topic, catalogue id, and
    the abstract and keywords read from the PDF title page (never invented);
  * a linked file for every matching PDF in 01_Literature/library/, written as a
    path relative to the .rdf file, so no PDF is copied.

The reference number is the position of the entry in 03_Thesis/thesis.bbl (biblatex
numeric, sorted by name, year, title), the order the PDF prints. The script refuses
to number from a bbl that does not match the last LaTeX run (thesis.aux).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[3]
BIB = ROOT / '_shared' / 'references.bib'
OUT = ROOT / '_shared' / 'references-zotero.rdf'
BBL = ROOT / '03_Thesis' / 'thesis.bbl'
AUX = ROOT / '03_Thesis' / 'thesis.aux'
THESIS = ROOT / '03_Thesis'
LIBRARY = ROOT / '01_Literature' / 'library'
INDEX = ROOT / '01_Literature' / 'catalog' / 'literature-index.json'
OVERRIDES = Path(__file__).with_name('pdf_overrides.csv')
GENERATOR = 'scripts/zotero-library/v001/build_zotero_library.py'


# ---------------------------------------------------------------- BibTeX
class Entry:
    def __init__(self, key, kind, fields, comment):
        self.key, self.kind, self.fields, self.comment = key, kind, fields, comment

    def get(self, name, default=''):
        return self.fields.get(name, default)


def _balanced(text, i):
    """text[i] == '{': return (inner, index after the closing brace)."""
    depth, j = 0, i
    while j < len(text):
        c = text[j]
        if c == '\\':
            j += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return text[i + 1:j], j + 1
        j += 1
    raise ValueError('unbalanced braces in the .bib file')


def parse_bib(text):
    """Entries in file order. Comment lines directly above an entry belong to it."""
    text = text.replace('\r\n', '\n')
    entries, pending = [], []
    pos = 0
    while pos < len(text):
        eol = text.find('\n', pos)
        eol = len(text) if eol < 0 else eol
        line = text[pos:eol]
        if line.startswith('%'):
            pending.append(line[1:].strip())
            pos = eol + 1
            continue
        m = re.match(r'@(\w+)\s*\{\s*([^,\s]+)\s*,', line)
        if not m:
            if line.strip() == '':
                pending = []
            pos = eol + 1
            continue
        start = text.index('{', pos)
        body, end = _balanced(text, start)
        fields, i = {}, text.index(',', start) - start
        while True:
            fm = re.compile(r'\s*(\w+)\s*=\s*').match(body, i)
            if not fm:
                break
            i = fm.end()
            if body[i] == '{':
                value, i = _balanced(body, i)
            elif body[i] == '"':
                j = body.index('"', i + 1)
                value, i = body[i + 1:j], j + 1
            else:
                bm = re.compile(r'[^,\s]+').match(body, i)
                value, i = bm.group(0), bm.end()
            fields[fm.group(1).lower()] = re.sub(r'\s+', ' ', value).strip()
            cm = re.compile(r'\s*,').match(body, i)
            i = cm.end() if cm else len(body)
        comment = [c for c in pending if c and not set(c) <= set('-=')]
        entries.append(Entry(m.group(2), m.group(1).lower(), fields, comment))
        pending = []
        pos = end
    return entries


ACCENT = {"'": '\u0301', '"': '\u0308', '`': '\u0300', '^': '\u0302', '~': '\u0303', 'u': '\u0306', 'v': '\u030c',
          'c': '\u0327', 'H': '\u030b', '.': '\u0307', '=': '\u0304'}
LETTERS = {'ss': 'ß', 'o': 'ø', 'O': 'Ø', 'ae': 'æ', 'AE': 'Æ', 'oe': 'œ', 'OE': 'Œ', 'aa': 'å', 'AA': 'Å', 'l': 'ł',
           'L': 'Ł', 'i': 'ı', 'S': '§', 'P': '¶'}


def latex_to_text(s):
    """BibTeX field -> plain Unicode text (accents, dashes, braces, ties)."""
    s = re.sub(r'\\([\'"`^~uvcH.=])\s*\{(\\?\w)\}|\\([\'"`^~.=])(\w)|\\([uvcH])\s+(\w)',
               lambda m: unicodedata.normalize('NFC', (m.group(2) or m.group(4) or m.group(6)).lstrip('\\')
                                               + ACCENT[m.group(1) or m.group(3) or m.group(5)]), s)
    s = re.sub(r'\\(ss|oe|OE|ae|AE|aa|AA|[oOlLiSP])(?![A-Za-z])\s*', lambda m: LETTERS[m.group(1)], s)
    s = s.replace('\\&', '&').replace('\\%', '%').replace('\\_', '_').replace('\\$', '$').replace('\\#', '#')
    s = s.replace('\\,', '\u202f').replace('\\;', ' ').replace('\\:', ' ').replace('\\ ', ' ').replace('\\!', '')
    s = s.replace('---', '\u2014').replace('--', '\u2013').replace('~', '\u00a0')
    s = re.sub(r'\\[a-zA-Z]+\s?', '', s)
    s = re.sub(r'[{}]', '', s)
    return re.sub(r'[ \t]+', ' ', s).strip()


def split_names(value):
    """'A, B and {Org}' -> [(family, given)]; an organisation has an empty given name."""
    parts, depth, cur = [], 0, ''
    for tok in re.split(r'(\s+and\s+)', value):
        if re.fullmatch(r'\s+and\s+', tok) and depth == 0:
            parts.append(cur)
            cur = ''
            continue
        depth += tok.count('{') - tok.count('}')
        cur += tok
    parts.append(cur)
    names = []
    for p in (x.strip() for x in parts if x.strip()):
        if p.startswith('{') and p.endswith('}') and _balanced(p, 0)[1] == len(p):
            names.append((latex_to_text(p), ''))
        elif ',' in p:
            fam, giv = p.split(',', 1)
            names.append((latex_to_text(fam), latex_to_text(giv)))
        else:
            words = p.split()
            names.append((latex_to_text(words[-1]), latex_to_text(' '.join(words[:-1]))))
    return names


# ------------------------------------------------------------ reference numbers
def fold(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()


def bbl_order(bbl_text):
    return re.findall(r'^\s*\\entry\{([^}]+)\}', bbl_text, re.M)


def aux_cited(aux_text):
    return set(re.findall(r'\\abx@aux@cite\{[^}]*\}\{([^}]+)\}', aux_text))


def nyt_order(entries, cited):
    """Order biblatex would print (sorting=nyt): names, year, title. A cross-check only."""
    def key(e):
        names = ' '.join(f for f, _ in split_names(e.get('author') or e.get('editor')))
        return (fold(names), (e.get('date') or e.get('year'))[:4], fold(latex_to_text(e.get('title'))))
    return [e.key for e in sorted((e for e in entries if e.key in cited), key=key)]


CITE = re.compile(r'\\(?!thesiscite\b)[a-zA-Z]*cite[a-zA-Z]*\*?(?:\[[^\]]*\]){0,2}\{([^}]+)\}')


def source_citations(thesis_dir=THESIS):
    """Keys cited by the .tex sources now (comments ignored), tables and appendices included."""
    keys = set()
    paths = [thesis_dir / 'thesis.tex'] + [p for d in ('chapters', 'appendix', 'tables', 'config')
                                             for p in sorted((thesis_dir / d).glob('*.tex'))]
    for path in paths:
        if path.exists():
            text = re.sub(r'(?<!\\)%.*', '', path.read_text(encoding='utf-8'))
            for m in CITE.finditer(text):
                keys.update(k.strip() for k in m.group(1).split(','))
    return keys


def stale_note(numbers, source_keys):
    """A message when the sources cite other works than the last LaTeX run did (the numbers will move)."""
    if source_keys is None:
        return None
    gone, new = sorted(set(numbers) - source_keys), sorted(source_keys - set(numbers))
    if not gone and not new:
        return None
    return ('the .tex sources changed since the last compile: now not cited anymore: ' + (', '.join(gone) or '-')
            + '; newly cited: ' + (', '.join(new) or '-')
            + '. The numbers are those of the last compile (the PDF you see); compile and run this script again to move them.')


def reference_numbers(entries, bbl_text, aux_text=None):
    """({key: n}, [messages]); raises ValueError when the bbl cannot be trusted."""
    order = bbl_order(bbl_text)
    bib_keys = {e.key for e in entries}
    messages = []
    if len(set(order)) != len(order):
        raise ValueError('thesis.bbl lists an entry twice')
    unknown = [k for k in order if k not in bib_keys]
    if unknown:
        raise ValueError(f'thesis.bbl cites keys that are not in references.bib: {unknown}')
    if aux_text is not None and aux_cited(aux_text) != set(order):
        diff = sorted(aux_cited(aux_text) ^ set(order))
        raise ValueError(f'thesis.bbl does not match thesis.aux (compile the thesis again); differing keys: {diff}')
    expected = nyt_order(entries, set(order))
    if expected != order:
        messages.append('thesis.bbl order differs from a name-year-title sort of the cited entries; '
                        'the bbl order is used because it is what the PDF prints')
    return {k: n for n, k in enumerate(order, 1)}, messages


# ------------------------------------------------------------------- PDFs
def _camel(s):
    return [w.lower() for w in re.findall(r'[A-Z]+(?![a-z])|[A-Z][a-z0-9]*|[a-z0-9]+', s)]


def _words(s):
    return {w for w in re.findall(r'[a-z0-9]+', fold(s)) if len(w) >= 3}


def parse_pdf_name(filename):
    """Author_Year_ShortTitle[_suffix].pdf -> dict, or None."""
    parts = Path(filename).stem.split('_')
    if len(parts) < 3:
        return None
    if re.fullmatch(r'\d{4}', parts[1]):
        author, year, rest = parts[0], parts[1], parts[2:]
    elif len(parts) > 3 and re.fullmatch(r'\d{4}', parts[2]):   # De_2016_..., Von_Elm
        author, year, rest = parts[0] + parts[1], parts[2], parts[3:]
    else:
        return None
    suffix = rest[-1] if len(rest) > 1 and rest[-1] in SUFFIXES else ''
    title = rest[:-1] if suffix else rest
    return {'file': filename, 'author': re.sub(r'[^a-z0-9]', '', fold(author)), 'year': int(year), 'suffix': suffix,
            'words': {w for t in title for part in t.split('-') for w in _camel(part) if len(w) >= 3}}


SUFFIXES = ('published', 'manuscript', 'preprint', 'supplement', 'excerpt', 'web-capture', 'toc-excerpt')
PRIORITY = {'': 0, 'published': 0, 'preprint': 1, 'manuscript': 2, 'web-capture': 3, 'excerpt': 4, 'toc-excerpt': 4,
            'supplement': 5}


def entry_pdfs(entry, library_files):
    """PDFs of the library that belong to this entry, best first: [(score, filename)]."""
    year_m = re.search(r'\d{4}', entry.key)
    years = {int(y) for y in (entry.get('year')[:4], entry.get('date')[:4], year_m.group(0) if year_m else '') if y}
    if not years:
        return []
    first = (split_names(entry.get('author') or entry.get('editor')) or [('', '')])[0][0]
    authors = {re.sub(r'[^a-z0-9]', '', fold(first)), re.match(r'[a-z0-9]*?(?=\d{4})', entry.key).group(0)}
    authors.discard('')
    tw = _words(latex_to_text(entry.get('title')))
    found = []
    for fn in library_files:
        info = parse_pdf_name(fn)
        if not info or not (info['year'] in years or {info['year'] - 1, info['year'] + 1} & years):
            continue
        if not any(info['author'] == a or (len(a) > 3 and (info['author'].startswith(a) or a.startswith(info['author'])))
                   for a in authors):
            continue
        hits = sum(1 for w in info['words'] if any(x.startswith(w) or w.startswith(x) for x in tw))
        score = hits / max(1, len(info['words']))
        if score >= 0.5:
            found.append((score, PRIORITY.get(info['suffix'], 6), fn))
    found.sort(key=lambda t: (t[1], -t[0], t[2]))
    return [(s, fn) for s, _, fn in found]


def read_overrides(path=OVERRIDES):
    """key,file rows: file '-' forbids a match; several rows add several files."""
    if not path.exists():
        return {}
    out = {}
    for row in csv.DictReader(l for l in path.read_text(encoding='utf-8').splitlines() if l.strip() and not l.startswith('#')):
        out.setdefault(row['key'], []).append(row['file'])
    return out


def assign_pdfs(entries, library_files, overrides=None):
    """key -> [filenames]. A file belongs to one entry: the one it matches best."""
    overrides = overrides or {}
    cand = {e.key: entry_pdfs(e, library_files) for e in entries}
    owner = {}
    for key, lst in cand.items():
        for score, fn in lst:
            if fn not in owner or score > owner[fn][0]:
                owner[fn] = (score, key)
    forced = {fn for fns in overrides.values() for fn in fns}
    result = {}
    for e in entries:
        if e.key in overrides:
            result[e.key] = [f for f in overrides[e.key] if f != '-']
        else:
            result[e.key] = [fn for _, fn in cand[e.key] if owner[fn][1] == e.key and fn not in forced]
    return result


# ---------------------------------------------------------------- Zotero items
HAS_CALL_NUMBER = {'journalArticle', 'conferencePaper', 'bookSection', 'book', 'computerProgram', 'preprint', 'document',
                   'report'}   # webPage has no Call Number field; Rights exists for every type


def zotero_type(e):
    kind = e.kind
    if kind == 'article':
        return 'journalArticle'
    if kind == 'inproceedings':
        return 'conferencePaper'
    if kind == 'incollection':
        return 'bookSection'
    if kind == 'book':
        return 'book'
    if kind == 'software':
        return 'computerProgram'
    if kind == 'online':
        return 'webpage'
    if re.search(r'arXiv|ePrint', e.get('howpublished') + ' ' + e.get('eprinttype')):
        return 'preprint'
    return 'document'


def full_date(e):
    return e.get('date') or e.get('year')


def sql_date(d):
    return d + ' 00:00:00' if re.fullmatch(r'\d{4}-\d{2}-\d{2}', d) else d


def zotero_fields(e):
    """(zotero type, {field: value}, {used bib fields}) for one entry."""
    t = zotero_type(e)
    g = lambda n: latex_to_text(e.get(n))
    f = {'title': g('title'), 'date': full_date(e), 'DOI': e.get('doi'), 'url': e.get('url'),
         'citationKey': e.key}
    if e.get('urldate'):
        f['accessDate'] = sql_date(e.get('urldate'))
    used = {'author', 'editor', 'title', 'year', 'date', 'doi', 'url', 'urldate'}

    def take(zname, bname, convert=True):
        if e.get(bname):
            f[zname] = g(bname) if convert else e.get(bname)
            used.add(bname)

    if t == 'journalArticle':
        take('publicationTitle', 'journal'); take('volume', 'volume'); take('issue', 'number')
        take('pages', 'pages'); take('publisher', 'publisher'); take('place', 'address'); take('series', 'series')
        if not f.get('pages') and e.get('articleno'):
            take('pages', 'articleno')
        elif e.get('eid') and not f.get('pages'):
            take('pages', 'eid')
        take('ISSN', 'issn')
    elif t == 'conferencePaper':
        take('proceedingsTitle', 'booktitle'); take('volume', 'volume'); take('issue', 'number'); take('pages', 'pages')
        take('publisher', 'publisher'); take('place', 'address'); take('series', 'series'); take('ISBN', 'isbn')
    elif t == 'bookSection':
        take('bookTitle', 'booktitle'); take('pages', 'pages'); take('publisher', 'publisher'); take('place', 'address')
        take('ISBN', 'isbn'); take('series', 'series'); take('volume', 'volume'); take('edition', 'edition')
    elif t == 'book':
        take('publisher', 'publisher'); take('place', 'address'); take('edition', 'edition'); take('ISBN', 'isbn')
        take('series', 'series'); take('volume', 'volume')
        if e.get('numpages'):
            take('numPages', 'numpages')
    elif t == 'computerProgram':
        take('versionNumber', 'version'); take('company', 'publisher'); take('place', 'address')
    elif t == 'webpage':
        take('publisher', 'publisher'); take('place', 'address')
    elif t == 'preprint':
        hp = e.get('howpublished')
        em = re.search(r'arXiv:\s*(\S+)', hp) or re.search(r'Paper\s+(\d{4}/\d+)', hp)
        if e.get('eprinttype') == 'arXiv' or 'arXiv' in hp:
            f['repository'] = 'arXiv'
            f['archiveID'] = 'arXiv:' + (e.get('eprint') or (em.group(1) if em else ''))
            f['archiveID'] = f['archiveID'].rstrip(':')
        else:
            f['repository'] = g('howpublished').split(',')[0]
            f['archiveID'] = em.group(1) if em else ''
        used |= {'howpublished', 'eprint', 'eprinttype'}
        take('place', 'address'); take('publisher', 'publisher')
    else:   # document
        take('publisher', 'publisher'); take('place', 'address')
        if e.get('organization'):
            f['publisher'] = f.get('publisher') or g('organization')
            used.add('organization')
    return t, {k: v for k, v in f.items() if v}, used


def extra_lines(e, used, number, catalog, pdfs, abstract_source):
    lines = []
    if number is None:
        lines.append('Thesis reference: not cited in the thesis')
    lines.append(f'BibTeX type: {e.kind}')
    for name in sorted(set(e.fields) - used):
        lines.append(f'BibTeX {name}: {latex_to_text(e.fields[name])}')
    if catalog:
        for label, name in (('Catalogue id', 'id'), ('Reading status', 'status'), ('Priority', 'priority'),
                            ('Topic', 'topic')):
            if catalog.get(name):
                lines.append(f'{label}: {catalog[name]}')
        if catalog.get('keywords'):
            lines.append(f'Keywords (PDF title page): {catalog["keywords"]}')
    if abstract_source:
        lines.append(f'Abstract source: {abstract_source}')
    for p in pdfs:
        lines.append(f'Linked file: 01_Literature/library/{p}')
    return lines


# ------------------------------------------------------------------ catalogue
def load_catalogue(path=INDEX):
    if not path.exists():
        return {}, {}
    items = json.loads(path.read_text(encoding='utf-8-sig'))['items']
    by_file = {Path(i['file']).name: i for i in items if i.get('file')}
    by_key = {i['bib_key']: i for i in items if i.get('bib_key')}
    return by_key, by_file


def pdf_title_page(path):
    """Abstract and keywords from the first pages of a PDF (scripts/literature_index.extract)."""
    sys.path.insert(0, str(ROOT / 'scripts'))
    try:
        import literature_index
        return literature_index.extract(path)
    except Exception:   # PyMuPDF missing or unreadable file: no abstract rather than a wrong one
        return {'abstract': '', 'keywords': ''}


# ------------------------------------------------------------------------ RDF
NS = {'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#', 'z': 'http://www.zotero.org/namespaces/export#',
      'dc': 'http://purl.org/dc/elements/1.1/', 'dcterms': 'http://purl.org/dc/terms/',
      'bib': 'http://purl.org/net/biblio#', 'foaf': 'http://xmlns.com/foaf/0.1/',
      'link': 'http://purl.org/rss/1.0/modules/link/', 'schema': 'http://schema.org/'}
_BAD = re.compile('[\x00-\x08\x0b\x0c\x0e-\x1f\ufffe\uffff]')


def x(s):
    return escape(_BAD.sub('', str(s)))


def programmers(names):
    """Zotero's RDF import reads a computer program's programmers from schema:author."""
    out = []
    for fam, giv in names:
        given = f'<foaf:givenName>{x(giv)}</foaf:givenName>' if giv else ''
        out.append(f'    <schema:author><foaf:Person><foaf:surname>{x(fam)}</foaf:surname>{given}</foaf:Person></schema:author>')
    return '\n'.join(out)


def people(tag, names):
    if not names:
        return ''
    out = [f'    <{tag}><rdf:Seq>']
    for fam, giv in names:
        out.append('      <rdf:li><foaf:Person>')
        out.append(f'        <foaf:surname>{x(fam)}</foaf:surname>')
        if giv:
            out.append(f'        <foaf:givenName>{x(giv)}</foaf:givenName>')
        out.append('      </foaf:Person></rdf:li>')
    out.append(f'    </rdf:Seq></{tag}>')
    return '\n'.join(out)


def rdf_item(e, ztype, fields, number, extra, abstract, tags, note, pdfs):
    f = dict(fields)
    if number is not None:
        f['rights'] = f'[{number}]'
        if ztype in HAS_CALL_NUMBER:
            f['callNumber'] = f'[{number}]'
    f['extra'] = '\n'.join(extra)
    out = [f'  <rdf:Description rdf:about="#item_{x(e.key)}">', f'    <z:itemType>{ztype}</z:itemType>',
           f'    <dc:title>{x(f.pop("title"))}</dc:title>']
    authors, editors = split_names(e.get('author')), split_names(e.get('editor'))
    if authors:
        out.append(programmers(authors) if ztype == 'computerProgram' else people('bib:authors', authors))
    if editors:
        out.append(people('bib:editors', editors))
    if abstract:
        out.append(f'    <dcterms:abstract>{x(abstract)}</dcterms:abstract>')
    for name, value in f.items():
        out.append(f'    <z:{name}>{x(value)}</z:{name}>')
    for tag in tags:
        out.append(f'    <dc:subject>{x(tag)}</dc:subject>')
    if note:
        out.append('    <dcterms:isReferencedBy>')
        out.append(f'      <bib:Memo rdf:about="#note_{x(e.key)}"><rdf:value>{x(note)}</rdf:value></bib:Memo>')
        out.append('    </dcterms:isReferencedBy>')
    for n, fn in enumerate(pdfs, 1):
        out.append(f'    <link:link rdf:resource="#file_{x(e.key)}_{n}"/>')
    out.append('  </rdf:Description>')
    for n, fn in enumerate(pdfs, 1):
        out.append(f'  <z:Attachment rdf:about="#file_{x(e.key)}_{n}">')
        out.append('    <z:itemType>attachment</z:itemType>')
        out.append(f'    <rdf:resource rdf:resource="../01_Literature/library/{x(fn)}"/>')
        out.append(f'    <dc:title>{x(fn)}</dc:title>')
        out.append('    <z:linkMode>2</z:linkMode>')
        out.append('    <link:type>application/pdf</link:type>')
        out.append('  </z:Attachment>')
    return '\n'.join(s for s in out if s)


def bib_digest(text):
    return hashlib.sha256(text.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def build(bib_text, bbl_text, aux_text, library_files, catalogue, abstracts, overrides=None, source_keys=None):
    """-> (rdf text, report dict). `abstracts` maps filename -> {'abstract', 'keywords'}."""
    entries = parse_bib(bib_text)
    numbers, messages = ({}, ['reference numbers skipped']) if bbl_text is None else \
        reference_numbers(entries, bbl_text, aux_text)
    note = stale_note(numbers, source_keys)
    if note:
        messages.append(note)
    by_key, by_file = catalogue
    pdfs = assign_pdfs(entries, library_files, overrides)
    items, report = [], {'entries': len(entries), 'cited': len(numbers), 'with_pdf': 0, 'no_pdf': [], 'messages': messages,
                         'with_abstract': 0}
    for e in entries:
        files = pdfs[e.key]
        cat = by_key.get(e.key) or next((by_file[f] for f in files if f in by_file), None)
        title_page = next((abstracts[f] for f in files if f in abstracts), {})
        abstract = (cat or {}).get('abstract') or title_page.get('abstract', '')
        source = ''
        if abstract:
            source = 'PDF title page, extracted automatically (can include trailing front matter)'
            report['with_abstract'] += 1
        cat_view = dict(cat or {})
        if title_page.get('keywords') and not cat_view.get('keywords'):
            cat_view['keywords'] = title_page['keywords']
        ztype, fields, used = zotero_fields(e)
        number = numbers.get(e.key)
        extra = extra_lines(e, used, number, cat_view, files, source)
        tags = ['thesis:cited' if number is not None else 'thesis:uncited']
        if cat:
            tags += [f'status:{cat["status"]}'] if cat.get('status') else []
            tags += [f'topic:{cat["topic"]}'] if cat.get('topic') else []
            tags += [f'priority:{cat["priority"]}'] if cat.get('priority') else []
        note = ''
        if e.comment:
            note = ('<div><p><b>references.bib comment</b></p><p>'
                    + '</p><p>'.join(escape(c) for c in e.comment) + '</p></div>')   # HTML; rdf_item escapes it for XML
        items.append(rdf_item(e, ztype, fields, number, extra, abstract, tags, note, files))
        if files:
            report['with_pdf'] += 1
        else:
            report['no_pdf'].append(e.key)
    header = ('<?xml version="1.0" encoding="UTF-8"?>\n'
              f'<!-- Generated by {GENERATOR}; do not edit. Source: _shared/references.bib\n'
              f'     bib-sha256={bib_digest(bib_text)}\n'
              f'     entries={len(entries)} cited={len(numbers)} numbers-from={"03_Thesis/thesis.bbl" if bbl_text is not None else "none"}\n'
              '     Import with File > Import and "Link to files in original location". -->\n'
              '<rdf:RDF\n' + ''.join(f' xmlns:{p}="{u}"\n' for p, u in NS.items()).rstrip('\n') + '>\n')
    return header + '\n'.join(items) + '\n</rdf:RDF>\n', report


def read_text(path):
    return path.read_text(encoding='utf-8') if path.exists() else None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--out', type=Path, default=OUT)
    ap.add_argument('--check', action='store_true', help='exit 1 if --out was built from another references.bib')
    ap.add_argument('--no-numbers', action='store_true', help='build without reference numbers (no thesis.bbl)')
    ap.add_argument('--no-pdf-read', action='store_true', help='do not read abstracts from PDFs the catalogue lacks')
    args = ap.parse_args(argv)
    bib_text = BIB.read_text(encoding='utf-8')
    if args.check:
        have = re.search(r'bib-sha256=([0-9a-f]{64})', args.out.read_text(encoding='utf-8')[:600]) if args.out.exists() else None
        if not have or have.group(1) != bib_digest(bib_text):
            print(f'{args.out.name} is out of date: run python {GENERATOR}')
            return 1
        print(f'{args.out.name} matches references.bib')
        return 0
    bbl_text = None if args.no_numbers else read_text(BBL)
    if bbl_text is None and not args.no_numbers:
        print('03_Thesis/thesis.bbl is missing: compile the thesis first (or pass --no-numbers).', file=sys.stderr)
        return 2
    library_files = sorted(p.name for p in LIBRARY.glob('*.pdf'))
    catalogue = load_catalogue()
    entries = parse_bib(bib_text)
    pdfs = assign_pdfs(entries, library_files, read_overrides())
    abstracts = {}
    if not args.no_pdf_read:
        indexed = set(catalogue[1])
        for e in entries:
            cat = catalogue[0].get(e.key)
            if cat and cat.get('abstract'):
                continue
            for fn in pdfs[e.key][:1]:
                if fn not in indexed:
                    abstracts[fn] = pdf_title_page(LIBRARY / fn)
    try:
        rdf, report = build(bib_text, bbl_text, read_text(AUX), library_files, catalogue, abstracts, read_overrides(), source_citations())
    except ValueError as err:
        print(f'cannot number the entries: {err}', file=sys.stderr)
        return 2
    args.out.write_text(rdf, encoding='utf-8', newline='\n')
    print(f'{args.out}: {report["entries"]} entries, {report["cited"]} numbered, {report["with_pdf"]} with a PDF, '
          f'{report["with_abstract"]} with an abstract')
    print('no PDF:', ', '.join(report['no_pdf']))
    for m in report['messages']:
        print('note:', m)
    return 0


if __name__ == '__main__':
    sys.exit(main())
