import streamlit as st
import streamlit.components.v1 as components

# -----------------------------
# 노래 목록(여기에만 추가/수정)
# -----------------------------
SONGS = [
    {"id": "river-flows-in-you", "title": "River Flows in You", "artist": "Yiruma", "videoId": "7maJOI3QMu0"},
]

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
    # ✅ 플레이어 아래 여백 줄이기: height를 과하게 크게 잡지 않음
    components.html(html, height=340)

def heart_icon(is_fav: bool) -> str:
    return "🩷" if is_fav else "🤍"

def check_icon(is_selected: bool) -> str:
    return "✅" if is_selected else "☐"

# -----------------------------
# 페이지 설정 + 스타일
# -----------------------------
st.set_page_config(page_title="노래", page_icon="🎧", layout="wide")

st.markdown(
    """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* 전체 여백/간격 줄이기 */
.block-container {padding-top: 1.6rem; padding-bottom: 1.2rem; max-width: 1200px;}
div[data-testid="stVerticalBlock"]{ gap: 0.55rem; }

div[data-testid="stVerticalBlockBorderWrapper"]{
  border-radius: 18px !important;
}

/* 플레이어 */
.yt-wrap{
  position:relative;
  padding-top:56.25%;
  border-radius:18px;
  overflow:hidden;
  background:#000;
  box-shadow: 0 8px 30px rgba(0,0,0,0.10);
  margin-bottom: 0; /* 아래 여백 제거 */
}
.yt-wrap iframe{
  position:absolute; inset:0;
  width:100%; height:100%;
  border:0;
}

/* 버튼 */
.stButton button{
  border-radius: 12px;
  padding: 0.55rem 0.85rem;
  white-space: nowrap;
}

/* 텍스트 크기 */
.player-title {font-size: 1.55rem; font-weight: 800; letter-spacing: -0.3px; margin: 0;}
.player-artist {font-size: 1.20rem; font-weight: 750; color: rgba(0,0,0,0.68); margin-top: 0.15rem;}

.list-title {font-size: 1.05rem; font-weight: 750; margin: 0;}
.list-artist {font-size: 1.00rem; font-weight: 650; color: rgba(0,0,0,0.62); margin-top: 0.15rem;}

/* 액션(체크/하트) 가운데 정렬 */
.action-pad{
  display:flex;
  height: 100%;
  align-items: center;
  justify-content: center;
}
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# 상태(선택곡 / 즐겨찾기)
# -----------------------------
if "selected_id" not in st.session_state:
    st.session_state.selected_id = SONGS[0]["id"] if SONGS else None

if "favorites" not in st.session_state:
    st.session_state.favorites = set()

# 옵션(원하시면 통째로 삭제 가능)
with st.sidebar:
    only_fav = st.checkbox("🩷 즐겨찾기만 보기", value=False)

visible_songs = SONGS if not only_fav else [s for s in SONGS if s["id"] in st.session_state.favorites]

# -----------------------------
# 레이아웃 (재생 왼쪽 / 목록 오른쪽)
# -----------------------------
player_col, list_col = st.columns([1.0, 1.25], gap="large")

# ---- 왼쪽: 재생 ----
with player_col:
    current = next((s for s in SONGS if s["id"] == st.session_state.selected_id), None)
    if current:
        is_fav = (current["id"] in st.session_state.favorites)

        t1, t2 = st.columns([0.86, 0.14], gap="small")
        with t1:
            st.markdown(f"<div class='player-title'>{current['title']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='player-artist'>{current.get('artist','')}</div>", unsafe_allow_html=True)
        with t2:
            if st.button(heart_icon(is_fav), key=f"fav_now_{current['id']}"):
                if is_fav:
                    st.session_state.favorites.remove(current["id"])
                else:
                    st.session_state.favorites.add(current["id"])
                st.rerun()

        yt_embed(current["videoId"], current["title"])
    else:
        st.info("오른쪽에서 노래를 체크해 주세요.")

# ---- 오른쪽: 목록 ----
with list_col:
    if not visible_songs:
        st.info("표시할 노래가 없습니다.")
    else:
        for song in visible_songs:
            is_selected = (song["id"] == st.session_state.selected_id)
            is_fav = (song["id"] in st.session_state.favorites)

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
