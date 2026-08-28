# CV build pipeline

Custom LaTeX-free pipeline for Joshua Vogelstein's academic CV: Python parses
the bib/tex source data and renders HTML, Playwright prints it to PDF.

## Layout

- `cv_build/` — source data: `jovo-cv.yaml`, `*.bib` (publications, funding,
  people, press, talks), and `tex/jovo_cv_SOM.tex` (structural data for
  Personal Information, Service, Awards, etc., in LaTeX/moderncv `\cventry`
  syntax — parsed as data only, never compiled with LaTeX).
- `cv_new/` — the build pipeline:
  - `bibparse.py`, `texparse.py`, `latexutil.py` — parsing/HTML-escaping helpers
  - `build_cv.py` — renders each CV section to HTML
  - `assemble.py` — wraps sections in the full HTML document + CSS
  - `render.js` — Playwright script, prints `cv.html` to PDF
  - `jovo_cv.pdf` — last rendered output

## Build

```bash
cd cv_new
npm install
python3 build_cv.py && python3 assemble.py && node render.js
```

Verify the output has no leaked LaTeX/double-escaped HTML:

```bash
pdftotext jovo_cv.pdf - | grep -nE '\\[a-zA-Z]+|&amp;[a-z]+;' | grep -v '^[0-9]*:https\?://'
```

This should print nothing.
