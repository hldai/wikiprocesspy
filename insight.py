import gzip
import json
import pandas as pd
import os
import config
import wikiutils


cleaned_wikidata_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20150525-fet.json')
f = open(cleaned_wikidata_file, encoding='utf-8')
for i, line in enumerate(f):
    item = json.loads(line)
    vals = item.get('insof')
    if vals:
        if 'Q18388277' in vals:
            print(item)
    # if i > 100:
    #     break
f.close()
