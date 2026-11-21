"""Build public HTML versions of Marp decks into source/docs/talks/.

Each deck is trimmed (slides dropped by title), stripped of speaker notes,
rendered with Marp, and published with only the local files it references.
Relative paths keep the decks-repository layout, so fonts land in
talks/theme/fonts/ and shared images in talks/people/ and so on.

Run from the repository root:  python3 misc/talks/build_talks.py
The decks repository (DECKS_DIR, default ~/github/decks) must be on a clean main.
"""
import html as htmllib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

DECKS = Path(os.environ.get("DECKS_DIR", Path.home() / "github/decks"))
DEST = Path("source/docs/talks").resolve()

# name: (source deck folder, [(drop-from title, drop-until title or None)])
TALKS = {
    "prospective-learning-astera": (
        DECKS / "prospective-learning-astera",
        [("V. Future plans", "References"), ("Appendix", None)],
    ),
    "prospective-learning-janelia": (
        DECKS / "prospective-learning-janelia",
        [("Appendix", None)],
    ),
    "prospective-learning-columbia": (
        DECKS / "prospective-learning-columbia",
        [],
    ),
}

DIRECTIVE = re.compile(r"^\s*_?[A-Za-z]+\s*:")
COMMENT = re.compile(r"<!--(.*?)-->", re.S)
REF = re.compile(r"""(?:src|href)=["']([^"']+)["']|url\(\s*['"]?([^'")]+)['"]?\s*\)""")


def title(slide):
    m = re.search(r"^# (.+)$", slide, re.M)
    return re.sub(r"<[^>]+>|\*", "", m.group(1)).strip() if m else ""


def trim(md, drops):
    parts = re.split(r"^---$", md, flags=re.M)
    front, slides = parts[1], parts[2:]
    keep, dropping, until = [], False, None
    for s in slides:
        t = title(s)
        if dropping and until and t == until:
            dropping = False
        for start, stop in drops:
            if t == start:
                dropping, until = True, stop
        if not dropping:
            keep.append(s)
    hit = sum(1 for s in slides if title(s) in {d[0] for d in drops})
    if hit != len(drops):
        sys.exit(f"drop titles not all found: {drops}")
    body = "---".join(keep)
    body = COMMENT.sub(lambda m: m.group(0) if DIRECTIVE.match(m.group(1)) else "", body)
    return f"---{front}---" + body


def require_clean_main():
    git = ["git", "-C", str(DECKS)]
    branch = subprocess.run(git + ["branch", "--show-current"],
                            capture_output=True, text=True, check=True).stdout.strip()
    dirty = subprocess.run(git + ["status", "--porcelain", "--untracked-files=no"],
                           capture_output=True, text=True, check=True).stdout.strip()
    if branch != "main" or dirty:
        sys.exit(f"{DECKS} must be on a clean main (branch {branch!r}, changes: {bool(dirty)})")


def main():
    require_clean_main()
    for name, (src, drops) in TALKS.items():
        out = DEST / name
        if out.exists():
            shutil.rmtree(out)
        out.mkdir(parents=True)
        md = out / "_public.md"
        md.write_text(trim((src / "deck.md").read_text(), drops))
        subprocess.run(
            ["npx", "marp", "--html", "--theme-set", str(DECKS / "theme/base.css"),
             "-o", str(out / "index.html"), "--", str(md)],
            check=True, cwd=DECKS, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
        )
        md.unlink()
        html = htmllib.unescape((out / "index.html").read_text())
        refs = set()
        for a, b in REF.findall(html):
            r = (a or b).split("?")[0].split("#")[0]
            if r and not re.match(r"^(https?:|data:|mailto:|//)", r):
                refs.add(unquote(r))
        for r in sorted(refs):
            f = (src / r).resolve()
            if not f.is_file():
                sys.exit(f"{name}: missing {r}")
            target = (out / r).resolve()
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, target)
        print(f"{name}: {len(refs)} files")


if __name__ == "__main__":
    main()
