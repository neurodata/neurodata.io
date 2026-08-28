import re
import html as htmlmod

def tex_to_html(s):
    if s is None:
        return ''
    s = s.strip()
    # strip a single fully-enclosing brace pair (bibtex case-protection idiom: title = {{Text}})
    while len(s) >= 2 and s[0] == '{' and s[-1] == '}':
        depth = 0
        fully_wraps = True
        for idx, ch in enumerate(s):
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0 and idx != len(s) - 1:
                    fully_wraps = False
                    break
        if fully_wraps:
            s = s[1:-1].strip()
        else:
            break
    # protect literal \$ (currency) so it can't be mistaken for a math-mode $ delimiter
    s = s.replace('\\$', '\x00DOLLAR\x00')
    # strip bare math-mode $...$ delimiters (used here only for typographic escaping, not real math)
    s = re.sub(r'\$([^$]*)\$', r'\1', s)
    s = s.replace('\x00DOLLAR\x00', '$')
    # escaped specials -> literal chars
    s = s.replace('\\&', '&').replace('\\%', '%').replace('\\#', '#').replace('\\_', '_')
    s = s.replace('\\times', '&times;').replace('\\sim', '~').replace("\\'", "'")
    # href
    def href_repl(m):
        url = m.group(1)
        text = m.group(2)
        return f'@@LINK_START@@{url}@@LINK_MID@@{text}@@LINK_END@@'
    # handle nested-brace-safe href via manual scan (titles can contain nested braces)
    out = []
    i = 0
    n = len(s)
    while i < n:
        mu = re.match(r'\\url\{', s[i:])
        if mu:
            i += mu.end()
            start = i
            depth = 1
            while depth > 0 and i < n:
                if s[i] == '{':
                    depth += 1
                elif s[i] == '}':
                    depth -= 1
                i += 1
            url = s[start:i-1]
            out.append(('LINK', url, url))
            continue
        m = re.match(r'\\href\{', s[i:])
        if m:
            i += m.end()
            start = i
            depth = 1
            while depth > 0 and i < n:
                if s[i] == '{':
                    depth += 1
                elif s[i] == '}':
                    depth -= 1
                i += 1
            url = s[start:i-1]
            m2 = re.match(r'\{', s[i:])
            if m2:
                i += 1
                start2 = i
                depth = 1
                while depth > 0 and i < n:
                    if s[i] == '{':
                        depth += 1
                    elif s[i] == '}':
                        depth -= 1
                    i += 1
                text = s[start2:i-1]
                out.append(('LINK', url, text))
                continue
        mb = re.match(r'\\(textbf|textit|emph|textnormal|uline|underline)\{', s[i:])
        if mb:
            cmd = mb.group(1)
            i += mb.end()
            start = i
            depth = 1
            while depth > 0 and i < n:
                if s[i] == '{':
                    depth += 1
                elif s[i] == '}':
                    depth -= 1
                i += 1
            out.append((cmd.upper(), s[start:i-1]))
            continue
        out.append(('CHAR', s[i]))
        i += 1

    WRAP = {
        'TEXTBF': ('<b>', '</b>'),
        'TEXTIT': ('<i>', '</i>'),
        'EMPH': ('<i>', '</i>'),
        'ULINE': ('<u>', '</u>'),
        'UNDERLINE': ('<u>', '</u>'),
        'TEXTNORMAL': ('', ''),
    }
    result = []
    for tok in out:
        if tok[0] == 'LINK':
            url, text = tok[1], tok[2]
            result.append(f'<a href="{htmlmod.escape(url)}">{tex_to_html(text)}</a>')
        elif tok[0] in WRAP:
            openw, closew = WRAP[tok[0]]
            result.append(f'{openw}{tex_to_html(tok[1])}{closew}')
        else:
            result.append(htmlmod.escape(tok[1]))
    final = ''.join(result)
    final = final.replace('$\\sim$', '~').replace('\\newline', '<br>')
    final = final.replace('---', '&mdash;').replace('--', '&ndash;')
    final = final.replace('~', '&nbsp;')
    return final


def format_authors(author_field, an_field):
    """Return HTML string of authors with jovo bolded and trainees underlined."""
    from bibparse import split_authors, parse_author_an
    authors = split_authors(author_field)
    roles = parse_author_an(an_field)
    parts = []
    for idx, a in enumerate(authors, start=1):
        name = a.strip()
        # bib names are "Last, First" -> convert to "First Last"
        if ',' in name:
            last, first = name.split(',', 1)
            disp = f'{first.strip()} {last.strip()}'
        else:
            disp = name
        disp_html = htmlmod.escape(disp)
        role = roles.get(idx)
        if role == 'highlight':
            disp_html = f'<b>{disp_html}</b>'
        elif role == 'trainee':
            disp_html = f'<u>{disp_html}</u>'
        parts.append(disp_html)
    if len(parts) > 1:
        return ', '.join(parts[:-1]) + ', and ' + parts[-1]
    elif parts:
        return parts[0]
    return ''
