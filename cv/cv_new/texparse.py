import re

def strip_comments(text):
    out_lines = []
    for line in text.split('\n'):
        # naive: drop lines starting with % (after optional whitespace), keep others as-is
        # (none of our content lines use literal \% so this is safe enough)
        stripped = line.lstrip()
        if stripped.startswith('%'):
            continue
        out_lines.append(line)
    return '\n'.join(out_lines)


def read_braced_args(s, i, n_args):
    """Starting at s[i] == '{', read n_args consecutive {..} groups (brace-matched). Returns (list_of_strings, next_index)."""
    args = []
    for _ in range(n_args):
        while i < len(s) and s[i] != '{':
            if s[i] not in ' \t\n':
                return None, i
            i += 1
        if i >= len(s) or s[i] != '{':
            return None, i
        i += 1
        start = i
        depth = 1
        while depth > 0 and i < len(s):
            if s[i] == '{':
                depth += 1
            elif s[i] == '}':
                depth -= 1
            i += 1
        args.append(s[start:i-1])
    return args, i


def parse_sections(tex_text):
    """Walk the document body, tracking section/subsection/subsubsection headers and
    collecting \\cventry{..}x6 entries under each. Returns nested dict structure."""
    text = strip_comments(tex_text)
    # only look at the document body
    body_start = text.index(r'\begin{document}')
    body_end = text.index(r'\end{document}')
    text = text[body_start:body_end]

    tokens = []  # list of ('section'|'subsection'|'subsubsection'|'entry', data)
    i = 0
    n = len(text)
    while i < n:
        m = re.match(r'\\(section|subsection|subsubsection)\*?\{', text[i:])
        if m:
            level = m.group(1)
            j = i + m.end()
            depth = 1
            start = j
            while depth > 0 and j < n:
                if text[j] == '{':
                    depth += 1
                elif text[j] == '}':
                    depth -= 1
                j += 1
            title_raw = text[start:j-1]
            tokens.append((level, title_raw))
            i = j
            continue
        m2 = re.match(r'\\cventry\{', text[i:])
        if m2:
            j = i + len('\\cventry')
            args, j = read_braced_args(text, j, 6)
            if args:
                tokens.append(('entry', args))
            i = j
            continue
        i += 1
    return tokens


def strip_href_title(title_raw):
    """If title is \\href{url}{text}, return text (plain-ish); else return as-is."""
    m = re.match(r'\\href\{.*?\}\{(.*)\}$', title_raw.strip(), re.DOTALL)
    if m:
        return m.group(1)
    return title_raw
