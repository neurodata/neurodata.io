import re
from datetime import datetime

import bibtexparser
from bibtexparser.bparser import BibTexParser
from jinja2.ext import Extension
import io

def mo_co(mo):

    MONTH_CONVERT = {
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
    try:
        return(int(mo))
    except:
        return MONTH_CONVERT[mo]


def load_bibtex(bibfile):

    parser = BibTexParser()
    parser.ignore_nonstandard_types = False

    with io.open(bibfile, 'r', encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file, parser=parser)

    bib_entries = bib_database.entries

    bib_entries.sort(key=lambda x: x.get("author", ""))
    bib_entries.sort(key=lambda x: mo_co(x.get("month", "")), reverse=True)
    bib_entries.sort(key=lambda x: x.get("year", ""), reverse=True)

    return bib_entries


def load_members(bibfile):
    parser = BibTexParser()
    parser.ignore_nonstandard_types = False

    with io.open(bibfile, 'r', encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file, parser=parser)

    bib_entries = bib_database.entries

    position_order = ['director','faculty','faculty - research','staff','postdoc','student','undergrad','associate','highschool', 'other']

    order = {key: i  for i, key in enumerate(position_order)}
    bib_entries.sort(key=lambda d: d.get("author", ""))
    bib_entries.sort(key=lambda d: order[d.get("userd")])

    #bib_entries.sort(key=lambda x: x.get("author", ""))
    #bib_entries.sort(key=lambda x: mo_co(x.get("month", "")), reverse=True)
    #bib_entries.sort(key=lambda x: x.get("year", ""), reverse=True)

    return bib_entries


def auth_formatted(authors):
    """format the authors in intials. last name
    e.g. J. V. Vogelstein
    """

    auths_format = []
    for author in authors:
        names = author.split(", ")
        last = names[0]
        if last[0] == "{" and last[-1] == "}":
            last = last[1:-1]
        initials = []
        if len(names) > 1:
            for n in names[1].split(" "):
                if len(n) > 1:
                    initials += n[0] + ". "
                else:
                    initials += n + ". "
        full_name_format = "".join(initials) + last
        auths_format.append(full_name_format)

    return auths_format


def all_authors(bib_entry):
    authors = bib_entry["author"].split(" and ")

    auths_format = auth_formatted(authors)

    return auths_format


def all_authors_annotated(bib_entry):
    authors = bib_entry["author"].split(" and ")
    auths_format = auth_formatted(authors)

    an_entries = bib_entry.get("author+an", None)

    if an_entries is not None:
        an_entries_list = an_entries.split(";")
        for an_entry in an_entries_list:
            an_parts = an_entry.split("=")
            an_id = int(an_parts[0]) - 1
            an_type = an_parts[1]

            cur_auth = auths_format[an_id]
            if an_type == "highlight":
                auths_format[an_id] = '<span class="font-bold">' + cur_auth + '</span>'
            elif an_type == "trainee":
                auths_format[an_id] = '<span class="italic">' + cur_auth + '</span>'

    return auths_format


def print_authors(bib_entry):
    authors = bib_entry["author"].split(" and ")

    auths_format = auth_formatted(authors)

    # return et al if # of auths_format > 3
    if len(auths_format) > 3:
        return auths_format[0] + " et al."
    elif len(auths_format) == 1:
        return auths_format[0] + "."
    else:
        return u"{} and {}.".format(", ".join(auths_format[0:-1]), auths_format[-1])


def print_link(bib_entry):
    if "doi" in bib_entry:
        return "https://doi.org/" + bib_entry["doi"]
    if "url" in bib_entry:
        return bib_entry["url"]
    if "arxivid" in bib_entry:
        arxivID = bib_entry["arxivid"].replace("arXiv:", "")
        return "https://arxiv.org/abs/{}".format(arxivID)
    print("{} did not have a link".format(bib_entry["ID"]))
    # print('here are the keys')
    # for key in bib_entry:
    #     print(key)


def print_venue(bib_entry):
    if "journal" in bib_entry:
        return bib_entry["journal"]

    # probably a conference
    if "booktitle" in bib_entry:
        return bib_entry["booktitle"]


def print_address(bib_entry):
    if "address" in bib_entry:
        address = bib_entry["address"]
        address = address.replace("\\&", "&")
        return address


def print_title(bib_entry):
    title = bib_entry["title"]

    title = title.replace("\\&", "&")

    if title[0] == "{" and title[-1] == "}":
        title = title[1:-1]

    if "\href" in title:
        m = re.findall(r"\\href\{(.+)\}{(.+)}", title)
        link = m[0][0]
        t = m[0][1]
        title = '<a href="{}">{}</a>'.format(link, t)

    return title


def print_issue_data(bib_entry):
    if "pages" in bib_entry and "number" in bib_entry and "volume" in bib_entry:
        return print_issue(bib_entry) + print_volume(bib_entry) + print_pages(bib_entry)
    else:
        return ""


def print_pages(bib_entry):
    pages = bib_entry["pages"]
    pages = pages.replace("--", "-")
    return ":" + pages + ", "


def print_volume(bib_entry):
    return "{}".format(bib_entry["volume"])


def print_issue(bib_entry):
    return "({})".format(bib_entry["number"])


def print_current_year(_):
    return datetime.now().year


def print_usera(bib_entry):
    usera = bib_entry["usera"]
    usera = usera.replace("\\&", "&")
    if usera[0] == "{" and usera[-1] == "}":
        usera = usera[1:-1]
    return usera

def print_userb(bib_entry):
    userb = bib_entry["userb"]
    userb = userb.replace("\\&", "&")
    if userb[0] == "{" and userb[-1] == "}":
        userb = userb[1:-1]
    return userb

def print_series(bib_entry):
    series = bib_entry["series"]
    series = series.replace("\\&", "&")
    if series[0] == "{" and series[-1] == "}":
        series = series[1:-1]
    return series

def print_userd(bib_entry):
    userd = bib_entry["userd"]
    userd = userd.replace("\\&", "&")
    if userd[0] == "{" and userd[-1] == "}":
        userd = userd[1:-1]
    return userd

def print_abstract(bib_entry):
    abstract = bib_entry["abstract"]
    abstract = abstract.replace("\\&", "&")
    if abstract[0] == "{" and abstract[-1] == "}":
        abstract = abstract[1:-1]
    return abstract


class BIBTEX_PRINT(Extension):
    def __init__(self, environment):
        super(BIBTEX_PRINT, self).__init__(environment)
        environment.filters["load_bibtex"] = load_bibtex
        environment.filters["load_members"] = load_members
        environment.filters["all_authors"] = all_authors
        environment.filters["all_authors_annotated"] = all_authors_annotated
        environment.filters["print_authors"] = print_authors
        environment.filters["print_link"] = print_link
        environment.filters["print_title"] = print_title
        environment.filters["print_venue"] = print_venue
        environment.filters["print_address"] = print_address
        environment.filters["print_issue_data"] = print_issue_data
        environment.filters["print_current_year"] = print_current_year
        environment.filters["print_usera"] = print_usera
        environment.filters["print_userb"] = print_userb
        environment.filters["print_userd"] = print_userd
        environment.filters["print_series"] = print_series
        environment.filters["print_abstract"] = print_abstract
