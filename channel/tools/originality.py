#!/usr/bin/env python3
"""Originality gate (YouTube "inauthentic content" policy): compare a new script with every earlier script.

    python3 channel/tools/originality.py channel/stories/s04_script.py
Flags spoken lines that are near-copies (>= 0.8 similar) of lines in earlier scripts, and prints the share of
our titles that use the same shape as the new title. Fail (exit 1) if > 3 copied lines or the title shape is
already on >= 40% of our videos. A shared intro/outro line is allowed (listed in ALLOWED).
"""
import ast
import difflib
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED = {"i'm penny. these people are made up. every number is real."}


def lines_of(path):
    try:
        tree = ast.parse(open(path).read())
    except SyntaxError:
        return []
    out = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            s = re.sub(r'^[A-Z]\|!?|^!', '', n.value).strip()
            if len(s.split()) >= 6 and not s.startswith(('#', '/', 'http')) and '\n' not in s:
                out.append(s)
    for n in ast.walk(tree):  # f-strings: keep their literal parts
        if isinstance(n, ast.JoinedStr):
            s = ''.join(v.value for v in n.values if isinstance(v, ast.Constant))
            s = re.sub(r'^[A-Z]\|!?|^!', '', s).strip()
            if len(s.split()) >= 6:
                out.append(s)
    return out


def shape(title):
    t = re.sub(r'\$?\d[\d,]*(?:\.\d+)?%?', 'N', title)
    parts = [p for p in re.split(r'(?<=[.?!])\s+', t.strip()) if p]
    return ' | '.join(('Q' if p.endswith('?') else 'S') + str(min(len(p.split()), 6) // 3) for p in parts)


def title_of(path):
    m = re.search(r'^TITLE\s*=\s*["\'](.+?)["\']', open(path).read(), re.M)
    return m.group(1) if m else None


def main(new):
    new = os.path.abspath(new)
    olds = [p for p in glob.glob(os.path.join(HERE, 'ep*.py')) + glob.glob(os.path.join(HERE, 'sx*.py'))
            + glob.glob(os.path.join(HERE, 'stories', 's*_script.py')) if os.path.abspath(p) != new]
    corpus = [(os.path.basename(p), l) for p in olds for l in lines_of(p)]
    copied = []
    for l in lines_of(new):
        if l.lower() in ALLOWED:
            continue
        best = max(((difflib.SequenceMatcher(None, l.lower(), o.lower()).ratio(), f, o) for f, o in corpus
                    if abs(len(o) - len(l)) < 40), default=(0, '', ''))
        if best[0] >= .8:
            copied.append((best[0], l, best[1], best[2]))
    for r, l, f, o in copied:
        print(f'COPY {r:.2f}  "{l}"\n           ~ {f}: "{o}"')
    titles = []
    for p in glob.glob(os.path.join(HERE, 'out', '*.upload.json')):
        try:
            t = json.load(open(p)).get('title')
        except Exception:
            t = None
        if t:
            titles.append(t)
    t = title_of(new)
    share = 0
    if t and titles:
        share = sum(shape(x) == shape(t) for x in titles) / len(titles)
        print(f'title shape "{shape(t)}" on {share:.0%} of {len(titles)} titles  ({t})')
    ok = len(copied) <= 3 and share < .4
    print('ORIGINALITY', 'PASS' if ok else 'FAIL', f'({len(copied)} copied lines)')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
