import os
import config
import wikidataproc
from specific import wikidatafet

# wikidata_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-all.json.gz')
# cleaned_wikidata_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-fet.json')
# insof_type_items_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-fet-insof-items.json')
# subcls_type_items_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-fet-subcls-items.json')
# occupation_type_items_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-fet-occupation-items.json')
# insof_type_cnts_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-fet-insof-type-cnts.txt')
# occupation_type_cnts_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-fet-occupation-type-cnts.txt')
# subcls_type_cnts_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-fet-subcls-type-cnts.txt')

wikidata_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20190923-all.json.gz')
raw_cleaned_wikidata_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20190923-fet.json')
cleaned_wikidata_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20190923-fet.json.gz')
insof_type_items_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20190923-fet-insof-items.json')
subcls_type_items_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20190923-fet-subcls-items.json')
occupation_type_items_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20190923-fet-occupation-items.json')
insof_type_cnts_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20190923-fet-insof-type-cnts-tmp.txt')
occupation_type_cnts_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20190923-fet-occupation-type-cnts.txt')
subcls_type_cnts_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20190923-fet-subcls-type-cnts.txt')
wikidata_wikipedia_map_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20190923-wikipedia-map.txt')
wiki_title_wid_file = os.path.join(config.RES_DIR, 'wiki/enwiki-20190101-title-wid.txt')
wid_wikidata_types_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20190923-wid-types-tmp.txt')


# wikidataproc.filter_wikidata(wikidata_file, raw_cleaned_wikidata_file)
# wikidataproc.check_item(wikidata_file, 'Q18388277')
# wikidatafet.gen_type_items_file(cleaned_wikidata_file, insof_type_items_file, subcls_type_items_file,
#                                 occupation_type_items_file)
# wikidatafet.gen_type_cnts_file(insof_type_items_file, insof_type_cnts_file)
# wikidatafet.gen_type_cnts_file(occupation_type_items_file, occupation_type_cnts_file)
# wikidatafet.gen_type_cnts_file(subcls_type_items_file, subcls_type_cnts_file)
# wikidataproc.gen_wikidata_wikipedia_map_file(cleaned_wikidata_file, wikidata_wikipedia_map_file)
wikidatafet.gen_wid_wikidata_types_file(cleaned_wikidata_file, wiki_title_wid_file, wid_wikidata_types_file)
