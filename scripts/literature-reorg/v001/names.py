"""Name rules for the library: Author_Year_ShortTitle.pdf (see 01_Literature/README.md)."""
import re
import unicodedata

STOP = set('a an the of in on for and to with at by from is are as or how what why does do can via using use its it their into '
           'toward towards new between'.split())
AUTHOR_OVERRIDE = {'Article 29 Working Party': 'Article29WP', 'Association of Internet Researchers': 'AoIR',
                   'APA': 'APA', 'BfArM': 'BfArM'}


def fold(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()


def camel(words):
    out = []
    for w in words:
        w = re.sub(r'[^A-Za-z0-9]', '', fold(w))
        if w:
            out.append(w if w.isupper() or any(c.isupper() for c in w[1:]) else w[:1].upper() + w[1:])
    return ''.join(out)


def author_token(ref_author):
    """'Citron & Solove' / 'Alfawzan et al.' / "O'Loughlin et al." -> first author, no separators."""
    for k, v in AUTHOR_OVERRIDE.items():
        if ref_author.startswith(k):
            return v
    first = re.split(r'\s*(?:&|\band\b|et al\.?|,)\s*', ref_author.strip())[0]
    return camel(re.split(r"[\s'’-]+", first))


def short_title(title, n=5, cap=44):
    main = re.split(r'\s+-\s+|:\s+|\?\s+|\s+–\s+', title.strip())[0]
    words = [w for w in re.split(r'[\s_/]+', fold(main).replace('-', ' ')) if w]
    keep = [w for w in words if w.lower() not in STOP] or words
    out = camel(keep[:n])
    while len(out) > cap and n > 2:
        n -= 1
        out = camel(keep[:n])
    return out
