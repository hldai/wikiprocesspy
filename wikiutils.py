import re
import pandas as pd
import urllib.parse
from collections import namedtuple


text_doc_head_pattern_str = "<doc id=\"(.*?)\" url=\"(.*?)\" title=\"(.*?)\""
anchor_pattern_str = "<a href=\"(.*?)\">(.*?)</a>"

WikiTextInfo = namedtuple('WikiTextInfo', ['title', 'wid', 'text'])

no_comma_util_title_starts = ['List of', 'Lists of']
comma_util_title_starts = ['Wikipedia:', 'File:', 'Draft:', 'Template:', 'MediaWiki:', 'Category:',
                           'Help:', 'wikt:', 'Portal:']
# code judges based on 'of' and 'in'
special_intro_title_starts = ['Geography of', 'Monarchy of', 'History of', 'Politics of', 'Economy of',
                              'Transport in', 'Foreign relations of', 'Foreign Relations of',
                              'Demographics of', 'Transportation in', 'Telecommunications in', 'Culture of']


def next_xml_page(f):
    page_xml = ''
    for line in f:
        if line == '  <page>\n':
            page_xml += line
            break

    if not page_xml:
        return None

    for line in f:
        page_xml += line
        if line == '  </page>\n':
            break
    return page_xml


def next_text_page(f):
    wid, title = None, None
    for line in f:
        if line.startswith('<doc id="'):
            m = re.match(text_doc_head_pattern_str, line)
            if m:
                title = m.group(3)
                wid = int(m.group(1))
                break
            else:
                print('fine "<doc id=" but not matched')
                print(line.strip())
    if wid is None:
        return None

    text = ''
    for i, line in enumerate(f):
        if line.strip() == '</doc>':
            break

        if i == 0 and line.strip() == title:
            continue
        text += line
    return WikiTextInfo(title, wid, text.strip())


def find_anchors(text_with_anchors):
    miter = re.finditer(anchor_pattern_str, text_with_anchors)
    anchors = list()
    for m in miter:
        target = urllib.parse.unquote(m.group(1))
        mention_str = m.group(2)
        anchors.append((mention_str, target))
    return anchors


def load_redirects_file(filename):
    with open(filename, encoding='utf-8') as f:
        df = pd.read_csv(f, na_filter=False)

    redirects_dict = {title_from: title_to for title_from, title_to in df.itertuples(False, None)}
    return redirects_dict


def is_not_util_page_title(page_title: str):
    if ':' in page_title:
        for s in comma_util_title_starts:
            if page_title.startswith(s):
                return False

    for s in no_comma_util_title_starts:
        if page_title.startswith(s):
            return False
    return True


def __starts_with_year(title: str):
    if len(title) < 4:
        return False
    for i in range(4):
        if not title[i].isdigit():
            return False
    return True


def is_special_intro_title(page_title: str):
    if ' of' not in page_title and ' in' not in page_title:
        return False

    if len(page_title) > 7 and __starts_with_year(page_title) and page_title[4:7] == ' in':
        return True

    for s in special_intro_title_starts:
        if page_title.startswith(s):
            return True
    return False
