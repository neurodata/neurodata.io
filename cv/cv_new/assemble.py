import pickle
from datetime import date

with open('sections.pkl', 'rb') as f:
    sections_html = pickle.load(f)

FONT_LINK = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Oswald:wght@500;700&display=swap">'

CSS = '''
* { box-sizing: border-box; }

@page {
  size: letter;
  margin: 0.55in 0.65in 0.6in 0.65in;
}

html, body {
  margin: 0;
  padding: 0;
}

body {
  font-family: 'EB Garamond', Garamond, 'Times New Roman', Times, serif;
  font-size: 10.6pt;
  line-height: 1.26;
  color: #161616;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

a {
  color: #1a3d7c;
  text-decoration: none;
}
a:hover { text-decoration: underline; }

/* ---------- Header ---------- */
.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 1.4pt solid #161616;
  padding-bottom: 10pt;
  margin-bottom: 16pt;
}
.name {
  font-family: 'Oswald', 'Arial Narrow', Arial, sans-serif;
  font-weight: 700;
  font-size: 27pt;
  letter-spacing: 2.2pt;
  text-transform: uppercase;
  color: #111;
}
.name .last {
  font-weight: 700;
}
.name .suffix {
  font-size: 13pt;
  font-weight: 500;
  color: #555;
  letter-spacing: 1pt;
  margin-left: 4pt;
}
.tagline {
  font-family: 'Oswald', sans-serif;
  font-size: 9.6pt;
  letter-spacing: 1.1pt;
  text-transform: uppercase;
  color: #444;
  margin-top: 3pt;
}
.contact-block {
  text-align: right;
  font-size: 9.6pt;
  color: #333;
  line-height: 1.55;
  white-space: nowrap;
  padding-top: 3pt;
}
.contact-block a { color: #1a3d7c; }

/* ---------- Section / subsection headers ---------- */
h3.sechead {
  font-family: 'Oswald', 'Arial Narrow', Arial, sans-serif;
  font-weight: 700;
  font-size: 13pt;
  letter-spacing: 2.4pt;
  text-transform: uppercase;
  color: #111;
  border-bottom: 0.9pt solid #b8b8b8;
  padding-bottom: 2pt;
  margin: 12pt 0 5pt 0;
  break-after: avoid;
  break-before: auto;
}
h3.sechead:first-of-type { margin-top: 0; }

h4.subhead {
  font-family: 'Oswald', 'Arial Narrow', Arial, sans-serif;
  font-weight: 500;
  font-size: 10pt;
  letter-spacing: 1.6pt;
  text-transform: uppercase;
  color: #555;
  margin: 7pt 0 3pt 0;
  break-after: avoid;
}
h5.subsubhead {
  font-family: 'EB Garamond', serif;
  font-weight: 600;
  font-style: italic;
  font-size: 10.4pt;
  color: #333;
  margin: 5pt 0 2pt 0;
  break-after: avoid;
}

/* ---------- dated item rows ---------- */
.item-list { margin-bottom: 0; }
.item {
  display: grid;
  grid-template-columns: 0.85in 1fr;
  column-gap: 8pt;
  margin-bottom: 2pt;
  break-inside: avoid;
}
.item-date {
  font-size: 9.1pt;
  color: #7a7a7a;
  letter-spacing: 0.3pt;
  white-space: nowrap;
}
.item-body { min-width: 0; }
.entry-line {
  font-size: 9.9pt;
  color: #333;
}
.entry-line b {
  font-weight: 600;
  color: #161616;
  font-style: normal;
}
.entry-line i {
  font-style: italic;
  color: #3a3a3a;
}
.entry-line + .entry-line { margin-top: 0.5pt; }

/* ---------- publication list ---------- */
.pub-note {
  font-size: 9.3pt;
  color: #555;
  margin-bottom: 7pt;
  line-height: 1.5;
}
div.pub-list { margin: 0 0 4pt 0; }
div.pub-list > .pub-item {
  padding-left: 2.05em;
  text-indent: -2.05em;
  font-size: 9.9pt;
  line-height: 1.42;
  margin-bottom: 5.5pt;
  break-inside: avoid;
}
.pub-num {
  color: #888;
  font-size: 9pt;
  display: inline-block;
  width: 2.05em;
  text-indent: 0;
}
.pub-item u { text-decoration-thickness: 0.6pt; text-underline-offset: 1.5pt; }
.pub-item a { word-break: break-all; }

/* ---------- misc ---------- */
.section-block { break-before: auto; }
'''


def name_header():
    return '''
<div class="header">
  <div>
    <div class="name">Joshua T. <span class="last">Vogelstein</span><span class="suffix">Ph.D.</span></div>
    <div class="tagline">Co-Founder, Flourish</div>
    <div class="tagline">Associate Professor, Biomedical Engineering, Johns Hopkins University</div>
  </div>
  <div class="contact-block">
    Baltimore, MD, USA<br>
    <a href="mailto:j@progl.ai">j@progl.ai</a><br>
    <a href="https://jovo.me">jovo.me</a>
  </div>
</div>
'''

parts = ['<!doctype html><html><head><meta charset="utf-8"><title>Joshua T. Vogelstein CV</title>' + FONT_LINK + '<style>' + CSS + '</style></head><body>']
parts.append(name_header())
for title, body in sections_html:
    parts.append(f'<div class="section-block"><h3 class="sechead">{title}</h3>{body}</div>')
parts.append('</body></html>')

with open('cv.html', 'w', encoding='utf-8') as f:
    f.write('\n'.join(parts))

print('wrote cv.html, size=', sum(len(p) for p in parts))
