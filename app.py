import streamlit as st
import urllib.parse

# ১. পেজ সেটআপ
st.set_page_config(
    page_title="SILENT Universal Downloader",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ২. থিম এবং কিউট ক্যাট অ্যানিমেশন CSS
theme_choice = st.radio("🎨 Theme / থিম সিলেক্ট করুন:", ["Dark Animated", "Light Clean"], horizontal=True)

base_style = """
<style>
/* Cat Animation Container */
.cat-container {
    text-align: center;
    margin: 20px 0;
    padding: 15px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    border: 1px dashed #ff94c2;
}

/* Cute Bouncing Cat Icon */
.cute-cat {
    font-size: 50px;
    display: inline-block;
    animation: catPlay 1.2s infinite alternate ease-in-out;
}

@keyframes catPlay {
    0% {
        transform: translateY(0) rotate(0deg) scale(1);
    }
    50% {
        transform: translateY(-15px) rotate(-10deg) scale(1.1);
    }
    100% {
        transform: translateY(0) rotate(10deg) scale(1);
    }
}

.playing-text {
    font-size: 16px;
    font-weight: bold;
    color: #ff94c2;
    margin-top: 8px;
    animation: blinkText 1.5s infinite;
}

@keyframes blinkText {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
</style>
"""

if theme_choice == "Dark Animated":
    theme_css = base_style + """
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
    theme_css = base_style + """
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
        "select_format": "রেজোলিউশন / কোয়ালিটি বাছাই করুন:",
        "err_empty": "দয়া করে একটি সঠিক লিঙ্ক দিন।"
    },
    "en": {
        "title": "🎬 All-in-One Super Downloader",
        "subtitle": "Paste any video link and download in your preferred resolution easily.",
        "url_label": "Enter Video Link Here:",
        "url_placeholder": "https://www.youtube.com/watch?v=...",
        "fetch_btn": "Process Video 🔍",
        "select_format": "Select Resolution / Quality:",
        "err_empty": "Please enter a valid video link."
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

quality_options = [
    "1080p Full HD (MP4)",
    "720p HD (MP4)",
    "480p SD (MP4)",
    "360p Low (MP4)",
    "Audio Only (MP3)"
]

selected_quality = st.selectbox(t["select_format"], quality_options)

if st.button(t["fetch_btn"]):
    if not url_input.strip():
        st.warning(t["err_empty"])
    else:
        st.session_state["target_url"] = url_input.strip()

if "target_url" in st.session_state and url_input.strip():
    clean_url = st.session_state["target_url"]
    encoded_url = urllib.parse.quote(clean_url)
    
    st.markdown("---")
    
    # 🐾 Cute Cat Animation Section
    st.markdown("""
    <div class="cat-container">
        <div class="cute-cat">🐱🐾 🧶</div>
        <div class="playing-text">ক্যাট আপনার ভিডিও প্রসেস করছে... ডাউনলোড করতে নিচের সার্ভারে ক্লিক করুন! ✨</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 🟢 Download Buttons Section
    cobalt_link = f"https://cobalt.tools/?url={encoded_url}"
    ss_link = clean_url.replace("youtube.com", "ssyoutube.com").replace("youtu.be/", "ssyoutube.com/watch?v=")
    
    embed_html = f"""
    <div style="text-align: center;">
        <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
            <a href="{cobalt_link}" target="_blank" style="text-decoration: none; flex: 1; min-width: 200px;">
                <button style="width: 100%; background: #22c55e; color: white; border: none; padding: 14px; border-radius: 10px; font-weight: bold; font-size: 16px; cursor: pointer; transition: 0.3s;">
                    🚀 Main Server (Direct Fast Stream)
                </button>
            </a>
            <a href="{ss_link}" target="_blank" style="text-decoration: none; flex: 1; min-width: 200px;">
                <button style="width: 100%; background: #3b82f6; color: white; border: none; padding: 14px; border-radius: 10px; font-weight: bold; font-size: 16px; cursor: pointer; transition: 0.3s;">
                    ⚡ Mirror Server (Fallback Download)
                </button>
            </a>
        </div>
    </div>
    """
    
    st.components.v1.html(embed_html, height=80)

st.markdown("---")
st.markdown('<p style="text-align: center;">SILENT Universal Downloader | Mobile & Desktop Supported</p>', unsafe_allow_html=True)
