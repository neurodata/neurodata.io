import codecs
import io
import bibtexparser
import yaml
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def mo_co(mo):
    MONTH_CONVERT = {
        "": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "11": 11,
        "12": 12,
        "jan": 1,
        "Jan": 1,
        "january": 1,
        "January": 1,
        "feb": 2,
        "Feb": 2,
        "february": 2,
        "February": 2,
        "mar": 3,
        "Mar": 3,
        "march": 3,
        "March": 3,
        "apr": 4,
        "Apr": 4,
        "april": 4,
        "April": 4,
        "may": 5,
        "May": 5,
        "jun": 6,
        "June": 6,
        "june": 6,
        "June": 6,
        "jul": 7,
        "Jul": 7,
        "july": 7,
        "July": 7,
        "aug": 8,
        "Aug": 8,
        "august": 8,
        "August": 8,
        "sep": 9,
        "Sep": 9,
        "september": 9,
        "September": 9,
        "oct": 10,
        "Oct": 10,
        "october": 10,
        "October": 10,
        "nov": 11,
        "Nov": 11,
        "november": 11,
        "November": 11,
        "dec": 12,
        "Dec": 12,
        "december": 12,
        "December": 12,
    }

    return MONTH_CONVERT[mo]


def return_yaml_data(filename):
    with open(filename) as contentfile:
        data = contentfile.read()
    yaml_content = data.split("---")[1]
    yaml_data = yaml.load(yaml_content, Loader=Loader)
    return yaml_data


def entries_to_file(entries, fn):
    writer = BibTexWriter()

    db = BibDatabase()
    db.entries = entries
    with codecs.open(fn, 'w', "utf-8") as bibtex_file:
        bibtex_file.write(writer.write(db))


def main(out_dir):
    print('wablatong')
    bibs = [('content/research/publications.html', 'content/pubs/pubs.bib', ["pre_prints", "peer_reviewed", "conf", "tech_reports", "other"], "pubs"),
            ('content/research/talks.html', 'content/talks/talks.bib', ["local", "international"], "talks")]

    links = []
    for bib in bibs:

        yaml_data = return_yaml_data(bib[0])

        categories = bib[2]

        with io.open(bib[1],'r', encoding='utf-8') as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
        entries = bib_database.entries_dict

        # excluded entries first
        all_cats = [item for sublist in [yaml_data[cat]
                                         for cat in categories] for item in sublist]
        excluded_entries = [value for key,
                            value in entries.items() if key not in all_cats]
        fn = bib[3] + '_excluded_entries.bib'
        entries_to_file(excluded_entries, out_dir + fn)
        links.append(fn)

        for cat in categories:
            cat_entries = [entries[key] for key in yaml_data[cat]]
            fn = bib[3] + "_" + cat + '.bib'
            entries_to_file(cat_entries, out_dir + fn)
            links.append(fn)

        with open(out_dir + "index.html", 'w') as indexfile:
            indexfile.write("<html><body>")
            for link in links:
                indexfile.write("<a href=" + link + ">" + link + "</a><br>")
            indexfile.write("</body></html>")


if __name__ == "__main__":
    main("build/bib_files/")
