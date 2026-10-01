"""日本 JPX 每週信用交易餘額（東京＋名古屋，買殘＝融資）→ data/margin_jp.json

series: [基準日, 買殘金額(兆日圓)]
JPX 每週只放最新一份，所以歷史是一週一週累積起來的。
"""
import io
import re
from datetime import datetime

import openpyxl

from common import get, run

BASE = "https://www.jpx.co.jp"
PAGE = BASE + "/english/markets/statistics-equities/margin/04.html"


def latest():
    html = get(PAGE).decode("utf-8", "replace")
    href = re.search(r'href="([^"]+_mtcurrent\.xlsx)"', html).group(1)
    ws = openpyxl.load_workbook(io.BytesIO(get(BASE + href)), data_only=True).worksheets[0]
    rows = [[c for c in r if c is not None] for r in ws.iter_rows(values_only=True)]
    as_of = next(r[0] for r in rows if r and isinstance(r[0], datetime))
    total_idx = next(i for i, r in enumerate(rows) if r and "Total Outstanding Margin Trading" in str(r[0]))
    val_row = rows[total_idx + 1]  # 金額Val. 那一列：[標籤, 賣殘, 前週比, 買殘, 前週比, ...]
    purchases = float(val_row[3])  # 百萬日圓
    return [as_of.date().isoformat(), round(purchases / 1e6, 3)]


def update(old):
    rows = {r[0]: r for r in old.get("series", [])}
    r = latest()
    rows[r[0]] = r
    return {"source": "jpx", "unit": "兆日圓", "series": sorted(rows.values())[-260:]}


if __name__ == "__main__":
    run("margin_jp.json", update)
