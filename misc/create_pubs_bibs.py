import codecs
from bibtexparser.bibdatabase import BibDatabase
import bibtexparser
from bibtexparser.bwriter import BibTexWriter


def mo_co(mo):
    MONTH_CONVERT = {
        "": 0,
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


pre_prints = [
    "perry2019manifold",
    "deeplearning2019",
    "neurosubtypes2019",
    "heritability2019",
    "mgcpy2019",
    "graphyti2019",
    "alignment2019",
    "geodesic2019",
    "mgcpy2019",
    "estimatingforests2019",
    "networkinference2019",
    "graphindependence2019",
    "vertex2019",
    "bagging2019",
    "graspy2019",
    "kiar2017comprehensive",
    "vogelstein2018geometric",
    "ShenDecision2018",
    "Greenberg479055",
    "Vogelstein2018equivalence",
    "Kiar2018",
    "Wang2018",
    "Wang2017",
    "Tang2017",
    "Tomita2018",
    "Lyzinski2014",
    "wang2018statistical",
    "francca2017kernel",
    "mhembere2019",
    "Branch639674", ]

peer_reviewed = [
    "Kiar2017",
    "klein2019",
    "connectalcoding",
    "lee2017",
    "priebe2018two",
    "shen2016discovering",
    "tang2016law",
    "Shen2018",
    "burns2018community",
    "Durante2017",
    "Cohen2018",
    "Zheng2016b",
    "dyer2017quantifying",
    "simhal2017probabilistic",
    "Shen201741",
    "hildebrand2017whole",
    "Chen2017",
    "wang2017selected",
    "Binkiewicz2014",
    "Chen2016b",
    "Raag2016",
    "Durante2016",
    "Chen2015",
    "harris2015resource",
    "Koutra2016",
    "Roncal2015b",
    "kasthuri2015saturated",
    "Vogelstein2015",
    "Vogelstein2015b",
    "Lyzinski2015",
    "Lyzinski2014a",
    "Weiler2014",
    "Priebe2015",
    "Sweeney2014",
    "vogelstein2014discovery",
    "Carlson2014",
    "Vogelstein2013",
    "Craddock2013",
    "Priebe2013",
    "Dai2012",
    "Fishkind2013",
    "Roberts2012",
    "Gray2012",
    "Vogelstein2011b",
    "Hofer2011",
    "Mishchenko2011",
    "Vogelstein2010",
    "Paninski2010",
    "Vogelstein2009",
    "Vogelstein2007",
    "Vogelstein2003",
    "Greenspan1997",
    "Athreya2018", ]

conf = [
    "zheng2016flashr",
    "Browne2018",
    "Lillaney2018",
    "Nikolaidis343392",
    "Cornelis2013",
    "Kutten2016",
    "Fiori2013",
    "Carlson2013a",
    "Mhembere2013",
    "GrayRoncal2013",
    "Koutra2013",
    "Kulkarni2013",
    "Petralia2013",
    "Kutten2016b",
    "Huys2009",
    "GrayRoncal2015a",
    "Zheng2015",
    "burns2013open",
    "tomita2017roflmao",
    "mhembere2017knor", ]

tech_reports = [
    "kiar2018neurostorm",
    "Kazhdan2013",
    "Banerjee2013",
    "Priebe2017",
    "Zheng2016",
    "Zheng2016c",
    "sinha2014automatic", ]

other = [
    "oopsi",
    "neuro2016",
    "GlobalBrain",
    "BrainWorkshop",
    "burns2014cosmos",
    "Yuste2011",
    "Vogelstein2011c",
    "Vogelstein1999", ]

categories = ["pre_prints", "peer_reviewed", "conf", "tech_reports", "other"]

with open('content/pubs/pubs.bib') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

entries = bib_database.entries_dict

writer = BibTexWriter()

for cat in categories:
    cat_entries = [entries[key] for key in eval(cat)]

    cat_entries.sort(key=lambda x: x.get("author", ""))
    cat_entries.sort(key=lambda x: mo_co(x.get("month", "")), reverse=True)
    cat_entries.sort(key=lambda x: x.get("year", ""), reverse=True)

    db = BibDatabase()
    db.entries = cat_entries

    with codecs.open('content/pubs/' + cat + '.bib', 'w', "utf-8") as bibtex_file:
        bibtex_file.write(writer.write(db))

all_cats = [item for item in eval(cat) for cat in categories]
excluded_entries = [value for key,
                    value in entries.items() if key not in all_cats]

with open('content/pubs/excluded_entries.bib', 'w') as bibtex_file:
    bibtex_file.write(writer.write(db))
