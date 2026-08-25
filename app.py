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

# ২. ডাইনামিক থিম CSS
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
.stButton>button, .stDownloadButton>button {
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
.stButton>button:hover, .stDownloadButton>button:hover {
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
        "fetching": "ভিডিওর তথ্য প্রসেস করা হচ্ছে...",
        "select_format": "রেজোলিউশন / কোয়ালিটি বাছাই করুন:",
        "download_start": "ডাউনলোড লিঙ্ক তৈরি করুন ⬇️",
        "err_empty": "দয়া করে একটি সঠিক লিঙ্ক দিন।",
        "err_fetch": "ভিডিও প্রসেস করতে ব্যর্থ হয়েছে। লিঙ্কটি রি-চেক করুন।"
    },
    "en": {
        "title": "🎬 All-in-One Super Downloader",
        "subtitle": "Paste any video link and download in your preferred resolution easily.",
        "url_label": "Enter Video Link Here:",
        "url_placeholder": "https://www.youtube.com/watch?v=...",
        "fetch_btn": "Process Video 🔍",
        "fetching": "Processing video info...",
        "select_format": "Select Resolution / Quality:",
        "download_start": "Generate Download Link ⬇️",
        "err_empty": "Please enter a valid video link.",
        "err_fetch": "Failed to process video. Please check the link."
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

url = st.text_input(t["url_label"], placeholder=t["url_placeholder"])

# Cobalt API Integration Function
def fetch_cobalt_download(video_url, quality="1080", is_audio=False):
    api_url = "https://api.cobalt.tools/"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "url": video_url,
        "videoQuality": quality,
        "downloadMode": "audio" if is_audio else "auto"
    }
    
    response = requests.post(api_url, json=payload, headers=headers, timeout=15)
    return response.json()

if st.button(t["fetch_btn"]):
    if not url.strip():
        st.warning(t["err_empty"])
    else:
        st.session_state["valid_url"] = url.strip()

if "valid_url" in st.session_state and st.session_state["valid_url"] == url.strip():
    st.markdown("---")
    
    # রেজোলিউশন অপশন ডিক্লেয়ারেশন
    quality_options = {
        "1080p Full HD (MP4)": "1080",
        "720p HD (MP4)": "720",
        "480p SD (MP4)": "480",
        "360p Low (MP4)": "360",
        "Audio Only (MP3)": "audio"
    }
    
    selected_option = st.selectbox(t["select_format"], list(quality_options.keys()))
    
    if st.button(t["download_start"]):
        with st.spinner(t["fetching"]):
            try:
                selected_val = quality_options[selected_option]
                is_audio = (selected_val == "audio")
                quality_code = "1080" if is_audio else selected_val
                
                res = fetch_cobalt_download(st.session_state["valid_url"], quality=quality_code, is_audio=is_audio)
                
                if res.get("status") in ["tunnel", "redirect"]:
                    download_url = res.get("url")
                    st.success("🎉 আপনার ভিডিও প্রস্তুত!")
                    st.markdown(f'''
                        <a href="{download_url}" target="_blank" style="text-decoration: none;">
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
                                margin-top: 10px;">
                                💾 ফাইলটি সেভ করুন (Click to Download)
                            </button>
                        </a>
                    ''', unsafe_allow_html=True)
                elif res.get("status") == "picker":
                    st.success("🎉 আপনার ভিডিও প্রস্তুত!")
                    for item in res.get("picker", []):
                        st.markdown(f"[⬇️ Download ({item.get('type', 'file')})]({item.get('url')})")
                else:
                    st.error(f"{t['err_fetch']} ({res.get('text', 'Unknown Error')})")
            except Exception as e:
                st.error(f"{t['err_fetch']} {str(e)}")

st.markdown("---")
st.markdown('<p style="text-align: center;">SILENT Universal Downloader | Mobile & Desktop Supported</p>', unsafe_allow_html=True)
