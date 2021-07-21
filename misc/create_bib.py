# '''
# This script was run against a listing of publications to get a basic bibtex file from google scholar.

# Google scholar throttles these queries, so this was not viable for the long term.  
# References are now managed in mendeley with a synchronized bibtex file in the content/pubs director.
# '''

# import pprint
# import subprocess
# from pathlib import Path

# import requests
# from ruamel.yaml import YAML
# from scholar import *

# yaml = YAML(typ='safe')

# p = Path('content/publications')
# pubs = [fn for fn in p.iterdir() if fn.name[0] != '_']

# bib_fn = Path('data/pubs_retry.bib')

# result_csv = []
# for pub in pubs:
#     try:
#         with pub.open() as pf:
#             pub_data = yaml.load(pf)
#     except:
#         print('failed to load pub: ', pub)
#         continue

#     # pprint.pprint(pub_data)
#     # if pub_data['link'] is None:
#     #     print(pub, 'missing link')
#     # else:
#     #     print(pub_data['link'])

#     ScholarConf.COOKIE_JAR_FILE = 'cookie_file.txt'

#     querier = ScholarQuerier()
#     settings = ScholarSettings()
#     settings.set_citation_format(ScholarSettings.CITFORM_BIBTEX)
#     querier.apply_settings(settings)

#     query = SearchScholarQuery()
#     query.set_words(pub_data['article_title'])
#     query.set_scope(True)
#     query.set_num_page_results(1)

#     querier.send_query(query)
#     articles = querier.articles

#     if not articles:
#         # perform query on URL
#         query = SearchScholarQuery()
#         query.set_words(pub_data['link'])
#         query.set_num_page_results(1)

#         querier.send_query(query)
#         articles = querier.articles

#     result = None
#     for art in articles:
#         result = art.as_citation()
#         result_csv.append(csv(querier, header=True))

#     # scholar.py -c 1 --author "albert einstein" --phrase "quantum theory" --citation bt
#     # cmd_base = 'misc/scholar.py'
#     # cmd = 'python.exe {} -c 1 -A "{}" --citation bt'.format(
#     #     cmd_base, pub_data['article_title'])
#     # result = subprocess.check_output(cmd)

#     # print(str(result))
#     if result:
#         with open(bib_fn, 'ab') as bf:
#             bf.write(result)
#     else:
#         print('no result found for:', pub)
