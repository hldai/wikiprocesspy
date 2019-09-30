import os
import config
import wikidataproc
from specific import wikidatafet

cleaned_wikidata_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-fet.json')
type_items_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-fet-type-items.json')


wikidata_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-all.json.gz')
# wikidataproc.filter_wikidata(os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-all.json.gz'),
#                              cleaned_wiki_data_file)
# wikidataproc.check_item(wikidata_file, 'Q3282637')
wikidatafet.gen_type_items_file(cleaned_wikidata_file, type_items_file)
