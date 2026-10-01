"""各抓取腳本共用的小工具。"""
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml,application/json;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Upgrade-Insecure-Requests": "1",
}


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def get(url, headers=None, timeout=40):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def load(name, default):
    p = DATA / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def save(name, data):
    (DATA / name).write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def run(name, update):
    """執行 update(舊資料) -> 新資料；失敗就保留舊資料、標成 stale。"""
    old = load(name, {"series": []})
    try:
        new = update(old)
        new.update(status="ok", fetched_at=now_iso(), last_attempt=now_iso(), last_error=None)
    except Exception as e:
        new = old
        if new.get("series"):
            new["status"] = "stale"
        else:
            new["status"] = "error"
        new["last_attempt"] = now_iso()
        new["last_error"] = f"{type(e).__name__}: {e}"[:300]
        print(f"[{name}] 抓取失敗，保留上次資料：{new['last_error']}")
    save(name, new)
    s = new.get("series") or [[None, None]]
    print(f"[{name}] status={new['status']} 最新={s[-1]}  共 {len(new.get('series', []))} 筆")
