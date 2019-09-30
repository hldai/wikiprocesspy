import gzip
import json

f = gzip.open('d:/data/res/wikidata/wikidata-20190923-fet.json.gz', 'rt', encoding='utf-8')
for i, line in enumerate(f):
    item = json.loads(line)
    print(item)
    if i > 10:
        break
f.close()
