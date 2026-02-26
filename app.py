import streamlit as st
import streamlit.components.v1 as components

# -----------------------------
# 1) 노래 목록(여기에만 추가/수정)
# -----------------------------
SONGS = [
    {"id": "weightless", "title": "Weightless", "artist": "Marconi Union", "videoId": "UfcAVejslrU"},
    {"id": "example2", "title": "Never Gonna Give You Up", "artist": "Rick Astley", "videoId": "dQw4w9WgXcQ"},
    # {"id": "new", "title": "노래제목", "artist": "가수", "videoId": "유튜브_VIDEO_ID"},
]

# -----------------------------
# 2) 유튜브 임베드
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

def thumb_url(video_id: str):
    return f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"

# -----------------------------
# 3) 페이지 설정 + 스타일
# -----------------------------
st.set_page_config(page_title="노래 재생", page_icon="🎧", layout="wide")

st.markdown(
    """
<style>
/* Streamlit 기본 메뉴/푸터 숨기기 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* 전체 느낌 */
.block-container {padding-top: 2.2rem; padding-bottom: 2.2rem; max-width: 1200px;}
h1,h2,h3 {letter-spacing:-0.3px;}
.small-muted {color: rgba(0,0,0,0.55); font-size: 0.92rem;}

/* 카드 느낌 */
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

/* 버튼 높이 약간 */
.stButton button{
  border-radius: 12px;
  padding: 0.55rem 0.85rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# 4) 상태(선택곡 / 즐겨찾기)
# -----------------------------
if "selected_id" not in st.session_state:
    st.session_state.selected_id = SONGS[0]["id"] if SONGS else None

if "favorites" not in st.session_state:
    st.session_state.favorites = set()

# -----------------------------
# 5) 상단 헤더
# -----------------------------
st.markdown("## 🎧 노래 재생")

# 사이드바(원하시면 통째로 제거 가능)
with st.sidebar:
    st.markdown("### 옵션")
    only_fav = st.checkbox("★ 즐겨찾기만 보기", value=False)
    st.caption("노래 추가/수정은 코드(SONGS)에서만 하시면 됩니다.")

# 필터링
visible_songs = SONGS
if only_fav:
    visible_songs = [s for s in SONGS if s["id"] in st.session_state.favorites]

# -----------------------------
# 6) 레이아웃: 왼쪽(목록) / 오른쪽(플레이어)
# -----------------------------
left, right = st.columns([1.15, 1.0], gap="large")

with left:
    st.markdown("### 목록")

    if not visible_songs:
        st.info("표시할 노래가 없습니다.")
    else:
        # 3열 그리드
        cols = st.columns(3, gap="medium")
        for i, song in enumerate(visible_songs):
            c = cols[i % 3]
            with c:
                with st.container(border=True):
                    st.image(thumb_url(song["videoId"]), use_container_width=True)

                    fav = "★" if song["id"] in st.session_state.favorites else "☆"
                    st.markdown(f"**{song['title']}**")
                    st.markdown(f"<div class='small-muted'>{song.get('artist','')}</div>", unsafe_allow_html=True)

                    b1, b2 = st.columns([1, 1], gap="small")
                    with b1:
                        if st.button("재생", key=f"play_{song['id']}"):
                            st.session_state.selected_id = song["id"]
                            st.rerun()
                    with b2:
                        if st.button(fav, key=f"fav_{song['id']}"):
                            if song["id"] in st.session_state.favorites:
                                st.session_state.favorites.remove(song["id"])
                            else:
                                st.session_state.favorites.add(song["id"])
                            st.rerun()

with right:
    st.markdown("### 재생")

    current = next((s for s in SONGS if s["id"] == st.session_state.selected_id), None)
    if not current:
        st.info("왼쪽에서 노래를 선택해 주세요.")
    else:
        is_fav = current["id"] in st.session_state.favorites
        star_label = "★ 즐겨찾기 해제" if is_fav else "☆ 즐겨찾기"

        top1, top2 = st.columns([1.4, 1.0])
        with top1:
            st.markdown(f"#### {current['title']}")
            if current.get("artist"):
                st.markdown(f"<div class='small-muted'>{current['artist']}</div>", unsafe_allow_html=True)
        with top2:
            if st.button(star_label, use_container_width=True):
                if is_fav:
                    st.session_state.favorites.remove(current["id"])
                else:
                    st.session_state.favorites.add(current["id"])
                st.rerun()

        yt_embed(current["videoId"], current["title"])
        st.link_button("YouTube에서 열기", f"https://www.youtube.com/watch?v={current['videoId']}", use_container_width=True)
