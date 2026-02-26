import random
import streamlit as st
import streamlit.components.v1 as components

# -----------------------------
# 노래 목록 (괄호 및 괄호 안 내용 모두 제거)
# -----------------------------
SONGS = [
    {"id": "river-flows-in-you", "title": "River Flows in You", "artist": "Yiruma", "videoId": "7maJOI3QMu0"},
    {"id": "its-time", "title": "It's Time", "artist": "Imagine Dragons", "videoId": "NASqUELHjPE"},
    {"id": "iu-night-letter", "title": "밤편지", "artist": "아이유", "videoId": "EjMTw4xLcBI"},
    {"id": "stronger", "title": "Stronger", "artist": "Kelly Clarkson", "videoId": "Xn676-fLq7I"},
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
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

[data-testid="stAppViewContainer"] { background: #0f1014; }
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
  box-shadow: 0 12px 34px rgba(0,0,0,0.25);
}
.yt-wrap iframe{
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  border: 0;
}

/* ✅ 플레이어 아래 텍스트 (가운데 정렬 적용) */
.song-title{
  font-size: 1.45rem;
  font-weight: 700;
  letter-spacing: -0.4px;
  margin-top: 0.25rem;
  color: rgba(255,255,255,0.92);
  text-align: center; /* 👈 가운데 정렬 */
}
.song-artist{
  font-size: 1.40rem;
  font-weight: 600;
  letter-spacing: -0.4px;
  margin-top: 0.05rem;
  margin-bottom: 3.5rem; 
  color: rgba(255,255,255,0.70);
  text-align: center; /* 👈 가운데 정렬 */
}

/* 글래스모피즘 느낌 버튼 */
div[data-testid="stButton"] > button {
  width: 100%;
  text-align: left;
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

/* 첫 번째 줄(제목) 분리 */
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
  box-shadow: 0 8px 25px rgba(0,0,0,0.3);
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
</style>
""",
    unsafe_allow_html=True,
)

# 상태
if "selected_id" not in st.session_state:
    st.session_state.selected_id = SONGS[0]["id"] if SONGS else None

if "headline" not in st.session_state:
    st.session_state.headline = random.choice(HEADLINES)

st.markdown(f"<div class='headline'>{st.session_state.headline}</div>", unsafe_allow_html=True)

player_col, list_col = st.columns([1.08, 1.0], gap="large")

with player_col:
    current = next((s for s in SONGS if s["id"] == st.session_state.selected_id), None)
    if current:
        yt_embed(current["videoId"], current["title"])
        st.markdown(f"<div class='song-title'>{current['title']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='song-artist'>{current['artist']}</div>", unsafe_allow_html=True)

with list_col:
    for song in SONGS:
        is_selected = (song["id"] == st.session_state.selected_id)
        btn_type = "primary" if is_selected else "secondary"
        
        if st.button(f"{song['title']}\n{song['artist']}", key=f"song_{song['id']}", use_container_width=True, type=btn_type):
            st.session_state.selected_id = song["id"]
            st.session_state.headline = random.choice(HEADLINES)
            st.rerun()
