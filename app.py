import streamlit as st
import yt_dlp

# ১. পেজ কনফিগারেশন
st.set_page_config(
    page_title="SILENT Universal Downloader",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ২. থিম সিলেক্ট ও CSS ইনজেকশন
theme_choice = st.radio("🎨 Theme / থিম সিলেক্ট করুন:", ["Dark Animated", "Light Clean"], horizontal=True)

if theme_choice == "Dark Animated":
    st.markdown("""
    <style>
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #1a1a2e) !important;
        background-size: 400% 400% !important;
        animation: gradient 12s ease infinite !important;
        color: #ffffff !important;
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
    .cat-container {
        text-align: center;
        margin: 15px 0;
        padding: 15px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px dashed #ff94c2;
    }
    .cute-cat {
        font-size: 45px;
        display: inline-block;
        animation: catPlay 1.2s infinite alternate ease-in-out;
    }
    @keyframes catPlay {
        0% { transform: translateY(0) rotate(0deg) scale(1); }
        50% { transform: translateY(-12px) rotate(-10deg) scale(1.1); }
        100% { transform: translateY(0) rotate(10deg) scale(1); }
    }
    .playing-text {
        font-size: 15px;
        font-weight: bold;
        color: #ff94c2;
        margin-top: 5px;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 12px 20px;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .stApp {
        background-color: #f4f7f6 !important;
        color: #333333 !important;
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
    .cat-container {
        text-align: center;
        margin: 15px 0;
        padding: 15px;
        background: rgba(0, 0, 0, 0.05);
        border-radius: 15px;
        border: 1px dashed #ff4b4b;
    }
    .cute-cat {
        font-size: 45px;
        display: inline-block;
        animation: catPlay 1.2s infinite alternate ease-in-out;
    }
    @keyframes catPlay {
        0% { transform: translateY(0) rotate(0deg) scale(1); }
        50% { transform: translateY(-12px) rotate(-10deg) scale(1.1); }
        100% { transform: translateY(0) rotate(10deg) scale(1); }
    }
    .playing-text {
        font-size: 15px;
        font-weight: bold;
        color: #ff4b4b;
        margin-top: 5px;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 12px 20px;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

# ৩. ল্যাঙ্গুয়েজ ডিকশনারি
TEXTS = {
    "bn": {
        "title": "🎬 অল-ইন-ওয়ান সুপার ডাউনলোডার",
        "subtitle": "যেকোনো ওয়েবসাইটের লিঙ্ক পেস্ট করে আপনার পছন্দের কোয়ালিটিতে ভিডিও বা অডিও নামিয়ে নিন।",
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
        st.session_state["selected_q"] = selected_quality

if "target_url" in st.session_state and url_input.strip():
    clean_url = st.session_state["target_url"]
    chosen_q = st.session_state.get("selected_q", selected_quality)
    
    st.markdown("---")
    
    # 🐾 Cute Cat Animation Section
    st.markdown("""
    <div class="cat-container">
        <div class="cute-cat">🐱🐾 🧶</div>
        <div class="playing-text">ক্যাট আপনার ভিডিও প্রসেস করছে... নিচে আপনার ডাউনলোডের বাটনটি তৈরি হচ্ছে! ✨</div>
    </div>
    """, unsafe_allow_html=True)

    # 🟢 High-Res Dynamic Stream Extractor
    with st.spinner("ভিডিও এবং সিলেক্ট করা রেজোলিউশন লিংক এক্সট্র্যাক্ট করা হচ্ছে..."):
        try:
            # রেজোলিউশন ফিল্টার সেটআপ
            if "1080p" in chosen_q:
                fmt = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/best'
            elif "720p" in chosen_q:
                fmt = 'bestvideo[height<=720]+bestaudio/best[height<=720]/best'
            elif "480p" in chosen_q:
                fmt = 'bestvideo[height<=480]+bestaudio/best[height<=480]/best'
            elif "360p" in chosen_q:
                fmt = 'bestvideo[height<=360]+bestaudio/best[height<=360]/best'
            elif "Audio Only" in chosen_q:
                fmt = 'bestaudio/best'
            else:
                fmt = 'best'

            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'format': fmt
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(clean_url, download=False)
                video_title = info.get('title', 'video')
                
                # ডাইরেক্ট ডাউনলোড লিঙ্ক চেক
                direct_stream_url = info.get('url', None)

                if direct_stream_url:
                    st.success(f"🎬 **শিরোনাম:** {video_title}")
                    
                    # ⬇️ In-Site Direct Download Button
                    st.markdown(f'''
                        <a href="{direct_stream_url}" download="{video_title}.mp4" target="_blank" style="text-decoration: none;">
                            <button style="
                                width: 100%;
                                background-color: #28a745;
                                color: white;
                                font-weight: bold;
                                border-radius: 10px;
                                border: none;
                                padding: 16px;
                                font-size: 18px;
                                cursor: pointer;
                                margin-top: 10px;">
                                ⬇️ Download ({chosen_q})
                            </button>
                        </a>
                    ''', unsafe_allow_html=True)
                else:
                    st.error("নির্বাচিত কোয়ালিটির লিঙ্ক এক্সট্র্যাক্ট করা সম্ভব হয়নি। অন্য কোয়ালিটি দিয়ে চেষ্টা করুন।")

        except Exception as e:
            st.error(f"প্রসেস করতে সমস্যা হয়েছে: {str(e)}")

st.markdown("---")
st.markdown('<p style="text-align: center;">SILENT Universal Downloader | Mobile & Desktop Supported</p>', unsafe_allow_html=True)
