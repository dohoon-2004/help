import re
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="My Song Player", page_icon="🎧", layout="centered")

st.title("🎧 노래 재생")
st.caption("유튜브 링크만 넣으면 선택해서 재생됩니다. (자동재생은 브라우저 정책상 보통 막힙니다.)")

DEFAULT = """https://www.youtube.com/watch?v=UfcAVejslrU
https://youtu.be/dQw4w9WgXcQ
"""

def extract_video_id(url: str) -> str | None:
    url = url.strip()
    if not url:
        return None

    # 1) watch?v=VIDEO_ID
    m = re.search(r"[?&]v=([A-Za-z0-9_-]{6,})", url)
    if m:
        return m.group(1)

    # 2) youtu.be/VIDEO_ID
    m = re.search(r"youtu\.be/([A-Za-z0-9_-]{6,})", url)
    if m:
        return m.group(1)

    # 3) /embed/VIDEO_ID
    m = re.search(r"/embed/([A-Za-z0-9_-]{6,})", url)
    if m:
        return m.group(1)

    return None

def yt_embed(video_id: str, title: str = "YouTube player"):
    src = f"https://www.youtube-nocookie.com/embed/{video_id}?rel=0&controls=1"
    html = f"""
    <div style="position:relative;padding-top:56.25%;border-radius:16px;overflow:hidden;background:#000;">
      <iframe
        src="{src}"
        title="{title}"
        style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"
        allow="encrypted-media; picture-in-picture"
        allowfullscreen
      ></iframe>
    </div>
    """
    components.html(html, height=380)

urls_text = st.text_area("유튜브 링크(줄바꿈으로 여러 개)", value=DEFAULT, height=140)

urls = [u.strip() for u in urls_text.splitlines() if u.strip()]
items = []
for u in urls:
    vid = extract_video_id(u)
    if vid:
        items.append((u, vid))

if not items:
    st.warning("유효한 유튜브 링크가 없습니다. 예: https://www.youtube.com/watch?v=... 또는 https://youtu.be/...")
    st.stop()

labels = [f"{i+1}. {u}" for i, (u, _) in enumerate(items)]
choice = st.selectbox("재생할 곡 선택", labels, index=0)

idx = labels.index(choice)
url, video_id = items[idx]

yt_embed(video_id, title=url)
st.link_button("YouTube에서 열기", url)
