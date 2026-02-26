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
    # 모바일 공백 최소화
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

/* ---------- theme variables ---------- */
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

/* Streamlit dark theme (여러 버전 대비) */
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

/* ---------- headline ---------- */
.headline{
  font-size: 2.2rem;
  font-weight: 900;
  letter-spacing: -0.6px;
  margin: 0.2rem 0 0.4rem 0;
  color: var(--text) !important;
}

/* ---------- player ---------- */
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

/* ---------- song list button (st.button) ---------- */
.songlist div[data-testid="stButton"] > button{
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
.songlist div[data-testid="stButton"] > button p{ color: var(--muted) !important; }
.songlist div[data-testid="stButton"] > button::first-line,
.songlist div[data-testid="stButton"] > button p::first-line{
  font-size: 1.25rem !important;
  font-weight: 850 !important;
  color: var(--text) !important;
}

/* 선택된 노래만 색칠 (올려주신 방식 그대로) */
.songlist div[data-testid="stButton"] > button[kind="primary"]{
  background: var(--song-grad) !important;
  border: none !important;
  box-shadow: 0 8px 18px rgba(236,72,153,0.25) !important;
}
.songlist div[data-testid="stButton"] > button[kind="primary"] *{
  color: #ffffff !important;
}

/* ---------- pager (st.radio horizontal) ---------- */
.pager { 
  margin-top: 10px; 
  margin-bottom: 50px !important; /* ✅ 숫자버튼 크기(50px) 정도의 여백 추가! */
}

/* 'pages' 라벨 완벽 숨김 */
div[data-testid="stRadio"] > label {
  display: none !important;
}

.pager [role="radiogroup"]{
  display:flex !important;
  gap: 12px !important;            
  justify-content: center !important;
  flex-wrap: nowrap !important;
}

/* 라디오 항목을 원형 버튼처럼 - 완벽 중앙 정렬 */
.pager label{
  margin: 0 !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  position: relative !important;
  width: 48px !important;
  height: 48px !important;
  cursor: pointer !important;
}

/* 라디오 기본 점 숨김 */
.pager label > div:first-child {
  display: none !important;
}

/* 실제 동그라미 버튼 모양 (배경) */
.pager input[type="radio"]{
  appearance: none !important;
  -webkit-appearance: none !important;
  position: absolute !important;
  inset: 0 !important;
  width: 100% !important;
  height: 100% !important;
  border-radius: 50% !important;
  border: 1px solid var(--border) !important;
  background: var(--card) !important;
  margin: 0 !important;
  box-sizing: border-box !important;
  cursor: pointer !important;
  z-index: 1 !important;
}

/* 숫자 텍스트 - 정중앙에 고정! */
.pager label > div:last-child,
.pager label span {
  position: relative !important;
  z-index: 10 !important; /* 배경 위에 뜨도록 */
  pointer-events: none !important;
  font-size: 1.25rem !important;
  font-weight: 850 !important;
  color: var(--text) !important;
  margin: 0 !important;
  padding: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

/* 선택된 페이지: 파랑/하늘 그라데이션 (올려주신 방식 그대로) */
.pager input[type="radio"]:checked{
  background: var(--page-grad) !important;
  border: none !important;
  box-shadow: 0 8px 18px rgba(14,165,233,0.25) !important;
}
.pager input[type="radio"]:checked ~ div,
.pager input[type="radio"]:checked ~ div span,
.pager input[type="radio"]:checked ~ span {
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

    # 노래 목록 wrapper
    st.markdown("<div class='songlist'>", unsafe_allow_html=True)
    for song in current_songs:
        is_selected = (song["id"] == st.session_state.selected_id)
        btn_type = "primary" if is_selected else "secondary"

        if st.button(f"{song['title']}\n{song['artist']}", key=f"song_{song['id']}", use_container_width=True, type=btn_type):
            st.session_state.selected_id = song["id"]
            st.session_state.headline = random.choice(HEADLINES)
            st.session_state.scroll_to_top = True
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

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
        current_label = labels[0]

    st.markdown("<div class='pager'>", unsafe_allow_html=True)
    chosen = st.radio(
        label=" ", # ✅ "pages" 글씨를 아예 빈칸으로 비워버림
        options=labels,
        index=labels.index(current_label),
        horizontal=True,
        label_visibility="collapsed",
        key="pager_radio",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    new_page = int(chosen) - 1
    if new_page != st.session_state.page:
        st.session_state.page = new_page
        st.session_state.headline = random.choice(HEADLINES)
        st.session_state.scroll_to_top = True
        st.rerun()
