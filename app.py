import streamlit as st
import requests

# ১. পেজ কনফিগারেশন
st.set_page_config(
    page_title="SILENT Universal Downloader",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ২. থিম সেটআপ ও CSS
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

# ৩. ল্যাঙ্গুয়েজ অপশন
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
    "1080p Full HD",
    "720p HD",
    "480p SD",
    "360p Low",
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
    
    st.markdown("""
    <div class="cat-container">
        <div class="cute-cat">🐱🐾 🧶</div>
        <div class="playing-text">ক্যাট আপনার ভিডিও লিঙ্ক প্রস্তুত করেছে! নিচে ডাইরেক্ট ডাউনলোড করুন ✨</div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("লিঙ্ক প্রসেস করা হচ্ছে..."):
        try:
            # Cobalt API Payload Setup
            quality_map = {
                "1080p Full HD": "1080",
                "720p HD": "720",
                "480p SD": "480",
                "360p Low": "360"
            }
            
            payload = {"url": clean_url}
            
            if "Audio Only" in chosen_q:
                payload["downloadMode"] = "audio"
                payload["audioFormat"] = "mp3"
            else:
                payload["videoQuality"] = quality_map.get(chosen_q, "720")

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            res = requests.post("https://api.cobalt.tools/api/json", json=payload, headers=headers, timeout=15)
            data = res.json()

            if "url" in data:
                download_link = data["url"]
                st.success("🎉 ফাইল প্রসেস সম্পন্ন হয়েছে!")
                
                # Direct High-Speed Download Button
                st.markdown(f'''
                    <a href="{download_link}" target="_blank" style="text-decoration: none;">
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
                            ⬇️ Direct Download ({chosen_q})
                        </button>
                    </a>
                ''', unsafe_allow_html=True)
            else:
                st.error("লিঙ্কটি প্রসেস করতে ব্যর্থ হয়েছে। প্ল্যাটফর্মের কোনো প্রাইভেট ভিডিও বা ভুল লিঙ্ক কিনা চেক করুন।")

        except Exception as e:
            st.error(f"সার্ভারে কানেক্ট করতে সমস্যা হয়েছে: {str(e)}")

st.markdown("---")
st.markdown('<p style="text-align: center;">SILENT Universal Downloader | Mobile & Desktop Supported</p>', unsafe_allow_html=True)
