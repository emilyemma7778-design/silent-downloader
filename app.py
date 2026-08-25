import streamlit as st

# ১. পেজ কনফিগারেশন
st.set_page_config(
    page_title="SILENT Universal Downloader",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ২. CSS ইনজেকশন (UI, Theme & Cat Animations)
st.components.v1.html("""
<script>
var css = `
.stApp {
    background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #1a1a2e) !important;
    background-size: 400% 400% !important;
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
`;
var style = parent.document.createElement('style');
style.innerHTML = css;
parent.document.head.appendChild(style);
</script>
""", height=0)

# ৩. টেক্সট ও টাইটেল
st.title("🎬 অল-ইন-ওয়ান সুপার ডাউনলোডার")
st.markdown('<div class="builder-name">✨ Made by SILENT ✨</div>', unsafe_allow_html=True)
st.write("যেকোনো ওয়েবসাইটের লিঙ্ক পেস্ট করে আপনার সাইটের ভেতরেই সরাসরি প্রসেস ও ডাউনলোড করুন।")

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

if "target_url" in st.session_state and url_input.strip():
    clean_url = st.session_state["target_url"]
    
    st.markdown("---")
    
    # 🐾 Cute Cat Status
    st.markdown("""
    <div class="cat-container">
        <div class="cute-cat">🐱🐾 🧶</div>
        <div class="playing-text">ক্যাট আপনার ভিডিও তৈরি করছে... নিচে আপনার সাইটেই ডাউনলোড অপশন প্রস্তুত! ✨</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 🟢 100% In-Site Player & Stream Downloader (Client-Side Rendering)
    in_site_engine = f"""
    <div id="download-box" style="background: rgba(255, 255, 255, 0.07); padding: 20px; border-radius: 15px; text-align: center; border: 1px solid rgba(255,255,255,0.15);">
        <p style="color: #4ade80; font-weight: bold; font-size: 18px; margin-bottom: 10px;">✅ Direct Stream Ready!</p>
        
        <div id="loader" style="color: #ffd700; font-size: 14px; margin-bottom: 10px;">অটোমেটিক স্ট্রিম অপটিমাইজ করা হচ্ছে...</div>

        <iframe id="stream-frame" src="https://yt1s.io/api/widget?url={clean_url}" 
                style="width:100%; height:320px; border:none; border-radius:10px; background:transparent;" 
                onload="document.getElementById('loader').style.display='none';">
        </iframe>
    </div>
    """
    
    st.components.v1.html(in_site_engine, height=390)

st.markdown("---")
st.markdown('<p style="text-align: center;">SILENT Universal Downloader | Mobile & Desktop Supported</p>', unsafe_allow_html=True)
