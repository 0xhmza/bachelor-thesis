"""Turn the thesis review copy (03_Thesis/Thesis_Review-Copy.docx) into Google Docs
batchUpdate requests, one tab at a time.

    pandoc Thesis_Review-Copy.docx -t json -o review.json
    python gdocs_export.py plan review.json            # list the tabs and their sizes
    python gdocs_export.py build review.json KEY TABID OUT_PREFIX [--max N]
        writes OUT_PREFIX_01.json, _02.json ... : the `requests` of successive
        update_doc calls for tab KEY, to be sent in that order
    python gdocs_export.py expect review.json KEY       # the plain text the tab should hold
    python gdocs_export.py check review.json KEY DOC.json TABID   # compare with a read_doc result

Method: every block is inserted at index 1 of an empty tab, from the last block to
the first, and styled straight after its insert. Later inserts push earlier text
down without changing its offsets, so no index depends on a previous write and the
requests of one tab can be split over several calls in order. A table inserted at
index 1 leaves an empty paragraph before it, which the next text block (the one
above the table) fills, so no blank lines appear. Citations and cross-references
become plain text ([12], Section 4.2); external URLs stay links; figures keep
their caption with a note that the drawing is in the PDF; [TODO: ...] marks stay
bold on yellow, as in the review copy.
"""
import json, re, sys

SPACES = re.compile('[\u00a0\u2000-\u200a\u202f\u205f\u3000]')
INVIS = re.compile('[\u200b-\u200d\u00ad\ufeff\u2060]')

def clean(s):
    s = INVIS.sub('', SPACES.sub(' ', s))
    return s.replace('\u2011', '-')

def u16(s):
    return len(s.encode('utf-16-le')) // 2

# ---------------------------------------------------------------- inline text
def inline(xs, style=frozenset(), out=None):
    """Return list of (text, style, url) runs."""
    if out is None:
        out = []
    for x in xs:
        t = x.get('t'); c = x.get('c')
        if t == 'Str':
            out.append((clean(c), style, None))
        elif t in ('Space', 'SoftBreak', 'LineBreak'):
            out.append((' ', style, None))
        elif t == 'Strong':
            inline(c, style | {'b'}, out)
        elif t == 'Emph':
            inline(c, style | {'i'}, out)
        elif t == 'Underline':
            inline(c, style, out)
        elif t in ('Superscript', 'Subscript', 'SmallCaps', 'Strikeout'):
            inline(c, style, out)
        elif t == 'Code':
            out.append((clean(c[1]), style, None))
        elif t == 'Quoted':
            q = '“' if c[0]['t'] == 'DoubleQuote' else '‘'
            q2 = '”' if c[0]['t'] == 'DoubleQuote' else '’'
            out.append((q, style, None)); inline(c[1], style, out); out.append((q2, style, None))
        elif t == 'Span':
            cls = c[0][1]
            if 'anchor' in cls:
                continue
            inline(c[1], style | ({'todo'} if 'mark' in cls else set()), out)
        elif t == 'Link':
            url = c[2][0]
            if url.startswith('http'):
                sub = inline(c[1], style, [])
                out.extend((s, st, url) for s, st, _ in sub)
            else:
                inline(c[1], style, out)
        elif t == 'Math':
            out.append((c[1], style, None))
        elif t == 'Note':
            pass
        elif isinstance(c, list):
            inline(c, style, out)
    return out

def plain(xs):
    return ''.join(s for s, _, _ in inline(xs))

def merge(runs):
    """Concatenate runs into text plus style ranges [(start, end, style, url)]."""
    text = ''; spans = []
    for s, st, url in runs:
        if not s:
            continue
        a = u16(text); text += s; b = u16(text)
        if spans and spans[-1][2] == st and spans[-1][3] == url and spans[-1][1] == a:
            spans[-1] = (spans[-1][0], b, st, url)
        else:
            spans.append((a, b, st, url))
    # normalise whitespace
    return text, spans

CAPTION = re.compile(r'^(Figure|Table) ([A-Z]\.)?\d+(\.\d+)*\. ')
BULLET = re.compile(r'^[•–-] ')

def para_item(blocks_inlines, named='NORMAL_TEXT'):
    text, spans = merge(inline(blocks_inlines))
    item = {'k': 'p', 'text': text, 'spans': spans, 'named': named, 'bullet': False, 'cap': None}
    m = BULLET.match(text)
    if m and named == 'NORMAL_TEXT':
        cut = u16(m.group(0))
        item['text'] = text[len(m.group(0)):]
        item['spans'] = [(max(a - cut, 0), b - cut, st, u) for a, b, st, u in spans if b - cut > 0]
        item['bullet'] = True
    m = CAPTION.match(item['text'])
    if m and named == 'NORMAL_TEXT':
        item['cap'] = m.group(1)
    return item

def table_item(c):
    colspecs = c[2]; head = c[3]; bodies = c[4]; foot = c[5]
    C = len(colspecs)
    rows = []; hdr = 0
    def take(rowlist, is_head):
        nonlocal hdr
        for row in rowlist:
            cells = row[1]; out = []
            for cell in cells:
                colspan = cell[3]
                txt = ' '.join(plain(b['c']) if b['t'] in ('Plain', 'Para') else '' for b in cell[4]).strip()
                txt = re.sub(r'\s+', ' ', clean(txt))
                out.append(txt)
                out.extend([''] * (colspan - 1))
            out = (out + [''] * C)[:C]
            rows.append(out)
            if is_head:
                hdr += 1
    take(head[1], True)
    for body in bodies:
        take(body[2], True)   # intermediate head rows
        take(body[3], False)
    take(foot[1], False)
    if hdr == 0 and rows:
        hdr = 1  # first row of the review copy is the header row
    return {'k': 't', 'rows': rows, 'hdr': hdr}

# ---------------------------------------------------------------- split into tabs
def load(path):
    return json.load(open(path))['blocks']

def plan(blocks):
    """Return ordered list of tab dicts: key, title, parent, items (raw blocks), level offset."""
    tabs = []; cur = None
    def new(key, title, parent, shift):
        nonlocal cur
        cur = {'key': key, 'title': title, 'parent': parent, 'shift': shift, 'blocks': []}
        tabs.append(cur)
    chapter = None
    for b in blocks:
        if b['t'] == 'Header':
            lvl = b['c'][0]; title = plain(b['c'][2])
            if lvl == 1:
                chapter = title
                if title.startswith('Appendix') or title == 'AI Appendix':
                    new('app-' + (title.split(':')[0].split()[-1] if ':' in title else 'AI'), title, 'appendices', 0)
                elif title == 'Bibliography':
                    new('references', 'References', 'paper', 0)
                else:
                    key = title.split()[0] if title[0].isdigit() else title.lower()
                    new('ch' + key if key[0].isdigit() else key, title, 'paper', 0)
            elif lvl == 2 and chapter and chapter.startswith('4 '):
                new('m' + title.split()[0], title, 'ch4', 1)
        if cur is not None:
            cur['blocks'].append(b)
    return tabs

def items_of(tab):
    out = []
    for b in tab['blocks']:
        t = b['t']
        if t == 'Header':
            lvl = max(1, b['c'][0] - tab['shift'])
            if tab['key'] == 'references':
                out.append(para_item(b['c'][2], 'HEADING_1')); out[-1]['text'] = 'References'; out[-1]['spans'] = [(0, 10, frozenset(), None)]
                continue
            out.append(para_item(b['c'][2], 'HEADING_%d' % min(lvl, 6)))
        elif t in ('Para', 'Plain'):
            it = para_item(b['c'])
            if not it['text'].strip():
                continue
            out.append(it)
        elif t == 'Table':
            out.append(table_item(b['c']))
        elif t in ('BulletList', 'OrderedList'):
            for li in (b['c'] if t == 'BulletList' else b['c'][1]):
                for bb in li:
                    if bb['t'] in ('Para', 'Plain'):
                        it = para_item(bb['c']); it['bullet'] = True; out.append(it)
    return out

# ---------------------------------------------------------------- requests
RESET = 'bold,italic,underline,strikethrough,smallCaps,backgroundColor,foregroundColor,link,fontSize,weightedFontFamily,baselineOffset'
YELLOW = {'color': {'rgbColor': {'red': 1, 'green': 0.95, 'blue': 0.4}}}
BLUE = {'color': {'rgbColor': {'red': 0.07, 'green': 0.33, 'blue': 0.8}}}
GREY = {'color': {'rgbColor': {'red': 0.4, 'green': 0.4, 'blue': 0.4}}}

def rng(a, b, tab):
    return {'startIndex': a, 'endIndex': b, 'tabId': tab}

def text_group_requests(paras, tab, fill_empty):
    """Insert consecutive paragraphs at index 1. fill_empty: the paragraph now at 1 is
    empty (tab start or the paragraph before a table), so no trailing newline."""
    text = '\n'.join(p['text'] for p in paras) + ('' if fill_empty else '\n')
    L = u16(text)
    req = [{'insertText': {'location': {'index': 1, 'tabId': tab}, 'text': text}}]
    end_par = L + 1 + (1 if fill_empty else 0)   # through the last paragraph's newline
    req.append({'deleteParagraphBullets': {'range': rng(1, end_par, tab)}})
    req.append({'updateParagraphStyle': {'range': rng(1, end_par, tab),
                'paragraphStyle': {'namedStyleType': 'NORMAL_TEXT'}, 'fields': 'namedStyleType'}})
    req.append({'updateTextStyle': {'range': rng(1, 1 + max(L - (0 if fill_empty else 1), 1), tab), 'textStyle': {}, 'fields': RESET}})
    pos = 1; bullets = []
    for p in paras:
        n = u16(p['text'])
        if p['cap'] and n:
            req.append({'updateTextStyle': {'range': rng(pos, pos + n, tab), 'textStyle': {'italic': True}, 'fields': 'italic'}})
        for a, b, st, url in p['spans']:
            ts = {}; f = []
            if 'b' in st: ts['bold'] = True; f.append('bold')
            if 'i' in st: ts['italic'] = True; f.append('italic')
            if 'todo' in st:
                ts['bold'] = True; ts['backgroundColor'] = YELLOW; f += ['bold', 'backgroundColor']
            if 'note' in st:
                ts['italic'] = True; ts['foregroundColor'] = GREY; f += ['italic', 'foregroundColor']
            if url:
                ts['link'] = {'url': url}; ts['foregroundColor'] = BLUE; ts['underline'] = True
                f += ['link', 'foregroundColor', 'underline']
            if f and b > a:
                req.append({'updateTextStyle': {'range': rng(pos + a, pos + b, tab), 'textStyle': ts,
                            'fields': ','.join(dict.fromkeys(f))}})
        pos += n + 1
    return req

def final_pass(items, tab):
    """Headings and bullets at their final positions, after every insert of the tab."""
    req = []; pos = 1; prev = None; bullets = []
    for it in items:
        if it['k'] == 'p':
            n = u16(it['text'])
            if it['named'] != 'NORMAL_TEXT':
                req.append({'updateParagraphStyle': {'range': rng(pos, pos + n + 1, tab),
                            'paragraphStyle': {'namedStyleType': it['named']}, 'fields': 'namedStyleType'}})
            if it['bullet']:
                if bullets and bullets[-1][1] == pos:
                    bullets[-1][1] = pos + n + 1
                else:
                    bullets.append([pos, pos + n + 1])
            pos += n + 1
        else:
            if prev is None or prev == 't':
                pos += 1                      # the empty paragraph Google keeps before a table
            R = len(it['rows']); C = len(it['rows'][0])
            pos += R * (2 * C + 1) + sum(u16(x) for row in it['rows'] for x in row) + 2
        prev = it['k']
    for a, b in bullets:
        req.append({'createParagraphBullets': {'range': rng(a, b, tab), 'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'}})
    return req

def table_requests(t, tab):
    rows = t['rows']; R = len(rows); C = len(rows[0])
    req = [{'insertTable': {'rows': R, 'columns': C, 'location': {'index': 1, 'tabId': tab}}}]
    S = 0
    for r in range(R - 1, -1, -1):
        for c in range(C - 1, -1, -1):
            s = rows[r][c]
            if s:
                req.append({'insertText': {'location': {'index': 5 + r * (2 * C + 1) + 2 * c, 'tabId': tab}, 'text': s}})
                S += u16(s)
    end = 4 + R * (2 * C + 1) + S        # index of the paragraph after the table
    req.append({'updateParagraphStyle': {'range': rng(1, end, tab),
                'paragraphStyle': {'namedStyleType': 'NORMAL_TEXT'}, 'fields': 'namedStyleType'}})
    req.append({'updateTextStyle': {'range': rng(5, end - 1, tab), 'textStyle': {}, 'fields': RESET}})
    # header rows bold: rows 0..hdr-1 end where row hdr's first cell paragraph starts
    hdr = min(t['hdr'], R)
    if hdr:
        hl = sum(u16(rows[r][c]) for r in range(hdr) for c in range(C))
        hend = 5 + hdr * (2 * C + 1) + hl - 3
        if hl:
            req.append({'updateTextStyle': {'range': rng(5, hend + 1, tab), 'textStyle': {'bold': True}, 'fields': 'bold'}})
    return req

def build(items, tab, maxlen=18000):
    """Requests for one tab, split into calls of at most ~maxlen characters of JSON."""
    calls = []; cur = []; size = 0
    fill_empty = True
    i = len(items)
    groups = []
    while i > 0:
        if items[i - 1]['k'] == 't':
            groups.append(('t', items[i - 1])); i -= 1
        else:
            j = i
            while j > 0 and items[j - 1]['k'] == 'p':
                j -= 1
            groups.append(('p', items[j:i])); i = j
    # each group may itself be too large: split text groups into smaller runs (from the end)
    expanded = []
    for kind, g in groups:
        if kind == 'p':
            chunk = []; csize = 0
            for p in reversed(g):
                psize = len(p['text']) + 150 * (1 + len(p['spans']))
                if chunk and csize + psize > maxlen * 0.8:
                    expanded.append(('p', list(reversed(chunk)))); chunk = []; csize = 0
                chunk.append(p); csize += psize
            if chunk:
                expanded.append(('p', list(reversed(chunk))))
        else:
            expanded.append((kind, g))
    for kind, g in expanded:
        if kind == 't':
            r = table_requests(g, tab); nxt = True
        else:
            r = text_group_requests(g, tab, fill_empty); nxt = False
        js = len(json.dumps(r, ensure_ascii=False))
        if cur and size + js > maxlen:
            calls.append(cur); cur = []; size = 0
        cur += r; size += js
        fill_empty = nxt
    fp = final_pass(items, tab)
    if cur and size + len(json.dumps(fp)) > maxlen * 1.3:
        calls.append(cur); cur = []
    cur += fp
    if cur:
        calls.append(cur)
    return calls

def expect(items):
    lines = []
    for it in items:
        if it['k'] == 'p':
            lines.append(it['text'])
        else:
            for row in it['rows']:
                lines.extend(row)
    return '\n'.join(x for x in lines if x)

def doc_text(doc, tabid):
    def find(ts):
        for t in ts:
            if t['tabProperties']['tabId'] == tabid:
                return t
            r = find(t.get('childTabs', []))
            if r:
                return r
    t = find(doc['tabs'])
    out = []
    def walk(content):
        for c in content:
            if 'paragraph' in c:
                s = ''.join(e.get('textRun', {}).get('content', '') for e in c['paragraph']['elements']).rstrip('\n')
                if s:
                    out.append(s)
            elif 'table' in c:
                for row in c['table']['tableRows']:
                    for cell in row['tableCells']:
                        walk(cell['content'])
    walk(t['documentTab']['body']['content'])
    return '\n'.join(out)

if __name__ == '__main__':
    cmd = sys.argv[1]; blocks = load(sys.argv[2]); tabs = plan(blocks)
    if cmd == 'plan':
        for t in tabs:
            its = items_of(t)
            calls = build(its, 't.x')
            print(f"{t['key']:12s} parent={t['parent']:11s} items={len(its):4d} calls={len(calls)} "
                  f"json={sum(len(json.dumps(c, ensure_ascii=False)) for c in calls):7d}  {t['title']}")
    elif cmd == 'build':
        key, tabid, prefix = sys.argv[3:6]
        mx = int(sys.argv[sys.argv.index('--max') + 1]) if '--max' in sys.argv else 18000
        t = [x for x in tabs if x['key'] == key][0]
        calls = build(items_of(t), tabid, mx)
        for n, c in enumerate(calls, 1):
            json.dump(c, open(f'{prefix}_{n:02d}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
        print(len(calls), 'calls', [len(json.dumps(c, ensure_ascii=False, separators=(',', ':'))) for c in calls])
    elif cmd == 'expect':
        t = [x for x in tabs if x['key'] == sys.argv[3]][0]
        print(expect(items_of(t)))
    elif cmd == 'check':
        t = [x for x in tabs if x['key'] == sys.argv[3]][0]
        doc = json.load(open(sys.argv[4]))
        doc = doc.get('content', doc)
        a = expect(items_of(t)); b = doc_text(doc, sys.argv[5])
        if a == b:
            print('MATCH', len(a), 'chars')
        else:
            import difflib
            print('DIFF'); sys.stdout.writelines(list(difflib.unified_diff(a.splitlines(1), b.splitlines(1), n=1))[:60])
