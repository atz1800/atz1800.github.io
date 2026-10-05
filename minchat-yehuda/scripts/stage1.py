"""שלב 1: היפוך אותיות המילים ותיקון סדר מילים הפוך משכבת הטקסט הקיימת ב-PDF."""
import re, math, collections, json
HEB = re.compile(r'[֐-׿]')
raw = open('source/raw-text-layer.txt', encoding='utf-8').read().split('\n')
SEG = re.compile(r'(?<=[.:])\s+')

def flip_words(s):
    return [w[::-1] if HEB.search(w) else w for w in s.split()]

paras = [[flip_words(s) for s in SEG.split(l)] for l in raw]
big = collections.Counter()
def pairs(ws): return list(zip(ws, ws[1:]))
for p in paras:
    for ws in p: big.update(pairs(ws))

def score(ws):
    own = collections.Counter(pairs(ws))
    s = 0.0
    for a, b in own:
        f = big[(a, b)] - own[(a, b)]; r = big[(b, a)] - own.get((b, a), 0)
        s += own[(a, b)] * math.log((f + .2) / (r + .2))
    return s

out, flipped = [], 0
for p in paras:
    segs = []
    for ws in p:
        if score(ws) < -0.7:
            ws = ws[::-1]; flipped += 1
        segs.append(' '.join(ws))
    out.append(' '.join(segs))
open('build/stage1.txt', 'w', encoding='utf-8').write('\n'.join(out))
print(flipped, 'segments reversed')
