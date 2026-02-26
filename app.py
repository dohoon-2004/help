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
        new_song = song.copy()
        new_song["id"] = f"{song['id']}_{i}"
        SONGS.append(new_song)

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
if "scroll_to_top" in st.session_state and st.session_state.scroll_to_top:
    components.html(
        "<script>window.parent.scrollTo({top: 0, behavior: 'smooth'});</script>",
        height=0, width=0
    )
    st.session_state.scroll_to_top = False

st.markdown(
    """
<style>
/* ✅ 다크 모드 강제 차단! 무조건 라이트 모드로 인식하게 만듦 */
:root {
  color-scheme: light only !important;
}

@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v3.2.1/dist/web/static/pretendard.css");
* {
  font-family: "Pretendard", -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif !important;
}

#MainMenu {visibility: hidden !important;}
footer {visibility: hidden !important;}
header {visibility: hidden !important;}
.stAppDeployButton {display: none !important;}
[data-testid="stToolbar"] {display: none !important;}
[data-testid="stHeader"] {display: none !important;}

/* ✅ 아주 뽀얗고 예쁜 라이트 배경 강제 적용 */
.stApp, [data-testid="stAppViewContainer"], .block-container { 
  background-color: #f8fafc !important;
  background-image: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important; 
}
.block-container { padding-top: 1.0rem; padding-bottom: 0.8rem; max-width: 1200px; }

/* 상단 글귀 */
.headline{
  font-size: 2.2rem; 
  font-weight: 900;
  letter-spacing: -0.6px;
  margin-top: 0.7rem;
  margin-bottom: 0.9rem;
  color: #0f172a !important; /* 진한 남색/검정 */
}

/* 플레이어 */
.yt-wrap{
  position: relative;
  padding-top: 56.25%;
  border-radius: 18px;
  overflow: hidden;
  background: #000;
  box-shadow: 0 12px 34px rgba(0,0,0,0.15);
}
.yt-wrap iframe{
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  border: 0;
}

/* 플레이어 아래 텍스트 박스 */
.song-info-box {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  width: 100%;              
  margin-top: 0.5rem;
  margin-bottom: 3.5rem;
}
.song-title{
  font-size: 1.65rem;
  font-weight: 800;
  letter-spacing: -0.4px;
  color: #0f172a !important;
  text-align: left;
  margin: 0;
}
.song-artist{
  font-size: 1.40rem;
  font-weight: 600;
  letter-spacing: -0.4px;
  margin-top: 0.2rem;
  color: #64748b !important;
  text-align: left;
  margin-bottom: 0;
}

/* ✅ 곡 목록 버튼 (깨끗한 화이트 톤으로 다크모드 무시) */
div[data-testid="stButton"] > button {
  width: 100%;
  text-align: center;
  border-radius: 16px;
  padding: 18px 22px;
  background-color: #ffffff !important;
  background-image: none !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 4px 10px rgba(0,0,0,0.04) !important;
  white-space: pre-wrap; 
  transition: all 0.2s; 
  
  font-size: 0.95rem;
  font-weight: 600;
  color: #64748b !important;
  line-height: 1.6;
}

div[data-testid="stButton"] > button::first-line,
div[data-testid="stButton"] > button p::first-line {
  font-size: 1.25rem;
  font-weight: 800;
  color: #1e293b !important;
  line-height: 1.4;
}

div[data-testid="stButton"] > button[kind="secondary"]:hover {
  background-color: #f8fafc !important;
  border-color: #cbd5e1 !important;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.08) !important;
}

/* 선택된 곡/페이지 버튼 (그라데이션 포인트) */
div[data-testid="stButton"] > button[kind="primary"] {
  background-color: #8b5cf6 !important;
  background-image: linear-gradient(135deg, #6366f1, #a855f7) !important;
  border: none !important;
  box-shadow: 0 6px 15px rgba(139, 92, 246, 0.35) !important;
  transform: translateY(0px) !important; 
}
div[data-testid="stButton"] > button[kind="primary"]::first-line,
div[data-testid="stButton"] > button[kind="primary"] p::first-line,
div[data-testid="stButton"] > button[kind="primary"] {
  color: #ffffff !important;
}

div[data-testid="stButton"] > button:focus:not(:active) { border-color: inherit !important; box-shadow: inherit !important; }

/* =========================================================
   ✅ 여백 완전 제거! 숫자 버튼 픽셀 단위로 강제 고정
   ========================================================= */
.page-numbers-row + div[data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    justify-content: center !important;
    gap: 10px !important;  /* 👈 버튼 사이 간격 딱 이만큼만 허용 */
    margin-top: 15px !important;
}

/* 쓸데없이 넓어지는 컬럼(여백) 크기를 45px로 꽉 묶어버림 */
.page-numbers-row + div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
    min-width: 45px !important;
    max-width: 45px !important;
    width: 45px !important;
    flex: 0 0 45px !important;
    padding: 0 !important;
}

/* 숫자 버튼 자체도 45x45 완벽한 동그라미로 고정 */
.page-numbers-row + div[data-testid="stHorizontalBlock"] button {
    width: 45px !important;
    height: 45px !important;
    border-radius: 50% !important; 
    padding: 0 !important;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 1.15rem !important;
    font-weight: 800 !important;
}
.page-numbers-row + div[data-testid="stHorizontalBlock"] button::first-line {
    font-size: 1.15rem !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# 상태 초기화
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
            <div class='song-info-box'>
              <div class='song-title'>{current['title']}</div>
              <div class='song-artist'>{current['artist']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

with list_col:
    ITEMS_PER_PAGE = 5
    total_pages = math.ceil(len(SONGS) / ITEMS_PER_PAGE)
    
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

    # 페이지네이션 
    MAX_VISIBLE_BUTTONS = 5
    half_window = MAX_VISIBLE_BUTTONS // 2
    
    start_page = max(0, st.session_state.page - half_window)
    end_page = start_page + MAX_VISIBLE_BUTTONS
    
    if end_page > total_pages:
        end_page = total_pages
        start_page = max(0, total_pages - MAX_VISIBLE_BUTTONS)
        
    visible_pages = list(range(start_page, end_page))

    # ✅ 숫자 버튼 사이의 여백을 완벽 통제하기 위한 마커
    st.markdown('<div class="page-numbers-row"></div>', unsafe_allow_html=True)
    
    cols = st.columns(len(visible_pages))
    
    for idx, p in enumerate(visible_pages):
        with cols[idx]:
            btn_type = "primary" if st.session_state.page == p else "secondary"
            if st.button(str(p + 1), key=f"page_btn_{p}", use_container_width=True, type=btn_type):
                st.session_state.page = p
                st.session_state.headline = random.choice(HEADLINES)
                st.session_state.scroll_to_top = True
                st.rerun()
