import json
import pandas as pd


def save_csv(data, columns, output_file):
    with open(output_file, 'w', encoding='utf-8', newline='\n') as fout:
        pd.DataFrame(data, columns=columns).to_csv(fout, index=False, line_terminator='\n')


def load_wiki_title_wid_file(filename, to_wid_title_dict=False):
    with open(filename, encoding='utf-8') as f:
        df = pd.read_csv(f, na_filter=False)
    if to_wid_title_dict:
        return {wid: title for title, wid in df.itertuples(False, None)}
    return {title: wid for title, wid in df.itertuples(False, None)}
