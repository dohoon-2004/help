import streamlit as st
import streamlit.components.v1 as components

# -----------------------------
# 노래 목록(✅ 기본값: River Flows in You)
# -----------------------------
SONGS = [
    {"id": "river-flows-in-you", "title": "River Flows in You", "artist": "Yiruma", "videoId": "7maJOI3QMu0"},
    # 필요하면 여기 아래로 계속 추가하세요:
    # {"id": "new", "title": "노래제목", "artist": "가수", "videoId": "유튜브_VIDEO_ID"},
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
    # ✅ 플레이어 사이즈 "정말 조금" 키움
    components.html(html, height=380)

def heart_icon(is_fav: bool) -> str:
    return "🩷" if is_fav else "🤍"

def check_icon(is_selected: bool) -> str:
    return "✅" if is_selected else "☐"

# -----------------------------
# 페이지 설정 + 스타일
# -----------------------------
st.set_page_config(page_title="player", page_icon="🎧", layout="wide")

st.markdown(
    """
<style>
/* 기본 UI 숨김 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* 배경/레이아웃 */
[data-testid="stAppViewContainer"] { background: #f7f7fb; }
.block-container { padding-top: 1.4rem; padding-bottom: 1.1rem; max-width: 1200px; }
div[data-testid="stVerticalBlock"]{ gap: 0.40rem; }

/* 카드 느낌 */
div[data-testid="stVerticalBlockBorderWrapper"]{
  border-radius: 18px !important;
  background: #ffffff !important;
  border: 1px solid rgba(0,0,0,0.06) !important;
  box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
}

/* 플레이어 */
.yt-wrap{
  position: relative;
  padding-top: 56.25%;
  border-radius: 18px;
  overflow: hidden;
  background: #000;
  box-shadow: 0 12px 34px rgba(0,0,0,0.10);
  margin-bottom: 0;   /* 아래 여백 제거 */
}
.yt-wrap iframe{
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  border: 0;
}

/* 버튼 */
.stButton button{
  border-radius: 12px;
  padding: 0.55rem 0.85rem;
  white-space: nowrap;
}

/* 텍스트(가수 이름 더 크게) */
.player-title { font-size: 1.55rem; font-weight: 850; letter-spacing: -0.3px; margin: 0; }
.player-artist { font-size: 1.35rem; font-weight: 800; color: rgba(0,0,0,0.70); margin-top: 0.10rem; }

.list-title { font-size: 1.05rem; font-weight: 800; margin: 0; }
.list-artist { font-size: 1.05rem; font-weight: 750; color: rgba(0,0,0,0.62); margin-top: 0.10rem; }

/* 액션(체크/하트) 가운데 정렬 */
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

# -----------------------------
# 상태(선택곡 / 즐겨찾기)
# -----------------------------
if "selected_id" not in st.session_state:
    st.session_state.selected_id = SONGS[0]["id"] if SONGS else None

if "favorites" not in st.session_state:
    st.session_state.favorites = set()

# -----------------------------
# 레이아웃 (재생 왼쪽 / 목록 오른쪽)
# -----------------------------
player_col, list_col = st.columns([1.08, 1.0], gap="large")

# ---- 왼쪽: 재생 ----
with player_col:
    current = next((s for s in SONGS if s["id"] == st.session_state.selected_id), None)
    if current:
        is_fav = (current["id"] in st.session_state.favorites)

        t1, t2 = st.columns([0.88, 0.12], gap="small")
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

# ---- 오른쪽: 목록(썸네일 없음, 문구 없음) ----
with list_col:
    if not SONGS:
        st.info("SONGS에 노래를 추가해 주세요.")
    else:
        for song in SONGS:
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
