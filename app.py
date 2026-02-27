import math
import random
import streamlit as st
import streamlit.components.v1 as components

# -----------------------------
# 노래 목록 (딱 기본 10곡만 출력)
# -----------------------------
SONGS = [
    {"id": "river-flows-in-you", "title": "River Flows in You", "artist": "Yiruma", "videoId": "7maJOI3QMu0"},
    {"id": "its-time", "title": "It's Time", "artist": "Imagine Dragons", "videoId": "NASqUELHjPE"},
    {"id": "iu-night-letter", "title": "밤편지", "artist": "아이유", "videoId": "EjMTw4xLcBI"},
    {"id": "stronger", "title": "Stronger", "artist": "Kelly Clarkson", "videoId": "Xn676-fLq7I"},
    {"id": "blackpink-ddu-du-ddu-du", "title": "DDU-DU DDU-DU", "artist": "BLACKPINK", "videoId": "IHNzOHi8sJs"},
    {"id": "sia-unstoppable", "title": "Unstoppable", "artist": "Sia", "videoId": "kIjUfXfJjGU"},
    {"id": "iu-blueming", "title": "Blueming", "artist": "아이유", "videoId": "D1PvIWdJ8xo"},
    {"id": "iu-celebrity", "title": "Celebrity", "artist": "아이유", "videoId": "0-q1KafFCLU"},
    {"id": "akmu-200-percent", "title": "200%", "artist": "AKMU", "videoId": "0Oi8jDMvd_w"},
    {"id": "bol4-hug", "title": "Hug", "artist": "볼빨간사춘기", "videoId": "qfeoX17dav0"},
    {"id": "panic-high-hopes", "title": "High Hopes", "artist": "Panic! At The Disco", "videoId": "IPXIgEAGe4U"},
    {"id": "fall-out-boy-immortals", "title": "Immortals", "artist": "Fall Out Boy", "videoId": "Y4o_8zbelwY"},
    {"id": "alice-merton-no-roots", "title": "No Roots", "artist": "Alice Merton", "videoId": "PUdyuKaGQd4"},
    {"id": "gaho-start", "title": "Start (시작)", "artist": "Gaho (가호)", "videoId": "kjYW63CVbsE"},
    {"id": "eddy-kim-ippudanikka", "title": "이쁘다니까", "artist": "Eddy Kim(에디킴)", "videoId": "hvq5Q9yaCfo"},
    {"id": "loveholics-butterfly", "title": "Butterfly", "artist": "러브홀릭스(Loveholics)", "videoId": "U93tNuQuREo"},
    {"id": "koyote-our-dream", "title": "우리의 꿈", "artist": "코요태(Koyote)", "videoId": "zfP4Gh8Kquo"},
    {"id": "turtles-airplane", "title": "비행기", "artist": "거북이(Turtles)", "videoId": "yCzg389Ut6w"},
    {"id": "onerepublic-i-aint-worried", "title": "I Ain't Worried", "artist": "OneRepublic", "videoId": "INak4ORss18"},
    {"id": "lizzo-juice", "title": "Juice", "artist": "Lizzo", "videoId": "hqL9MD2sDRw"},
    {"id": "justin-timberlake-cant-stop-the-feeling", "title": "Can't Stop the Feeling!", "artist": "Justin Timberlake", "videoId": "0Ui-QzihJGo"},
    {"id": "zico-soulmate", "title": "SoulMate (Feat. 아이유)", "artist": "지코(ZICO) ft. 아이유(IU)", "videoId": "Vl1kO9hObpA"},
    {"id": "akmu-tictoc-tictoc-tictoc", "title": "째깍 째깍 째깍 (with Beenzino)", "artist": "AKMU(악동뮤지션)", "videoId": "VkMs8P1YYNs"},

]

HEADLINES = ["진짜 사랑해", "고마워", "옆에 있어줘", "덕분에 행복해", "안아줄게", "맛있는 거 먹자", "바다보러 갈래?"]

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
    # 모바일 공백 최소화
    components.html(html, height=190)

st.set_page_config(page_title="player", page_icon="🎧", layout="wide")

# 맨 위로 스크롤
if st.session_state.get("scroll_to_top"):
    components.html("<script>window.parent.scrollTo({top: 0, behavior: 'smooth'});</script>", height=0, width=0)
    st.session_state.scroll_to_top = False

# -----------------------------
# CSS 
# -----------------------------
st.markdown(
    """
<style>
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v3.2.1/dist/web/static/pretendard.css");

/* Streamlit 기본 UI 숨김 */
#MainMenu, footer, header, .stAppDeployButton, [data-testid="stToolbar"], [data-testid="stHeader"] {
  display: none !important;
}

/* 폰트 */
* {
  font-family: "Pretendard", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans KR", Arial, sans-serif !important;
  -webkit-font-smoothing: antialiased !important;
  -moz-osx-font-smoothing: grayscale !important;
  text-rendering: optimizeLegibility !important;
}
html, body { -webkit-text-size-adjust: 100%; text-size-adjust: 100%; }

/* =========================================================
   ✅ 핑크 팔레트 + (글귀/나머지 텍스트) 색 분리
   ========================================================= */
:root{
  color-scheme: light;

  --bg: #ffffff;
  --card: #fff5fb;
  --border: #ffd0e8;

  /* 기본 텍스트(검정X): 플럼/퍼플 계열 */
  --text: #5a2b5f;
  --muted: #a65b93;

  /* 글귀(HEADLINE) 전용: 더 쨍한 핑크 */
  --headline: #ff2d8b;

  /* 제목(곡명) 전용: 또 다른 톤 */
  --title: #7a1b6a;

  --shadow: 0 12px 34px rgba(0,0,0,0.12);

  --song-grad: linear-gradient(135deg, #ff4fa3, #ff2d8b);
  --page-grad: linear-gradient(135deg, #ff4fa3, #ff2d8b);
}

@media (prefers-color-scheme: dark) {
  :root{
    color-scheme: dark;
    --bg: #0f1014;
    --card: #1b1520;
    --border: #3a2346;

    --text: #ffd7ee;     /* 연핑크 라이트 텍스트 */
    --muted: #e6a6cf;
    --headline: #ff4fa3; /* 다크에서도 쨍한 핑크 */
    --title: #ffb6df;

    --shadow: 0 12px 34px rgba(0,0,0,0.35);
  }
}

/* Streamlit 다크 DOM에도 강제 */
[data-theme="dark"], html.dark, body.dark, .stApp.dark {
  --bg: #0f1014 !important;
  --card: #1b1520 !important;
  --border: #3a2346 !important;
  --text: #ffd7ee !important;
  --muted: #e6a6cf !important;
  --headline: #ff4fa3 !important;
  --title: #ffb6df !important;
}

/* 전역 */
html, body, .stApp, [data-testid="stAppViewContainer"], .block-container{
  background: var(--bg) !important;
  color: var(--text) !important;
}
p, span, label, small, li, div,
h1, h2, h3, h4, h5, h6,
.stMarkdown, .stMarkdown p {
  color: var(--text) !important;
  -webkit-text-fill-color: var(--text) !important;
}

.block-container{
  padding-top: 0.2rem !important;
  padding-bottom: 0.6rem !important;
  max-width: 1200px;
}

/* 글귀 */
.headline{
  font-size: clamp(1.6rem, 5vw, 2.0rem) !important;
  font-weight: 900;
  letter-spacing: -0.6px;
  margin: 0.15rem 0 1.0rem 0 !important;
  text-align: center !important;
  color: var(--headline) !important;
}

/* 유튜브 */
.yt-wrap{
  position: relative;
  padding-top: 56.25%;
  border-radius: 18px;
  overflow: hidden;
  background: #000;
  box-shadow: var(--shadow) !important;
}
.yt-wrap iframe{ position:absolute; inset:0; width:100%; height:100%; border:0; }

/* 플레이어 아래 제목/가수 */
div[data-testid="stIFrame"]{
  margin-bottom: -18px !important;
  padding-bottom: 0 !important;
}
.song-info{
  margin-top: -0.75rem !important;
  margin-bottom: 1.1rem !important;
  padding-left: 10px !important;
}
.song-title{
  font-size: clamp(1.25rem, 3.6vw, 1.5rem) !important;
  font-weight: 850;
  margin:0 !important;
  line-height: 1.08 !important;
  color: var(--title) !important;
}
.song-artist{
  font-size: clamp(1.05rem, 3.2vw, 1.25rem) !important;
  font-weight: 650;
  margin:0.02rem 0 0 0 !important;
  line-height: 1.08 !important;
  color: var(--muted) !important;
}

/* 노래 목록 버튼 */
div[data-testid="stButton"] > button {
  width: 100%;
  text-align: center;
  border-radius: 16px !important;
  padding: 16px 20px !important;
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  box-shadow: 0 4px 10px rgba(0,0,0,0.03) !important;
  white-space: pre-wrap !important;
  transition: all 0.15s;
  font-size: clamp(0.9rem, 2.8vw, 0.95rem) !important;
  font-weight: 650;
}
div[data-testid="stButton"] > button p { color: var(--muted) !important; }
div[data-testid="stButton"] > button::first-line,
div[data-testid="stButton"] > button p::first-line {
  font-size: clamp(1.05rem, 3.2vw, 1.25rem) !important;
  font-weight: 900 !important;
  color: var(--title) !important;
}
div[data-testid="stButton"] > button[kind="primary"] {
  background: var(--song-grad) !important;
  border: none !important;
  box-shadow: 0 10px 22px rgba(255,45,139,0.22) !important;
}
div[data-testid="stButton"] > button[kind="primary"] * {
  color: #ffffff !important;
  -webkit-text-fill-color: #ffffff !important;
}

/* =========================================================
   ✅ 페이지네이션 및 숫자 버튼
   ========================================================= */
div[data-testid="stRadio"] {
  margin-top: 4px !important;
  margin-bottom: 60px !important; /* 하단 넉넉한 여백 */
}

div[data-testid="stRadio"] > label {
  display: none !important;
}

div[data-testid="stRadio"] [role="radiogroup"] {
  display: flex !important;
  flex-direction: row !important;
  justify-content: center !important;
  align-items: center !important;
  gap: 12px !important;
  flex-wrap: nowrap !important;
  width: 100% !important;
  margin: 0 !important;
  padding-left: 12px !important;
  padding-right: 12px !important;
  box-sizing: border-box !important;
}

div[data-testid="stRadio"] [role="radiogroup"] label {
  width: 48px !important;
  height: 48px !important;
  margin: 0 !important;
  padding: 0 !important;
  display: inline-flex !important;
  position: relative !important;
  cursor: pointer !important;
  background: transparent !important;
  border: none !important;
}

div[data-testid="stRadio"] [role="radiogroup"] label > div:first-of-type {
  display: none !important;
}

div[data-testid="stRadio"] [role="radiogroup"] input[type="radio"] {
  position: absolute !important;
  inset: 0 !important;
  width: 100% !important;
  height: 100% !important;
  opacity: 0 !important;
  margin: 0 !important;
  z-index: 10 !important;
  cursor: pointer !important;
}

div[data-testid="stRadio"] [role="radiogroup"] label > div:last-child {
  position: absolute !important;
  inset: 0 !important;
  width: 100% !important;
  height: 100% !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  border-radius: 999px !important;
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  box-sizing: border-box !important;
  transition: all 0.18s !important;
}

div[data-testid="stRadio"] [role="radiogroup"] label > div:last-child > div,
div[data-testid="stRadio"] [role="radiogroup"] label [data-testid="stMarkdownContainer"] {
  width: 100% !important;
  height: 100% !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  margin: 0 !important;
  padding: 0 !important;
}

div[data-testid="stRadio"] [role="radiogroup"] label p {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 100% !important;
  height: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  line-height: 1 !important;
  text-align: center !important;
  font-size: 1.15rem !important;
  font-weight: 900 !important;
  color: var(--title) !important;
}

div[data-testid="stRadio"] [role="radiogroup"] input[type="radio"]:checked ~ div:last-child {
  background: var(--page-grad) !important;
  border: none !important;
  box-shadow: 0 10px 22px rgba(255,45,139,0.22) !important;
}
div[data-testid="stRadio"] [role="radiogroup"] input[type="radio"]:checked ~ div:last-child p {
  color: #ffffff !important;
  -webkit-text-fill-color: #ffffff !important;
}

@media (max-width: 520px) {
  .block-container{ padding-left: 0.8rem !important; padding-right: 0.8rem !important; }
  div[data-testid="stIFrame"]{ margin-bottom: -20px !important; }
  .song-info{ margin-top: -0.85rem !important; margin-bottom: 0.95rem !important; padding-left: 8px !important; }
  div[data-testid="stRadio"] { margin-bottom: 50px !important; }
}
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# 상태
# -----------------------------
if "selected_id" not in st.session_state:
    st.session_state.selected_id = SONGS[0]["id"] if SONGS else None
if "headline" not in st.session_state:
    st.session_state.headline = random.choice(HEADLINES)
if "page" not in st.session_state:
    st.session_state.page = 0

st.markdown(f"<div class='headline'>{st.session_state.headline}</div>", unsafe_allow_html=True)

player_col, list_col = st.columns([1.08, 1.0], gap="large")

with player_col:
    current = next((s for s in SONGS if s["id"] == st.session_state.selected_id), None)
    if current:
        yt_embed(current["videoId"], current["title"])
        st.markdown(
            f"""
            <div class="song-info">
              <div class="song-title">{current['title']}</div>
              <div class="song-artist">{current['artist']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

with list_col:
    ITEMS_PER_PAGE = 5
    total_pages = max(1, math.ceil(len(SONGS) / ITEMS_PER_PAGE))

    start_idx = st.session_state.page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    current_songs = SONGS[start_idx:end_idx]

    # 노래 목록
    for song in current_songs:
        is_selected = (song["id"] == st.session_state.selected_id)
        btn_type = "primary" if is_selected else "secondary"

        if st.button(
            f"{song['title']}\n{song['artist']}",
            key=f"song_{song['id']}",
            use_container_width=True,
            type=btn_type
        ):
            st.session_state.selected_id = song["id"]
            st.session_state.headline = random.choice(HEADLINES)
            st.session_state.scroll_to_top = True
            st.rerun()

    # 페이지네이션
    MAX_VISIBLE_BUTTONS = 5
    half_window = MAX_VISIBLE_BUTTONS // 2

    start_page = max(0, st.session_state.page - half_window)
    end_page = min(total_pages, start_page + MAX_VISIBLE_BUTTONS)
    start_page = max(0, end_page - MAX_VISIBLE_BUTTONS)

    visible_pages = list(range(start_page, end_page))
    labels = [str(p + 1) for p in visible_pages]

    current_label = str(st.session_state.page + 1)
    if current_label not in labels:
        current_label = labels[0] if labels else "1"

    chosen = st.radio(
        label="",
        options=labels,
        index=labels.index(current_label) if labels else 0,
        horizontal=True,
        label_visibility="collapsed",
        key="pager_radio",
    )

    if labels:
        new_page = int(chosen) - 1
        if new_page != st.session_state.page:
            st.session_state.page = new_page
            st.session_state.headline = random.choice(HEADLINES)
            st.session_state.scroll_to_top = True
            st.rerun()
