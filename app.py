import random
import streamlit as st
import streamlit.components.v1 as components

# -----------------------------
# 노래 목록(코드에 고정)
# -----------------------------
SONGS = [
    {"id": "river-flows-in-you", "title": "River Flows in You", "artist": "Yiruma", "videoId": "7maJOI3QMu0"},
    {"id": "its-time", "title": "It's Time", "artist": "Imagine Dragons", "videoId": "NASqUELHjPE"},
    {"id": "iu-night-letter", "title": "밤편지", "artist": "아이유(IU)", "videoId": "EjMTw4xLcBI"},
    {"id": "stronger", "title": "Stronger (What Doesn't Kill You)", "artist": "Kelly Clarkson", "videoId": "Xn676-fLq7I"},
]

HEADLINES = ["진짜 사랑해", "고마워", "옆에 있어줘", "덕분에 행복해", "안아줄게", "맛있는 거 먹자", "바다보러 갈래?","보고 싶어"]

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
    # 공백 줄이기 (모바일용)
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

/* 플레이어 아래 텍스트 */
.song-title{
  font-size: 1.45rem;
  font-weight: 700;
  letter-spacing: -0.4px;
  margin-top: 0.25rem;
  color: rgba(255,255,255,0.92);
}
.song-artist{
  font-size: 1.40rem;
  font-weight: 600;
  letter-spacing: -0.4px;
  margin-top: 0.05rem;
  color: rgba(255,255,255,0.70);
}

/* ✅ 목록 버튼을 "카드"처럼 보이게 */
div[data-testid="stButton"] > button{
  width: 100%;
  text-align: left;
  border-radius: 20px;
  padding: 18px 20px;
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(255,255,255,0.14);
  color: rgba(255,255,255,0.92);
  box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
  white-space: normal;
}

/* 버튼 hover */
div[data-testid="stButton"] > button:hover{
  background: rgba(255,255,255,0.10);
  border-color: rgba(255,255,255,0.20);
}

/* ✅ 선택된 곡은 살짝 하이라이트(체크 없이도 티 나게) */
.selected-btn div[data-testid="stButton"] > button{
  background: rgba(255,255,255,0.14) !important;
  border-color: rgba(255,255,255,0.28) !important;
}

/* 버튼 안 텍스트 스타일 */
.card-title{
  font-size: 1.25rem;
  font-weight: 900;
  line-height: 1.2;
  margin: 0;
}
.card-artist{
  font-size: 1.10rem;
  font-weight: 650;
  color: rgba(255,255,255,0.68);
  margin-top: 8px;
}
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

        # ✅ 선택된 항목만 wrapper에 class를 걸어서 하이라이트
        if is_selected:
            st.markdown("<div class='selected-btn'>", unsafe_allow_html=True)

        label_html = f"""
        <div class="card-title">{song['title']}</div>
        <div class="card-artist">{song['artist']}</div>
        """

        # Streamlit button은 문자열을 그대로 출력하므로 HTML은 unsafe로 못 넣습니다.
        # 대신 "제목\\n가수" 형태로 넣고, 폰트는 전체 버튼 스타일로 맞춥니다.
        # (HTML 그대로 넣고 싶으면 custom component로 가야 합니다.)
        if st.button(f"{song['title']}\n{song['artist']}", key=f"song_{song['id']}", use_container_width=True):
            st.session_state.selected_id = song["id"]
            st.session_state.headline = random.choice(HEADLINES)
            st.rerun()

        if is_selected:
            st.markdown("</div>", unsafe_allow_html=True)
