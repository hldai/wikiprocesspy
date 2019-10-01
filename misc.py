import json


def __text_from_anchor_sents_file(anchor_sents_file, output_file):
    f = open(anchor_sents_file, encoding='utf-8')
    fout = open(output_file, 'w', encoding='utf-8', newline='\n')
    for i, line in enumerate(f):
        sent = json.loads(line)
        fout.write('{}\n'.format(sent['tokens']))
        # if i > 5:
        #     break
    f.close()
    fout.close()


wiki19_anchor_sents_file = 'd:/data/res/wiki/anchor/enwiki-20190101-anchor-sents.txt'
anchor_sent_texts_file = 'd:/data/res/wiki/anchor/enwiki-20190101-anchor-sents-tok-texts.txt'
__text_from_anchor_sents_file(wiki19_anchor_sents_file, anchor_sent_texts_file)
