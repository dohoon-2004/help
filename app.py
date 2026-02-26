import random
import streamlit as st
import streamlit.components.v1 as components

# -----------------------------
# 노래 목록(코드에 고정)
# -----------------------------
SONGS = [
    {"id": "river-flows-in-you", "title": "River Flows in You", "artist": "Yiruma", "videoId": "7maJOI3QMu0"},
    {"id": "its-time", "title": "It's Time", "artist": "Imagine Dragons", "videoId": "NASqUELHjPE"},
]

# 상단 문구
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
    # ✅ 모바일 빈 공간 제거 핵심: height를 과하게 크게 잡지 않기
    # (가로폭이 줄면 실제 16:9 높이는 더 작아지므로, 400 같은 값은 빈 공간을 만듭니다)
    components.html(html, height=270)

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

[data-testid="stAppViewContainer"] { background: #0f1014; }
.block-container { padding-top: 1.1rem; padding-bottom: 0.8rem; max-width: 1200px; }
div[data-testid="stVerticalBlock"]{ gap: 0.2rem; }

/* 상단 문구 */
.headline{
  font-size: 2.0rem;
  font-weight: 900;
  letter-spacing: -0.6px;
  margin: 0.2rem 0 0.5rem 0;
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
  font-size: 1.6rem;
  font-weight: 900;
  letter-spacing: -0.4px;
  margin-top: 0.55rem;
  color: rgba(255,255,255,0.92);
}
.song-artist{
  font-size: 1.9rem;         /* ✅ 가수 이름 더 크게 */
  font-weight: 900;
  letter-spacing: -0.4px;
  margin-top: 0.05rem;
  color: rgba(255,255,255,0.70);
}

/* 버튼 */
.stButton button{
  border-radius: 14px;
  padding: 0.60rem 0.85rem;
  white-space: nowrap;
}

/* (선택) 카드 느낌 */
div[data-testid="stVerticalBlockBorderWrapper"]{
  border-radius: 18px !important;
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
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
if "headline" not in st.session_state:
    st.session_state.headline = random.choice(HEADLINES)

# 상단 문구
st.markdown(f"<div class='headline'>{st.session_state.headline}</div>", unsafe_allow_html=True)

# ✅ 모바일에서는 columns가 세로로 쌓입니다(정상)
player_col, list_col = st.columns([1.08, 1.0], gap="large")

with player_col:
    current = next((s for s in SONGS if s["id"] == st.session_state.selected_id), None)
    if current:
        is_fav = current["id"] in st.session_state.favorites

        # ✅ 플레이어 폭을 100%로 만들기 위해:
        # 하트 버튼을 "플레이어 위 오른쪽"으로 빼서, 플레이어를 옆에서 안 깎습니다.
        top_l, top_r = st.columns([0.80, 0.20])
        with top_l:
            st.write("")  # 자리만
        with top_r:
            if st.button(heart_icon(is_fav), key=f"fav_now_{current['id']}", use_container_width=True):
                if is_fav:
                    st.session_state.favorites.remove(current["id"])
                else:
                    st.session_state.favorites.add(current["id"])
                st.rerun()

        yt_embed(current["videoId"], current["title"])

        # ✅ 플레이어 아래: 왼쪽 정렬 제목/가수
        st.markdown(f"<div class='song-title'>{current['title']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='song-artist'>{current.get('artist','')}</div>", unsafe_allow_html=True)

with list_col:
    # 지금은 곡 1개라 단순 목록(원하시면 나중에 여러 곡 확장)
    for song in SONGS:
        is_selected = song["id"] == st.session_state.selected_id
        is_fav = song["id"] in st.session_state.favorites

        with st.container(border=True):
            c1, c2 = st.columns([0.72, 0.28], gap="small")
            with c1:
                st.markdown(f"<div style='color:rgba(255,255,255,0.92);font-weight:900;font-size:1.05rem'>{song['title']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='color:rgba(255,255,255,0.65);font-weight:800;font-size:1.10rem;margin-top:0.1rem'>{song['artist']}</div>", unsafe_allow_html=True)
            with c2:
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
