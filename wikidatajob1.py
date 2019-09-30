import os
import config
import wikidataproc

cleaned_wiki_data_file = 'd:/data/res/wikidata/wikidata-20150525-fet.json'
wikidata_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-all.json.gz')
# wikidataproc.filter_wikidata(os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-all.json.gz'),
#                              cleaned_wiki_data_file)
wikidataproc.check_item(wikidata_file, 'Q23')
