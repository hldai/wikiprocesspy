import gzip
import json
import pandas as pd
import os
import wikiutils


res_dir = 'd:/data/res'
mid_wid_file = os.path.join(res_dir, 'freebase/mid-wiki-id.txt')
title_wid_file = os.path.join(res_dir, 'wiki/el/enwiki-20151002-title-wid-entityonly.txt')

in_fb_wids = set()
with open(mid_wid_file, encoding='utf-8') as f:
    for line in f:
        _, wid = line.strip().split('\t')
        in_fb_wids.add(wid)

with open(title_wid_file, encoding='utf-8') as f:
    df = pd.read_csv(f, na_filter=False)

for title, wid in df.itertuples(False, None):
    if wid not in in_fb_wids:
        print(title)
        # title_words = title.split(' ')
        # if 'of' in title_words or 'in' in title_words or '/' in title:
        #     print(title)
