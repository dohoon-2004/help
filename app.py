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
# CSS 
# -----------------------------
st.markdown(
    """
<style>
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v3.2.1/dist/web/static/pretendard.css");
* { font-family: "Pretendard", -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif !important; }

#MainMenu, footer, header, .stAppDeployButton, [data-testid="stToolbar"], [data-testid="stHeader"] {
  display: none !important;
}

/* ---------- 다크/라이트 모드 테마 변수 ---------- */
:root{
  --bg: #ffffff;
  --card: #f8fafc;
  --border: #e2e8f0;
  --text: #0f172a;
  --muted: #64748b;
  --shadow: 0 12px 34px rgba(0,0,0,0.12);

  --song-grad: linear-gradient(135deg, #a855f7, #ec4899);
  --page-grad: linear-gradient(135deg, #0ea5e9, #06b6d4);
}

html[data-theme="dark"], body[data-theme="dark"], .stApp[data-theme="dark"],
html.dark, body.dark, .stApp.dark{
  --bg: #0f1014;
  --card: rgba(255,255,255,0.06);
  --border: rgba(255,255,255,0.14);
  --text: rgba(255,255,255,0.95);
  --muted: rgba(255,255,255,0.65);
  --shadow: 0 12px 34px rgba(0,0,0,0.25);
}

html, body, .stApp, [data-testid="stAppViewContainer"], .block-container{
  background: var(--bg) !important;
}
.block-container{
  padding-top: 0.2rem !important;
  padding-bottom: 0.8rem;
  max-width: 1200px;
}

.headline{
  font-size: 2.2rem;
  font-weight: 900;
  letter-spacing: -0.6px;
  margin: 0.2rem 0 0.4rem 0;
  color: var(--text) !important;
}

.yt-wrap{
  position: relative;
  padding-top: 56.25%;
  border-radius: 18px;
  overflow: hidden;
  background: #000;
  box-shadow: var(--shadow);
}
.yt-wrap iframe{ position:absolute; inset:0; width:100%; height:100%; border:0; }

.song-info{
  margin-top: 0.5rem;
  margin-bottom: 1.8rem;
}
.song-title{ font-size: 1.65rem; font-weight: 800; color: var(--text); margin:0; }
.song-artist{ font-size: 1.40rem; font-weight: 600; color: var(--muted); margin:0.2rem 0 0 0; }

/* =========================================================
   ✅ 노래 목록 버튼 (핑크/보라 유지)
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
  font-size: 0.95rem;
  font-weight: 650;
}
div[data-testid="stButton"] > button p { color: var(--muted) !important; }
div[data-testid="stButton"] > button::first-line,
div[data-testid="stButton"] > button p::first-line {
  font-size: 1.25rem !important;
  font-weight: 850 !important;
  color: var(--text) !important;
}

/* 노래 버튼 선택 시 핑크/보라 그라데이션 */
div[data-testid="stButton"] > button[kind="primary"] {
  background: var(--song-grad) !important;
  border: none !important;
  box-shadow: 0 8px 18px rgba(236,72,153,0.25) !important;
}
div[data-testid="stButton"] > button[kind="primary"] * {
  color: #ffffff !important;
}

/* =========================================================
   ✅ 숫자 버튼 (st.radio) 중앙 정렬 & 숫자를 원 중앙에
   ========================================================= */
div[data-testid="stRadio"] { 
  margin-top: 10px; 
  margin-bottom: 50px !important; /* 👈 숫자 버튼 크기 정도의 하단 여백 추가! */
}

/* 라디오 버튼 그룹 가로 중앙 정렬 */
div[data-testid="stRadio"] [role="radiogroup"] {
  display: flex !important;
  flex-direction: row !important;
  justify-content: center !important; 
  gap: 12px !important;
  flex-wrap: nowrap !important;
  width: 100% !important;
}

/* 라디오 라벨 컨테이너 (여기에 아무것도 가리지 않게 수정) */
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

/* 기존 Streamlit의 파란 점(기본 라디오 표시) 없애기 */
div[data-testid="stRadio"] label > div:first-of-type {
  display: none !important;
}

/* 실제 클릭되는 라디오 input (눈에 안 보이지만 원 전체를 덮음) */
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

/* 텍스트와 배경이 들어가는 실제 원형 박스 (이게 숫자를 담는 그릇입니다) */
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

/* 숫자 폰트 크기 및 색상 */
div[data-testid="stRadio"] label p {
  font-size: 1.25rem !important;
  font-weight: 850 !important;
  color: var(--text) !important;
  margin: 0 !important;
  padding: 0 !important;
  line-height: 1 !important;
}

/* =========================================================
   ✅ 핵심: 선택된 숫자 버튼 색상 변경 (모바일 호환 100%)
   ========================================================= */
/* 체크된 input의 '바로 옆'에 있는 div의 배경을 파랑/하늘색으로 바꿈 */
div[data-testid="stRadio"] input[type="radio"]:checked ~ div:last-child {
  background: var(--page-grad) !important;
  border: none !important;
  box-shadow: 0 6px 15px rgba(14,165,233,0.3) !important;
}

/* 체크된 input의 '바로 옆'에 있는 div 안의 숫자를 하얀색으로 바꿈 */
div[data-testid="stRadio"] input[type="radio"]:checked ~ div:last-child p {
  color: #ffffff !important;
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
        label="",
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
