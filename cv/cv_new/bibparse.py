import re

def parse_bib(path):
    """Parse a .bib file into a list of dicts with brace-matching (handles nested braces in fields)."""
    with open(path, encoding='utf-8') as f:
        content = f.read()

    entries = []
    i, n = 0, len(content)
    while i < n:
        if content[i] == '@':
            j = content.index('{', i)
            etype = content[i+1:j].strip().lower()
            depth = 1
            k = j + 1
            while depth > 0 and k < n:
                if content[k] == '{':
                    depth += 1
                elif content[k] == '}':
                    depth -= 1
                k += 1
            raw = content[j+1:k-1]  # inside outer braces
            entries.append((etype, raw))
            i = k
        else:
            i += 1

    parsed = []
    for etype, raw in entries:
        comma = raw.index(',')
        key = raw[:comma].strip()
        body = raw[comma+1:]
        fields = {}
        m = 0
        L = len(body)
        while m < L:
            fm = re.match(r'\s*([A-Za-z+_]+)\s*=\s*', body[m:])
            if not fm:
                break
            fname = fm.group(1).strip().lower()
            m += fm.end()
            if m < L and body[m] == '{':
                depth = 1
                start = m + 1
                p = start
                while depth > 0 and p < L:
                    if body[p] == '{':
                        depth += 1
                    elif body[p] == '}':
                        depth -= 1
                    p += 1
                val = body[start:p-1]
                m = p
            elif m < L and body[m] == '"':
                start = m + 1
                p = body.index('"', start)
                val = body[start:p]
                m = p + 1
            else:
                cm = re.match(r'([^,]*)', body[m:])
                val = cm.group(1)
                m += cm.end()
            fields[fname] = val.strip()
            # skip to next comma
            cm2 = re.match(r'\s*,', body[m:])
            if cm2:
                m += cm2.end()
        fields['_type'] = etype
        fields['_key'] = key
        parsed.append(fields)
    return parsed


def parse_author_an(annotation):
    """Parse author+an = {1=trainee;4=trainee;3=highlight} -> {1: 'trainee', 3: 'highlight', ...}"""
    result = {}
    if not annotation:
        return result
    for part in annotation.split(';'):
        part = part.strip()
        if not part or '=' not in part:
            continue
        pos, role = part.split('=', 1)
        try:
            result[int(pos.strip())] = role.strip()
        except ValueError:
            pass
    return result


def split_authors(author_field):
    if not author_field:
        return []
    return [a.strip() for a in re.split(r'\s+and\s+', author_field.strip())]
