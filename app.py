import math
import random
import streamlit as st
import streamlit.components.v1 as components

# -----------------------------
# 노래 목록 (테스트용 30곡)
# -----------------------------
BASE_SONGS = [
    {"id": "river-flows-in-you", "title": "River Flows in You", "artist": "Yiruma", "videoId": "7maJOI3QMu0"},
    {"id": "its-time", "title": "It's Time", "artist": "Imagine Dragons", "videoId": "NASqUELHjPE"},
    {"id": "iu-night-letter", "title": "밤편지", "artist": "아이유", "videoId": "EjMTw4xLcBI"},
    {"id": "stronger", "title": "Stronger", "artist": "Kelly Clarkson", "videoId": "Xn676-fLq7I"},
    {"id": "blackpink-ddu-du-ddu-du", "title": "DDU-DU DDU-DU", "artist": "BLACKPINK", "videoId": "IHNzOHi8sJs"},
    {"id": "sia-unstoppable", "title": "Unstoppable", "artist": "Sia", "videoId": "kIjUfXfJjGU"},
    {"id": "iu-blueming", "title": "Blueming", "artist": "아이유", "videoId": "D1PvIWdJ8xo"},
    {"id": "iu-celebrity", "title": "Celebrity", "artist": "아이유", "videoId": "0-q1KafFCLU"},
    {"id": "akmu-200-percent", "title": "200%", "artist": "AKMU", "videoId": "0Oi8jDMvd_w"},
    {"id": "bol4-hug", "title": "Hug", "artist": "볼빨간사춘기", "videoId": "qfeoX17dav0"},
]
SONGS = []
for i in range(3):
    for song in BASE_SONGS:
        s = song.copy()
        s["id"] = f"{song['id']}_{i}"
        SONGS.append(s)

HEADLINES = ["진짜 사랑해", "고마워", "옆에 있어줘", "덕분에 행복해", "안아줄게", "맛있는 거 먹자", "바다보러 갈래?"]

def yt_embed(video_id: str, title: str):
    src = f"https://www.youtube-nocookie.com/embed/{video_id}?rel=0&controls=1"
    html = f"""
    <div class="yt-wrap">
      <iframe
        src="{src}"
        title="{title}"
        allow="encrypted-media; picture-in-picture"
        allowfullscreen
      ></iframe>
    </div>
    """
    components.html(html, height=190)

st.set_page_config(page_title="player", page_icon="🎧", layout="wide")

# 맨 위로 스크롤
if st.session_state.get("scroll_to_top"):
    components.html("<script>window.parent.scrollTo({top: 0, behavior: 'smooth'});</script>", height=0, width=0)
    st.session_state.scroll_to_top = False

# -----------------------------
# CSS (폰트/색상/모바일 다크 안정화)
# -----------------------------
st.markdown(
    """
<style>
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v3.2.1/dist/web/static/pretendard.css");

/* Streamlit 기본 UI 숨김 */
#MainMenu, footer, header, .stAppDeployButton, [data-testid="stToolbar"], [data-testid="stHeader"] {
  display: none !important;
}

/* =========================================================
   ✅ 폰트 최적화 (가독성/스무딩/반응형)
   ========================================================= */
* {
  font-family: "Pretendard", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans KR", Arial, sans-serif !important;
  -webkit-font-smoothing: antialiased !important;
  -moz-osx-font-smoothing: grayscale !important;
  text-rendering: optimizeLegibility !important;
}

html, body {
  -webkit-text-size-adjust: 100%;
  text-size-adjust: 100%;
}

/* =========================================================
   ✅ 모바일 다크모드(색 꼬임) 안정화: 투명 rgba 최소화 + 변수 고정
   ========================================================= */
:root{
  color-scheme: light;
  --bg: #ffffff;
  --card: #f8fafc;
  --border: #e2e8f0;
  --text: #0f172a;
  --muted: #64748b;
  --shadow: 0 12px 34px rgba(0,0,0,0.12);

  --song-grad: linear-gradient(135deg, #a855f7, #ec4899);
  --page-grad: linear-gradient(135deg, #0ea5e9, #06b6d4);
}

@media (prefers-color-scheme: dark) {
  :root{
    color-scheme: dark;
    --bg: #0f1014;
    --card: #171a22;     /* ✅ rgba → 고정 hex로 */
    --border: #2a2f3a;   /* ✅ rgba → 고정 hex로 */
    --text: #f1f5f9;
    --muted: #aab2c2;
    --shadow: 0 12px 34px rgba(0,0,0,0.35);
  }
}

/* Streamlit 다크 DOM/변형에도 변수 강제 */
[data-theme="dark"], html.dark, body.dark, .stApp.dark {
  --bg: #0f1014 !important;
  --card: #171a22 !important;
  --border: #2a2f3a !important;
  --text: #f1f5f9 !important;
  --muted: #aab2c2 !important;
  --shadow: 0 12px 34px rgba(0,0,0,0.35) !important;
}

/* =========================================================
   ✅ 전체 배경/텍스트 색상 최적화 (모바일에서 글자색 꼬임 방지)
   ========================================================= */
html, body, .stApp, [data-testid="stAppViewContainer"], .block-container{
  background: var(--bg) !important;
  color: var(--text) !important;
}

p, span, label, small, li, div,
h1, h2, h3, h4, h5, h6,
.stMarkdown, .stMarkdown p {
  color: var(--text) !important;
  -webkit-text-fill-color: var(--text) !important;
}

/* 레이아웃 */
.block-container{
  padding-top: 0.2rem !important;
  padding-bottom: 0.8rem;
  max-width: 1200px;
}

/* =========================================================
   ✅ 상단 글귀 (반응형 폰트 + 중앙)
   ========================================================= */
.headline{
  font-size: clamp(1.6rem, 5vw, 2.0rem) !important;
  font-weight: 900;
  letter-spacing: -0.6px;
  margin: 0.2rem 0 1.5rem 0 !important;
  color: var(--text) !important;
  text-align: center !important; 
}

/* 유튜브 */
.yt-wrap{
  position: relative;
  padding-top: 56.25%;
  border-radius: 18px;
  overflow: hidden;
  background: #000;
  box-shadow: var(--shadow) !important;
}
.yt-wrap iframe{ position:absolute; inset:0; width:100%; height:100%; border:0; }

/* =========================================================
   ✅ 플레이어 아래 텍스트: 더 가깝게 + 오른쪽 살짝 이동
   ========================================================= */
.song-info{
  margin-top: 0rem !important;        /* ✅ 더 붙이기 */
  margin-bottom: 1.8rem;
  padding-left: 10px !important;      /* ✅ 살짝 오른쪽 이동 */
}
.song-title{ 
  font-size: clamp(1.25rem, 3.6vw, 1.5rem) !important;
  font-weight: 800; 
  color: var(--text) !important; 
  margin:0 !important;
  line-height: 1.15 !important;
}
.song-artist{ 
  font-size: clamp(1.05rem, 3.2vw, 1.25rem) !important;
  font-weight: 600; 
  color: var(--muted) !important; 
  margin:0.05rem 0 0 0 !important;    /* ✅ 제목-가수 간격 더 좁게 */
  line-height: 1.15 !important;
}

/* =========================================================
   ✅ 노래 목록 버튼 (텍스트 색/대비 개선)
   ========================================================= */
div[data-testid="stButton"] > button {
  width: 100%;
  text-align: center;
  border-radius: 16px !important;
  padding: 16px 20px !important;
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  box-shadow: 0 4px 10px rgba(0,0,0,0.03) !important;
  white-space: pre-wrap !important;
  transition: all 0.15s;
  font-size: clamp(0.9rem, 2.8vw, 0.95rem) !important;
  font-weight: 650;
}
div[data-testid="stButton"] > button p { color: var(--muted) !important; }
div[data-testid="stButton"] > button::first-line,
div[data-testid="stButton"] > button p::first-line {
  font-size: clamp(1.05rem, 3.2vw, 1.25rem) !important;
  font-weight: 850 !important;
  color: var(--text) !important;
}

div[data-testid="stButton"] > button[kind="primary"] {
  background: var(--song-grad) !important;
  border: none !important;
  box-shadow: 0 8px 18px rgba(236,72,153,0.25) !important;
}
div[data-testid="stButton"] > button[kind="primary"] * {
  color: #ffffff !important;
  -webkit-text-fill-color: #ffffff !important;
}

/* =========================================================
   ✅ 페이지네이션(숫자 버튼): "가운데 정렬" 확실히 고정
   ========================================================= */
div[data-testid="stRadio"] { 
  margin-top: 10px; 
  margin-bottom: 50px !important; 
}

div[data-testid="stRadio"] [role="radiogroup"] {
  display: flex !important;
  flex-direction: row !important;
  justify-content: center !important; /* ✅ 가운데 */
  align-items: center !important;

  gap: 12px !important;
  flex-wrap: nowrap !important;

  width: fit-content !important;      /* ✅ 콘텐츠 폭만 */
  margin: 0 auto !important;          /* ✅ 전체에서 중앙 */
  padding: 0 !important;
}

div[data-testid="stRadio"] label {
  width: 48px !important;
  height: 48px !important;
  margin: 0 !important;
  padding: 0 !important;
  display: inline-flex !important;
  position: relative !important;
  cursor: pointer !important;
  border: none !important;
  background: transparent !important;
}

div[data-testid="stRadio"] label > div:first-of-type {
  display: none !important;
}

div[data-testid="stRadio"] input[type="radio"] {
  position: absolute !important;
  inset: 0 !important;
  width: 100% !important;
  height: 100% !important;
  opacity: 0 !important; 
  margin: 0 !important;
  z-index: 10 !important;
  cursor: pointer !important;
}

div[data-testid="stRadio"] label > div:last-child {
  position: absolute !important;
  inset: 0 !important;
  width: 100% !important;
  height: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important; 
  border-radius: 50% !important;
  background: var(--card) !important; 
  border: 1px solid var(--border) !important;
  z-index: 1 !important;
  box-sizing: border-box !important;
  transition: all 0.2s !important;
}

div[data-testid="stRadio"] label p {
  font-size: clamp(1.05rem, 3.2vw, 1.25rem) !important;
  font-weight: 850 !important;
  color: var(--text) !important;
  margin: 0 !important;
  padding: 0 !important;
  line-height: 1 !important;
}

/* 선택된 숫자 버튼 */
div[data-testid="stRadio"] input[type="radio"]:checked ~ div:last-child {
  background: var(--page-grad) !important;
  border: none !important;
  box-shadow: 0 6px 15px rgba(14,165,233,0.3) !important;
}
div[data-testid="stRadio"] input[type="radio"]:checked ~ div:last-child p {
  color: #ffffff !important;
  -webkit-text-fill-color: #ffffff !important;
}

/* =========================================================
   ✅ 모바일에서 여백/크기 조금 더 다듬기 (선택)
   ========================================================= */
@media (max-width: 520px) {
  .block-container{ padding-left: 0.8rem !important; padding-right: 0.8rem !important; }
  .song-info{ padding-left: 6px !important; margin-bottom: 1.4rem !important; }
  div[data-testid="stButton"] > button { padding: 14px 16px !important; border-radius: 14px !important; }
}
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# 상태
# -----------------------------
if "selected_id" not in st.session_state:
    st.session_state.selected_id = SONGS[0]["id"] if SONGS else None
if "headline" not in st.session_state:
    st.session_state.headline = random.choice(HEADLINES)
if "page" not in st.session_state:
    st.session_state.page = 0

st.markdown(f"<div class='headline'>{st.session_state.headline}</div>", unsafe_allow_html=True)

player_col, list_col = st.columns([1.08, 1.0], gap="large")

with player_col:
    current = next((s for s in SONGS if s["id"] == st.session_state.selected_id), None)
    if current:
        yt_embed(current["videoId"], current["title"])
        st.markdown(
            f"""
            <div class="song-info">
              <div class="song-title">{current['title']}</div>
              <div class="song-artist">{current['artist']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

with list_col:
    ITEMS_PER_PAGE = 5
    total_pages = max(1, math.ceil(len(SONGS) / ITEMS_PER_PAGE))

    start_idx = st.session_state.page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    current_songs = SONGS[start_idx:end_idx]

    # 노래 목록
    for song in current_songs:
        is_selected = (song["id"] == st.session_state.selected_id)
        btn_type = "primary" if is_selected else "secondary"

        if st.button(f"{song['title']}\n{song['artist']}", key=f"song_{song['id']}", use_container_width=True, type=btn_type):
            st.session_state.selected_id = song["id"]
            st.session_state.headline = random.choice(HEADLINES)
            st.session_state.scroll_to_top = True
            st.rerun()

    # 페이지네이션: st.radio (horizontal)
    MAX_VISIBLE_BUTTONS = 5
    half_window = MAX_VISIBLE_BUTTONS // 2

    start_page = max(0, st.session_state.page - half_window)
    end_page = min(total_pages, start_page + MAX_VISIBLE_BUTTONS)
    start_page = max(0, end_page - MAX_VISIBLE_BUTTONS)

    visible_pages = list(range(start_page, end_page))
    labels = [str(p + 1) for p in visible_pages]

    # 현재 선택값
    current_label = str(st.session_state.page + 1)
    if current_label not in labels:
        current_label = labels[0] if labels else "1"

    chosen = st.radio(
        label="pagination",
        options=labels,
        index=labels.index(current_label) if labels else 0,
        horizontal=True,
        label_visibility="collapsed",
        key="pager_radio",
    )

    if labels:
        new_page = int(chosen) - 1
        if new_page != st.session_state.page:
            st.session_state.page = new_page
            st.session_state.headline = random.choice(HEADLINES)
            st.session_state.scroll_to_top = True
            st.rerun()
