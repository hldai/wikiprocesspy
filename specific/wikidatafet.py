import json


def gen_type_items_file(cleaned_fet_wikidata_file, output_file):
    f = open(cleaned_fet_wikidata_file, encoding='utf-8')
    for i, line in enumerate(f):
        obj = json.loads(line)
        print(obj)
        if i > 100:
            break
    f.close()
