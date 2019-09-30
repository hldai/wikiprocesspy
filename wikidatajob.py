import os
import config
import wikidataproc
from specific import wikidatafet

wikidata_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-all.json.gz')
cleaned_wikidata_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-fet.json')
insof_type_items_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-fet-insof-items.json')
subcls_type_items_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-fet-subcls-items.json')
occupation_type_items_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-fet-occupation-items.json')
insof_type_cnts_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-fet-insof-type-cnts.txt')
occupation_type_cnts_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-fet-occupation-type-cnts.txt')
subcls_type_cnts_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-fet-subcls-type-cnts.txt')


# wikidataproc.filter_wikidata(os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-all.json.gz'),
#                              cleaned_wiki_data_file)
wikidataproc.check_item(wikidata_file, 'Q18388277')
# wikidatafet.gen_type_items_file(cleaned_wikidata_file, insof_type_items_file, subcls_type_items_file,
#                                 occupation_type_items_file)
# wikidatafet.gen_type_cnts_file(insof_type_items_file, insof_type_cnts_file)
# wikidatafet.gen_type_cnts_file(occupation_type_items_file, occupation_type_cnts_file)
# wikidatafet.gen_type_cnts_file(subcls_type_items_file, subcls_type_cnts_file)
