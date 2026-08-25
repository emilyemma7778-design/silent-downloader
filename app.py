import streamlit as st
import requests
import re

# ১. পেজ সেটআপ
st.set_page_config(
    page_title="SILENT Universal Downloader",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ২. থিম CSS
theme_choice = st.radio("🎨 Theme / থিম সিলেক্ট করুন:", ["Dark Animated", "Light Clean"], horizontal=True)

if theme_choice == "Dark Animated":
    theme_css = """
    <style>
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #1a1a2e);
        background-size: 400% 400%;
        animation: gradient 12s ease infinite;
        color: #ffffff;
    }
    h1, h2, h3, p, label, .stMarkdown { color: #ffffff !important; }
    .builder-name {
        background-color: rgba(255, 215, 0, 0.15);
        padding: 10px;
        border-radius: 12px;
        font-weight: bold;
        color: #ffd700 !important;
        font-size: 20px;
        text-align: center;
        border: 2px solid #ffd700;
        margin-bottom: 20px;
    }
    </style>
    """
else:
    theme_css = """
    <style>
    .stApp {
        background-color: #f4f7f6;
        color: #333333;
    }
    h1, h2, h3, p, label, .stMarkdown { color: #2c3e50 !important; }
    .builder-name {
        background-color: #eef2f5;
        padding: 10px;
        border-radius: 12px;
        font-weight: bold;
        color: #d35400 !important;
        font-size: 20px;
        text-align: center;
        border: 2px solid #d35400;
        margin-bottom: 20px;
    }
    </style>
    """

st.markdown(theme_css, unsafe_allow_html=True)

st.markdown("""
<style>
.stButton>button {
    width: 100%;
    background-color: #ff4b4b;
    color: white;
    font-weight: bold;
    border-radius: 10px;
    border: none;
    padding: 12px 20px;
    font-size: 16px;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background-color: #ff6b6b;
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

# ৩. ল্যাঙ্গুয়েজ টেক্সট
TEXTS = {
    "bn": {
        "title": "🎬 অল-ইন-ওয়ান সুপার ডাউনলোডার",
        "subtitle": "যেকোনো ওয়েবসাইটের লিঙ্ক পেস্ট করে আপনার পছন্দের কোয়ালিটিতে ভিডিও নামিয়ে নিন।",
        "url_label": "ভিডিও লিঙ্কটি এখানে দিন:",
        "url_placeholder": "https://www.youtube.com/watch?v=...",
        "fetch_btn": "ভিডিও প্রসেস করুন 🔍",
        "fetching": "ভিডিওর লিঙ্ক প্রসেস করা হচ্ছে...",
        "select_format": "রেজোলিউশন / কোয়ালিটি বাছাই করুন:",
        "download_start": "ডাউনলোড লিঙ্ক তৈরি করুন ⬇️",
        "err_empty": "দয়া করে একটি সঠিক লিঙ্ক দিন।",
        "err_fetch": "ভিডিও স্ট্রিম লিঙ্ক এক্সট্র্যাক্ট করা সম্ভব হয়নি।"
    },
    "en": {
        "title": "🎬 All-in-One Super Downloader",
        "subtitle": "Paste any video link and download in your preferred resolution easily.",
        "url_label": "Enter Video Link Here:",
        "url_placeholder": "https://www.youtube.com/watch?v=...",
        "fetch_btn": "Process Video 🔍",
        "fetching": "Processing video link...",
        "select_format": "Select Resolution / Quality:",
        "download_start": "Generate Download Link ⬇️",
        "err_empty": "Please enter a valid video link.",
        "err_fetch": "Failed to extract video stream link."
    }
}

col1, col2 = st.columns([3, 1])
with col2:
    lang = st.selectbox("🌐 Language", ["বাংলা", "English"])
    lang_code = "bn" if lang == "বাংলা" else "en"

t = TEXTS[lang_code]

st.title(t["title"])
st.markdown('<div class="builder-name">✨ Made by SILENT ✨</div>', unsafe_allow_html=True)
st.write(t["subtitle"])

url_input = st.text_input(t["url_label"], placeholder=t["url_placeholder"])

def extract_youtube_id(url):
    regex = r"(?:v=|\/([0-9A-Za-z_-]{11})|youtu\.be\/|\/embed\/|\/v\/|\/e\/|watch\?v=|\?v=)([^#\&\?]*)"
    match = re.search(regex, url)
    if match:
        return match.group(1) if match.group(1) else match.group(2)
    return None

def get_piped_streams(video_id):
    instances = [
        "https://pipedapi.kavin.rocks",
        "https://api.piped.private.coffee",
        "https://piped-api.garudalinux.org"
    ]
    for instance in instances:
        try:
            res = requests.get(f"{instance}/streams/{video_id}", timeout=5)
            if res.status_code == 200:
                return res.json()
        except Exception:
            continue
    return None

if st.button(t["fetch_btn"]):
    if not url_input.strip():
        st.warning(t["err_empty"])
    else:
        v_id = extract_youtube_id(url_input.strip())
        if v_id:
            with st.spinner(t["fetching"]):
                data = get_piped_streams(v_id)
                if data:
                    st.session_state["stream_data"] = data
                    st.session_state["active_url"] = url_input.strip()
                else:
                    st.error(t["err_fetch"])
        else:
            st.error(t["err_empty"])

if "stream_data" in st.session_state and st.session_state.get("active_url") == url_input.strip():
    data = st.session_state["stream_data"]
    title = data.get("title", "YouTube Video")
    
    st.markdown("---")
    st.subheader(f"📹 {title}")
    
    video_streams = data.get("videoStreams", [])
    audio_streams = data.get("audioStreams", [])
    
    options = {}
    
    # MP4 সোর্স ফিল্টার
    for s in video_streams:
        if s.get("format") == "MPEG_4" or s.get("mimeType") == "video/mp4":
            quality = s.get("quality", "Video")
            url = s.get("url")
            if url and quality not in options:
                options[f"{quality} (MP4)"] = url
                
    for a in audio_streams:
        if "audio/mp4" in a.get("mimeType", "") or "audio/webm" in a.get("mimeType", ""):
            url = a.get("url")
            if url:
                options["Audio Only (MP3/M4A)"] = url
                break

    if not options:
        # Fallback to direct streams
        for s in video_streams:
            quality = s.get("quality", "Video")
            url = s.get("url")
            if url:
                options[f"{quality}"] = url

    selected_label = st.selectbox(t["select_format"], list(options.keys()))
    
    if selected_label:
        dl_url = options[selected_label]
        st.markdown(f'''
            <a href="{dl_url}" target="_blank" download style="text-decoration: none;">
                <button style="
                    width: 100%;
                    background-color: #28a745;
                    color: white;
                    font-weight: bold;
                    border-radius: 10px;
                    border: none;
                    padding: 14px 20px;
                    font-size: 18px;
                    cursor: pointer;
                    margin-top: 15px;">
                    💾 ফাইলটি ডাউনলোড করুন (Direct Link)
                </button>
            </a>
        ''', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<p style="text-align: center;">SILENT Universal Downloader | Mobile & Desktop Supported</p>', unsafe_allow_html=True)
