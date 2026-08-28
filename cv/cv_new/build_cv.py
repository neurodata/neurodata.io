import html as htmlmod
import re
from datetime import date

from bibparse import parse_bib, parse_author_an, split_authors
from latexutil import tex_to_html, format_authors
from texparse import parse_sections, strip_href_title

BIB_DIR = '../../content/bibs'
TEX_PATH = '../../content/bibs/tex/jovo_cv_SOM.tex'

MONTH_NUM = {
    'jan': 1, 'january': 1, 'feb': 2, 'february': 2, 'mar': 3, 'march': 3,
    'apr': 4, 'april': 4, 'may': 5, 'jun': 6, 'june': 6, 'jul': 7, 'july': 7,
    'aug': 8, 'august': 8, 'sep': 9, 'sept': 9, 'september': 9,
    'oct': 10, 'october': 10, 'nov': 11, 'november': 11, 'dec': 12, 'december': 12,
}

def month_num(m):
    if not m:
        return 0
    m = m.strip().lower()
    if m.isdigit():
        return int(m)
    return MONTH_NUM.get(m, 0)

def sort_key(e):
    try:
        y = int(e.get('year', '0') or '0')
    except ValueError:
        y = 0
    return (y, month_num(e.get('month', '')))

# ---------- load bib data ----------
pubs = parse_bib(f'{BIB_DIR}/pubs.bib')
talks = parse_bib(f'{BIB_DIR}/talks.bib')
funding = parse_bib(f'{BIB_DIR}/funding.bib')
people = parse_bib(f'{BIB_DIR}/people.bib')
press = parse_bib(f'{BIB_DIR}/press.bib')

with open(TEX_PATH, encoding='utf-8') as f:
    tex_text = f.read()
tokens = parse_sections(tex_text)

# ---------- build a lookup: section title (raw) -> {subsection title -> [entries]} ----------
def build_tex_tree(tokens):
    tree = []  # list of (section_title, [(subsection_title, [(subsub_title_or_None, [entry_args...])])])
    cur_sec = None
    cur_sub = None
    cur_subsub = None
    for kind, data in tokens:
        if kind == 'section':
            cur_sec = {'title': data, 'subs': []}
            tree.append(cur_sec)
            cur_sub = None
            cur_subsub = None
        elif kind == 'subsection':
            cur_sub = {'title': data, 'entries': [], 'subsubs': []}
            if cur_sec is None:
                cur_sec = {'title': '', 'subs': []}
                tree.append(cur_sec)
            cur_sec['subs'].append(cur_sub)
            cur_subsub = None
        elif kind == 'subsubsection':
            cur_subsub = {'title': data, 'entries': []}
            if cur_sub is None:
                cur_sub = {'title': '', 'entries': [], 'subsubs': []}
                cur_sec['subs'].append(cur_sub)
            cur_sub['subsubs'].append(cur_subsub)
        elif kind == 'entry':
            target = cur_subsub['entries'] if cur_subsub else (cur_sub['entries'] if cur_sub else None)
            if target is None:
                # entry directly under section w/o subsection (shouldn't happen much)
                cur_sub = {'title': '', 'entries': [], 'subsubs': []}
                cur_sec['subs'].append(cur_sub)
                target = cur_sub['entries']
            target.append(data)
    return tree

tex_tree = build_tex_tree(tokens)

def find_section(tree, title_substr):
    for sec in tree:
        if title_substr.lower() in sec['title'].lower():
            return sec
    return None

# ============================================================
# HTML rendering helpers
# ============================================================

def esc(s):
    return htmlmod.escape(s or '')

_TAG_RE = re.compile(r'<[^>]+>')

def _visible_len(html_fragment):
    return len(_TAG_RE.sub('', html_fragment))

LINE_BUDGET = 128  # measured: ~130 chars actually fit at this font/column width in print

def _style(kind, html):
    if kind == 'title':
        return f'<b>{html}</b>'
    if kind == 'orgloc':
        return f'<i>{html}</i>'
    return html

def dated_entry(date_str, title, org, loc, extra1='', extra2=''):
    date_h = tex_to_html(date_str)
    extras_raw = list(extra1) if isinstance(extra1, list) else [extra1, extra2]
    # (kind, raw_text) for every candidate field, in display order
    fields = [('title', title), ('orgloc', org), ('orgloc', loc)] + [('extra', x) for x in extras_raw]
    fields = [(kind, tex_to_html(x)) for kind, x in fields if x]

    # greedily pack short fields onto shared lines; long fields (paragraphs,
    # abstracts) always get their own line
    lines = []
    current, current_len = [], 0
    for kind, html in fields:
        vlen = _visible_len(html)
        is_long = vlen > LINE_BUDGET
        if is_long:
            if current:
                lines.append(current)
                current, current_len = [], 0
            lines.append([(kind, html)])
            continue
        if current and current_len + 2 + vlen > LINE_BUDGET:
            lines.append(current)
            current, current_len = [], 0
        current.append((kind, html))
        current_len += vlen + 2
    if current:
        lines.append(current)

    body_bits = []
    for line in lines:
        joined = ', '.join(_style(kind, h) for kind, h in line)
        body_bits.append(f'<div class="entry-line">{joined}</div>')

    return f'''<div class="item">
  <div class="item-date">{date_h}</div>
  <div class="item-body">
    {''.join(body_bits)}
  </div>
</div>'''

def render_cventries(entries, wrap_class='item-list'):
    out = [f'<div class="{wrap_class}">']
    for args in entries:
        d, t, o, l, e1, e2 = (args + ['']*6)[:6]
        out.append(dated_entry(d, t, o, l, e1, e2))
    out.append('</div>')
    return '\n'.join(out)

def subsection_html(title, inner_html, level=4):
    return f'<h{level} class="subhead">{tex_to_html(title)}</h{level}>\n{inner_html}'

def render_tex_subsection_block(sub):
    parts = []
    if sub['entries']:
        parts.append(render_cventries(sub['entries']))
    for subsub in sub['subsubs']:
        parts.append(f'<h5 class="subsubhead">{tex_to_html(subsub["title"])}</h5>')
        parts.append(render_cventries(subsub['entries']))
    return '\n'.join(parts)

def render_tex_section(sec_title_match, out, skip_subs=None, only_subs=None):
    sec = find_section(tex_tree, sec_title_match)
    if not sec:
        return
    skip_subs = skip_subs or []
    for sub in sec['subs']:
        if any(s.lower() in sub['title'].lower() for s in skip_subs):
            continue
        if only_subs and not any(s.lower() in sub['title'].lower() for s in only_subs):
            continue
        out.append(f'<h4 class="subhead">{tex_to_html(sub["title"])}</h4>')
        out.append(render_tex_subsection_block(sub))

# ---------- Publication bibliography rendering ----------

def pub_authors_html(e):
    return format_authors(e.get('author', ''), e.get('author+an', ''))

def journal_line(e):
    bits = []
    j = e.get('journal', '')
    if j:
        bits.append(f'<i>{tex_to_html(j)}</i>')
    y = e.get('year', '')
    m = e.get('month', '')
    if m and y:
        bits.append(f'({m if not m.isdigit() else date(2000,int(m),1).strftime("%b")} {y})')
    elif y:
        bits.append(f'({y})')
    return ', '.join(bits)

def render_pub_list(entries, numbered=True, note_html=''):
    if not entries:
        return ''
    entries_sorted = sorted(entries, key=sort_key, reverse=True)
    total = len(entries_sorted)
    out = []
    if note_html:
        out.append(f'<div class="pub-note">{note_html}</div>')
    out.append('<div class="pub-list">')
    for idx, e in enumerate(entries_sorted):
        num = total - idx
        title = tex_to_html(e.get('title', ''))
        authors = pub_authors_html(e)
        jline = journal_line(e)
        url = e.get('url', '')
        note = e.get('note', '')
        bits = [f'{authors}. &ldquo;{title}.&rdquo;']
        if jline:
            bits.append(jline + '.')
        if note:
            bits.append(tex_to_html(note) + '.')
        if url:
            bits.append(f'<a href="{esc(url)}">{esc(url)}</a>')
        li_content = ' '.join(bits)
        prefix = f'<span class="pub-num">[{num}]</span> ' if numbered else ''
        out.append(f'<div class="pub-item">{prefix}{li_content}</div>')
    out.append('</div>')
    return '\n'.join(out)

# ============================================================
# Build page sections
# ============================================================

sections_html = []

# ---- Personal Information ----
pi = find_section(tex_tree, 'Personal Information')
pi_html = []
for sub in pi['subs']:
    pi_html.append(f'<h4 class="subhead">{tex_to_html(sub["title"])}</h4>')
    pi_html.append(render_cventries(sub['entries']))
sections_html.append(('Personal Information', '\n'.join(pi_html)))

# ---- Publications ----
peer = [e for e in pubs if e.get('keywords') == 'peer-reviewed']
inreview = [e for e in pubs if e.get('keywords') == 'in-review']
conference = [e for e in pubs if e.get('keywords') == 'conference']
book = [e for e in pubs if e.get('keywords') == 'book']
tech = [e for e in pubs if e.get('keywords') == 'tech']
other = [e for e in pubs if e.get('keywords') == 'other']
abspos = [e for e in pubs if e.get('keywords') == 'abspos']

today_str = date.today().strftime('%B %d, %Y')
note = (f'Note: CV author in bold; trainees are underlined.<br>'
        f'<b>{len(peer)} papers; 19,457 total citations; top 10 cited 8,722 times; H&#8209;index 60; '
        f'13 first, 33 last, 78 middle authorships</b> (Google Scholar, as of {today_str}).')

pubs_html = []
pubs_html.append('<h4 class="subhead">Published Peer-Reviewed Research Articles</h4>')
pubs_html.append(render_pub_list(peer, note_html=note))
if inreview:
    pubs_html.append('<h4 class="subhead">Manuscripts Not Yet Accepted</h4>')
    pubs_html.append(render_pub_list(inreview))
if conference:
    pubs_html.append('<h4 class="subhead">Conference Papers</h4>')
    pubs_html.append(render_pub_list(conference))
if book:
    pubs_html.append('<h4 class="subhead">Book Chapters</h4>')
    pubs_html.append(render_pub_list(book))
if tech:
    pubs_html.append('<h4 class="subhead">Technical Reports</h4>')
    pubs_html.append(render_pub_list(tech))
if other:
    pubs_html.append('<h4 class="subhead">Other Publications</h4>')
    pubs_html.append(render_pub_list(other))
sections_html.append(('Published Research', '\n'.join(pubs_html)))

# ---- Funding ----
fund_current = [e for e in funding if e.get('keywords') == 'current']
fund_complete = [e for e in funding if e.get('keywords') == 'complete']

def render_funding(entries):
    entries_sorted = sorted(entries, key=lambda e: (e.get('year',''), e.get('month','')), reverse=True)
    out = ['<div class="item-list">']
    for e in entries_sorted:
        title = e.get('usera', '')
        subtitle = e.get('userb', '')
        series = e.get('series', '')
        pi_name = e.get('author', '')
        role = e.get('userc', '')
        term = e.get('userd', '')
        total_amt = e.get('usere', '')
        year_amt = e.get('userf', '')
        abstract = e.get('abstract', '')
        num = e.get('number', '')
        line1 = f'PI: {pi_name} · Role: {role} · Term: {term}'
        line1b = f'Funding to lab, entire period: {total_amt}; current year: {year_amt}'
        full_title = ', '.join(x for x in [title, f'{subtitle} {series}'.strip()] if x)
        out.append(dated_entry(num, full_title, '', '', [line1, line1b, abstract]))
    out.append('</div>')
    return '\n'.join(out)

funding_html = []
if fund_current:
    funding_html.append('<h4 class="subhead">External Research Support: Current</h4>')
    funding_html.append(render_funding(fund_current))
if fund_complete:
    funding_html.append('<h4 class="subhead">External Research Support: Completed</h4>')
    funding_html.append(render_funding(fund_complete))
sections_html.append(('Funding', '\n'.join(funding_html)))

# ---- Talks ----
talks_local = [e for e in talks if e.get('keywords') == 'local']
talks_intl = [e for e in talks if e.get('keywords') == 'international']

def render_talks(entries):
    entries_sorted = sorted(entries, key=sort_key, reverse=True)
    out = ['<div class="pub-list">']
    for e in entries_sorted:
        title = tex_to_html(e.get('title', ''))
        addr = tex_to_html(e.get('address', ''))
        y = e.get('year', '')
        out.append(f'<div class="pub-item">&ldquo;{title}.&rdquo; {addr}{", " + y if y else ""}.</div>')
    out.append('</div>')
    return '\n'.join(out)

talks_html = []
talks_html.append('<h4 class="subhead">Invited Talks</h4>')
talks_html.append(render_talks(talks_local))
talks_html.append('<h4 class="subhead">Other Talks</h4>')
talks_html.append(render_talks(talks_intl))
sections_html.append(('Talks', '\n'.join(talks_html)))

# ---- Abstracts/Posters ----
sections_html.append(('Abstracts/Poster Presentations',
    '<h4 class="subhead">Abstracts / Posters</h4>' + render_pub_list(abspos, numbered=False)))

# ---- Educational Activities ----
edu_html = []
render_tex_section('Educational Activities', edu_html)
sections_html.append(('Educational Activities', '\n'.join(edu_html)))

# ---- Mentorship ----
PEOPLE_CATS = [
    ('researchtrackfaculty', 'Research Track Faculty Mentorship'),
    ('staffresearch', 'Staff Research Scientists'),
    ('postdoc', 'Postdoctoral Fellows'),
    ('phdstudent', 'Ph.D. Students'),
    ('visiting-phdstudent', 'Visiting Doctoral Student'),
    ('msstudent', 'M.S. Students'),
    ('undergrad', 'Undergraduate Students'),
    ('highschool', 'Highschool Student'),
]

def render_people(entries):
    out = ['<div class="item-list">']
    for e in entries:
        name = e.get('author', '')
        title = e.get('usera', '')
        degree = e.get('userb', '')
        dept = e.get('userc', '')
        abstract = e.get('abstract', '')
        yrs = e.get('number', '')
        subtitle = ' · '.join(x for x in [title, degree, dept] if x)
        out.append(dated_entry(yrs, name, subtitle, '', [abstract]))
    out.append('</div>')
    return '\n'.join(out)

mentor_html = []
for key, label in PEOPLE_CATS:
    ents = [e for e in people if e.get('keywords', '').lower() == key]
    if not ents:
        continue
    mentor_html.append(f'<h4 class="subhead">{label}</h4>')
    mentor_html.append(render_people(ents))
# thesis committee (from tex, under Mentorship section)
mentorsec = find_section(tex_tree, 'Mentorship')
for sub in mentorsec['subs']:
    if 'thesis' in sub['title'].lower():
        mentor_html.append(f'<h4 class="subhead">{tex_to_html(sub["title"])}</h4>')
        mentor_html.append(render_cventries(sub['entries']))
sections_html.append(('Mentorship', '\n'.join(mentor_html)))

# ---- Service ----
service_html = []
render_tex_section('Service', service_html)
sections_html.append(('Service', '\n'.join(service_html)))

# ---- Awards ----
awards_html = []
render_tex_section('Awards and Recognition', awards_html)
sections_html.append(('Awards and Recognition', '\n'.join(awards_html)))

# ---- Other Media (press.bib) ----
press_sorted = sorted(press, key=sort_key, reverse=True)
media_html = ['<div class="item-list">']
for e in press_sorted:
    title = '“' + e.get('title', '') + '”'
    addr = e.get('address', '')
    url = e.get('url', '')
    y = e.get('year', '')
    url_field = f'\\url{{{url}}}' if url else ''
    media_html.append(dated_entry(y, title, addr, '', [url_field]))
media_html.append('</div>')
sections_html.append(('Other Media', '\n'.join(media_html)))

# ---- Professional/Social Media Presence ----
soc_html = []
render_tex_section('Professional/Social Media Presence', soc_html)
if not soc_html:
    sec = find_section(tex_tree, 'Professional/Social Media Presence')
    if sec:
        allentries = []
        for sub in sec['subs']:
            allentries += sub['entries']
sections_html.append(('Professional/Social Media Presence', '\n'.join(soc_html)))

# ---- Translation / Tech Transfer ----
transfer_html = []
render_tex_section('Translation', transfer_html)
sections_html.append(('Translation / Technology Transfer Activities', '\n'.join(transfer_html)))

print("Sections built:", [s[0] for s in sections_html])
for name, h in sections_html:
    print(name, len(h))

import pickle
with open('sections.pkl', 'wb') as f:
    pickle.dump(sections_html, f)
