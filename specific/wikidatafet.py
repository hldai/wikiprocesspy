import json
from utils import datautils


def __get_value_by_lan_cleaned(item, value_name, language):
    val = item.get(value_name, None)
    if val is None:
        return None
    return val.get(language)


def gen_type_cnts_file(type_items_file, output_file):
    type_cnts = list()
    with open(type_items_file, encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            label = __get_value_by_lan_cleaned(item, 'label', 'en')
            if not label or ';' in label:
                continue
            type_name_str = label
            aliases = __get_value_by_lan_cleaned(item, 'aliases', 'en')
            if aliases:
                aliases = [v for v in aliases if ';' not in v]
                type_name_str = ';'.join([label] + aliases)
                # print(type_name_str)
            cnt = item.get('use_cnt', 0)
            type_cnts.append((type_name_str, cnt))
    type_cnts.sort(key=lambda x: -x[1])
    datautils.save_csv(type_cnts, ['type', 'cnt'], output_file)


def gen_type_items_file(cleaned_fet_wikidata_file, insof_output_file, subcls_output_file, occupation_output_file):
    def _count_vals(cur_item, val_name, target_dict):
        vals = cur_item.get(val_name, None)
        if vals is not None:
            for val in vals:
                cnt = target_dict.get(val, 0)
                target_dict[val] = cnt + 1

    subcls_type_cnts_dict, ins_type_cnts_dict, occupation_cnts_dict = dict(), dict(), dict()
    f = open(cleaned_fet_wikidata_file, encoding='utf-8')
    for i, line in enumerate(f):
        item = json.loads(line)

        _count_vals(item, 'insof', ins_type_cnts_dict)
        _count_vals(item, 'subclassof', subcls_type_cnts_dict)
        _count_vals(item, 'occupation', occupation_cnts_dict)

        # if i > 1000000:
        #     break
        if i % 1000000 == 0:
            print(i)
    f.close()

    def _check_item_and_write(cur_item, cnts_dict, fout):
        cnt = cnts_dict.get(cur_item['id'], 0)
        if cnt > 0:
            cur_item['use_cnt'] = cnt
            fout.write('{}\n'.format(json.dumps(cur_item)))

    f = open(cleaned_fet_wikidata_file, encoding='utf-8')
    fout_insof = open(insof_output_file, 'w', encoding='utf-8', newline='\n')
    fout_subcls = open(subcls_output_file, 'w', encoding='utf-8', newline='\n')
    fout_occupation = open(occupation_output_file, 'w', encoding='utf-8', newline='\n')
    for i, line in enumerate(f):
        item = json.loads(line)
        _check_item_and_write(item, ins_type_cnts_dict, fout_insof)
        _check_item_and_write(item, subcls_type_cnts_dict, fout_subcls)
        _check_item_and_write(item, occupation_cnts_dict, fout_occupation)
        # if i > 1000000:
        #     break
        if i % 1000000 == 0:
            print(i)
    f.close()
    fout_insof.close()
    fout_subcls.close()
    fout_occupation.close()
