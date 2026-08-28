"""Parses Joshua Vogelstein's CV data out of content/bibs/tex/jovo_cv_SOM.tex
(a LaTeX/moderncv-syntax file used as structured data, never compiled with
real LaTeX) into the same {title, listitems: [...]} shape that
content/jovo/jovo-cv.yaml used to provide, so content/about/jovo.html and
the downloadable-PDF pipeline (cv/cv_new/build_cv.py) both render from one
source of truth instead of two independently-edited copies.

Sections handled: Personal Information, Educational Activities, Mentorship
(Thesis Committee Service), Service, Awards and Recognition, Translation /
Technology Transfer Activities. Publications/Funding/Talks/Press stay on
the existing load_bibtex filter (bibtex_print.py) -- those already have a
single bib-file source and aren't duplicated anywhere.
"""

import re
from datetime import date

from jinja2.ext import Extension

HREF_RE = re.compile(r'\\href\{([^{}]*)\}\{([^{}]*)\}')
URL_RE = re.compile(r'\\url\{([^{}]*)\}')


def _read_braces(s, i):
    assert s[i] == '{'
    depth = 0
    j = i
    while j < len(s):
        if s[j] == '{':
            depth += 1
        elif s[j] == '}':
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise ValueError('unbalanced braces: ' + s[i:i + 80])


def _parse_cventries(block):
    """Every \\cventry{...}{...}... in block, as a list of raw arg strings."""
    out = []
    for m in re.finditer(r'\\cventry\s*', block):
        i = m.end()
        while i < len(block) and block[i] != '{':
            i += 1
        args = []
        while i < len(block) and block[i] == '{':
            content, i = _read_braces(block, i)
            args.append(content)
            while i < len(block) and block[i] in ' \t':
                i += 1
        out.append(args)
    return out


def _strip_tex(s):
    if not s:
        return ''
    s = s.strip()
    s = re.sub(r'\\textbf\{([^{}]*)\}', r'<strong>\1</strong>', s)
    s = re.sub(r'\\textit\{([^{}]*)\}', r'<em>\1</em>', s)
    s = HREF_RE.sub(r'<a href="\1">\2</a>', s)
    s = URL_RE.sub(r'\1', s)
    s = s.replace('~', ' ').replace('\\,', ',').replace('--', '\u2013')
    s = s.replace("\\'", "'").replace('``', '"').replace("''", '"')
    s = re.sub(r'\\%', '%', s)
    s = s.replace('\\&', '&').replace('\\_', '_').replace('\\#', '#')
    # protect escaped currency signs before the bare-$...$ math-mode stripper
    # runs, or "\$500M ... \$2.5B" gets misread as one math span and eaten
    s = s.replace('\\$', '\x00DOLLAR\x00').replace('\\ ', ' ')
    s = re.sub(r'\$([^$]*)\$',
               lambda m: m.group(1).replace('\\times', '\u00d7').replace('\\sim', '~').strip(), s)
    s = s.replace('\x00DOLLAR\x00', '$')
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def _only_href(s):
    """If s is exactly one \\href{url}{text}, return (text, url); else (text, None)."""
    m = HREF_RE.fullmatch(s.strip())
    if m:
        return _strip_tex(m.group(2)), m.group(1)
    return _strip_tex(s), None


def _get_section(text, name):
    pat = re.compile(r'\\section\{(?:\\href\{[^}]*\}\{)?' + re.escape(name), re.IGNORECASE)
    m = pat.search(text)
    if not m:
        return ''
    start = m.end()
    nxt = re.search(r'\\section\{', text[start:])
    return text[start:start + nxt.start()] if nxt else text[start:]


def _get_subsections(block):
    """[(title, subblock), ...] split on \\subsection / \\subsubsection markers."""
    parts = []
    matches = list(re.finditer(r'\\subsection\{([^{}]*)\}|\\subsubsection\{([^{}]*)\}', block))
    for idx, m in enumerate(matches):
        title = (m.group(1) or m.group(2)).strip()
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(block)
        parts.append((title, block[start:end]))
    return parts


def _args6(args):
    return (args + [''] * 6)[:6]


def _parse_personal(text):
    keep = ('Primary Appointment', 'Joint Appointments', 'Institutional and Center Appointments',
            'Education & Training', 'Academic Experience')
    out = []
    for raw_title, sub in _get_subsections(_get_section(text, 'Personal Information')):
        title = _strip_tex(raw_title)
        if title not in keep:
            continue
        disp = 'Education' if 'Education' in title else title
        items = []
        for args in _parse_cventries(sub):
            date_s, pos, org, loc, e1, e2 = _args6(args)
            date_s, pos_t, org_t, loc_t, e1_t, e2_t = (
                _strip_tex(date_s), _strip_tex(pos), _strip_tex(org),
                _strip_tex(loc), _strip_tex(e1), _strip_tex(e2))
            if disp == 'Education' and (e1_t or 'Advisor' in loc_t):
                lines = [p for p in (org_t, loc_t, e1_t) if p]
                item = {'date': date_s, 'position': pos_t, 'institution': '\n'.join(lines) + '\n'}
            else:
                inst = org_t + (', ' + loc_t if loc_t else '')
                if inst and not inst.endswith('.'):
                    inst += '.'
                extra = ' '.join(x for x in (e1_t, e2_t) if x)
                item = {'date': date_s, 'position': pos_t,
                        'institution': inst + ('\n' + extra + '\n' if extra else '')}
            hm = HREF_RE.fullmatch(pos.strip())
            if hm:
                item['position'] = _strip_tex(hm.group(2))
                item['link'] = hm.group(1)
            items.append(item)
        if items:
            out.append({'title': disp, 'listitems': items})
    return out


def _parse_educational(text):
    out = []
    for title, sub in _get_subsections(_get_section(text, 'Educational Activities')):
        items = []
        for args in _parse_cventries(sub):
            date_s, role, code, name_field, e1, e2 = _args6(args)
            name_t, name_url = _only_href(name_field)
            item = {'date': _strip_tex(date_s), 'title': name_t}
            if name_url:
                item['url'] = name_url
            ref_parts = [p for p in (_strip_tex(code), _strip_tex(role), _strip_tex(e1), _strip_tex(e2)) if p]
            item['ref'] = ', '.join(ref_parts) + ('.' if ref_parts and not ref_parts[-1].endswith('.') else '')
            items.append(item)
        if items:
            out.append({'title': title, 'listitems': items})
    return out


def _parse_thesiscomitee(text):
    mentor_sec = _get_section(text, 'Mentorship')
    thesis_block = ''
    for title, sub in _get_subsections(mentor_sec):
        if title.startswith('Thesis Committee'):
            thesis_block = sub
    out = []
    for args in _parse_cventries(thesis_block):
        date_s, person, course, e1, e2, e3 = _args6(args)
        desc = ', '.join(x for x in (_strip_tex(e1), _strip_tex(e2)) if x)
        out.append({'date': _strip_tex(date_s), 'person': _strip_tex(person),
                     'course': _strip_tex(course), 'desc': desc})
    return out


def _parse_service(text):
    out = []
    for title, sub in _get_subsections(_get_section(text, 'Service')):
        disp = {'Editorial Board': 'Journal Service: Editorial Board',
                'Conference and Journal Reviewer': 'Journal Service: Conference and Journal Reviewer'
                }.get(title, title)
        items = []
        for args in _parse_cventries(sub):
            date_s, pos, org, loc, e1, e2 = _args6(args)
            pos_t, _pos_url = _only_href(pos)
            item = {'position': pos_t}
            if _strip_tex(date_s):
                item['date'] = _strip_tex(date_s)
            org_t = _strip_tex(org)
            if org_t:
                item['institution'] = org_t
            desc = ' '.join(x for x in (_strip_tex(loc), _strip_tex(e1), _strip_tex(e2)) if x)
            if desc:
                item['desc'] = desc
            items.append(item)
        if items:
            out.append({'title': disp, 'listitems': items})
    return out


def _parse_awards(text):
    out = []
    for title, sub in _get_subsections(_get_section(text, 'Awards and Recognition')):
        disp = re.sub(r'\s*\(\d+\)\s*$', '', title)
        items = []
        for args in _parse_cventries(sub):
            date_s, award, desc, e1, e2, e3 = _args6(args)
            award_t, award_url = _only_href(award)
            item = {'date': _strip_tex(date_s), 'award': award_t, 'desc': _strip_tex(desc)}
            if award_url:
                item['url'] = award_url
            items.append(item)
        if items:
            out.append({'title': disp, 'listitems': items})
    return out


_STARTUP_LIKE = ('Advisory Board Appointments', 'Startups', 'Consultancy')


def _parse_transfer(text):
    out = []
    for title, sub in _get_subsections(_get_section(text, 'Translation / Technology Transfer Activities')):
        items = []
        for args in _parse_cventries(sub):
            date_s, position_or_title, org, loc, e1, e2 = _args6(args)
            text_t, url = _only_href(position_or_title)
            item = {'date': _strip_tex(date_s)}
            if url:
                item['url'] = url
            if title in _STARTUP_LIKE:
                item['position'] = text_t
                org_t, org_url = _only_href(org)
                item['title'] = org_t
                if org_url:
                    item['url'] = org_url
            else:
                item['title'] = text_t
            loc_t, e1_t, e2_t = _strip_tex(loc), _strip_tex(e1), _strip_tex(e2)
            if title in _STARTUP_LIKE:
                # tex field order here: loc=long description, e1=short status note, e2=stats
                desc = (loc_t + (' ' + e1_t if e1_t else '')).strip()
                if desc:
                    item['desc'] = desc
                if e2_t:
                    item['stats'] = e2_t
            else:
                # tex field order here: loc=short stats line, e1=long description
                stats = loc_t
                if e1_t:
                    item['desc'] = e1_t
                if e2_t:
                    stats = (stats + ' ' + e2_t).strip() if stats else e2_t
                if stats:
                    item['stats'] = stats
            items.append(item)
        if items:
            out.append({'title': title, 'listitems': items})
    return out


def load_tex_cv(tex_path):
    with open(tex_path, encoding='utf-8') as f:
        text = f.read()
    # strip full-line LaTeX comments (e.g. an intentionally-disabled cventry)
    text = '\n'.join(line for line in text.split('\n') if not line.strip().startswith('%'))

    return {
        'personal': _parse_personal(text),
        'educational': _parse_educational(text),
        'thesiscomitee': _parse_thesiscomitee(text),
        'service': _parse_service(text),
        'awards': _parse_awards(text),
        'transfer': _parse_transfer(text),
        'updated': date.today().strftime('%Y/%m/%d'),
    }


class TEX_CV(Extension):
    def __init__(self, environment):
        super(TEX_CV, self).__init__(environment)
        environment.filters['load_tex_cv'] = load_tex_cv
