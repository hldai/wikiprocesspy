import gzip
import json
import os
import random

for _ in range(5):
    print(random.randrange(0,9), random.randrange(0,9))

# f = gzip.open('d:/data/res/wikidata/wikidata-20190923-fet.json.gz', 'rt', encoding='utf-8')
# f = open('d:/data/res/wikidata/wikidata-20190923-fet.json', encoding='utf-8')
# for i, line in enumerate(f):
#     item = json.loads(line)
#     print(item)
#     if i > 10:
#         break
# f.close()
