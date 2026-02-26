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
# 최대 5개 표시 테스트용 복사
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

/* ✅ 모바일 강제 다크모드 방어: 확실한 밝은 배경 */
.stApp, [data-testid="stAppViewContainer"] { 
  background-color: #fdfbfb !important;
  background-image: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%) !important; 
}
.block-container { padding-top: 1.0rem; padding-bottom: 0.8rem; max-width: 1200px; }

/* 상단 글귀 */
.headline{
  font-size: 2.2rem; 
  font-weight: 900;
  letter-spacing: -0.6px;
  margin-top: 0.7rem;
  margin-bottom: 0.9rem;
  color: #111827 !important;
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
  color: #111827 !important;
  text-align: left;
  margin: 0;
}
.song-artist{
  font-size: 1.40rem;
  font-weight: 600;
  letter-spacing: -0.4px;
  margin-top: 0.2rem;
  color: #4b5563 !important;
  text-align: left;
  margin-bottom: 0;
}

/* 목록 버튼 공통 */
div[data-testid="stButton"] > button {
  width: 100%;
  text-align: center;
  border-radius: 16px;
  padding: 18px 22px;
  background: rgba(255, 255, 255, 0.85) !important;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 0, 0, 0.08) !important;
  box-shadow: 0 4px 15px rgba(0,0,0,0.03) !important;
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
  color: #0f172a !important;
  line-height: 1.4;
}

div[data-testid="stButton"] > button[kind="secondary"]:hover {
  background: rgba(255, 255, 255, 1) !important;
  border-color: rgba(0, 0, 0, 0.15) !important;
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.08) !important;
}

/* 선택된 버튼 하이라이트 */
div[data-testid="stButton"] > button[kind="primary"] {
  background: linear-gradient(135deg, #6366f1, #a855f7) !important;
  border: none !important;
  box-shadow: 0 6px 20px rgba(168, 85, 247, 0.3) !important;
  transform: translateY(0px) !important; 
}
div[data-testid="stButton"] > button[kind="primary"]::first-line,
div[data-testid="stButton"] > button[kind="primary"] p::first-line {
  color: #ffffff !important;
}
div[data-testid="stButton"] > button[kind="primary"] {
  color: rgba(255,255,255,0.85) !important;
}
div[data-testid="stButton"] > button:focus:not(:active) { border-color: inherit !important; box-shadow: inherit !important; }

/* =========================================================
   ✅ 모바일 호환 100%: 이중 구조를 이용한 페이지 버튼 타겟팅
   (최신 CSS가 무시되는 모바일에서도 절대 안 깨집니다)
   ========================================================= */
div[data-testid="stHorizontalBlock"] div[data-testid="stHorizontalBlock"] {
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 8px !important;
    justify-content: center !important;
    margin-top: 15px !important;
    width: 100% !important;
}
div[data-testid="stHorizontalBlock"] div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
    min-width: unset !important;
    width: auto !important;
    flex: 0 0 auto !important;
    padding: 0 !important;
}
/* 숫자 버튼 동그라미 강제 */
div[data-testid="stHorizontalBlock"] div[data-testid="stHorizontalBlock"] button {
    padding: 0 !important;
    border-radius: 50% !important; /* 완벽한 원형 */
    width: 3.0rem !important;      /* 고정 크기 */
    height: 3.0rem !important;
    font-size: 1.15rem !important;
    font-weight: 800 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    white-space: nowrap !important;
}
div[data-testid="stHorizontalBlock"] div[data-testid="stHorizontalBlock"] button::first-line,
div[data-testid="stHorizontalBlock"] div[data-testid="stHorizontalBlock"] button p::first-line {
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

    # 모바일에서도 완벽 호환되는 중첩 st.columns 로직
    cols = st.columns(len(visible_pages))
    
    for idx, p in enumerate(visible_pages):
        with cols[idx]:
            btn_type = "primary" if st.session_state.page == p else "secondary"
            if st.button(str(p + 1), key=f"page_btn_{p}", use_container_width=True, type=btn_type):
                st.session_state.page = p
                st.session_state.headline = random.choice(HEADLINES)
                st.session_state.scroll_to_top = True
                st.rerun()
