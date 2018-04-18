'''
Checks over the older publications to see which are missing from the bibtex file
'''

import pprint
from pathlib import Path

import bibtexparser
from ruamel.yaml import YAML

yaml = YAML(typ='safe')

p = Path('content/publications')
pubs = [fn for fn in p.iterdir() if fn.name[0] != '_']

bib_fn = Path('content/pubs/pubs.bib')
with open(bib_fn) as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)
entries = bib_database.entries
entry_titles = [x['title'].lower() if x['title'][0] !=
                '{' else x['title'][1:-1].lower() for x in entries]
entry_dois = [x['doi'] if 'doi' in x else None for x in entries]
entry_urls = [x['url'] if 'url' in x else None for x in entries]

for i, pub in enumerate(pubs):
    try:
        with pub.open() as pf:
            pub_data = yaml.load(pf)
    except:
        print('failed to load pub: ', pub)
        continue

    if pub_data['article_title'].lower() not in entry_titles:
        print('pub: ', i)
        print('missing title:', pub_data['article_title'])
