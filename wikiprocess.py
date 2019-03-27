import bz2
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


res_dir = 'd:/data/res'
# wiki_file = os.path.join(res_dir, 'wiki/enwiki-20190101-pages-articles-multistream.xml.bz2')
# redirects_file = os.path.join(res_dir, 'wiki/enwiki-20190101-redirects.txt')
# title_wid_file = os.path.join(res_dir, 'wiki/enwiki-20190101-title-wid.txt')
wiki_file = os.path.join(res_dir, 'wiki/enwiki-20151002-pages-articles.xml.bz2')
redirects_file = os.path.join(res_dir, 'wiki/enwiki-20151002-redirects.txt')
title_wid_file = os.path.join(res_dir, 'wiki/enwiki-20151002-title-wid.txt')
# gen_redirects_file(wiki_file, redirects_file)
gen_title_wid_file(wiki_file, title_wid_file)
