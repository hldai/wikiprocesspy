import re


def has_sep_space(s):
    return '\t' in s or '\r' in s or '\n' in s


def norm_mention_str(s: str):
    rs = ''
    for ch in s:
        if ch.isalnum() or ch == ' ':
            rs += ch
    return re.sub(r'\s+', ' ', rs)
