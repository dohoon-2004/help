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

# -----------------------------
# 상단 글귀(짧게)
# -----------------------------
HEADLINES = ["진짜 사랑해", "고마워", "옆에 있어줘", "덕분에 행복해"]

# -----------------------------
# 유튜브 임베드
# -----------------------------
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
    # ✅ 요청하신 대로 높이를 190으로 줄였습니다.
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

/* ✅ 상단 글귀 사이즈 (font-size 값을 원하시는 대로 조절하세요) */
.headline{
  font-size: 2.2rem; 
  font-weight: 900;
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

/* ✅ 플레이어 바로 아래 텍스트 (위로 끌어올림) */
.song-title{
  font-size: 1.45rem;
  font-weight: 600;
  letter-spacing: -0.4px;
  margin-top: -1.0rem;    /* 높이를 190으로 맞췄으므로 이 정도 음수면 딱 맞습니다 */
  position: relative; 
  z-index: 10;
  color: rgba(255,255,255,0.92);
}
.song-artist{
  font-size: 1.60rem;
  font-weight: 900;
  letter-spacing: -0.4px;
  margin-top: 0.08rem;
  position: relative;
  z-index: 10;
  color: rgba(255,255,255,0.70);
}

/* 목록 줄 */
.list-row{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap: 12px;
  padding: 14px 14px;
  border-radius: 18px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
  margin-bottom: 12px;
}
.list-text{
  min-width: 0;
}
.list-title{
  font-size: 1.05rem;
  font-weight: 900;
  color: rgba(255,255,255,0.92);
  line-height: 1.2;
}
.list-artist{
  font-size: 1.10rem;
  font-weight: 850;
  color: rgba(255,255,255,0.65);
  margin-top: 4px;
  line-height: 1.2;
}

/* 체크 버튼 */
.check-wrap{
  flex: 0 0 auto;
}
.stButton button{
  border-radius: 14px;
  padding: 0.60rem 0.90rem;
  white-space: nowrap;
}
</style>
""",
    unsafe_allow_html=True,
)

# 상태
if "selected_id" not in st.session_state:
    st.session_state.selected_id = SONGS[0]["id"] if SONGS else None

# 상단 글귀 초기화
if "headline" not in st.session_state:
    st.session_state.headline = random.choice(HEADLINES)

st.markdown(f"<div class='headline'>{st.session_state.headline}</div>", unsafe_allow_html=True)

# 레이아웃
player_col, list_col = st.columns([1.08, 1.0], gap="large")

with player_col:
    current = next((s for s in SONGS if s["id"] == st.session_state.selected_id), None)
    if current:
        yt_embed(current["videoId"], current["title"])
        # 플레이어 바로 밑에 제목/가수
        st.markdown(f"<div class='song-title'>{current['title']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='song-artist'>{current['artist']}</div>", unsafe_allow_html=True)

with list_col:
    for song in SONGS:
        is_selected = (song["id"] == st.session_state.selected_id)

        st.markdown(
            f"""
            <div class="list-row">
              <div class="list-text">
                <div class="list-title">{song['title']}</div>
                <div class="list-artist">{song['artist']}</div>
              </div>
              <div class="check-wrap" id="check_{song['id']}"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        btn_col_l, btn_col_r = st.columns([0.82, 0.18])
        with btn_col_l:
            st.write("")
        with btn_col_r:
            if st.button(check_icon(is_selected), key=f"pick_{song['id']}", use_container_width=True):
                st.session_state.selected_id = song["id"]
                # ✅ 노래를 바꿀 때마다 새로운 글귀로 변경
                st.session_state.headline = random.choice(HEADLINES)
                st.rerun()
