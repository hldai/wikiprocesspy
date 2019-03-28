import os
import wikiprocess


res_dir = 'd:/data/res'
# wiki_file = os.path.join(res_dir, 'wiki/enwiki-20190101-pages-articles-multistream.xml.bz2')
# redirects_file = os.path.join(res_dir, 'wiki/enwiki-20190101-redirects.txt')
# title_wid_file = os.path.join(res_dir, 'wiki/enwiki-20190101-title-wid.txt')
wiki_file = os.path.join(res_dir, 'wiki/enwiki-20151002-pages-articles.xml.bz2')
wiki_text_file = os.path.join(res_dir, 'wiki/enwiki-20151002-pages-articles-text.txt.gz')
redirects_file = os.path.join(res_dir, 'wiki/enwiki-20151002-redirects.txt')
title_wid_file = os.path.join(res_dir, 'wiki/enwiki-20151002-title-wid.txt')
mention_str_target_cnt_file = os.path.join(res_dir, 'wiki/enwiki-20151002-mentionstr-target-cnt.txt')
entity_linked_cnt_file = os.path.join(res_dir, 'wiki/enwiki-20151002-entity-linked-cnts.txt')
# wikiprocess.gen_redirects_file(wiki_file, redirects_file)
# wikiprocess.gen_title_wid_file(wiki_file, title_wid_file)
wikiprocess.gen_mention_str_to_target_cnt_file(
    wiki_text_file, redirects_file, mention_str_target_cnt_file, entity_linked_cnt_file)
