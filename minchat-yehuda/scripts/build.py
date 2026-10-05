"""בניית book.json ואתר בקובץ יחיד מתוך קבצי ההגהה build/clean/*.md -> text/*.md"""
import glob, json, re, os
src = sorted(glob.glob('text/*.md'))
lines = '\n'.join(open(f, encoding='utf-8').read().strip() for f in src).split('\n')
sections, sec, ch, buf = [], None, None, []
def flush():
    global buf
    if buf and ch is not None:
        ch['paras'].append(' '.join(buf).strip())
    buf = []
n = 0
for raw in lines:
    l = raw.strip()
    if l.startswith('# '):
        flush(); title = l[2:].strip()
        if sec and sec['title'] == title: continue  # המשך אותה פרשה מקטע קודם
        sec = {'title': title, 'chapters': []}; sections.append(sec); ch = None
    elif l.startswith('## '):
        flush(); n += 1
        if sec is None: sec = {'title': 'פרשת בראשית', 'chapters': []}; sections.append(sec)
        ch = {'id': f's{n}', 'n': n, 'title': l[3:].strip(), 'paras': []}; sec['chapters'].append(ch)
    elif not l:
        flush()
    else:
        if ch is None:
            if sec is None: sec = {'title': 'פתיחה', 'chapters': []}; sections.append(sec)
            ch = {'id': f'p{len(sections)}', 'n': 0, 'title': sec['title'], 'paras': []}; sec['chapters'].append(ch)
        buf.append(l)
flush()
for s in sections: s['chapters'] = [c for c in s['chapters'] if c['paras'] or c['n']]
sections = [s for s in sections if s['chapters']]
# הסימנים על הנביאים מקובצים תחת "נביאים", ושם הספר והפרק נכנס לכותרת הסימן
grouped, neviim = [], None
for s in sections:
    t = s['title']
    if t.startswith(('פרשת', 'שער', 'הקדמ')):
        grouped.append(s); continue
    t = t.replace('נביאים.', '').strip()
    if neviim is None:
        neviim = {'title': 'נביאים', 'chapters': []}; grouped.append(neviim)
    for c in s['chapters']:
        c['ref'] = t
    neviim['chapters'] += s['chapters']
sections = grouped
book = {'title': 'מנחת יהודה', 'author': 'ר׳ יהודה משה פתיה', 'sections': sections}
os.makedirs('dist', exist_ok=True)
json.dump(book, open('book.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
tpl = open('site/template.html', encoding='utf-8').read()
data = json.dumps(book, ensure_ascii=False).replace('</', '<\\/')
page = tpl.replace('__BOOK_JSON__', data)
open('dist/artifact.html', 'w', encoding='utf-8').write(page)
# האתר עצמו (עם doctype) – מוגש ב-GitHub Pages
open('index.html', 'w', encoding='utf-8').write('<!doctype html>\n<html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' + page.replace('<header', '</head><body>\n<header', 1) + '\n</body></html>')
print(len(sections), 'sections', n, 'simanim', sum(len(c['paras']) for s in sections for c in s['chapters']), 'paragraphs')
