import gzip
import json

VALUE_UNKNOWN = 'UNKNOWN'


def get_en_value(value_dict):
    val = value_dict.get('en', None)
    return None if val is None else val.get('value', None)


def get_en_label(entry):
    entry_label = entry.get('labels')
    if entry_label is not None:
        entry_label = get_en_value(entry_label)
    return VALUE_UNKNOWN if entry_label is None else entry_label


def get_en_description(entry):
    desc = entry.get('descriptions')
    if desc is not None:
        desc = get_en_value(desc)
    return VALUE_UNKNOWN if desc is None else desc


def __get_item_id_val_from_claims(entry, property_id):
    claims = entry.get('claims')
    if claims is None:
        return None
    vals = claims.get(property_id)
    if vals is None:
        return None
    extracted_vals = list()
    for insof_val in vals:
        mainsnak = insof_val.get('mainsnak')
        if mainsnak is None:
            continue
        datavalue = mainsnak.get('datavalue')
        if datavalue is None:
            continue
        # if datavalue['type'] != 'wikibase-entityid' or datavalue['value']['entity-type'] != 'item' or (
        #         'numeric-id' not in datavalue['value']):
        #     print(datavalue)
        extracted_vals.append('Q{}'.format(datavalue['value']['numeric-id']))
    return extracted_vals


def __get_enwiki_title(entry):
    sitelinks = entry.get('sitelinks')
    if sitelinks is None:
        return None
    enwiki = sitelinks.get('enwiki')
    if enwiki is None:
        return None
    return enwiki.get('title')


def filter_wikidata(full_data_file, output_file):
    f = gzip.open(full_data_file, 'rt', encoding='utf-8')
    fout = open(output_file, 'w', encoding='utf-8')
    next(f)
    for i, line in enumerate(f):
        line = line.strip()
        if line[-1] == ',':
            entry = json.loads(line[:-1])
        elif line[-1] == ']':
            continue
        else:
            entry = json.loads(line)

        entry_label = get_en_label(entry)
        desc = get_en_description(entry)

        insof_vals = __get_item_id_val_from_claims(entry, 'P31')
        occupation_vals = __get_item_id_val_from_claims(entry, 'P106')
        wiki_title = __get_enwiki_title(entry)

        claims = entry.get('claims')
        properties = None if claims is None else list(claims.keys())

        cleaned_entry = {'id': entry['id'], 'type': entry['type'], 'label': entry_label, 'desc': desc}
        if insof_vals is not None and len(insof_vals) > 0:
            cleaned_entry['insof'] = insof_vals
        if occupation_vals is not None and len(occupation_vals) > 0:
            cleaned_entry['occupation'] = occupation_vals
        if wiki_title is not None:
            cleaned_entry['wiki'] = wiki_title
        if properties is not None:
            cleaned_entry['property'] = properties
        fout.write('{}\n'.format(json.dumps(cleaned_entry)))
        # if i > 100:
        #     break
        if i % 100000 == 0:
            print(i)
    f.close()
    fout.close()
