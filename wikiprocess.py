import bz2
import gzip
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


def gen_mention_str_to_target_cnt_file(wiki_text_file, redirects_file, output_file):
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

            target_title = redirects_dict.get(target, target)
            if not wikiutils.is_not_util_page(target_title):
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

    mention_str_targets_tups = list(mention_str_targets_dict.items())
    mention_str_targets_tups.sort(key=lambda x: x[0])
    fout = open(output_file, 'w', encoding='utf-8', newline='\n')
    print('writing {} ... '.format(output_file), end='', flush=True)
    for mention_str, target_cnts_tup in mention_str_targets_tups:
        target_cnt_tups = list(zip(*target_cnts_tup))
        target_cnt_tups.sort(key=lambda x: -x[1])
        for target_title, cnt in target_cnt_tups:
            fout.write('{}\t{}\t{}\n'.format(mention_str, target_title, cnt))
    fout.close()
    print('done')
