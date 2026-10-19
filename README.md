# chuiFather.github.io

츄이 시리즈 공식 홈페이지 (GitHub Pages). 규칙은 chui-series `SERIES.md` §5·§13.

## 시리즈 홈 (`/`, `/en/`) — 이 저장소가 직접 만든다
- https://chuifather.github.io/ — 게임 목록·공지·쿠폰·콜라보 코드 (영어 `/en/`)
- 원본 = `data/` 세 파일. 고친 뒤 `python3 tools/make_home.py` → `index.html`·`en/index.html` 커밋
  - `data/apps.json`: 앱 목록. `show`(홈에 보일지) · `status`(`released`/`testing`/`dev`) · `collab_live`(콜라보 코드 공개, 출시 뒤 그 앱에 새 콜라보가 들어간 버전이 나가면 true)
  - `data/notices.json`: 공지. `app` = `series`(사이트에만) 또는 앱 id (그 앱 Firebase `notices`에도)
  - `data/coupons.json`: 쿠폰. `builtin: true` = 앱 core에 든 영구 쿠폰(사이트에만), 아니면 Firebase `coupons`에도. 기간 지난 쿠폰은 페이지가 알아서 숨김
- Firebase에 넣을 값: `python3 tools/firebase_values.py [앱 id]` → PC 세션이 그 앱 Remote Config에 게시 (`collab_partners`·`notices`·`coupons`)
- 앱 아이콘 `assets/icons/<id>.png` = 각 앱 `docs/store/icon_512.png` 사본 (확정된 것만)
- **앱 저장소의 사이트 스크립트는 루트 `index.html`·`en/index.html`·`data/`·`tools/`·`assets/`를 덮어쓰지 않는다.**

## 츄이의 우주정거장 (`/station/`, 처리방침·확률은 루트 경로 유지)
- https://chuifather.github.io/station/ — 게임 소개 (2026-10-19 루트에서 옮김)
- https://chuifather.github.io/privacy/ — 개인정보처리방침
- https://chuifather.github.io/app-ads.txt — AdMob (출시 후 추가)

파일은 게임 저장소 `chuiFather/space-pom-station`의 `python3 tools/store/make_site.py` → `docs/site/` 에서 만든다. 원본 문서: `docs/privacy-policy.md`. ⚠️ 그 스크립트가 아직 `docs/site/index.html`(옛 루트 소개)을 만든다 → 복사할 때 `index.html`은 빼고 `station/index.html`로 (우주정거장 세션이 스크립트 고치기 전까지).

## 츄이 디펜스 (`/defense/`)
- https://chuifather.github.io/defense/privacy/ — 개인정보처리방침
- https://chuifather.github.io/defense/odds/ — 모집 확률
- https://chuifather.github.io/defense/en/ — 영어 (privacy/·odds/)

파일은 게임 저장소 `chuiFather/pom-defense`의 `python3 tools/store/make_site.py` → `docs/site/defense/`에서 만든다. 원본: `docs/privacy-policy.md`·`docs/privacy-policy.en.md`, `docs/odds.md`(영어 확률표는 같은 숫자 + 앱 strings 영어 이름).

## 츄이 서바이버즈 (`/survivors/`)
- https://chuifather.github.io/survivors/ — 게임 소개
- https://chuifather.github.io/survivors/privacy/ — 개인정보처리방침 (게임 설정 화면 버튼이 이 주소를 엶)

파일은 게임 저장소 `chuiFather/pom-survivors`의 `python3 tools/store/make_site.py` → `docs/site/survivors/`에서 만든다. 원본: `docs/privacy-policy.md`.
