"""抓 CNN Fear & Greed，寫進 data/fng.json。

抓不到時保留上次的數字，只把 status 改成 stale 並記下錯誤，
讓網頁顯示「尚未更新」而不是整張卡壞掉。
"""
import json
import math
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

URL = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
OUT = Path(__file__).resolve().parent.parent / "data" / "fng.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://edition.cnn.com/",
    "Origin": "https://edition.cnn.com",
}
HISTORY_DAYS = 370


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fetch():
    req = urllib.request.Request(URL, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def parse(raw):
    # CNN 網頁顯示的是捨去小數，不是四捨五入
    fg = raw["fear_and_greed"]
    ts = datetime.fromisoformat(fg["timestamp"].replace("Z", "+00:00")).astimezone(timezone.utc)
    cutoff = ts.timestamp() * 1000 - HISTORY_DAYS * 86400 * 1000
    history = [
        [int(p["x"]), round(p["y"], 1)]
        for p in raw.get("fear_and_greed_historical", {}).get("data", [])
        if p["x"] >= cutoff
    ]
    return {
        "source": "cnn",
        "status": "ok",
        "data_time": ts.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "fetched_at": now_iso(),
        "last_attempt": now_iso(),
        "last_error": None,
        "score": math.floor(fg["score"]),
        "rating": fg["rating"],
        "previous_close": math.floor(fg["previous_close"]),
        "previous_1_week": math.floor(fg["previous_1_week"]),
        "previous_1_month": math.floor(fg["previous_1_month"]),
        "previous_1_year": math.floor(fg["previous_1_year"]),
        "history": history,
    }


def main():
    try:
        data = parse(fetch())
    except Exception as e:  # 任何失敗都保留舊資料
        data = json.loads(OUT.read_text(encoding="utf-8"))
        if data.get("source") == "cnn":
            data["status"] = "stale"
        data["last_attempt"] = now_iso()
        data["last_error"] = f"{type(e).__name__}: {e}"[:300]
        print(f"抓取失敗，保留上次資料：{data['last_error']}", file=sys.stderr)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"score={data['score']} status={data['status']} data_time={data['data_time']}")


if __name__ == "__main__":
    main()
