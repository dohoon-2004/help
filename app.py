import math
import random
import streamlit as st
import streamlit.components.v1 as components

# -----------------------------
# 노래 목록
# -----------------------------
SONGS = [
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

# ✅ 페이지 이동 시 맨 위로 스크롤하는 자바스크립트 실행 (상태에 따라 한 번만 동작)
if "scroll_to_top" in st.session_state and st.session_state.scroll_to_top:
    components.html(
        """
        <script>
            window.parent.scrollTo({top: 0, behavior: 'smooth'});
        </script>
        """,
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

/* ✅ 배경을 이전보다 훨씬 부드럽고 밝은 다크 네이비/슬레이트 톤으로 변경 */
[data-testid="stAppViewContainer"] { 
  background: linear-gradient(135deg, #1f232d 0%, #2e3542 100%); 
}
.block-container { padding-top: 1.0rem; padding-bottom: 0.8rem; max-width: 1200px; }

/* 상단 글귀 */
.headline{
  font-size: 2.2rem; 
  font-weight: 800;
  letter-spacing: -0.6px;
  margin-top: 0.7rem;
  margin-bottom: 0.9rem;
  color: rgba(255,255,255,0.95);
}

/* 플레이어 */
.yt-wrap{
  position: relative;
  padding-top: 56.25%;
  border-radius: 18px;
  overflow: hidden;
  background: #000;
  box-shadow: 0 12px 34px rgba(0,0,0,0.25);
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

/* ✅ 플레이어 밑 제목 살짝 더 키움 (1.65rem) */
.song-title{
  font-size: 1.65rem;
  font-weight: 700;
  letter-spacing: -0.4px;
  color: #ffffff;
  text-align: left;
  margin: 0;
}
.song-artist{
  font-size: 1.40rem;
  font-weight: 500;
  letter-spacing: -0.4px;
  margin-top: 0.2rem;
  color: rgba(255,255,255,0.75);
  text-align: left;
  margin-bottom: 0;
}

/* 목록 버튼 (글래스모피즘) */
div[data-testid="stButton"] > button {
  width: 100%;
  text-align: center;
  border-radius: 16px;
  padding: 18px 22px;
  background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.1);
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  white-space: pre-wrap; 
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1); 
  
  font-size: 0.95rem;
  font-weight: 500;
  color: rgba(255,255,255,0.6) !important;
  line-height: 1.6;
}

/* 첫 번째 줄(제목) 분리 */
div[data-testid="stButton"] > button::first-line,
div[data-testid="stButton"] > button p::first-line {
  font-size: 1.25rem;
  font-weight: 800;
  color: #ffffff;
  line-height: 1.4;
}

/* Hover 효과 */
div[data-testid="stButton"] > button[kind="secondary"]:hover {
  background: linear-gradient(145deg, rgba(255,255,255,0.12), rgba(255,255,255,0.05));
  border-color: rgba(255,255,255,0.3);
  transform: translateY(-3px);
  color: rgba(255,255,255,0.8) !important;
}

/* 선택된 버튼 하이라이트 */
div[data-testid="stButton"] > button[kind="primary"] {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.35), rgba(168, 85, 247, 0.35)) !important;
  border: 1px solid rgba(168, 85, 247, 0.6) !important;
  box-shadow: 0 0 20px rgba(168, 85, 247, 0.2) !important;
  transform: translateY(0px); 
}

div[data-testid="stButton"] > button[kind="primary"]::first-line,
div[data-testid="stButton"] > button[kind="primary"] p::first-line {
  color: #ffffff;
}

div[data-testid="stButton"] > button:focus:not(:active) { border-color: inherit !important; box-shadow: inherit !important; }

/* =========================================================
   ✅ 최신 CSS 트릭: 모바일에서 1, 2 버튼이 절대 안 깨지게 강제 가로 정렬
   ========================================================= */
div[data-testid="stElementContainer"]:has(.page-numbers-row) + div[data-testid="stHorizontalBlock"] {
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 12px !important;
    justify-content: center !important;
    margin-top: 15px;
}
div[data-testid="stElementContainer"]:has(.page-numbers-row) + div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
    min-width: 0 !important;
    width: auto !important;
    flex: 1 1 0px !important;
}

/* 숫자 버튼 자체의 디자인 (목록 버튼과 다르게 설정) */
div[data-testid="stElementContainer"]:has(.page-numbers-row) + div[data-testid="stHorizontalBlock"] button {
    padding: 12px 10px !important;
    border-radius: 14px !important;
    font-size: 1.15rem !important;
    font-weight: 800 !important;
}
div[data-testid="stElementContainer"]:has(.page-numbers-row) + div[data-testid="stHorizontalBlock"] button::first-line {
    font-size: 1.15rem !important; /* 숫자 버튼은 글씨 크기 고정 */
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
            st.session_state.scroll_to_top = True # 노래 바꿔도 맨 위로 스크롤
            st.rerun()

    # ✅ 모바일 가로 정렬을 위한 비밀 마커 삽입
    st.markdown('<div class="page-numbers-row"></div>', unsafe_allow_html=True)
    
    # 숫자 버튼 (가운데 정렬을 위해 빈 공간을 양쪽에 넣음)
    layout = [1.5] + [1] * total_pages + [1.5]
    cols = st.columns(layout)
    
    for i in range(total_pages):
        with cols[i + 1]:
            btn_type = "primary" if st.session_state.page == i else "secondary"
            if st.button(str(i + 1), key=f"page_btn_{i}", use_container_width=True, type=btn_type):
                st.session_state.page = i
                st.session_state.headline = random.choice(HEADLINES) # ✅ 글귀 변경
                st.session_state.scroll_to_top = True # ✅ 맨 위로 스크롤
                st.rerun()
