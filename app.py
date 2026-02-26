import random
import streamlit as st
import streamlit.components.v1 as components

# -----------------------------
# 노래 목록(코드에 고정)
# -----------------------------
SONGS = [
    {"id": "river-flows-in-you", "title": "River Flows in You", "artist": "Yiruma", "videoId": "7maJOI3QMu0"},
    {"id": "its-time", "title": "It's Time", "artist": "Imagine Dragons", "videoId": "NASqUELHjPE"},
    # {"id": "new", "title": "노래제목", "artist": "가수", "videoId": "유튜브_VIDEO_ID"},
]

# -----------------------------
# 상단 고정 문구(짧게)
# -----------------------------
HEADLINES = ["사랑해", "고마워", "옆에 있어줘", "덕분에 행복해"]

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
    # 플레이어 크기: "정말 조금" 키움
    components.html(html, height=400)

def heart_icon(is_fav: bool) -> str:
    return "🩷" if is_fav else "🤍"

def check_icon(is_selected: bool) -> str:
    return "✅" if is_selected else "☐"

st.set_page_config(page_title="player", page_icon="🎧", layout="wide")

st.markdown(
    """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

[data-testid="stAppViewContainer"] { background: #f7f7fb; }
.block-container { padding-top: 1.2rem; padding-bottom: 1.0rem; max-width: 1200px; }
div[data-testid="stVerticalBlock"]{ gap: 0.35rem; }

div[data-testid="stVerticalBlockBorderWrapper"]{
  border-radius: 18px !important;
  background: #ffffff !important;
  border: 1px solid rgba(0,0,0,0.06) !important;
  box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
}

/* 상단 문구 */
.headline{
  font-size: 1.35rem;
  font-weight: 900;
  letter-spacing: -0.4px;
  margin: 0.1rem 0 0.6rem 0;
  color: rgba(15,23,42,0.92);
}

/* 플레이어 */
.yt-wrap{
  position: relative;
  padding-top: 56.25%;
  border-radius: 18px;
  overflow: hidden;
  background: #000;
  box-shadow: 0 12px 34px rgba(0,0,0,0.10);
  margin-bottom: 0;
}
.yt-wrap iframe{
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  border: 0;
}

/* 텍스트: 플레이어 아래 */
.song-title { font-size: 1.20rem; font-weight: 900; letter-spacing: -0.3px; margin: 0; }
.song-artist { font-size: 1.35rem; font-weight: 900; color: rgba(0,0,0,0.68); margin-top: 0.10rem; }

/* 목록 텍스트 */
.list-title { font-size: 1.05rem; font-weight: 900; margin: 0; }
.list-artist { font-size: 1.10rem; font-weight: 850; color: rgba(0,0,0,0.62); margin-top: 0.10rem; }

/* 버튼 */
.stButton button{
  border-radius: 12px;
  padding: 0.55rem 0.85rem;
  white-space: nowrap;
}

/* 액션 가운데 정렬 */
.action-pad{
  display: flex;
  height: 100%;
  align-items: center;
  justify-content: center;
}
</style>
""",
    unsafe_allow_html=True,
)

# 상태
if "selected_id" not in st.session_state:
    st.session_state.selected_id = SONGS[0]["id"] if SONGS else None
if "favorites" not in st.session_state:
    st.session_state.favorites = set()

# 상단 문구(세션마다 1개 고정)
if "headline" not in st.session_state:
    st.session_state.headline = random.choice(HEADLINES)

st.markdown(f"<div class='headline'>{st.session_state.headline}</div>", unsafe_allow_html=True)

# 레이아웃 (왼쪽: 플레이어 / 오른쪽: 목록)
player_col, list_col = st.columns([1.08, 1.0], gap="large")

with player_col:
    current = next((s for s in SONGS if s["id"] == st.session_state.selected_id), None)
    if current:
        is_fav = current["id"] in st.session_state.favorites

        # 플레이어 + (오른쪽) 하트 버튼
        p1, p2 = st.columns([0.88, 0.12], gap="small")
        with p1:
            yt_embed(current["videoId"], current["title"])
        with p2:
            if st.button(heart_icon(is_fav), key=f"fav_now_{current['id']}"):
                if is_fav:
                    st.session_state.favorites.remove(current["id"])
                else:
                    st.session_state.favorites.add(current["id"])
                st.rerun()

        # ✅ 플레이어 아래: 제목/가수 (왼쪽)
        st.markdown(f"<div class='song-title'>{current['title']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='song-artist'>{current.get('artist','')}</div>", unsafe_allow_html=True)

with list_col:
    for song in SONGS:
        is_selected = song["id"] == st.session_state.selected_id
        is_fav = song["id"] in st.session_state.favorites

        with st.container(border=True):
            c1, c2 = st.columns([0.78, 0.22], gap="medium")

            with c1:
                st.markdown(f"<div class='list-title'>{song['title']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='list-artist'>{song.get('artist','')}</div>", unsafe_allow_html=True)

            with c2:
                st.markdown("<div class='action-pad'>", unsafe_allow_html=True)
                b1, b2 = st.columns([1, 1], gap="small")
                with b1:
                    if st.button(check_icon(is_selected), key=f"pick_{song['id']}", use_container_width=True):
                        st.session_state.selected_id = song["id"]
                        st.rerun()
                with b2:
                    if st.button(heart_icon(is_fav), key=f"fav_{song['id']}", use_container_width=True):
                        if is_fav:
                            st.session_state.favorites.remove(song["id"])
                        else:
                            st.session_state.favorites.add(song["id"])
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
