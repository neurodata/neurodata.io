import codecs
from bibtexparser.bibdatabase import BibDatabase
import bibtexparser
from bibtexparser.bwriter import BibTexWriter


invited_talks = ["j1cohbm2019",
                 "bootcamp2019",
                 "j1cohbm2019",
                 "goldsachs2019",
                 "dipy19",
                 "sfn2018",
                 "princeton2018",
                 "bridgefordohbm2018",
                 "perlman3dem",
                 "big-data-talk2018",
                 "jovoyalemgc2018",
                 "sfnDC2017",
                 "JovoSOHOPa",
                 "dc-sfn2017",
                 "KeyStateBrain",
                 "JovoSOHOPb",
                 "kndi2016",
                 "paninski2015",
                 "TopChaBig",
                 "BigNeuSta",
                 "StaInf2",
                 "StaInf3",
                 "BeyLitNeu",
                 "BigNeu2",
                 "StaCon",
                 "WhaCanTra",
                 "ConClaSta",
                 "ConConCla",
                 "OncConWha",
                 "OncGetCon",
                 "InfSpiTraCI",
                 "InfSpiTraCI2",
                 "InfSpiTra",
                 "ModBasOpt",
                 "discoveringstanford2017",
                 "StaModInf",
                 "OpeProNeu",
                 "DecTheApp", ]

other_talks = ["l2f18mo",
               "dscore2019",
               "forestpacking2019",
               "reg2019daniel",
               "sloan2019",
               "jhu-bmes19",
               "kavli19",
               "l2f1year",
               "ndtools",
               "jovodata2019",
               "neuronex18",
               "exactequivalence2019",
               "jovodarpamgc2018",
               "neuronex-stanford2018",
               "kiarconnectomecoding2018",
               "BSI-google2018",
               "L2F2018",
               "dibs2018",
               "disa2017",
               "kiarscienceinthecloud2017",
               "leejsm2017",
               "knor2017",
               "sdm17",
               "sfnDC2017",
               "allen2017",
               "china2017",
               "feldman2017",
               "neurostorm2017",
               "multiscale2016",
               "ODEN2018",
               "brain2016",
               "kndi2016",
               "nd2016",
               "post2016",
               "sfn2016",
               "src2016",
               "open2016",
               "localdistance2015",
               "OpeChaBig",
               "FroRagRic",
               "LawLarGra",
               "LowBarEnt",
               "KavSpeSymp",
               "CasC",
               "JovoSimA",
               "JovoSimB",
               "opensource2015",
               "bigtime2015",
               "BigStaBra",
               "BigNeuSta",
               "OpeConPro",
               "ConsGraCla",
               "AreMenPro",
               "TowInfAna",
               "SeqMonCar",
               "OopFamOpt",
               "TowInfNeu",
               "NeuGraThe",
               "InfSpiTim",
               ]


with open('content/talks/talks.bib') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

entries = bib_database.entries_dict

invited_entries = [entries[key] for key in invited_talks]
other_entries = [entries[key] for key in other_talks]
excluded_entries = [value for key,
                    value in entries.items() if key not in invited_talks and key not in other_talks]

writer = BibTexWriter()

db = BibDatabase()
db.entries = invited_entries
with codecs.open('content/talks/invited.bib', 'w', "utf-8") as bibtex_file:
    bibtex_file.write(writer.write(db))


db = BibDatabase()
db.entries = other_entries
with codecs.open('content/talks/other.bib', 'w', "utf-8") as bibtex_file:
    bibtex_file.write(writer.write(db))


db = BibDatabase()
db.entries = excluded_entries
with codecs.open('content/talks/excluded_entries.bib', 'w', "utf-8") as bibtex_file:
    bibtex_file.write(writer.write(db))
