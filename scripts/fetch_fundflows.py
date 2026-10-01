"""ICI 每週基金＋ETF 資金流（百萬美元）→ data/fundflows.json

series: [週別日期, 全部長期基金, 股票型, 美股, 海外股, 債券型]
"""
from datetime import date, datetime

import xlrd

from common import get, run

URL = "https://www.ici.org/combined_flows_data_{}.xls"


def parse(year):
    sh = xlrd.open_workbook(file_contents=get(URL.format(year))).sheet_by_index(0)
    out, weekly = [], False
    for r in range(sh.nrows):
        row = [c for c in sh.row_values(r) if c != ""]
        if not row:
            continue
        head = str(row[0]).strip()
        if not head[:1].isdigit():  # 區段標題，例如 "Monthly fund flows" / "Weekly ..."
            if "monthly" in head.lower() or "weekly" in head.lower():
                weekly = "weekly" in head.lower()
            continue
        if not weekly:
            continue
        try:
            d = datetime.strptime(head, "%m/%d/%Y").date()
        except ValueError:
            continue
        total, eq, dom, world, _hybrid, bond = row[1:7]
        out.append([d.isoformat(), total, eq, dom, world, bond])
    return out


def update(old):
    rows = {r[0]: r for r in old.get("series", [])}
    y = date.today().year
    for year in ([y - 1, y] if not rows else [y]):
        for r in parse(year):
            rows[r[0]] = r
    if not rows:
        raise RuntimeError("沒有週資料")
    return {"source": "ici", "unit": "百萬美元", "series": sorted(rows.values())[-104:]}


if __name__ == "__main__":
    run("fundflows.json", update)
