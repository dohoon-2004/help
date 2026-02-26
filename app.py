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

# 상단 글귀
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

st.markdown(
    """
<style>
/* ✅ 최고급 웹 폰트 'Pretendard' 불러오기 */
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v3.2.1/dist/web/static/pretendard.css");

* {
  font-family: "Pretendard", -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif !important;
}

/* Streamlit 기본 잡동사니 완벽 제거 */
#MainMenu {visibility: hidden !important;}
footer {visibility: hidden !important;}
header {visibility: hidden !important;}
.stAppDeployButton {display: none !important;}
[data-testid="stToolbar"] {display: none !important;}
[data-testid="stHeader"] {display: none !important;}

/* ✅ 전체 배경색을 오묘하고 세련된 다크 그라데이션으로 변경 */
[data-testid="stAppViewContainer"] { 
  background: linear-gradient(135deg, #0b0c10 0%, #1a1e26 100%); 
}
.block-container { padding-top: 1.0rem; padding-bottom: 0.8rem; max-width: 1200px; }

/* 상단 글귀 */
.headline{
  font-size: 2.2rem; 
  font-weight: 800;
  letter-spacing: -0.6px;
  margin-top: 0.7rem;
  margin-bottom: 0.9rem;
  color: rgba(255,255,255,0.92);
}

/* 플레이어 */
.yt-wrap{
  position: relative;
  padding-top: 56.25%;
  border-radius: 18px;
  overflow: hidden;
  background: #000;
  box-shadow: 0 12px 34px rgba(0,0,0,0.3);
}
.yt-wrap iframe{
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  border: 0;
}

/* 플레이어 아래 텍스트 박스 (왼쪽 정렬) */
.song-info-box {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  width: 100%;              
  margin-top: 0.5rem;
  margin-bottom: 3.5rem;
}

/* ✅ 플레이어 밑 제목 크기 살짝 키움 (1.45rem -> 1.55rem) */
.song-title{
  font-size: 1.55rem;
  font-weight: 700;
  letter-spacing: -0.4px;
  color: rgba(255,255,255,0.95);
  text-align: left;
  margin: 0;
}
.song-artist{
  font-size: 1.40rem;
  font-weight: 500;
  letter-spacing: -0.4px;
  margin-top: 0.2rem;
  color: rgba(255,255,255,0.65);
  text-align: left;
  margin-bottom: 0;
}

/* 목록 버튼 공통 (글래스모피즘) */
div[data-testid="stButton"] > button {
  width: 100%;
  text-align: center;
  border-radius: 16px;
  padding: 18px 22px;
  background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.01));
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 4px 15px rgba(0,0,0,0.15);
  white-space: pre-wrap; 
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1); 
  
  font-size: 0.95rem;
  font-weight: 500;
  color: rgba(255,255,255,0.55) !important;
  line-height: 1.6;
}

/* 목록 첫 번째 줄(제목) */
div[data-testid="stButton"] > button::first-line,
div[data-testid="stButton"] > button p::first-line {
  font-size: 1.25rem;
  font-weight: 800;
  color: rgba(255,255,255,0.95);
  line-height: 1.4;
}

/* Hover 효과 */
div[data-testid="stButton"] > button[kind="secondary"]:hover {
  background: linear-gradient(145deg, rgba(255,255,255,0.1), rgba(255,255,255,0.03));
  border-color: rgba(255,255,255,0.25);
  transform: translateY(-3px);
  color: rgba(255,255,255,0.65) !important;
}

/* 선택된 버튼 하이라이트 */
div[data-testid="stButton"] > button[kind="primary"] {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.25), rgba(168, 85, 247, 0.25)) !important;
  border: 1px solid rgba(168, 85, 247, 0.5) !important;
  box-shadow: 0 0 20px rgba(168, 85, 247, 0.15) !important;
  transform: translateY(0px); 
}

div[data-testid="stButton"] > button[kind="primary"]::first-line,
div[data-testid="stButton"] > button[kind="primary"] p::first-line {
  color: #ffffff;
}

div[data-testid="stButton"] > button:focus:not(:active) { border-color: inherit !important; box-shadow: inherit !important; }

/* =========================================
   ✅ 모바일 페이지네이션 무조건 한 줄로 강제 고정 
   ========================================= */
.pagination-marker + div[data-testid="stHorizontalBlock"] {
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    justify-content: center !important;
    gap: 8px !important;
    margin-top: 10px;
}
.pagination-marker + div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
    width: auto !important;
    min-width: 0 !important;
    flex: 0 1 auto !important;
}

/* 페이지네이션 전용 버튼 디자인 (목록 버튼 디자인 무시하고 동그랗게) */
.pagination-marker + div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button {
    padding: 8px 16px !important;
    border-radius: 12px !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    text-align: center !important;
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    min-height: 0 !important;
    transform: none !important; /* 떠오르는 효과 제거 */
}
.pagination-marker + div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.6), rgba(168, 85, 247, 0.6)) !important;
    border-color: rgba(255,255,255,0.3) !important;
    color: white !important;
}
.pagination-marker + div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button::first-line {
    font-size: 1.1rem !important;
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
    # 5개씩 자르기
    ITEMS_PER_PAGE = 5
    total_pages = math.ceil(len(SONGS) / ITEMS_PER_PAGE)
    
    start_idx = st.session_state.page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    current_songs = SONGS[start_idx:end_idx]

    # 현재 페이지 노래 목록 렌더링
    for song in current_songs:
        is_selected = (song["id"] == st.session_state.selected_id)
        btn_type = "primary" if is_selected else "secondary"
        
        if st.button(f"{song['title']}\n{song['artist']}", key=f"song_{song['id']}", use_container_width=True, type=btn_type):
            st.session_state.selected_id = song["id"]
            st.session_state.headline = random.choice(HEADLINES)
            st.rerun()

    # ✅ 모바일에서도 한 줄로 유지되도록 돕는 CSS 마커 삽입
    st.markdown('<div class="pagination-marker"></div>', unsafe_allow_html=True)
    
    # 1, 2 버튼 배치
    cols = st.columns(total_pages)
    
    for i in range(total_pages):
        with cols[i]:
            btn_type = "primary" if st.session_state.page == i else "secondary"
            if st.button(str(i + 1), key=f"page_btn_{i}", use_container_width=True, type=btn_type):
                st.session_state.page = i
                st.rerun()
