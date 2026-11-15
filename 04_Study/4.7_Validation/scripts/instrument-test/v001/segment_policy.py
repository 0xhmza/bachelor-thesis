"""Split the archived privacy policy into coding units (Section "Coding Units").

    python segment_policy.py <policy.html> <units.jsonl>

A unit is one paragraph. A list stays with the sentence that introduces it, as
codebook rule 1 demands. Each unit keeps its nearest heading and the hash of the
archived document, so that an evidence span can be checked against the source.
"""
import hashlib
import json
import re
import sys

from bs4 import BeautifulSoup

HEADINGS = {'h1': 1, 'h2': 2, 'h3': 3, 'h4': 4}


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def blocks(html):
    """Yield (kind, text) for headings, paragraphs, lists and tables in order."""
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(['script', 'style', 'noscript', 'svg', 'nav', 'footer', 'header']):
        tag.decompose()
    root = soup.find('main') or soup.body
    for el in root.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol', 'table']):
        if el.find_parent(['ul', 'ol', 'table']) is not None:
            continue
        text = clean(el.get_text(' '))
        if not text:
            continue
        if el.name in HEADINGS:
            yield el.name, text
        elif el.name in ('ul', 'ol'):
            items = [clean(li.get_text(' ')) for li in el.find_all('li', recursive=False)]
            yield 'list', ' | '.join(i for i in items if i)
        elif el.name == 'table':
            rows = [' ; '.join(clean(c.get_text(' ')) for c in r.find_all(['td', 'th']))
                    for r in el.find_all('tr')]
            yield 'list', ' | '.join(r for r in rows if r)
        else:
            yield 'p', text


def units(html):
    """Group blocks into units; a list joins the paragraph before it."""
    heading = ''
    out = []
    for kind, text in blocks(html):
        if kind in HEADINGS:
            heading = text  # the page's heading levels are not consistent
            continue
        if kind == 'list' and out and out[-1]['heading'] == heading:
            out[-1]['text'] += ' ' + text
        else:
            out.append({'heading': heading, 'text': text})
    for i, unit in enumerate(out, 1):
        unit['unit'] = f'U{i:03d}'
    return out


def main(src, dst):
    raw = open(src, 'rb').read()
    us = units(raw.decode('utf-8', 'replace'))
    digest = hashlib.sha256(raw).hexdigest()
    with open(dst, 'w', encoding='utf-8') as f:
        for u in us:
            u['source_sha256'] = digest
            f.write(json.dumps(u, ensure_ascii=False) + '\n')
    print(f'{len(us)} units, {sum(len(u["text"].split()) for u in us)} words, sha256 {digest}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
