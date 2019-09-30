import gzip
import json
import pandas as pd
import os
import config
import wikiutils


def __chech_val():
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


def __count_lines():
    wikidata_file = os.path.join(config.RES_DIR, 'wikidata/wikidata-20190923-all.json.gz')
    cnt = 0
    with gzip.open(wikidata_file, 'rt', encoding='utf-8') as f:
        for _ in f:
            cnt += 1
            if cnt % 1000000 == 0:
                print(cnt)
    print(cnt)


__count_lines()
