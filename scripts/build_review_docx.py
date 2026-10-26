"""Build the supervisor's review copy of the thesis as a Word document.

    python scripts/build_review_docx.py            # from the working tree
    python scripts/build_review_docx.py --staged   # from the git index (used by the hook)
    python scripts/build_review_docx.py --text     # also print the plain text (for checks)

Writes 03_Thesis/Thesis_Review-Copy.docx. The LaTeX sources stay authoritative:
this script reads thesis.tex, the chapter and appendix files it inputs and
_shared/references.bib, and writes a .docx the supervisor can annotate with
Word comments or tracked changes. Citations become numbered [n] links that jump
to a bookmark on the bibliography entry (numbering as biblatex numeric-comp,
sorting=nyt); entries link to their DOI or URL. \\ref/\\Cref become internal
links. TikZ figures are replaced by their \\Description text.

The pre-commit hook (scripts/hooks/pre-commit) runs this with --staged whenever
a commit touches the thesis sources, and adds the result to the same commit, so
the copy in the repository always matches the committed draft. Only the Python
standard library is used, so the hook never fails on a missing package.
"""
import datetime
import html
import os
import re
import subprocess
import sys
import unicodedata
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THESIS_DIR = os.path.join(ROOT, '03_Thesis')
OUT = os.path.join(THESIS_DIR, 'Thesis_Review-Copy.docx')
BIB = os.path.join(ROOT, '_shared', 'references.bib')
BS = chr(92)


STAGED = '--staged' in sys.argv


def git(*args):
    try:
        return subprocess.run(['git', *args], cwd=ROOT, capture_output=True, timeout=20)
    except Exception:
        return None


def read(path):
    """Read a source file from the working tree, or from the git index with --staged."""
    if STAGED:
        rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
        res = git('show', ':' + rel)
        if res is not None and res.returncode == 0:
            return res.stdout.decode('utf8')
    with open(path, encoding='utf8') as fh:
        return fh.read()


def exists(path):
    if STAGED:
        rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
        res = git('cat-file', '-e', ':' + rel)
        if res is not None and res.returncode == 0:
            return True
    return os.path.exists(path)


def strip_comments(s):
    return re.sub(r'(?<!\\)%.*', '', s)


# ===================================================================== metadata
def metadata():
    meta = {}
    for m in re.finditer(r'\\newcommand\{\\(\w+)\}\{([^}]*)\}', read(os.path.join(THESIS_DIR, 'config', 'metadata.tex'))):
        meta[m.group(1)] = m.group(2)
    return meta


def git_stamp():
    """One sentence for the first page saying which draft this copy shows."""
    def run(*args):
        res = git(*args)
        return res.stdout.decode('utf8', 'replace').strip() if res is not None and res.returncode == 0 else ''
    head = run('rev-parse', '--short', 'HEAD') or 'unknown'
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    if STAGED:  # the commit being made has no hash yet
        return head, f'Generated automatically from the LaTeX sources of the commit made on {now} (the commit after {head}).'
    sources = ['03_Thesis/thesis.tex', '03_Thesis/chapters', '03_Thesis/appendix', '03_Thesis/config',
               '_shared/references.bib']
    dirty = bool(run('status', '--porcelain', '--', *sources))
    date = run('log', '-1', '--format=%cd', '--date=format:%Y-%m-%d %H:%M')
    return head, (f'Generated automatically from the LaTeX sources at commit {head} ({date})'
                  + (', plus uncommitted edits.' if dirty else '.'))


# ================================================================= bibliography
ACCENTS = {("'", 'e'): 'é', ("'", 'E'): 'É', ('"', 'o'): 'ö', ('"', 'u'): 'ü', ('"', 'a'): 'ä', ('"', 'O'): 'Ö',
           ('"', 'U'): 'Ü', ('"', 'A'): 'Ä', ("'", 'a'): 'á', ("'", 'i'): 'í', ("'", 'o'): 'ó', ('`', 'e'): 'è'}


def bib_clean(s):
    s = re.sub(r'\\mkbibquote\{(.*?)\}', '\u201c\\1\u201d', s, flags=re.S)
    s = re.sub(r'\{\\([\'"`])(\w)\}', lambda m: ACCENTS.get((m.group(1), m.group(2)), m.group(2)), s)
    s = re.sub(r'\\([\'"`])\{?(\w)\}?', lambda m: ACCENTS.get((m.group(1), m.group(2)), m.group(2)), s)
    s = re.sub(r'\{\\u (\w)\}', lambda m: 'ğ' if m.group(1) == 'g' else m.group(1), s)
    s = s.replace(BS + '&', '&').replace('---', '\u2014').replace('--', '\u2013')
    s = s.replace('``', '\u201c').replace("''", '\u201d').replace('`', '\u2018').replace("'", '\u2019')
    s = s.replace('~', '\u00a0')
    s = re.sub(r'[{}]', '', s)
    return re.sub(r'\s+', ' ', s).strip()


def parse_bib():
    entries = {}
    text = read(BIB)
    for m in re.finditer(r'@(\w+)\s*\{\s*([^,\s]+)\s*,', text):
        kind, key = m.group(1).lower(), m.group(2)
        i, depth = m.end(), 1
        while i < len(text) and depth:
            depth += {'{': 1, '}': -1}.get(text[i], 0)
            i += 1
        body = text[m.end():i - 1]
        fields = {}
        for f in re.finditer(r'(\w+)\s*=\s*', body):
            j = f.end()
            if j < len(body) and body[j] == '{':
                d, k = 0, j
                while k < len(body):
                    d += {'{': 1, '}': -1}.get(body[k], 0)
                    k += 1
                    if d == 0:
                        break
                fields.setdefault(f.group(1).lower(), body[j + 1:k - 1])
            elif j < len(body) and body[j] == '"':
                k = body.index('"', j + 1)
                fields.setdefault(f.group(1).lower(), body[j + 1:k])
        entries[key] = (kind, fields)
    return entries


def split_names(a):
    parts, depth, cur = [], 0, ''
    for tok in re.split(r'(\{|\}|\s+and\s+)', a):
        if tok == '{':
            depth += 1
        elif tok == '}':
            depth -= 1
        if depth == 0 and tok and re.fullmatch(r'\s+and\s+', tok):
            parts.append(cur)
            cur = ''
        else:
            cur += tok or ''
    parts.append(cur)
    names = []
    for p in parts:
        p = p.strip()
        if p.startswith('{'):
            names.append(('', bib_clean(p)))
        elif ',' in p:
            last, first = p.split(',', 1)
            names.append((bib_clean(first), bib_clean(last)))
        elif p:
            bits = p.split()
            names.append((bib_clean(' '.join(bits[:-1])), bib_clean(bits[-1])))
    return names


def sort_key(fields):
    names = split_names(fields.get('author', fields.get('editor', '')))
    fam = ' '.join(last for _, last in names)
    norm = unicodedata.normalize('NFKD', fam).encode('ascii', 'ignore').decode().lower()
    year = (fields.get('date') or fields.get('year') or '')[:4]
    title = bib_clean(fields.get('title', '')).lower()
    return (norm, year, title)


def format_entry(kind, f):
    names = split_names(f.get('author', f.get('editor', '')))
    shown = [(first + ' ' + last).strip() for first, last in names]
    who = shown[0] if len(shown) == 1 else ', '.join(shown[:-1]) + ' and ' + shown[-1] if shown else ''
    year = (f.get('date') or f.get('year') or 'n.d.')[:4]
    runs = [(f'{who} ({year}). {bib_clean(f.get("title", ""))}. ', set())]
    if 'journal' in f:
        runs.append((bib_clean(f['journal']), {'i'}))
        tail = (' ' + f['volume'] if 'volume' in f else '') + (f'({bib_clean(f["number"])})' if 'number' in f else '')
        tail += (', ' + bib_clean(f['pages']) if 'pages' in f else '')
        runs.append((tail, set()))
    elif 'booktitle' in f:
        runs.append(('In ', set()))
        runs.append((bib_clean(f['booktitle']), {'i'}))
        runs.append(((', pp. ' + bib_clean(f['pages']) if 'pages' in f else '')
                     + ('. ' + bib_clean(f['publisher']) if 'publisher' in f else ''), set()))
    elif 'howpublished' in f:
        runs.append((bib_clean(f['howpublished']), set()))
    elif 'organization' in f or 'institution' in f:
        runs.append((bib_clean(f.get('organization', f.get('institution', ''))), set()))
    else:
        bits = []
        if 'edition' in f:
            bits.append(f['edition'] + 'th ed.')
        if 'publisher' in f:
            bits.append(bib_clean(f['publisher']) + (', ' + bib_clean(f['address']) if 'address' in f else ''))
        runs.append((' '.join(bits), set()))
    for extra in ('addendum', 'note'):
        if extra in f:
            runs.append(('. ' + bib_clean(f[extra]).rstrip('.'), set()))
    runs.append(('.', set()))
    link = None
    if 'doi' in f:
        link = 'https://doi.org/' + f['doi'].strip()
    elif 'url' in f:
        link = f['url'].strip()
    return runs, link


# ======================================================================= inline
class Ctx:
    """Shared state while rendering: labels, citation numbers, link targets."""

    def __init__(self):
        self.labels = {}       # label -> (display text, bookmark)
        self.cite_order = []   # keys in order of first citation
        self.cite_num = {}     # key -> number, set before rendering


def find_close(s, i):
    depth = 0
    for j in range(i, len(s)):
        if s[j] == '{' and (j == 0 or s[j - 1] != BS):
            depth += 1
        elif s[j] == '}' and (j == 0 or s[j - 1] != BS):
            depth -= 1
            if depth == 0:
                return j
    return len(s) - 1


SIMPLE = [('---', '\u2014'), ('--', '\u2013'), ('``', '\u201c'), ("''", '\u201d'), ('~', '\u00a0'),
          (BS + ',', '\u202f'), (BS + '%', '%'), (BS + '&', '&'), (BS + '_', '_'), (BS + '#', '#'),
          (BS + '$', '$'), (BS + ' ', ' '), ('{,}', ',')]
MATH = {'kappa': 'κ', 'alpha': 'α', 'times': '×', 'leq': '≤', 'geq': '≥', 'approx': '≈', 'rightarrow': '→',
        'to': '→', 'ge': '≥', 'le': '≤', 'pm': '±', 'cdot': '·'}
DROP_WITH_ARG = {'label', 'Description', 'addcontentsline', 'setlength', 'vspace', 'hspace', 'arrayrulecolor',
                 'cmidrule', 'phantomsection', 'index'}
FORMAT = {'textbf': 'b', 'emph': 'i', 'textit': 'i', 'texttt': 'mono', 'path': 'mono', 'textsc': '', 'textrm': '', 'mbox': '',
          'text': '', 'textsf': '', 'underline': 'u', 'textcolor': ''}


def inline(s, ctx, fmt=frozenset()):
    """LaTeX fragment -> list of runs (text, fmt, link). link is ('ext', url) or ('int', bookmark)."""
    runs = []
    i, buf = 0, ''

    def flush():
        nonlocal buf
        if buf:
            runs.append((buf, fmt, None))
            buf = ''

    while i < len(s):
        c = s[i]
        hit = next(((a, b) for a, b in SIMPLE if s.startswith(a, i)), None)
        if hit:
            buf += hit[1]
            i += len(hit[0])
            continue
        if c == '$':
            j = s.find('$', i + 1)
            j = len(s) if j < 0 else j
            math = re.sub(r'\\(\w+)', lambda m: MATH.get(m.group(1), m.group(1)), s[i + 1:j])
            buf += re.sub(r'[{}^_]', '', math)
            i = j + 1
            continue
        if c in '{}':
            i += 1
            continue
        if c == BS:
            if s.startswith(BS + BS, i):
                flush()
                runs.append(('\n', fmt, None))
                i += 2
                continue
            m = re.match(r'\\([a-zA-Z]+)\*?', s[i:])
            if not m:
                buf += s[i + 1:i + 2]
                i += 2
                continue
            name = m.group(1)
            j = i + m.end()
            opt = None
            if j < len(s) and s[j] == '[':
                k = s.find(']', j)
                opt, j = s[j + 1:k], k + 1
            arg = None
            if j < len(s) and s[j] == '{':
                k = find_close(s, j)
                arg, j = s[j + 1:k], k + 1
            if name == 'S':
                buf += '§'
                i = j if arg is None else i + m.end()
                continue
            if name in MATH and arg is None:
                buf += MATH[name]
                i = j
                continue
            if name in ('parencite', 'cite', 'autocite', 'textcite', 'parencites') and arg is not None:
                prev = buf or (runs[-1][0] if runs else '')
                flush()
                keys = [k.strip() for k in arg.split(',') if k.strip()]
                spaced = prev.endswith((' ', '\u00a0', '(')) or not prev
                runs.append(('[' if spaced else '\u00a0[', fmt, None))
                for key in keys:
                    if key not in ctx.cite_order:
                        ctx.cite_order.append(key)
                # numeric-comp: sorted, three or more consecutive numbers compressed to a range
                nums = sorted({ctx.cite_num[k] for k in keys if k in ctx.cite_num}) or ['?']
                groups = []
                for num in nums:
                    if groups and isinstance(num, int) and num == groups[-1][-1] + 1:
                        groups[-1].append(num)
                    else:
                        groups.append([num])
                for n, grp in enumerate(groups):
                    if n:
                        runs.append((', ', fmt, None))
                    shown = [grp[0], grp[-1]] if len(grp) >= 3 else grp
                    for m_i, num in enumerate(shown):
                        if m_i:
                            runs.append(('\u2013' if len(grp) >= 3 else ', ', fmt, None))
                        runs.append((str(num), fmt, ('int', f'ref_{num}')))
                if opt:
                    runs.extend((t, fmt | f2, l) for t, f2, l in inline(', ' + opt, ctx))
                runs.append((']', fmt, None))
                i = j
                continue
            if name in ('ref', 'Cref', 'cref', 'autoref', 'pageref') and arg is not None:
                flush()
                text, mark = ctx.labels.get(arg, ('??', None))
                if name == 'ref':
                    text = text.split(' ', 1)[-1]
                elif name == 'cref':
                    text = text[0].lower() + text[1:]
                runs.append((text, fmt, ('int', mark) if mark else None))
                i = j
                continue
            if name == 'enquote' and arg is not None:
                flush()
                runs.append(('\u201c', fmt, None))
                runs.extend(inline(arg, ctx, fmt))
                runs.append(('\u201d', fmt, None))
                i = j
                continue
            if name == 'todo' and arg is not None:
                flush()
                runs.extend((t, f | {'todo', 'b'}, l) for t, f, l in inline('[TODO: ' + arg + ']', ctx, fmt))
                i = j
                continue
            if name == 'href' and arg is not None:
                url = arg
                k = j
                if k < len(s) and s[k] == '{':
                    e = find_close(s, k)
                    flush()
                    runs.extend((t, f, ('ext', url)) for t, f, _ in inline(s[k + 1:e], ctx, fmt))
                    i = e + 1
                    continue
            if name == 'url' and arg is not None:
                flush()
                runs.append((arg, fmt, ('ext', arg)))
                i = j
                continue
            if name == 'multicolumn' and arg is not None:  # \multicolumn{n}{spec}{text}: keep the text
                k = find_close(s, j)
                e = find_close(s, k + 1)
                flush()
                runs.extend(inline(s[k + 2:e], ctx, fmt))
                i = e + 1
                continue
            if name in FORMAT and arg is not None:
                flush()
                if name == 'textcolor':  # \textcolor{red}{x}: arg is the colour, next group the text
                    k = j
                    if k < len(s) and s[k] == '{':
                        e = find_close(s, k)
                        runs.extend(inline(s[k + 1:e], ctx, fmt))
                        i = e + 1
                        continue
                add = FORMAT[name]
                runs.extend(inline(arg, ctx, fmt | ({add} if add else set())))
                i = j
                continue
            if name in DROP_WITH_ARG:
                i = j
                continue
            if name in ('noindent', 'centering', 'raggedright', 'arraybackslash', 'small', 'footnotesize',
                        'scriptsize', 'normalfont', 'bfseries', 'itshape', 'ttfamily', 'par', 'smallskip',
                        'medskip', 'bigskip', 'newline', 'hfill', 'clearpage', 'item', 'rowrule', 'midrule',
                        'toprule', 'bottomrule', 'addlinespace', 'hline'):
                if name in ('newline',):
                    buf += '\n'
                i = i + m.end() if arg is None else j
                if arg is not None and name not in ('rowrule',):
                    # e.g. \small{...}: keep the text
                    runs_inner = inline(arg, ctx, fmt)
                    flush()
                    runs.extend(runs_inner)
                continue
            # unknown command: keep its argument text
            flush()
            if arg is not None:
                runs.extend(inline(arg, ctx, fmt))
            i = j if arg is not None else i + m.end()
            continue
        if c == '\n':
            buf += ' '
            i += 1
            continue
        buf += c
        i += 1
    flush()
    merged = []
    for t, f, l in runs:
        t = re.sub(r'[ \t]{2,}', ' ', t)
        if merged and merged[-1][1] == f and merged[-1][2] == l and l is None:
            merged[-1] = (merged[-1][0] + t, f, l)
        else:
            merged.append((t, f, l))
    if merged:
        merged[0] = (merged[0][0].lstrip(), merged[0][1], merged[0][2])
        merged[-1] = (merged[-1][0].rstrip(), merged[-1][1], merged[-1][2])
    return [r for r in merged if r[0]]


# ======================================================================= blocks
class Doc:
    def __init__(self):
        self.blocks = []          # (kind, payload)
        self.chapter = 0
        self.appendix = False
        self.section = 0
        self.subsection = 0
        self.fig = 0
        self.tab = 0
        self.bm = 0

    def chapter_no(self):
        return chr(64 + self.chapter) if self.appendix else str(self.chapter)


def group_arg(s, start):
    """Return (content, end) of the {...} group starting at s[start] == '{'."""
    end = find_close(s, start)
    return s[start + 1:end], end + 1


def labels_in(s):
    return re.findall(r'\\label\{([^}]*)\}', s)


def parse_tabular(body):
    m = re.search(r'\\begin\{(tabularx|tabular)\}', body)
    if not m:
        return []
    i = m.end()
    if m.group(1) == 'tabularx':
        _, i = group_arg(body, body.index('{', i))
    _, i = group_arg(body, body.index('{', i))
    end = body.index(BS + 'end{' + m.group(1) + '}', i)
    t = body[i:end]
    t = re.sub(r'\\(toprule|midrule|bottomrule|rowrule|addlinespace|hline)(\[[^\]]*\])?', '', t)
    t = re.sub(r'\\cmidrule(\[[^\]]*\])?(\([^)]*\))?\{[^}]*\}', '', t)
    rows = []
    for row in re.split(r'\\\\(?:\[[^\]]*\])?', t):
        if not row.strip():
            continue
        cells, depth, cur = [], 0, ''
        for ch_i, ch in enumerate(row):
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
            if ch == '&' and depth == 0 and (ch_i == 0 or row[ch_i - 1] != BS):
                cells.append(cur)
                cur = ''
            else:
                cur += ch
        cells.append(cur)
        rows.append([c.strip() for c in cells])
    return rows


def longtable_as_table(body):
    """A longtable as a table holding one tabular: its first head, then its rows,
    with generated row files (\\input{tables/...}) read in."""
    def rows_file(m):
        path = os.path.join(THESIS_DIR, m.group(1) + ('' if m.group(1).endswith('.tex') else '.tex'))
        return strip_comments(read(path)) if exists(path) else ''
    body = re.sub(r'\\input\{([^}]*)\}', rows_file, body)
    body = re.sub(r'\\rowcolor\{[^}]*\}', '', body)
    head, _, rest = body.partition(BS + 'endfirsthead')
    caption, _, head = head.partition(BS + BS)  # \begin{longtable}{...}\caption{...}\label{...}\\
    rows = rest.split(BS + 'endfoot', 1)[-1].split(BS + 'end{longtable}')[0]
    return caption + '\n' + BS + 'begin{tabular}{l}' + head + rows + BS + 'end{tabular}'


def env_body(lines, i, env):
    """Collect lines from index i (which holds \\begin{env}) to the matching \\end{env}."""
    depth, buf, j = 0, [], i
    while j < len(lines):
        depth += lines[j].count(BS + 'begin{' + env + '}') - lines[j].count(BS + 'end{' + env + '}')
        buf.append(lines[j])
        if depth <= 0:
            break
        j += 1
    return '\n'.join(buf), j


def caption_of(body):
    k = body.find(BS + 'caption')
    if k < 0:
        return ''
    k = body.index('{', k)
    cap, _ = group_arg(body, k)
    return cap


def parse_items(body):
    inner = re.sub(r'^\\begin\{\w+\}(\[[^\]]*\])?', '', body.strip())
    inner = re.sub(r'\\end\{\w+\}$', '', inner.strip())
    items = []
    for part in re.split(r'\\item\b', inner)[1:]:
        label = None
        part = part.lstrip()
        if part.startswith('['):
            depth, k = 0, 0
            for k, ch in enumerate(part):
                depth += {'[': 1, ']': -1}.get(ch, 0)
                if depth == 0:
                    break
            label, part = part[1:k], part[k + 1:]
        items.append((label, part.strip()))
    return items


def parse_file(text, doc, ctx):
    text = strip_comments(text)
    lines = text.split('\n')
    i, para = 0, []

    def flush():
        nonlocal para
        body = '\n'.join(para).strip()
        if body:
            for lab in labels_in(body):
                doc.bm += 1
                ctx.labels.setdefault(lab, (ctx.labels.get(lab, ('', None))[0] or '', f'lbl_{doc.bm}'))
            doc.blocks.append(('p', body))
        para = []

    while i < len(lines):
        line = lines[i]
        st = line.strip()
        m = re.match(r'\\(chapter|section|subsection|subsubsection)(\*?)\s*(\[[^\]]*\])?\{', st)
        if m:
            flush()
            level, star = m.group(1), m.group(2)
            title, rest = group_arg(st, m.end() - 1)
            # a heading's argument may span lines
            while title.count('{') > title.count('}') and i + 1 < len(lines):
                i += 1
                st += ' ' + lines[i].strip()
                title, rest = group_arg(st, m.end() - 1)
            labs = labels_in(st)
            # text written on the same line after the heading starts the first paragraph
            tail = re.sub(r'\\label\{[^}]*\}', '', st[rest:]).strip()
            j = i + 1
            while j < len(lines) and lines[j].strip().startswith(BS + 'label'):
                labs += labels_in(lines[j])
                j += 1
            i = j
            number = ''
            if not star:
                if level == 'chapter':
                    doc.chapter += 1
                    doc.section = doc.subsection = doc.fig = doc.tab = 0
                    number = doc.chapter_no()
                elif level == 'section':
                    doc.section += 1
                    doc.subsection = 0
                    number = f'{doc.chapter_no()}.{doc.section}'
                elif level == 'subsection':
                    doc.subsection += 1
                    number = f'{doc.chapter_no()}.{doc.section}.{doc.subsection}'
            doc.bm += 1
            mark = f'h_{doc.bm}'
            kind = {'chapter': 'Appendix' if doc.appendix else 'Chapter', 'section': 'Section',
                    'subsection': 'Section', 'subsubsection': 'Section'}[level]
            for lab in labs:
                ctx.labels[lab] = (f'{kind} {number}', mark)
            lvl = {'chapter': 1, 'section': 2, 'subsection': 3, 'subsubsection': 4}[level]
            shown = (f'Appendix {number}: ' if level == 'chapter' and doc.appendix and number else
                     f'{number} ' if number else '')
            doc.blocks.append(('h', (lvl, shown, title, mark)))
            if tail:
                para.append(tail)
            continue
        m = re.match(r'\\lstinputlisting(?:\[[^\]]*\])?\{([^}]*)\}', st)
        if m:  # a listing read from a source file, e.g. a script shown in an appendix
            flush()
            path = os.path.normpath(os.path.join(THESIS_DIR, m.group(1)))
            if exists(path):
                doc.blocks.append(('code', read(path).rstrip('\n')))
            i += 1
            continue
        m = re.match(r'\\begin\{(table|longtable|figure|itemize|description|enumerate|lstlisting|verbatim)\*?\}', st)
        if m:
            flush()
            env = m.group(1)
            body, j = env_body(lines, i, env)
            i = j + 1
            if env == 'longtable':
                env, body = 'table', longtable_as_table(body)
            if env in ('table', 'figure'):
                doc.bm += 1
                mark = f'f_{doc.bm}'
                if env == 'table':
                    doc.tab += 1
                    number = f'{doc.chapter_no()}.{doc.tab}'
                    name = 'Table'
                else:
                    doc.fig += 1
                    number = f'{doc.chapter_no()}.{doc.fig}'
                    name = 'Figure'
                for lab in labels_in(body):
                    ctx.labels[lab] = (f'{name} {number}', mark)
                desc = ''
                k = body.find(BS + 'Description')
                if k >= 0:
                    desc, _ = group_arg(body, body.index('{', k))
                doc.blocks.append((env, {'number': f'{name} {number}', 'caption': caption_of(body),
                                         'rows': parse_tabular(body), 'desc': desc,
                                         'tikz': 'tikzpicture' in body, 'mark': mark}))
            elif env in ('lstlisting', 'verbatim'):
                code = re.sub(r'^\\begin\{\w+\}(\[[^\]]*\])?\n?', '', body)
                code = re.sub(r'\n?\\end\{\w+\}\s*$', '', code)
                doc.blocks.append(('code', code))
            else:
                doc.blocks.append(('list', (env, parse_items(body))))
            continue
        if re.match(r'\\(begin|end)\{(singlespace|center|flushleft|small|footnotesize|minipage|landscape)\}', st) \
                or re.match(r'\\(clearpage|cleardoublepage|newpage|bigskip|medskip|smallskip|vspace|setlength)', st):
            flush()
            i += 1
            continue
        if not st:
            flush()
        else:
            para.append(line)
        i += 1
    flush()


def load_thesis(ctx):
    doc = Doc()
    main = strip_comments(read(os.path.join(THESIS_DIR, 'thesis.tex')))
    main = main.split(BS + 'begin{document}', 1)[1]
    for m in re.finditer(r'\\appendix|\\chapter\*\{([^}]*)\}|\\input\{([^}]*)\}', main):
        if m.group(0) == BS + 'appendix':
            doc.appendix = True
            doc.chapter = 0
        elif m.group(1):
            pending = m.group(1)
            if pending == 'Abstract':
                doc.bm += 1
                doc.blocks.append(('h', (1, '', 'Abstract', f'h_{doc.bm}')))
        elif m.group(2) and m.group(2).startswith(('chapters/', 'appendix/')):
            path = os.path.join(THESIS_DIR, m.group(2) + ('' if m.group(2).endswith('.tex') else '.tex'))
            if exists(path):
                parse_file(read(path), doc, ctx)
    return doc


# ======================================================================== OOXML
def esc(t):
    return html.escape(t, quote=True)


HL = '<w:rStyle w:val="Hyperlink"/>'


class Writer:
    def __init__(self):
        self.rels = []            # external hyperlinks
        self.bm_id = 0

    def rid(self, url):
        for n, u in enumerate(self.rels):
            if u == url:
                return f'rIdL{n + 1}'
        self.rels.append(url)
        return f'rIdL{len(self.rels)}'

    def bookmark(self, name):
        self.bm_id += 1
        return f'<w:bookmarkStart w:id="{self.bm_id}" w:name="{name}"/><w:bookmarkEnd w:id="{self.bm_id}"/>'

    def run(self, text, fmt, extra=''):
        # Word rejects run properties out of schema order:
        # rStyle, rFonts, b, i, color, sz, highlight, u.
        props = extra
        if 'mono' in fmt:
            props += '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>'
        if 'b' in fmt:
            props += '<w:b/>'
        if 'i' in fmt:
            props += '<w:i/>'
        if 'todo' in fmt:
            props += '<w:color w:val="C00000"/>'
        if 'mono' in fmt:
            props += '<w:sz w:val="20"/>'
        if 'todo' in fmt:
            props += '<w:highlight w:val="yellow"/>'
        if 'u' in fmt:
            props += '<w:u w:val="single"/>'
        out = []
        for k, part in enumerate(text.split('\n')):
            if k:
                out.append(f'<w:r><w:rPr>{props}</w:rPr><w:br/></w:r>')
            if part:
                out.append(f'<w:r><w:rPr>{props}</w:rPr><w:t xml:space="preserve">{esc(part)}</w:t></w:r>')
        return ''.join(out)

    def runs(self, runs):
        out = []
        for text, fmt, link in runs:
            if link is None:
                out.append(self.run(text, fmt))
            elif link[0] == 'int':
                out.append(f'<w:hyperlink w:anchor="{link[1]}" w:history="1">' + self.run(text, fmt, HL) + '</w:hyperlink>')
            else:
                out.append(f'<w:hyperlink r:id="{self.rid(link[1])}" w:history="1">' + self.run(text, fmt, HL) + '</w:hyperlink>')
        return ''.join(out)

    def para(self, runs_xml, style=None, extra_ppr='', pre=''):
        ppr = (f'<w:pStyle w:val="{style}"/>' if style else '') + extra_ppr
        return f'<w:p><w:pPr>{ppr}</w:pPr>{pre}{runs_xml}</w:p>'

    def table(self, rows, ctx, widths=None, header=True):
        ncols = max(len(r) for r in rows)
        total = 9000
        widths = widths or [total // ncols] * ncols
        grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)
        out = [f'<w:tbl><w:tblPr><w:tblStyle w:val="ReviewTable"/><w:tblW w:w="{total}" w:type="dxa"/>'
               f'<w:tblLayout w:type="fixed"/></w:tblPr><w:tblGrid>{grid}</w:tblGrid>']
        for r_i, row in enumerate(rows):
            out.append('<w:tr>' + ('<w:trPr><w:tblHeader/></w:trPr>' if r_i == 0 and header else ''))
            for c_i in range(ncols):
                cell = row[c_i] if c_i < len(row) else ''
                span = 1
                if isinstance(cell, tuple):
                    cell, span = cell
                runs_ = inline(cell, ctx, frozenset({'b'}) if r_i == 0 and header else frozenset())
                tcpr = f'<w:tcW w:w="{sum(widths[c_i:c_i + span])}" w:type="dxa"/>'
                if span > 1:
                    tcpr += f'<w:gridSpan w:val="{span}"/>'
                out.append(f'<w:tc><w:tcPr>{tcpr}</w:tcPr>{self.para(self.runs(runs_), "TableText")}</w:tc>')
            out.append('</w:tr>')
        out.append('</w:tbl>')
        return ''.join(out)


STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri" w:eastAsia="Calibri"/>
<w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="en-GB"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/><w:pPr><w:jc w:val="both"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:qFormat/>
<w:pPr><w:jc w:val="center"/><w:spacing w:before="600" w:after="200"/></w:pPr><w:rPr><w:b/><w:sz w:val="40"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:basedOn w:val="Normal"/><w:qFormat/>
<w:pPr><w:jc w:val="center"/></w:pPr><w:rPr><w:sz w:val="24"/><w:color w:val="404040"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>
<w:pPr><w:keepNext/><w:pageBreakBefore/><w:spacing w:before="240" w:after="240"/><w:jc w:val="left"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="36"/><w:color w:val="1F3864"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>
<w:pPr><w:keepNext/><w:spacing w:before="320" w:after="120"/><w:jc w:val="left"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:sz w:val="28"/><w:color w:val="1F3864"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>
<w:pPr><w:keepNext/><w:spacing w:before="240" w:after="80"/><w:jc w:val="left"/><w:outlineLvl w:val="2"/></w:pPr><w:rPr><w:b/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading4"><w:name w:val="heading 4"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>
<w:pPr><w:keepNext/><w:jc w:val="left"/><w:outlineLvl w:val="3"/></w:pPr><w:rPr><w:b/><w:i/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="caption"/><w:basedOn w:val="Normal"/><w:qFormat/>
<w:pPr><w:keepNext/><w:spacing w:before="200" w:after="80"/><w:jc w:val="left"/></w:pPr><w:rPr><w:b/><w:sz w:val="20"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="FigureNote"><w:name w:val="Figure note"/><w:basedOn w:val="Normal"/>
<w:pPr><w:pBdr><w:top w:val="single" w:sz="4" w:space="4" w:color="A6A6A6"/><w:left w:val="single" w:sz="4" w:space="4" w:color="A6A6A6"/>
<w:bottom w:val="single" w:sz="4" w:space="4" w:color="A6A6A6"/><w:right w:val="single" w:sz="4" w:space="4" w:color="A6A6A6"/></w:pBdr>
<w:shd w:val="clear" w:color="auto" w:fill="F2F2F2"/><w:jc w:val="left"/></w:pPr><w:rPr><w:sz w:val="20"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="ReviewNote"><w:name w:val="Review note"/><w:basedOn w:val="Normal"/>
<w:pPr><w:pBdr><w:top w:val="single" w:sz="8" w:space="6" w:color="2E74B5"/><w:left w:val="single" w:sz="8" w:space="6" w:color="2E74B5"/>
<w:bottom w:val="single" w:sz="8" w:space="6" w:color="2E74B5"/><w:right w:val="single" w:sz="8" w:space="6" w:color="2E74B5"/></w:pBdr>
<w:shd w:val="clear" w:color="auto" w:fill="DEEAF6"/><w:jc w:val="left"/></w:pPr><w:rPr><w:sz w:val="20"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="TableText"><w:name w:val="Table text"/><w:basedOn w:val="Normal"/>
<w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr><w:rPr><w:sz w:val="18"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/><w:basedOn w:val="Normal"/>
<w:pPr><w:shd w:val="clear" w:color="auto" w:fill="F2F2F2"/><w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/><w:sz w:val="18"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="ListItem"><w:name w:val="List item"/><w:basedOn w:val="Normal"/>
<w:pPr><w:spacing w:after="60"/><w:ind w:left="567" w:hanging="283"/><w:jc w:val="left"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Bibliography"><w:name w:val="Bibliography"/><w:basedOn w:val="Normal"/>
<w:pPr><w:spacing w:after="80"/><w:ind w:left="567" w:hanging="567"/><w:jc w:val="left"/></w:pPr><w:rPr><w:sz w:val="20"/></w:rPr></w:style>
<w:style w:type="character" w:styleId="Hyperlink"><w:name w:val="Hyperlink"/><w:rPr><w:color w:val="0563C1"/><w:u w:val="single"/></w:rPr></w:style>
<w:style w:type="table" w:styleId="ReviewTable"><w:name w:val="Review table"/><w:tblPr>
<w:tblBorders><w:top w:val="single" w:sz="4" w:color="808080"/><w:left w:val="single" w:sz="4" w:color="808080"/>
<w:bottom w:val="single" w:sz="4" w:color="808080"/><w:right w:val="single" w:sz="4" w:color="808080"/>
<w:insideH w:val="single" w:sz="4" w:color="BFBFBF"/><w:insideV w:val="single" w:sz="4" w:color="BFBFBF"/></w:tblBorders>
<w:tblCellMar><w:top w:w="40" w:type="dxa"/><w:left w:w="80" w:type="dxa"/><w:bottom w:w="40" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar>
</w:tblPr></w:style>
</w:styles>'''


def build(print_text=False):
    ctx = Ctx()
    bib = parse_bib()
    # Pass 1 collects labels and citation order; pass 2 renders with numbers known.
    doc = load_thesis(ctx)
    for kind, payload in doc.blocks:
        if kind == 'p':
            inline(payload, ctx)
        elif kind == 'list':
            for label, body in payload[1]:
                inline((label or '') + ' ' + body, ctx)
        elif kind in ('table', 'figure'):
            inline(payload['caption'] + ' ' + payload['desc'], ctx)
            for row in payload['rows']:
                for cell in row:
                    inline(cell, ctx)
    cited = [k for k in ctx.cite_order if k in bib]
    missing = [k for k in ctx.cite_order if k not in bib]
    bbl = os.path.join(THESIS_DIR, 'thesis.bbl')
    if os.path.exists(bbl):
        order = [k for k in re.findall(r'\\entry\{([^}]+)\}', read(bbl)) if k in cited]
        order += [k for k in cited if k not in order]
    else:  # biblatex numeric-comp with sorting=nyt: name, year, title
        order = sorted(cited, key=lambda k: sort_key(bib[k][1]))
    ctx.cite_num = {k: n + 1 for n, k in enumerate(order)}

    meta = metadata()
    commit, stamp = git_stamp()
    w = Writer()
    body = []
    text_dump = []

    def add(xml, plain=''):
        body.append(xml)
        if plain:
            text_dump.append(plain)

    title = bib_clean(meta.get('thesistitle', 'Thesis'))
    add(w.para(w.run(title, set()), 'Title'), title)
    add(w.para(w.run(f'{meta.get("thesiskind", "Thesis")} · working draft for review', set()), 'Subtitle'))
    add(w.para(w.run(f'{meta.get("authorname", "")} · Advisor: {meta.get("advisorname", "")}', set()), 'Subtitle'))
    note = [
        ('Review copy for the supervisor. ', {'b'}),
        (stamp + ' It is rebuilt with every commit that changes the thesis, so this file always '
         'shows the latest committed draft.', set()),
        ('\nHow to review: ', {'b'}),
        ('add Word comments (Review → New Comment) or switch on Track Changes, then send the file back. '
         'Save your annotated version under a new name: the next commit overwrites this file.', set()),
        ('\nWhat differs from the PDF: ', {'b'}),
        ('thesis.pdf remains the authoritative layout. Diagrams drawn in TikZ appear here as their text '
         'description. Citation numbers [n] link to the bibliography entry; entries link to the DOI or URL. '
         'Items marked ', set()),
        ('[TODO: …]', {'b', 'todo'}),
        (' are open drafting points, not finished text.', set()),
    ]
    add(w.para(w.runs([(t, frozenset(f), None) for t, f in note]), 'ReviewNote'),
        ''.join(t for t, _ in note))

    for kind, payload in doc.blocks:
        if kind == 'h':
            lvl, shown, title_tex, mark = payload
            runs_ = inline(title_tex, ctx)
            style = f'Heading{min(lvl, 4)}'
            add(w.para(w.run(shown, set()) + w.runs(runs_), style, pre=w.bookmark(mark)),
                '#' * lvl + ' ' + shown + ''.join(r[0] for r in runs_))
        elif kind == 'p':
            runs_ = inline(payload, ctx)
            marks = ''.join(w.bookmark(ctx.labels[l][1]) for l in labels_in(payload) if l in ctx.labels)
            if runs_:
                add(w.para(w.runs(runs_), pre=marks), ''.join(r[0] for r in runs_))
        elif kind == 'list':
            env, items = payload
            for n, (label, item) in enumerate(items, 1):
                runs_ = inline(item, ctx)
                if env == 'description' and label is not None:
                    lead = [(t, f | {'b'}, l) for t, f, l in inline(label, ctx)] + [(' ', frozenset(), None)]
                    add(w.para(w.runs(lead + runs_), 'ListItem', '<w:ind w:left="284" w:hanging="0"/>'),
                        ''.join(r[0] for r in lead + runs_))
                else:
                    bullet = f'{n}.\t' if env == 'enumerate' else '•\t'
                    add(w.para(w.run(bullet, set()) + w.runs(runs_), 'ListItem'),
                        bullet + ''.join(r[0] for r in runs_))
        elif kind in ('table', 'figure'):
            cap = [(payload['number'] + '. ', frozenset({'b'}), None)] + inline(payload['caption'], ctx)
            add(w.para(w.runs(cap), 'Caption', pre=w.bookmark(payload['mark'])), ''.join(r[0] for r in cap))
            if payload['rows'] and not payload['tikz']:
                add(w.table(payload['rows'], ctx), '\n'.join(
                    ' | '.join(''.join(x[0] for x in inline(c, ctx)) for c in r) for r in payload['rows']))
                body.append(w.para('', extra_ppr='<w:spacing w:after="0"/>'))
            if payload['tikz'] or payload['desc']:
                d = [('Diagram (shown as a drawing in thesis.pdf): ', frozenset({'i'}), None)] + \
                    inline(payload['desc'] or 'see thesis.pdf.', ctx)
                add(w.para(w.runs(d), 'FigureNote'), ''.join(r[0] for r in d))
        elif kind == 'code':
            for line in payload.split('\n'):
                add(w.para(w.run(line, set()), 'Code'), line)
            body.append(w.para(''))

    add(w.para(w.run('Bibliography', set()), 'Heading1', pre=w.bookmark('bibliography')), '# Bibliography')
    for key in order:
        kind, fields = bib[key]
        runs_, link = format_entry(kind, fields)
        num = ctx.cite_num[key]
        xml = w.run(f'[{num}]\t', {'b'}) + w.runs([(t, frozenset(f), None) for t, f in runs_])
        if link:
            xml += w.run(' ', set()) + w.runs([(link, frozenset(), ('ext', link))])
        add(w.para(xml, 'Bibliography', '<w:tabs><w:tab w:val="left" w:pos="567"/></w:tabs>',
                   pre=w.bookmark(f'ref_{num}')),
            f'[{num}] ' + ''.join(t for t, _ in runs_) + (' ' + link if link else ''))

    ns = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
    sect = ('<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1418" w:right="1418" w:bottom="1418" '
            'w:left="1418" w:header="709" w:footer="709" w:gutter="0"/></w:sectPr>')
    document = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<w:document {ns}><w:body>'
                + ''.join(body) + sect + '</w:body></w:document>')
    doc_rels = ['<Relationship Id="rIdS" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
                '<Relationship Id="rIdT" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>']
    for n, url in enumerate(w.rels, 1):
        doc_rels.append(f'<Relationship Id="rIdL{n}" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                        f'relationships/hyperlink" Target="{esc(url)}" TargetMode="External"/>')
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    files = {
        '[Content_Types].xml': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
        '</Types>',
        '_rels/.rels': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '</Relationships>',
        'word/_rels/document.xml.rels': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + ''.join(doc_rels) + '</Relationships>',
        'word/document.xml': document,
        'word/styles.xml': STYLES,
        'word/settings.xml': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:defaultTabStop w:val="567"/><w:compat><w:compatSetting w:name="compatibilityMode" '
        'w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat></w:settings>',
        'docProps/core.xml': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        f'<dc:title>{esc(title)} (review copy)</dc:title><dc:creator>{esc(meta.get("authorname", ""))}</dc:creator>'
        f'<dc:description>{esc(stamp)}</dc:description>'
        f'<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>'
        f'<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified></cp:coreProperties>',
    }
    tmp = OUT + '.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            z.writestr(name, data)
    try:
        os.replace(tmp, OUT)
    except PermissionError:  # the file is open in Word; keep the build next to it
        alt = OUT.replace('.docx', f'_{commit}.docx')
        os.replace(tmp, alt)
        print(f'{OUT} is open (locked); wrote {alt} instead', file=sys.stderr)
    if print_text:
        print('\n\n'.join(text_dump))
    print(f'review copy: {os.path.relpath(OUT, ROOT)} (commit {commit}, {len(order)} references'
          + (f'; missing from bib: {", ".join(missing)}' if missing else '') + ')')


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    build('--text' in sys.argv)
