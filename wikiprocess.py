import bz2
import gzip
import time
from bisect import bisect_left
import os
import pandas as pd
import re
import wikiutils
import utils


page_pattern = r'  <page>\s*<title>(.*?)</title>.*?<id>(.*?)</id>.*'
redirect_page_pattern = r'  <page>\s*<title>(.*?)</title>.*?<id>(.*?)</id>.*?<redirect title="(.*?)"\s*/>.*'


def gen_redirects_file(wiki_file, output_file):
    f = bz2.open(wiki_file, 'rt', encoding='utf-8')
    page_cnt = 0
    redirect_title_tups = list()
    while True:
        page_xml = wikiutils.next_xml_page(f)
        if not page_xml:
            break
        page_cnt += 1
        if page_cnt % 100000 == 0:
            print(page_cnt, len(redirect_title_tups), 'pairs found')
        # if page_cnt > 10:
        #     break

        # print(page_xml)
        m = re.match(redirect_page_pattern, page_xml, re.DOTALL)
        if not m:
            continue

        title = m.group(1)
        redirect_title = m.group(3)
        redirect_title_tups.append((title, redirect_title))
    f.close()

    with open(output_file, 'w', encoding='utf-8', newline='\n') as fout:
        pd.DataFrame(redirect_title_tups, columns=['title_from', 'title_to']).to_csv(fout, index=False)


def gen_title_wid_file(wiki_file, output_file):
    f = bz2.open(wiki_file, 'rt', encoding='utf-8')
    page_cnt = 0
    title_wid_tups = list()
    while True:
        page_xml = wikiutils.next_xml_page(f)
        if not page_xml:
            break
        page_cnt += 1
        if page_cnt % 100000 == 0:
            print(page_cnt, len(title_wid_tups), 'pairs found')
        if page_cnt > 10000:
            break

        # print(page_xml)
        m = re.match(page_pattern, page_xml, re.DOTALL)
        if not m:
            continue

        title = m.group(1)
        wid = int(m.group(2))
        title_wid_tups.append((title, wid))
    f.close()

    with open(output_file, 'w', encoding='utf-8', newline='\n') as fout:
        pd.DataFrame(title_wid_tups, columns=['title', 'wid']).to_csv(fout, index=False)


def __get_linked_cnts_dict(mstr_target_cnts_dict):
    linked_cnts_dict = dict()
    for mstr, (target_titles, cnts) in mstr_target_cnts_dict.items():
        for title, cnt in zip(target_titles, cnts):
            cur_cnt = linked_cnts_dict.get(title, 0)
            linked_cnts_dict[title] = cur_cnt + cnt
    return linked_cnts_dict


def gen_mention_str_to_target_cnt_file(wiki_text_file, redirects_file, output_mstr_target_cnt_file,
                                       output_entity_linked_cnts_file):
    print('loading {} ... '.format(redirects_file), end='', flush=True)
    redirects_dict = wikiutils.load_redirects_file(redirects_file)
    print('done')

    mention_str_targets_dict = dict()
    # f = open(wiki_text_file, encoding='utf-8')
    f = gzip.open(wiki_text_file, 'rt', encoding='utf-8')
    cnt = 0
    while True:
        text_info = wikiutils.next_text_page(f)
        if text_info is None:
            break

        anchors = wikiutils.find_anchors(text_info.text)
        # print(text_info.wid, text_info.title)
        for mention_str, target in anchors:
            mention_str = mention_str.strip()
            target = target.strip()
            if not mention_str or not target or target.startswith('http://') or target.startswith('https://'):
                continue
            if utils.has_sep_space(mention_str) or utils.has_sep_space(target):
                continue

            if target[0].islower():
                target = target[0].upper() if len(target) == 1 else target[0].upper() + target[1:]

            target_title = redirects_dict.get(target, target)
            if not wikiutils.is_not_util_page_title(target_title):
                continue

            # print(mention_str, target_title)
            cur_target_cnts_tup = mention_str_targets_dict.get(mention_str, None)
            if cur_target_cnts_tup is None:
                mention_str_targets_dict[mention_str] = ([target_title], [1])
            else:
                target_titles, cnts = cur_target_cnts_tup
                pos = bisect_left(target_titles, target_title)
                if pos < len(target_titles) and target_titles[pos] == target_title:
                    cnts[pos] += 1
                else:
                    target_titles.insert(pos, target_title)
                    cnts.insert(pos, 1)

        cnt += 1
        if cnt % 10000 == 0:
            print(cnt)
        # if cnt > 10000:
        #     break
    f.close()

    entity_linked_cnts_dict = __get_linked_cnts_dict(mention_str_targets_dict)
    entity_linked_cnt_tups = list(entity_linked_cnts_dict.items())
    entity_linked_cnt_tups.sort(key=lambda x: x[0])
    print('writing {} ...'.format(output_entity_linked_cnts_file), end=' ', flush=True)
    with open(output_entity_linked_cnts_file, 'w', encoding='utf-8', newline='\n') as fout:
        pd.DataFrame(entity_linked_cnt_tups, columns=['title', 'cnt']).to_csv(
            fout, index=False, line_terminator='\n')
    print('done')

    mention_str_targets_tups = list(mention_str_targets_dict.items())
    mention_str_targets_tups.sort(key=lambda x: x[0])
    fout = open(output_mstr_target_cnt_file, 'w', encoding='utf-8', newline='\n')
    print('writing {} ... '.format(output_mstr_target_cnt_file), end='', flush=True)
    for mention_str, target_cnts_tup in mention_str_targets_tups:
        target_cnt_tups = list(zip(*target_cnts_tup))
        target_cnt_tups.sort(key=lambda x: -x[1])
        for target_title, cnt in target_cnt_tups:
            fout.write('{}\t{}\t{}\n'.format(mention_str, target_title, cnt))
    fout.close()
    print('done')


# TODO more disambiguation cases
def gen_entity_only_title_wid_file(xml_wiki_file, redirects_file, output_file):
    redirects_dict = wikiutils.load_redirects_file(redirects_file)

    title_wid_tups = list()
    cnt = 0
    p_normal = re.compile(page_pattern, re.DOTALL)
    p_disamb = re.compile(r'({{[D|d]isambig|{{surname|"preserve">.*\n?.*may refer to)')
    # p_redirect = re.compile(redirect_page_pattern, re.DOTALL)
    time_start = time.time()
    f = bz2.open(xml_wiki_file, 'rt', encoding='utf-8')
    while True:
        page_xml = wikiutils.next_xml_page(f)
        if not page_xml:
            break

        cnt += 1
        # if cnt > 200000:
        #     break
        if cnt % 100000 == 0:
            print(cnt, len(title_wid_tups), time.time() - time_start)

        m = p_normal.match(page_xml)
        if not m:
            print('not matched')
            print(page_xml)
            continue

        # if m.group(1) == 'Osborne':
        #     print(page_xml)
        #     exit()
        # else:
        #     continue

        m_disamb = p_disamb.search(page_xml)
        if m_disamb:
            # print(m.group(1), m_disamb.group(1))
            continue

        title = m.group(1)

        if not wikiutils.is_not_util_page_title(title):
            continue
        # m_redirect = p_redirect.match(page_xml)
        # if m_redirect:
        #     continue
        if title in redirects_dict:
            continue
        if wikiutils.is_special_intro_title(title):
            continue

        wid = int(m.group(2))
        title_wid_tups.append((title, wid))
    f.close()

    with open(output_file, 'w', encoding='utf-8', newline='\n') as fout:
        pd.DataFrame(title_wid_tups, columns=['title', 'wid']).to_csv(fout, index=False, line_terminator='\n')


# entity only entries mentioned at least once
def gen_core_title_wid_file(title_wid_file, linked_cnts_file, output_file):
    with open(title_wid_file, encoding='utf-8') as f:
        df_title_wid = pd.read_csv(f, na_filter=False)
    linked_cnts_dict = wikiutils.load_linked_cnts_file(linked_cnts_file)
    core_title_wid_tups = list()
    for title, wid in df_title_wid.itertuples(False, None):
        linked_cnt = linked_cnts_dict.get(title, 0)
        if linked_cnt > 0:
            core_title_wid_tups.append((title, wid))

    with open(output_file, 'w', encoding='utf-8', newline='\n') as fout:
        pd.DataFrame(core_title_wid_tups, columns=['title', 'wid']).to_csv(fout, index=False, line_terminator='\n')
