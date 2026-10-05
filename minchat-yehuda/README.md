# מנחת יהודה

הספר **מנחת יהודה** על התורה, לרבי יהודה משה פתיה (בגדאד): טקסט נקי ואתר ללימוד.

האתר: https://atz1800.github.io/minchat-yehuda/

| | |
|---|---|
| `source/raw-text-layer.txt` | שכבת הטקסט המקורית מה-PDF (HebrewBooks 33796): האותיות הפוכות ויש בה שגיאות OCR |
| `scripts/stage1.py` | הופך את המילים ומתקן שורות שסדר המילים בהן הפוך → `build/stage1.txt` |
| `scripts/PROOFREAD.md` | הוראות ההגהה (תיקון שגיאות OCR, כותרות, פסקאות) |
| `text/*.md` | **הטקסט הנקי**: `#` לפרשה, `##` לסימן |
| `scripts/build.py` | בונה את `book.json` ואת האתר `index.html` (קובץ יחיד) |

את הסקריפטים מריצים מתוך התיקייה `minchat-yehuda/`.

בנייה:

```
python3 scripts/stage1.py   # רק כשרוצים לייצר מחדש מהמקור
python3 scripts/build.py
```

בטקסט, `[?]` מסמן קריאה משוערת ו-`[...]` מסמן קטע שאינו קריא במקור.
