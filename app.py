import streamlit as st
import streamlit.components.v1 as components

# -----------------------------
# 1) 노래 목록(여기에만 추가/수정)
# -----------------------------
SONGS = [
    {"id": "river-flows-in-you", "title": "River Flows in You", "artist": "Yiruma", "videoId": "https://www.youtube.com/watch?v=7maJOI3QMu0&list=RD7maJOI3QMu0&start_radio=1"},
]

# -----------------------------
# 2) 유튜브/썸네일
# -----------------------------
def thumb_url(video_id: str) -> str:
    return f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"

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

# -----------------------------
# 3) 페이지 설정 + 스타일
# -----------------------------
st.set_page_config(page_title="노래 재생", page_icon="🎧", layout="wide")

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

/* 가로형 썸네일(고정 비율 + 크롭) */
.thumb{
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: 14px;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  box-shadow: 0 6px 22px rgba(0,0,0,0.08);
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
  white-space: nowrap; /* 버튼 글자 줄바꿈 방지 */
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
# 5) 헤더 + 사이드바 옵션
# -----------------------------
st.markdown("## 🎧 노래")

with st.sidebar:
    st.markdown("### 옵션")
    only_fav = st.checkbox("★ 즐겨찾기만 보기", value=False)

visible_songs = SONGS
if only_fav:
    visible_songs = [s for s in SONGS if s["id"] in st.session_state.favorites]

# -----------------------------
# 6) 레이아웃
# -----------------------------
left, right = st.columns([1.2, 1.0], gap="large")

with left:
    st.markdown("### 목록")

    if not visible_songs:
        st.info("표시할 노래가 없습니다.")
    else:
        # ✅ 가로형 리스트(한 곡 = 한 줄)
        for song in visible_songs:
            is_selected = (song["id"] == st.session_state.selected_id)
            is_fav = (song["id"] in st.session_state.favorites)
            fav_icon = "★" if is_fav else "☆"

            with st.container(border=True):
                c1, c2, c3 = st.columns([0.42, 0.43, 0.15], gap="medium")

                # 썸네일(고정 비율)
                with c1:
                    st.markdown(
                        f"<div class='thumb' style=\"background-image:url('{thumb_url(song['videoId'])}')\"></div>",
                        unsafe_allow_html=True,
                    )

                # 제목/아티스트
                with c2:
                    st.markdown(f"**{song['title']}**")
                    if song.get("artist"):
                        st.markdown(f"<div class='small-muted'>{song['artist']}</div>", unsafe_allow_html=True)
                    if is_selected:
                        st.caption("현재 선택됨")

                # 버튼(가로)
                with c3:
                    b1, b2 = st.columns(2, gap="small")
                    with b1:
                        if st.button("선택", key=f"pick_{song['id']}", use_container_width=True):
                            st.session_state.selected_id = song["id"]
                            st.rerun()
                    with b2:
                        if st.button(fav_icon, key=f"fav_{song['id']}", use_container_width=True):
                            if is_fav:
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

        top1, top2 = st.columns([1.2, 1.0])
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
