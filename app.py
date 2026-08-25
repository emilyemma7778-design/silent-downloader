import streamlit as st
import json

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

# ৩. ল্যাঙ্গুয়েজ টেক্সট
TEXTS = {
    "bn": {
        "title": "🎬 অল-ইন-ওয়ান সুপার ডাউনলোডার",
        "subtitle": "যেকোনো ওয়েবসাইটের লিঙ্ক পেস্ট করে আপনার পছন্দের কোয়ালিটিতে ভিডিও নামিয়ে নিন।",
        "url_label": "ভিডিও লিঙ্কটি এখানে দিন:",
        "url_placeholder": "https://www.youtube.com/watch?v=...",
        "select_format": "রেজোলিউশন / কোয়ালিটি বাছাই করুন:",
        "download_start": "ডাউনলোড লিঙ্ক তৈরি করুন ⬇️",
        "err_empty": "দয়া করে একটি সঠিক লিঙ্ক দিন।"
    },
    "en": {
        "title": "🎬 All-in-One Super Downloader",
        "subtitle": "Paste any video link and download in your preferred resolution easily.",
        "url_label": "Enter Video Link Here:",
        "url_placeholder": "https://www.youtube.com/watch?v=...",
        "select_format": "Select Resolution / Quality:",
        "download_start": "Generate Download Link ⬇️",
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

quality_options = {
    "1080p Full HD (MP4)": "1080",
    "720p HD (MP4)": "720",
    "480p SD (MP4)": "480",
    "360p Low (MP4)": "360",
    "Audio Only (MP3)": "audio"
}

selected_option = st.selectbox(t["select_format"], list(quality_options.keys()))

if st.button(t["download_start"]):
    if not url_input.strip():
        st.warning(t["err_empty"])
    else:
        quality_val = quality_options[selected_option]
        is_audio = "true" if quality_val == "audio" else "false"
        v_quality = "1080" if quality_val == "audio" else quality_val

        # ক্লায়েন্ট-সাইড প্রসেসিং Script (JavaScript Engine)
        js_code = f"""
        <div id="status-box" style="padding:15px; border-radius:10px; background:#1e293b; color:#fff; font-family:sans-serif; text-align:center;">
            ⏳ প্রসেসিং শুরু হচ্ছে...
        </div>
        
        <script>
        (async function() {{
            const statusBox = document.getElementById("status-box");
            const targetUrl = "{url_input.strip()}";
            const quality = "{v_quality}";
            const isAudio = {is_audio};
            
            // Multiple Public Engine Nodes
            const instances = [
                "https://co.wuk.sh/api/json",
                "https://cobalt.stream/api/json",
                "https://api.cobalt.tools/"
            ];

            let success = false;

            for (let endpoint of instances) {{
                try {{
                    statusBox.innerHTML = "🔄 ক্লায়েন্ট বাইপাস চলছে... (" + new URL(endpoint).hostname + ")";
                    
                    let bodyData = {{
                        url: targetUrl,
                        videoQuality: quality,
                        downloadMode: isAudio ? "audio" : "auto"
                    }};

                    let res = await fetch(endpoint, {{
                        method: "POST",
                        headers: {{
                            "Accept": "application/json",
                            "Content-Type": "application/json"
                        }},
                        body: JSON.stringify(bodyData)
                    }});

                    let data = await res.json();

                    if (data.url || (data.picker && data.picker.length > 0)) {{
                        let finalUrl = data.url || data.picker[0].url;
                        statusBox.innerHTML = `
                            <p style="color:#4ade80; font-size:18px; font-weight:bold;">🎉 ভিডিও ডাউনলোডের জন্য প্রস্তুত!</p>
                            <a href="${{finalUrl}}" target="_blank" style="text-decoration:none;">
                                <button style="width:100%; background:#22c55e; color:white; font-size:18px; font-weight:bold; padding:14px; border:none; border-radius:10px; cursor:pointer;">
                                    💾 ফাইলটি ডাউনলোড করুন (Click to Save)
                                </button>
                            </a>
                        `;
                        success = true;
                        break;
                    }}
                }} catch (e) {{
                    console.log("Failed node:", endpoint);
                }}
            }}

            if (!success) {{
                statusBox.innerHTML = `
                    <p style="color:#ef4444; font-size:16px;">⚠️ সরাসরি স্ট্রিম লিংক তৈরি করা সম্ভব হয়নি। নিচের ইমার্জেন্সি ডাউনলোডার ব্যবহার করুন:</p>
                    <a href="https://cobalt.tools/?url=${{encodeURIComponent(targetUrl)}}" target="_blank" style="text-decoration:none;">
                        <button style="width:100%; background:#eab308; color:black; font-size:16px; font-weight:bold; padding:12px; border:none; border-radius:10px; cursor:pointer;">
                            ⚡ Emergency Direct Portal Open করুন
                        </button>
                    </a>
                `;
            }}
        }})();
        </script>
        """
        st.components.v1.html(js_code, height=180)

st.markdown("---")
st.markdown('<p style="text-align: center;">SILENT Universal Downloader | Mobile & Desktop Supported</p>', unsafe_allow_html=True)
