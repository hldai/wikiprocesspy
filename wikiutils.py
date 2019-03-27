import re
from collections import namedtuple


text_doc_head_pattern_str = "<doc id=\"(.*?)\" url=\"(.*?)\" title=\"(.*?)\""
anchor_pattern_str = "<a href=\"(.*?)\">(.*?)</a>"

WikiTextInfo = namedtuple('WikiTextInfo', ['title', 'wid', 'text'])


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
        mention_str = m.group(0)
        target = m.group(1)
        anchors.append((mention_str, target))
    return anchors
