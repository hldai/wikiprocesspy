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
