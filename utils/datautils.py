import json
import pandas as pd


def save_csv(data, columns, output_file):
    with open(output_file, 'w', encoding='utf-8', newline='\n') as fout:
        pd.DataFrame(data, columns=columns).to_csv(fout, index=False, line_terminator='\n')
