import random
import streamlit as st
import streamlit.components.v1 as components

SONGS = [
    {"id": "river-flows-in-you", "title": "River Flows in You", "artist": "Yiruma", "videoId": "7maJOI3QMu0"},
    {"id": "its-time", "title": "It's Time", "artist": "Imagine Dragons", "videoId": "NASqUELHjPE"},
    {"id": "iu-night-letter", "title": "밤편지", "artist": "아이유(IU)", "videoId": "EjMTw4xLcBI"},
    {"id": "stronger", "title": "Stronger (What Doesn't Kill You)", "artist": "Kelly Clarkson", "videoId": "Xn676-fLq7I"},
]

HEADLINES = ["진짜 사랑해", "고마워", "옆에 있어줘", "덕분에 행복해"]

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

def check_icon(is_selected: bool) -> str:
    return "✅" if is_selected else "☐"

st.set_page_config(page_title="player", page_icon="🎧", layout="wide")

st.markdown(
    """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

[data-testid="stAppViewContainer"] { background: #0f1014; }
.block-container { padding-top: 1.0rem; padding-bottom: 0.8rem; max-width: 1200px; }

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

/* 플레이어 바로 아래 텍스트 */
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

/* ✅ 리스트 카드(더 크게) */
.list-card{
  border-radius: 20px;
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(255,255,255,0.14);
  padding: 18px 20px;      /* ✅ 카드 자체 padding 확대 */
  margin-bottom: 10px;
}

/* 카드 안 텍스트 */
.list-title{
  font-size: 1.25rem;      /* ✅ 제목 더 크게 */
  font-weight: 900;
  color: rgba(255,255,255,0.92);
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.list-artist{
  font-size: 1.15rem;      /* ✅ 가수도 더 크게 */
  font-weight: 650;
  color: rgba(255,255,255,0.68);
  margin-top: 8px;
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ✅ 체크 버튼이 "제목/가수 아래" 들어가게: 버튼 영역을 카드처럼 붙이기 */
.check-row{
  margin-top: 12px;        /* ✅ 제목/가수 아래 간격 */
  display: flex;
  justify-content: flex-end; /* 오른쪽 정렬 원하면 flex-end, 가운데면 center */
}

/* 버튼 스타일 */
.stButton button{
  border-radius: 14px;
  padding: 0.65rem 1.0rem;   /* ✅ 버튼도 살짝 큼 */
  white-space: nowrap;
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

        # ✅ 카드(텍스트)
        st.markdown(
            f"""
            <div class="list-card">
              <div class="list-title">{song['title']}</div>
              <div class="list-artist">{song['artist']}</div>
              <div class="check-row"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ✅ 카드 바로 아래에 "체크 버튼"을 붙여서
        # 제목/가수 밑에 들어간 것처럼 보이게 처리
        # (Streamlit 버튼은 HTML 안에 못 넣어서 이 방식이 가장 안정적)
        # 버튼을 카드 안쪽처럼 보이게 하려면 좌우 padding을 맞춰줍니다.
        pad_l, pad_r = st.columns([0.70, 0.30])
        with pad_l:
            st.write("")
        with pad_r:
            if st.button(check_icon(is_selected), key=f"pick_{song['id']}", use_container_width=True):
                st.session_state.selected_id = song["id"]
                st.session_state.headline = random.choice(HEADLINES)
                st.rerun()
