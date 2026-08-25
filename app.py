import streamlit as st
import json

# ১. পেজ সেটআপ
st.set_page_config(
    page_title="SILENT Universal Downloader",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ২. CSS ইনজেকশন
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
var style = parent.document.head.appendChild(parent.document.createElement('style'));
style.innerHTML = css;
</script>
""", height=0)

# ৩. টাইটেল ও ইনপুট
st.title("🎬 অল-ইন-ওয়ান সুপার ডাউনলোডার")
st.markdown('<div class="builder-name">✨ Made by SILENT ✨</div>', unsafe_allow_html=True)
st.write("যেকোনো ওয়েবসাইটের লিঙ্ক পেস্ট করে আপনার সাইটের ভেতরেই সরাসরি সেভ করুন।")

url_input = st.text_input("ভিডিও লিঙ্কটি এখানে দিন:", placeholder="https://www.youtube.com/watch?v=...")

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
        <div class="playing-text">ক্যাট ভিডিও লিংক প্রসেস করেছে! নিচে আপনার পছন্দমতো ফাইল সিলেক্ট করুন:</div>
    </div>
    """, unsafe_allow_html=True)

    # 🟢 Pure Client-side Downloader (No Redirect, In-Site Download)
    clean_url_json = json.dumps(clean_url)
    
    downloader_html = f"""
    <div id="loader-box" style="text-align: center; padding: 20px; color: #ffd700; font-weight: bold;">
        ⌛ ফাইল লিঙ্ক জেনারেট করা হচ্ছে...
    </div>
    <div id="download-links" style="display: flex; flex-direction: column; gap: 12px; width: 100%;"></div>

    <script>
    (function() {{
        const videoUrl = {clean_url_json};
        const box = document.getElementById('download-links');
        const loader = document.getElementById('loader-box');

        fetch('https://api.cobalt.tools/api/json', {{
            method: 'POST',
            headers: {{
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }},
            body: JSON.stringify({{ url: videoUrl }})
        }})
        .then(res => res.json())
        .then(data => {{
            loader.style.display = 'none';
            if(data.url) {{
                box.innerHTML = `
                    <a href="${{data.url}}" download style="text-decoration:none;">
                        <button style="width:100%; background:#22c55e; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; font-size:16px; cursor:pointer;">
                            ⬇️ Direct Download Video (Best Quality)
                        </button>
                    </a>`;
            }} else {{
                // Backup Downloader Fetcher
                const cleanId = videoUrl.replace(/.*v=([^&]+).*/, '$1').replace(/.*youtu\.be\/([^?]+).*/, '$1');
                box.innerHTML = `
                    <a href="https://loader.to/api/button/?url=${{encodeURIComponent(videoUrl)}}&f=mp4" download target="_self" style="text-decoration:none;">
                        <button style="width:100%; background:#22c55e; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; font-size:16px; cursor:pointer;">
                            ⬇️ Direct Download MP4 (HD)
                        </button>
                    </a>
                    <a href="https://loader.to/api/button/?url=${{encodeURIComponent(videoUrl)}}&f=mp3" download target="_self" style="text-decoration:none;">
                        <button style="width:100%; background:#3b82f6; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; font-size:16px; cursor:pointer;">
                            🎵 Direct Download Audio (MP3)
                        </button>
                    </a>`;
            }}
        }})
        .catch(err => {{
            loader.style.display = 'none';
            box.innerHTML = `
                <a href="https://loader.to/api/button/?url=${{encodeURIComponent(videoUrl)}}&f=mp4" style="text-decoration:none;">
                    <button style="width:100%; background:#22c55e; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; font-size:16px; cursor:pointer;">
                        ⬇️ Direct Download MP4 Video
                    </button>
                </a>`;
        }});
    }})();
    </script>
    """
    
    st.components.v1.html(downloader_html, height=180)

st.markdown("---")
st.markdown('<p style="text-align: center;">SILENT Universal Downloader | Mobile & Desktop Supported</p>', unsafe_allow_html=True)
