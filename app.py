import streamlit as st
import yt_dlp
import os
import tempfile

# ১. পেজ কনফিগারেশন
st.set_page_config(
    page_title="SILENT Universal Downloader",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ২. ডাইনামিক কুকি ফাইল হ্যান্ডলার (Streamlit Secrets থেকে তৈরি)
COOKIE_FILE_PATH = None
if "YOUTUBE_COOKIES" in st.secrets:
    COOKIE_FILE_PATH = os.path.join(tempfile.gettempdir(), "streamlit_yt_cookies.txt")
    with open(COOKIE_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(st.secrets["YOUTUBE_COOKIES"])

# ৩. থিম সেটআপ ও UI Styling
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

# ৪. মেইন অ্যাপ হেডার
st.title("🎬 অল-ইন-ওয়ান সুপার ডাউনলোডার")
st.markdown('<div class="builder-name">✨ Made by SILENT ✨</div>', unsafe_allow_html=True)

url_input = st.text_input("ভিডিও লিঙ্কটি এখানে দিন:", placeholder="https://www.youtube.com/watch?v=...")

quality_options = [
    "1080p Full HD (MP4)",
    "720p HD (MP4)",
    "480p SD (MP4)",
    "360p Low (MP4)",
    "Audio Only (MP3)"
]

selected_quality = st.selectbox("রেজোলিউশন / কোয়ালিটি বাছাই করুন:", quality_options)

if st.button("ভিডিও প্রসেস করুন 🔍"):
    if not url_input.strip():
        st.warning("দয়া করে একটি সঠিক লিঙ্ক দিন।")
    else:
        st.session_state["target_url"] = url_input.strip()
        st.session_state["selected_q"] = selected_quality

# ৫. ডাউনলোড প্রসেসিং লজিক
if "target_url" in st.session_state and url_input.strip():
    clean_url = st.session_state["target_url"]
    chosen_q = st.session_state.get("selected_q", selected_quality)
    
    st.markdown("---")
    st.markdown("""
    <div class="cat-container">
        <div class="cute-cat">🐱🐾 🧶</div>
        <div class="playing-text">ক্যাট আপনার ভিডিও প্রসেস করছে... ফাইল প্রস্তুত করা হচ্ছে! ✨</div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("ভিডিও ডাউনলোড এবং প্রসেস করা হচ্ছে..."):
        try:
            temp_dir = tempfile.gettempdir()
            out_template = os.path.join(temp_dir, '%(title)s.%(ext)s')

            # ফরম্যাট নির্বাচন
            if "1080p" in chosen_q:
                fmt = 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]/best'
            elif "720p" in chosen_q:
                fmt = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]/best'
            elif "480p" in chosen_q:
                fmt = 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]/best'
            elif "360p" in chosen_q:
                fmt = 'bestvideo[height<=360][ext=mp4]+bestaudio/best[height<=360]/best'
            elif "Audio Only" in chosen_q:
                fmt = 'bestaudio/best'
            else:
                fmt = 'best'

            ydl_opts = {
                'format': fmt,
                'outtmpl': out_template,
                'quiet': True,
                'no_warnings': True,
                'nocheckcertificate': True,
                # 🔥 YouTube Security Bypass Options
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web'],
                        'skip': ['hls', 'dash']
                    }
                }
            }

            # Secrets থেকে তৈরি কুকি ফাইল থাকলে তা যুক্ত করা
            if COOKIE_FILE_PATH and os.path.exists(COOKIE_FILE_PATH):
                ydl_opts['cookiefile'] = COOKIE_FILE_PATH

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(clean_url, download=True)
                file_path = ydl.prepare_filename(info)
                title = info.get('title', 'video')

                if os.path.exists(file_path):
                    with open(file_path, "rb") as file_data:
                        file_bytes = file_data.read()
                        
                    st.success(f"🎬 **শিরোনাম:** {title}")
                    
                    ext = "mp3" if "Audio Only" in chosen_q else "mp4"
                    mime_type = "audio/mp3" if "Audio Only" in chosen_q else "video/mp4"
                    
                    st.download_button(
                        label=f"⬇️ Direct Download ({chosen_q})",
                        data=file_bytes,
                        file_name=f"{title}.{ext}",
                        mime=mime_type,
                        use_container_width=True
                    )
                    
                    # প্রসেস শেষে টেম্প ফাইল ডিলিট
                    try:
                        os.remove(file_path)
                    except Exception:
                        pass
                else:
                    st.error("ফাইল তৈরি করতে সমস্যা হয়েছে। অন্য একটি কোয়ালিটি চেষ্টা করুন।")

        except Exception as e:
            st.error(f"প্রসেস করতে সমস্যা হয়েছে: {str(e)}")

st.markdown("---")
st.markdown('<p style="text-align: center;">SILENT Universal Downloader | Mobile & Desktop Supported</p>', unsafe_allow_html=True)
