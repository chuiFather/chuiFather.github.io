"""data/ → 앱별 Firebase Remote Config 값 (PC 세션이 콘솔에 붙여 넣음) — chui-series SERIES.md §6·§7·§12·§13

python3 tools/firebase_values.py            # 출시된 앱 전부
python3 tools/firebase_values.py station    # 한 앱

  collab_partners  출시됐고 콜라보를 연 앱 id (모든 앱에 같은 값)
  notices          그 앱 공지만 (app = 그 앱 id). id는 앱마다 규칙이 달라서(정거장 1000~, 디펜스 1~) data/notices.json에 그 규칙대로 적는다.
                   시리즈 공지(app = "series")는 사이트에만 (앱에 넣으면 앱별 id 규칙과 섞임)
  coupons          그 앱 쿠폰 중 앱 core에 들어 있지 않은 것 ("builtin": true가 아닌 것). end 없으면 영구
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(name):
    with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f:
        return json.load(f)


def main():
    apps = load("apps.json")
    want = sys.argv[1:] or [a["id"] for a in apps if a["status"] == "released"]
    partners = ",".join(a["id"] for a in apps if a["status"] == "released" and a.get("collab_live"))
    for app_id in want:
        notices = [{k: n[k] for k in ("id", "date", "title", "body", "title_en", "body_en") if k in n}
                   for n in load("notices.json") if n.get("app") == app_id]
        coupons = [{k: c[k] for k in ("code", "reward", "amount", "start", "end") if k in c}
                   for c in load("coupons.json") if c["app"] == app_id and not c.get("builtin")]
        print(f"== {app_id}")
        print("collab_partners =", partners)
        print("notices =", json.dumps(notices, ensure_ascii=False))
        print("coupons =", json.dumps(coupons, ensure_ascii=False))


if __name__ == "__main__":
    main()
