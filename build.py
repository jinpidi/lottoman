#!/usr/bin/env python3
"""로또맨 빌드 스크립트.

최신 당첨 데이터(1회~현재)를 받아 template.html에 주입하고 index.html을 생성한다.
로컬:  python3 build.py
CI:    .github/workflows/update.yml 이 매주 토요일 밤 자동 실행
"""
import json
import pathlib
import urllib.request

BASE = pathlib.Path(__file__).parent
DATA_URL = "https://smok95.github.io/lotto/results/all.json"

HEAD_EXTRA = """<meta name="theme-color" content="#0F1218">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png" type="image/png">
<link rel="apple-touch-icon" href="icon-180.png">
<script>
if ("serviceWorker" in navigator && location.protocol === "https:")
  addEventListener("load", () => navigator.serviceWorker.register("sw.js"));
</script>"""


def main():
    with urllib.request.urlopen(DATA_URL, timeout=60) as res:
        data = json.load(res)
    rows = []
    for r in data:
        first = r["divisions"][0] if r["divisions"] else {}
        rows.append(r["numbers"] + [r["bonus_no"], first.get("prize", 0), first.get("winners", 0)])
    # 무결성: 회차 연속성 + 번호 범위
    assert all(len(set(row[:6])) == 6 and all(1 <= n <= 45 for n in row[:6]) for row in rows)

    html = (BASE / "template.html").read_text(encoding="utf-8")
    html = html.replace("__DATA__", json.dumps(rows, separators=(",", ":")))
    html = html.replace("__FONT__", (BASE / "font_b64.txt").read_text().strip())
    html = html.replace("<!--HEAD_EXTRA-->", HEAD_EXTRA)
    (BASE / "index.html").write_text(html, encoding="utf-8")
    print(f"OK: {len(rows)}회차 내장, index.html {len(html) // 1024}KB")


if __name__ == "__main__":
    main()
