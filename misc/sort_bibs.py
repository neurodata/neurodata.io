"""Sort the bib files by ID (for doing a diff)
"""


import codecs

import bibtexparser

from .create_bibs import entries_to_file


bibs = [
    (
        "content/research/publications.html",
        "content/pubs/pubs.bib",
        ["pre_prints", "peer_reviewed", "conf", "tech_reports", "other"],
        "pubs",
    ),
    (
        "content/research/talks.html",
        "content/talks/talks.bib",
        ["local", "international"],
        "talks",
    ),
]

for bib in bibs:
    with codecs.open(bib[1], "r", "utf-8") as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    entries = bib_database.entries
    entries_sort = sorted(entries, key=lambda x: x["ID"])

    entries_to_file(entries_sort, bib[1])
