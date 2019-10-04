import gzip
import json

VALUE_UNKNOWN = 'UNKNOWN'


def get_value_of_language(value_dict, language='en'):
    lan_val = value_dict.get(language, None)
    if type(lan_val) == list:
        all_vals = list()
        for lv in lan_val:
            v = lv.get('value')
            if v is not None:
                all_vals.append(v)
        return all_vals
    else:
        return None if lan_val is None else lan_val.get('value', None)


def get_labels(entry, languages):
    entry_label = entry.get('labels')
    if entry_label is None:
        return None

    target_labels = dict()
    for lan in languages:
        val = get_value_of_language(entry_label, lan)
        if val is not None:
            target_labels[lan] = val
    return target_labels if target_labels else None


def get_aliases(entry, languages):
    aliases = entry.get('aliases')
    if aliases is None:
        return None
    target_aliases = dict()
    for lan in languages:
        val = get_value_of_language(aliases, lan)
        if val is not None:
            target_aliases[lan] = val
    return target_aliases if target_aliases else None


def get_en_description(entry):
    desc = entry.get('descriptions')
    if desc is None:
        return None
    desc = get_value_of_language(desc, 'en')
    return desc


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
    languages = ['en', 'zh', 'zh-hans', 'zh-hant', 'zh-cn', 'zh-tw', 'zh-hk']
    next(f)
    for i, line in enumerate(f):
        line = line.strip()
        if line[-1] == ',':
            entry = json.loads(line[:-1])
        elif line[-1] == ']':
            continue
        else:
            entry = json.loads(line)

        entry_labels = get_labels(entry, languages)
        aliases = get_aliases(entry, languages)
        desc = get_en_description(entry)

        insof_vals = __get_item_id_val_from_claims(entry, 'P31')
        occupation_vals = __get_item_id_val_from_claims(entry, 'P106')
        sublassof_vals = __get_item_id_val_from_claims(entry, 'P279')
        wiki_title = __get_enwiki_title(entry)

        # if occupation_vals:
        #     print(entry)

        claims = entry.get('claims')
        properties = None if claims is None else list(claims.keys())

        cleaned_entry = {'id': entry['id'], 'type': entry['type']}
        if entry_labels is not None:
            cleaned_entry['label'] = entry_labels
        if aliases is not None:
            cleaned_entry['aliases'] = aliases
        if desc is not None:
            cleaned_entry['desc'] = desc

        if insof_vals is not None and len(insof_vals) > 0:
            cleaned_entry['insof'] = insof_vals
        if occupation_vals is not None and len(occupation_vals) > 0:
            cleaned_entry['occupation'] = occupation_vals
        if wiki_title is not None:
            cleaned_entry['wiki'] = wiki_title
        if properties is not None:
            cleaned_entry['property'] = properties
        if sublassof_vals is not None:
            cleaned_entry['subclassof'] = sublassof_vals
        fout.write('{}\n'.format(json.dumps(cleaned_entry)))
        # if i > 1000:
        #     break
        if i % 100000 == 0:
            print(i)
    f.close()
    fout.close()


def check_item(filename, qid):
    f = gzip.open(filename, 'rt', encoding='utf-8')
    next(f)
    for i, line in enumerate(f):
        line = line.strip()
        # print(line)
        if line[-1] == ',':
            entry = json.loads(line[:-1])
        elif line[-1] == ']':
            continue
        else:
            entry = json.loads(line)

        cur_qid = entry['id']
        if cur_qid == qid:
            print(entry)
            print(entry['aliases'])
            break
        # if i > 10:
        #     break
        if i % 1000000 == 0:
            print(i)
    f.close()
