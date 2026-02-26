import streamlit as st
import streamlit.components.v1 as components

# -----------------------------
# 노래 목록(여기에만 추가/수정)
# -----------------------------
SONGS = [
    {"id": "weightless", "title": "Weightless", "artist": "Marconi Union", "videoId": "UfcAVejslrU"},
    {"id": "example2", "title": "Never Gonna Give You Up", "artist": "Rick Astley", "videoId": "dQw4w9WgXcQ"},
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
    components.html(html, height=420)

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

.block-container {padding-top: 2.2rem; padding-bottom: 2.2rem; max-width: 1200px;}
h1,h2,h3 {letter-spacing:-0.3px;}
.small-muted {color: rgba(0,0,0,0.55); font-size: 0.92rem;}

div[data-testid="stVerticalBlockBorderWrapper"]{
  border-radius: 18px !important;
}

/* 유튜브 래퍼 */
.yt-wrap{
  position:relative;
  padding-top:56.25%;
  border-radius:18px;
  overflow:hidden;
  background:#000;
  box-shadow: 0 8px 30px rgba(0,0,0,0.10);
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

/* 액션 영역(체크/하트) 세로 중앙 정렬 */
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

# -----------------------------
# 헤더 + 옵션
# -----------------------------
st.markdown("## 🎧 노래")

with st.sidebar:
    st.markdown("### 옵션")
    only_fav = st.checkbox("🩷 즐겨찾기만 보기", value=False)

visible_songs = SONGS
if only_fav:
    visible_songs = [s for s in SONGS if s["id"] in st.session_state.favorites]

# -----------------------------
# 레이아웃 (✅ 재생 왼쪽 / 목록 오른쪽)
# -----------------------------
player_col, list_col = st.columns([1.0, 1.25], gap="large")

# ---- 왼쪽: 재생 ----
with player_col:
    st.markdown("### 재생")

    current = next((s for s in SONGS if s["id"] == st.session_state.selected_id), None)
    if not current:
        st.info("오른쪽 목록에서 노래를 체크해 주세요.")
    else:
        is_fav = (current["id"] in st.session_state.favorites)

        top1, top2 = st.columns([0.84, 0.16], gap="small")
        with top1:
            st.markdown(f"#### {current['title']}")
            if current.get("artist"):
                st.markdown(f"<div class='small-muted'>{current['artist']}</div>", unsafe_allow_html=True)
        with top2:
            if st.button(heart_icon(is_fav), key=f"fav_now_{current['id']}"):
                if is_fav:
                    st.session_state.favorites.remove(current["id"])
                else:
                    st.session_state.favorites.add(current["id"])
                st.rerun()

        yt_embed(current["videoId"], current["title"])
        st.link_button(
            "YouTube에서 열기",
            f"https://www.youtube.com/watch?v={current['videoId']}",
            use_container_width=True,
        )

# ---- 오른쪽: 목록 ----
with list_col:
    st.markdown("### 목록")

    if not visible_songs:
        st.info("표시할 노래가 없습니다.")
    else:
        for song in visible_songs:
            is_selected = (song["id"] == st.session_state.selected_id)
            is_fav = (song["id"] in st.session_state.favorites)

            with st.container(border=True):
                c1, c2 = st.columns([0.78, 0.22], gap="medium")

                # 텍스트 정보(썸네일 제거)
                with c1:
                    st.markdown(f"**{song['title']}**")
                    if song.get("artist"):
                        st.markdown(f"<div class='small-muted'>{song['artist']}</div>", unsafe_allow_html=True)

                # 버튼(체크/하트) - 가운데 정렬 느낌
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
