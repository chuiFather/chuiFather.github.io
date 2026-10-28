"""츄이 시리즈 홈 (chuifather.github.io 루트) 생성 — chui-series SERIES.md §13

  data/apps.json     앱 목록 (show = 홈에 보일지, status = released/testing/dev, collab_live = 콜라보 코드 공개)
  data/notices.json  공지 [{"app","id","date","title","body","title_en","body_en"}]  app = "series" 또는 앱 id
  data/updates.json  게임별 업데이트 기록 [{"app","id","version","date","title","body","title_en","body_en"}] (SERIES.md §15)
                     앱 저장소 스크립트가 채운다 (우주정거장: tools/store/export_updates.py). 앱 안 업데이트 소식과 같은 글
  data/coupons.json  쿠폰 [{"app","code","reward","amount","start","end","label","label_en","builtin"}]
                     reward·amount = 앱 core 보상 key·수량 (Firebase용), label = 사이트에 보일 보상 글
                     builtin = true면 앱 core에 들어 있는 영구 쿠폰 (Firebase에 안 넣음, 사이트에만 보임)
                     end 없으면 영구. 기간은 한국 시간 기준, 페이지가 열릴 때 지난 쿠폰은 숨김

  → index.html (한국어), en/index.html (영어), updates/index.html·en/updates/index.html (업데이트 기록). 앱별 페이지(station/ survivors/ defense/ …)와 privacy/·odds/는 각 앱 저장소가 만든다.

python3 tools/make_home.py   (표준 라이브러리만)
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTACT = "polalis715@gmail.com"


def load(name):
    with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f:
        return json.load(f)


T = {
    "ko": {
        "title": "츄이 시리즈", "lead": "흰색·검은색 파티 포메라니안 <b>츄이</b>가 나오는 귀여운 도트 게임들",
        "news": "공지", "games": "게임", "coupons": "쿠폰", "collab": "콜라보 코드",
        "no_news": "아직 공지가 없어요.", "no_coupons": "지금 받을 수 있는 쿠폰이 없어요.",
        "no_collab": "콜라보 코드는 게임이 출시되면 여기에 올라와요.",
        "coupon_how": "게임 <b>설정 → 쿠폰 입력</b>에 넣으면 받을 수 있어요. 쿠폰 하나는 한 번만 받을 수 있어요.",
        "collab_how": "다른 츄이 게임의 <b>설정 → 쿠폰 입력</b>에 넣으면 그 게임에서 선물을 받아요.",
        "status": {"released": "출시", "testing": "출시 준비 중", "dev": "개발 중"},
        "play": "Google Play", "onestore": "원스토어", "more": "자세히",
        "forever": "기간 없음", "until": "까지", "copy": "복사", "copied": "복사됨",
        "privacy": "개인정보처리방침", "contact": "문의", "other": "English", "other_href": "en/",
        "series_tag": "츄이 시리즈", "dev": "개발자 chuiFather · 흑백너구리",
        "updates": "업데이트 기록", "no_updates": "아직 업데이트 기록이 없어요.", "home": "츄이 시리즈 홈",
    },
    "en": {
        "title": "Chui Series", "lead": "Cute pixel games starring <b>Chui</b>, a black-and-white parti Pomeranian",
        "news": "News", "games": "Games", "coupons": "Coupons", "collab": "Collab codes",
        "no_news": "No news yet.", "no_coupons": "No coupons available right now.",
        "no_collab": "Collab codes will appear here once each game is released.",
        "coupon_how": "Enter a code in the game under <b>Settings → Coupon</b>. Each coupon can be used once.",
        "collab_how": "Enter a code in another Chui game under <b>Settings → Coupon</b> to get a gift in that game.",
        "status": {"released": "Out now", "testing": "Coming soon", "dev": "In development"},
        "play": "Google Play", "onestore": "ONE store", "more": "More",
        "forever": "No end date", "until": "until", "copy": "Copy", "copied": "Copied",
        "privacy": "Privacy", "contact": "Contact", "other": "한국어", "other_href": "../",
        "series_tag": "Chui Series", "dev": "Developer chuiFather · Black and White Raccoon",
        "updates": "Update history", "no_updates": "No updates yet.", "home": "Chui Series home",
    },
}

CSS = """
:root{--bg:#1a1630;--panel:#26204a;--panel2:#2f2858;--edge:#4a3f8a;--text:#ecebf7;--muted:#b9b4d6;--gold:#ffcd75;--cyan:#73eff7;--green:#a7f070}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);
font:16px/1.7 -apple-system,"Apple SD Gothic Neo","Noto Sans KR","Malgun Gothic",sans-serif}
main{max-width:860px;margin:0 auto;padding:32px 16px 64px}
h1,h2,.name{font-family:"Jua",-apple-system,"Apple SD Gothic Neo","Noto Sans KR",sans-serif;font-weight:400}
h1{color:var(--gold);font-size:2rem;line-height:1.2;margin:0 0 4px}
h2{color:var(--gold);font-size:1.3rem;margin:2.2rem 0 .6rem}
a{color:var(--cyan)}.muted{color:var(--muted)}.small{font-size:.85rem}
nav{display:flex;gap:14px;flex-wrap:wrap;margin:14px 0 0;font-size:.95rem}
.card{background:var(--panel);border:2px solid var(--edge);border-radius:12px;padding:16px;margin:10px 0}
.games .card{margin:0}
.games{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}
.game{display:flex;gap:14px;align-items:flex-start}
.game img{width:72px;height:72px;border-radius:16px;image-rendering:pixelated;flex:none}
.name{font-size:1.2rem;color:var(--text)}
.badge{display:inline-block;font-size:.75rem;padding:0 8px;border-radius:99px;border:1px solid var(--edge);color:var(--muted);margin-left:4px;vertical-align:middle}
.badge.released{border-color:var(--green);color:var(--green)}
.links{display:flex;gap:10px;flex-wrap:wrap;font-size:.9rem;margin-top:6px}
.news .date{color:var(--muted);font-size:.85rem}.news b{color:var(--gold)}
.ver{color:var(--cyan);font-weight:700}
.code{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.code code{font:700 1.05rem/1.4 ui-monospace,Menlo,Consolas,monospace;color:var(--cyan);background:var(--panel2);padding:4px 10px;border-radius:8px;letter-spacing:.04em;word-break:break-all}
button{font:inherit;font-size:.85rem;color:var(--bg);background:var(--gold);border:0;border-radius:8px;padding:4px 12px;cursor:pointer}
footer{margin-top:3rem;border-top:1px solid var(--edge);padding-top:1rem;font-size:.85rem;color:var(--muted)}
footer a{color:var(--muted)}
"""

JS = """
(function(){
  // 쿠폰 기간: 한국 시간 날짜(YYYY-MM-DD)로 비교, 지난 것·아직인 것은 숨김
  var now=new Date(Date.now()+9*3600*1000).toISOString().slice(0,10);
  var shown=0;
  document.querySelectorAll('[data-start]').forEach(function(el){
    var s=el.getAttribute('data-start')||'', e=el.getAttribute('data-end')||'';
    var ok=(!s||s<=now)&&(!e||now<=e);
    el.hidden=!ok; if(ok) shown++;
  });
  var empty=document.getElementById('no-coupons');
  if(empty) empty.hidden=shown>0;
  document.querySelectorAll('button[data-copy]').forEach(function(b){
    b.addEventListener('click',function(){
      var t=b.getAttribute('data-copy'), label=b.textContent;
      (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){
        b.textContent=b.getAttribute('data-done'); setTimeout(function(){b.textContent=label},1500);
      },function(){});
    });
  });
})();
"""


def esc(s):
    return html.escape(s or "", quote=True)


def pick(d, key, lang):
    return d.get(f"{key}_en") if lang == "en" and d.get(f"{key}_en") else d.get(key, "")


def build(lang):
    t = T[lang]
    up = "../" if lang == "en" else ""
    apps = [a for a in load("apps.json") if a.get("show")]
    by_id = {a["id"]: a for a in load("apps.json")}

    def app_name(app_id):
        if app_id == "series":
            return t["series_tag"]
        a = by_id.get(app_id)
        return pick(a, "name", lang) if a else app_id

    # 공지 (최신 순, 그 언어 제목이 없으면 안 보임 — SERIES.md §6 notices와 같은 규칙)
    notices = sorted(load("notices.json"), key=lambda n: (n.get("date", ""), n.get("id", 0)), reverse=True)
    rows = []
    for n in notices:
        title = n.get("title_en") if lang == "en" else n.get("title")
        if not title:
            continue
        body = n.get("body_en") if lang == "en" else n.get("body")
        rows.append(f'<div class="card news"><span class="date">{esc(n.get("date"))} · {esc(app_name(n.get("app")))}</span><br>'
                    f'<b>{esc(title)}</b><br>{esc(body)}</div>')
    news_html = "".join(rows[:10]) or f'<p class="muted">{t["no_news"]}</p>'

    update_apps = {u["app"] for u in load_updates()}

    # 게임
    cards = []
    for a in apps:
        links = []
        if a["status"] == "released" and a.get("play"):
            links.append(f'<a href="{esc(a["play"])}">{t["play"]}</a>')
        if a["status"] == "released" and a.get("onestore"):
            links.append(f'<a href="{esc(a["onestore"])}">{t["onestore"]}</a>')
        if a.get("page"):
            page = a["page"] + ("en/" if lang == "en" and a["id"] != "station" else "")
            links.append(f'<a href="{up}{esc(page)}">{t["more"]}</a>')
        if a["id"] in update_apps:
            links.append(f'<a href="updates/#{esc(a["id"])}">{t["updates"]}</a>')
        icon = f'<img src="{up}{esc(a["icon"])}" alt="" width="72" height="72">' if a.get("icon") else ""
        cards.append(
            f'<div class="card game">{icon}<div><span class="name">{esc(pick(a, "name", lang))}</span>'
            f'<span class="badge {esc(a["status"])}">{t["status"][a["status"]]}</span>'
            f'<div class="muted small">{esc(pick(a, "tagline", lang))}</div>'
            f'<div class="small">{esc(pick(a, "desc", lang))}</div>'
            f'<div class="links">{"".join(links)}</div></div></div>')
    games_html = f'<div class="games">{"".join(cards)}</div>'

    # 쿠폰 (기간은 페이지 JS가 판단)
    rows = []
    for c in load("coupons.json"):
        period = f'{esc(c.get("start", ""))} ~ {esc(c["end"])}' if c.get("end") else t["forever"]
        rows.append(
            f'<div class="card" data-start="{esc(c.get("start", ""))}" data-end="{esc(c.get("end", ""))}">'
            f'<span class="muted small">{esc(app_name(c["app"]))} · {period}</span>'
            f'<div class="code"><code>{esc(c["code"])}</code>'
            f'<button data-copy="{esc(c["code"])}" data-done="{t["copied"]}">{t["copy"]}</button></div>'
            f'<div class="small">{esc(pick(c, "label", lang))}</div></div>')
    coupons_html = (f'<p class="small muted">{t["coupon_how"]}</p>' + "".join(rows) +
                    f'<p id="no-coupons" class="muted"{" hidden" if rows else ""}>{t["no_coupons"]}</p>')

    # 콜라보 코드: 출시됐고 콜라보를 연 앱만 (SERIES.md §7, 출시 뒤에만 공개)
    live = [a for a in load("apps.json") if a["status"] == "released" and a.get("collab_live")]
    rows = [f'<div class="card"><span class="muted small">{esc(pick(a, "name", lang))}</span>'
            f'<div class="code"><code>{esc(a["collab_code"])}</code>'
            f'<button data-copy="{esc(a["collab_code"])}" data-done="{t["copied"]}">{t["copy"]}</button></div></div>'
            for a in live]
    collab_html = (f'<p class="small muted">{t["collab_how"]}</p>' + "".join(rows)) if rows else f'<p class="muted">{t["no_collab"]}</p>'

    privacy = " · ".join(
        f'<a href="{up}{esc(a["page"] if a["id"] != "station" else "")}{"en/" if lang == "en" else ""}privacy/">{esc(pick(a, "name", lang))}</a>'
        for a in apps if a.get("page"))

    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t["title"]}</title>
<meta name="description" content="{esc(html.unescape(t["lead"].replace("<b>", "").replace("</b>", "")))}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jua&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><main>
<h1>{t["title"]}</h1>
<p class="muted">{t["lead"]}</p>
<nav><a href="#games">{t["games"]}</a><a href="#news">{t["news"]}</a><a href="updates/">{t["updates"]}</a><a href="#coupons">{t["coupons"]}</a><a href="#collab">{t["collab"]}</a><a href="{t["other_href"]}">{t["other"]}</a></nav>
<h2 id="games">{t["games"]}</h2>
{games_html}
<h2 id="news">{t["news"]}</h2>
{news_html}
<h2 id="coupons">{t["coupons"]}</h2>
{coupons_html}
<h2 id="collab">{t["collab"]}</h2>
{collab_html}
<footer>{t["dev"]} · {t["contact"]} <a href="mailto:{CONTACT}">{CONTACT}</a><br>{t["privacy"]}: {privacy}</footer>
</main><script>{JS}</script></body></html>
"""


def load_updates():
    path = os.path.join(ROOT, "data", "updates.json")
    return load("updates.json") if os.path.exists(path) else []


def build_updates(lang):
    """게임별 업데이트 기록 (최신 순). 앱 안 업데이트 소식과 같은 글 (SERIES.md §15)."""
    t = T[lang]
    by_app = {}
    for u in load_updates():
        by_app.setdefault(u["app"], []).append(u)
    sections = []
    for a in load("apps.json"):
        rows = sorted(by_app.get(a["id"], []), reverse=True,
                      key=lambda u: (u.get("date", ""), tuple(int(x) if x.isdigit() else 0 for x in u["version"].split(".")), u.get("id", 0)))
        cards = []
        for u in rows:
            title = pick(u, "title", lang)
            body = esc(pick(u, "body", lang)).replace("\n", "<br>")
            cards.append(f'<div class="card news"><span class="ver">v{esc(u["version"])}</span> <span class="date">{esc(u.get("date"))}</span><br>'
                         f'<b>{esc(title)}</b><br>{body}</div>')
        if cards:
            sections.append(f'<h2 id="{esc(a["id"])}">{esc(pick(a, "name", lang))}</h2>' + "".join(cards))
    content = "".join(sections) or f'<p class="muted">{t["no_updates"]}</p>'
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t["updates"]} — {t["title"]}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jua&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><main>
<h1>{t["updates"]}</h1>
<nav><a href="../">{t["home"]}</a></nav>
{content}
</main></body></html>
"""


def main():
    for lang, path in (("ko", "updates/index.html"), ("en", "en/updates/index.html")):
        out = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(build_updates(lang))
        print("wrote", path)
    for lang, path in (("ko", "index.html"), ("en", "en/index.html")):
        out = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(build(lang))
        print("wrote", path)


if __name__ == "__main__":
    main()
