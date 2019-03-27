import bz2
import gzip
import os
import pandas as pd
import re
import wikiutils


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


def gen_mention_str_to_target_cnt_file(wiki_text_file, output_file):
    # f = open(wiki_text_file, encoding='utf-8')
    f = gzip.open(wiki_text_file, 'rt', encoding='utf-8')
    cnt = 0
    while True:
        text_info = wikiutils.next_text_page(f)
        print(text_info.wid, text_info.title)
        if text_info is None:
            break

        cnt += 1
        if cnt > 10:
            break
    f.close()
