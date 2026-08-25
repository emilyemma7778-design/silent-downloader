import streamlit as st
import yt_dlp
import os
import glob
import tempfile

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

# ৩. কুকিজ হ্যান্ডলিং (Streamlit Secrets অথবা cookies.txt থেকে)
cookie_path = None
if "YOUTUBE_COOKIES" in st.secrets:
    temp_cookie = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
    temp_cookie.write(st.secrets["YOUTUBE_COOKIES"])
    temp_cookie.close()
    cookie_path = temp_cookie.name
elif os.path.exists("cookies.txt"):
    cookie_path = "cookies.txt"

# ৪. মাল্টি-ল্যাঙ্গুয়েজ টেক্সট
TEXTS = {
    "bn": {
        "title": "🎬 অল-ইন-ওয়ান সুপার ডাউনলোডার",
        "subtitle": "যেকোনো ওয়েবসাইটের লিঙ্ক পেস্ট করে আপনার পছন্দের কোয়ালিটিতে ভিডিও নামিয়ে নিন।",
        "url_label": "ভিডিও লিঙ্কটি এখানে দিন:",
        "url_placeholder": "https://www.youtube.com/watch?v=...",
        "fetch_btn": "ভিডিও প্রসেস করুন 🔍",
        "fetching": "ভিডিওর তথ্য আনা হচ্ছে... একটু অপেক্ষা করুন।",
        "select_format": "রেজোলিউশন / কোয়ালিটি বাছাই করুন:",
        "download_start": "ডাউনলোড শুরু করুন ⬇️",
        "downloading": "ভিডিও প্রসেসিং ও ডাউনলোড চলছে...",
        "success": "ডাউনলোড প্রস্তুত!",
        "download_file_btn": "💾 ফাইলটি সেভ করুন (Save File)",
        "err_empty": "দয়া করে একটি সঠিক লিঙ্ক দিন।",
        "err_fetch": "ভিডিওর তথ্য পাওয়া যায়নি: ",
        "err_dl": "ডাউনলোড ব্যর্থ হয়েছে: "
    },
    "en": {
        "title": "🎬 All-in-One Super Downloader",
        "subtitle": "Paste any video link and download in your preferred resolution easily.",
        "url_label": "Enter Video Link Here:",
        "url_placeholder": "https://www.youtube.com/watch?v=...",
        "fetch_btn": "Process Video 🔍",
        "fetching": "Fetching video info... Please wait.",
        "select_format": "Select Resolution / Quality:",
        "download_start": "Start Download ⬇️",
        "downloading": "Processing download... Please wait.",
        "success": "Download Ready!",
        "download_file_btn": "💾 Save File to Device",
        "err_empty": "Please enter a valid video link.",
        "err_fetch": "Could not fetch video info: ",
        "err_dl": "Download failed: "
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

if 'video_info' not in st.session_state:
    st.session_state.video_info = None
if 'video_url' not in st.session_state:
    st.session_state.video_url = ""

# 🟢 ইউটিউব ডিটেকশন ও ক্লায়েন্ট বাইপাস কনফিগারেশন
COMMON_YDL_OPTS = {
    'quiet': True,
    'nocheckcertificate': True,
    'no_warnings': True,
    'noplaylist': True,
    'ignoreerrors': True,
    'geo_bypass': True,
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    },
    'extractor_args': {
        'youtube': {
            'player_client': ['android', 'ios'],
            'player_skip': ['webpage', 'configs'],
        }
    }
}

if cookie_path:
    COMMON_YDL_OPTS['cookiefile'] = cookie_path

# ৫. ভিডিও তথ্য সংগ্রহ
if st.button(t["fetch_btn"]):
    if not url.strip():
        st.warning(t["err_empty"])
    else:
        with st.spinner(t["fetching"]):
            try:
                # লিঙ্ক ক্লিন-আপ
                clean_url = url.split("?si=")[0].split("&si=")[0]
                
                ydl_opts = COMMON_YDL_OPTS.copy()
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(clean_url, download=False)
                    st.session_state.video_info = info
                    st.session_state.video_url = url
            except Exception as e:
                st.error(f"{t['err_fetch']} {str(e)}")

# ৬. রেজোলিউশন ও ডাউনলোড হ্যান্ডলিং
if st.session_state.video_info and st.session_state.video_url == url:
    info = st.session_state.video_info
    title = info.get('title', 'Video')
    thumbnail = info.get('thumbnail')

    st.markdown("---")
    st.subheader(f"📹 {title}")
    if thumbnail:
        st.image(thumbnail, width="stretch")

    formats = info.get('formats', [])
    options = {"Audio Only (MP3)": "bestaudio/best"}
    
    height_map = {}
    for f in formats:
        h = f.get('height')
        ext = f.get('ext', '')
        vcodec = f.get('vcodec', 'none')
        
        if h and isinstance(h, int) and ext != 'mhtml' and vcodec != 'none':
            if h not in height_map:
                height_map[h] = f

    sorted_heights = sorted(list(height_map.keys()), reverse=True)

    if sorted_heights:
        for h in sorted_heights:
            res_str = f"{h}p (mp4)"
            options[res_str] = f"bestvideo[height<={h}]+bestaudio/best[height<={h}]/best"
    else:
        options["Best Quality Available"] = "bestvideo+bestaudio/best"

    selected_res = st.selectbox(t["select_format"], list(options.keys()))

    if st.button(t["download_start"]):
        with st.spinner(t["downloading"]):
            try:
                for old_file in glob.glob("dl_file*"):
                    try:
                        os.remove(old_file)
                    except:
                        pass

                clean_url = url.split("?si=")[0].split("&si=")[0]
                outtmpl = 'dl_file.%(ext)s'
                ydl_opts = COMMON_YDL_OPTS.copy()
                ydl_opts['outtmpl'] = outtmpl

                if selected_res == "Audio Only (MP3)":
                    ydl_opts['format'] = 'bestaudio/best'
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                else:
                    ydl_opts['format'] = options[selected_res]
                    ydl_opts['merge_output_format'] = 'mp4'

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([clean_url])

                downloaded_files = glob.glob("dl_file*")
                if downloaded_files:
                    file_path = downloaded_files[0]
                    file_ext = file_path.split('.')[-1]

                    with open(file_path, "rb") as file:
                        st.success(t["success"])
                        st.download_button(
                            label=t["download_file_btn"],
                            data=file,
                            file_name=f"{title}.{file_ext}",
                            mime=f"video/{file_ext}" if file_ext != "mp3" else "audio/mp3"
                        )
            except Exception as e:
                st.error(f"{t['err_dl']} {str(e)}")

st.markdown("---")
st.markdown('<p style="text-align: center;">SILENT Universal Downloader | Mobile & Desktop Supported</p>', unsafe_allow_html=True)
