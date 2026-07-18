# 로또맨 런칭 킷 — "로또는 통계다, 로또맨"

로또 6/45 통계 놀이터 앱을 실서비스로 배포하기 위한 모든 파일.

## 폴더 구성

| 파일 | 역할 |
|---|---|
| `template.html` | 앱 원본 템플릿 (`__DATA__`, `__FONT__`, `<!--HEAD_EXTRA-->` 치환자 포함) |
| `build.py` | 최신 당첨 데이터를 받아 `index.html` 생성 |
| `font_b64.txt` | Baloo 2 숫자 전용 서브셋 폰트 (base64) |
| `manifest.webmanifest` | PWA 매니페스트 (홈 화면 설치) |
| `sw.js` | 서비스워커 (오프라인 캐시) |
| `icon-192/512/180.png` | 앱 아이콘 (512는 마스커블) |
| `.github/workflows/update.yml` | 매주 토 21:40 KST 자동 데이터 갱신 |

데이터는 2중으로 갱신된다:
1. **빌드 시점**: CI가 매주 `index.html`에 최신 회차를 내장 (첫 화면부터 최신).
2. **런타임**: 앱이 열릴 때 `latest.json`을 확인해 새 회차를 받아 localStorage에 캐시 → 배포가 늦어도 사용자는 항상 최신.

## 배포 (무료, 10분)

```bash
cd lottoman-launch
python3 build.py                 # index.html 생성
git init && git add -A && git commit -m "로또맨 v1"
gh repo create lottoman --public --source . --push
gh api repos/{owner}/lottoman/pages -X POST -f 'source[branch]=main' -f 'source[path]=/'
```

이후 `https://<계정>.github.io/lottoman/` 접속 → 모바일 브라우저 "홈 화면에 추가"로 앱처럼 설치된다.
Actions 탭에서 `주간 데이터 갱신` 워크플로가 매주 돌아가는지 첫 주에 확인할 것.
(커스텀 도메인은 Settings → Pages에서 연결. Cloudflare Pages로 옮겨도 파일 그대로 동작.)

## 앱스토어 등록 (선택)

- **Android**: PWA를 그대로 감싸는 TWA(Trusted Web Activity) — [Bubblewrap](https://github.com/GoogleChromeLabs/bubblewrap)으로 `npx @bubblewrap/cli init --manifest=<배포주소>/manifest.webmanifest` 한 번이면 스토어용 AAB가 나온다. 구글플레이 정책상 실제 도박이 아닌 "정보/시뮬레이션" 앱으로 분류되지만, **복권 관련 앱은 심사 시 만 18+ 등급과 책임 고지 요구** — 앱 내 이미 포함된 면책 문구가 그 역할.
- **iOS**: 사파리 "홈 화면에 추가"는 즉시 가능. 앱스토어 등록은 Capacitor 래핑이 필요하고 심사가 더 까다로움(단순 웹뷰 리젝 사유 4.2) — 기록/공유 같은 네이티브 기능을 더 얹은 뒤 도전 권장.

## 런칭 전 체크리스트

### 법률·정책 (중요)
- [ ] **"예측·당첨·적중" 표현 금지** — 마케팅 문구 전부 "통계·분석·재미"로. 유료 예측 서비스는 소비자원 경고 및 규제 대상.
- [ ] 앱 내 면책 문구 유지 (확률 동일 고지 · 비공식 도구 고지 · 계획적 구매 권장) — 이미 포함됨.
- [ ] **상표**: [키프리스](http://www.kipris.or.kr)에서 "로또맨" 상표 검색, 가능하면 출원 (45류/9류). 스토어 동명 앱도 확인.
- [ ] "동행복권과 무관" 고지 유지, 동행복권 로고·명칭을 브랜드처럼 사용 금지.
- [ ] 광고 붙일 경우: 복권 광고는 매체 자율심의 대상 — "무료 번호 드립니다"류 문구 금지.

### 기술
- [ ] HTTPS 배포 (GitHub Pages 기본 제공) — 서비스워커·PWA 필수 조건.
- [ ] 첫 토요일 밤: CI 갱신 + 앱 내 "방금 갱신됨 ✓" 표시 확인.
- [ ] 데이터 소스 이중화: 현재 smok95 미러 사용 중. 트래픽이 커지면 자체 수집(동행복권 API는 국내 서버에서만 접근 가능)으로 전환 — `build.py`의 `DATA_URL`만 바꾸면 됨.
- [ ] Lighthouse PWA 점검 (Chrome DevTools → Lighthouse).

### 운영·수익화
- [ ] 개인정보처리방침 1장 — 현재 수집 정보 없음(모두 localStorage), 그대로 명시하면 됨. 광고 SDK를 붙이는 순간 갱신 필요.
- [ ] 수익 모델: ① 배너 광고(AdMob/카카오애드핏) ② 제휴(복권 판매점 지도 등) — **번호 판매·유료 예측은 금지선**.
- [ ] 공유 카드 → 인스타/카톡 유입 동선이 핵심 마케팅. 슬로건 고정: "로또는 통계다, 로또맨".

### 다음 기능 후보
- 추첨 직후 푸시 알림 (웹푸시 — 서버 키 필요)
- QR 스캔 당첨 확인
- 내 기록 통계 (누적 지출 대비 회수율 — 정직 컨셉 강화)
