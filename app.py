import asyncio
import json
import os
import random
import edge_tts
from moviepy import AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip
import streamlit as st

st.set_page_config(
    page_title="Shorts AI Studio | Pro Creator", page_icon="✨", layout="centered"
)

# --- VERİTABANI YÖNETİMİ (JSON) ---
DB_FILE = "users_db.json"

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f)

# --- URL SORGULARI VE ÖDEME KONTROLÜ ---
query_params = st.query_params
if "success" in query_params and query_params["success"] == "true":
    st.success("🎉 Ödemeniz başarıyla onaylandı! Pro paketinizin aktif olması için lütfen aşağıya e-posta adresinizi yazın.")

# ---------------------------------------------------------
# PROFESSIONAL SAAS & PRICING TASARIMI (TÜRKÇE)
# ---------------------------------------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
        font-family: 'Inter', sans-serif;
    }
    .stTextArea textarea {
        background-color: #1f2937 !important;
        color: #ffffff !important;
        border: 1px solid #374151 !important;
        border-radius: 12px !important;
    }
    .main-box {
        background: rgba(17, 24, 39, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
        margin-bottom: 25px;
    }
    .pricing-card {
        background: linear-gradient(145deg, #181d28, #111827);
        border: 1px solid rgba(168, 85, 247, 0.3);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        margin-bottom: 15px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 14px 28px !important;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.4);
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 30px rgba(168, 85, 247, 0.6);
    }
    .badge {
        background: rgba(168, 85, 247, 0.15);
        color: #c084fc;
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 700;
        border: 1px solid rgba(168, 85, 247, 0.3);
        display: inline-block;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ANA EKRAN & KULLANICI E-POSTA GİRİŞİ
# ---------------------------------------------------------
st.markdown('<div><span class="badge">✨ YAPAY ZEKA DESTEKLİ VİRAL SHORTS ÜRETİCİ</span></div>', unsafe_allow_html=True)
st.markdown("<h1 style='font-size:32px; font-weight:800; margin-bottom:5px;'>Saniyeler İçinde Viral Short'lar Üretin</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#9ca3af; font-size:15px;'>İstediğiniz konuyu yazın; kusursuz altyazı ve yüksek kaliteli yapay zeka seslendirmesi ile videonuz anında hazır olsun.</p>", unsafe_allow_html=True)

col_stat1, col_stat2 = st.columns([2, 1])
with col_stat1:
    user_email = st.text_input("E-Posta Adresiniz (Hakkınızı korumak ve ödemeyi eşleştirmek için zorunludur):", placeholder="ornek@gmail.com")

db = load_db()
current_credits = 1
is_pro_user = False

if user_email and "@" in user_email:
    user_email = user_email.strip().lower()
    if user_email not in db:
        db[user_email] = {"credits": 1, "is_pro": False}
        save_db(db)
    
    current_credits = db[user_email]["credits"]
    is_pro_user = db[user_email]["is_pro"]
    
    if "success" in query_params and query_params["success"] == "true":
        db[user_email]["is_pro"] = True
        db[user_email]["credits"] = 999
        save_db(db)
        is_pro_user = True
        current_credits = 999

with col_stat2:
    st.markdown("<br>", unsafe_allow_html=True)
    if not user_email:
        st.markdown("<div style='background:#374151; color:#f3f4f6; padding:10px; border-radius:10px; text-align:center; font-size:13px;'>📧 E-posta Girin</div>", unsafe_allow_html=True)
    elif is_pro_user:
        st.markdown("<div style='background:#065f46; color:#34d399; padding:10px; border-radius:10px; text-align:center; font-weight:bold;'>👑 PRO AKTİF</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background:#1f2937; color:#fbbf24; padding:10px; border-radius:10px; text-align:center; font-weight:bold;'>🎁 Kalan Hak: {current_credits}</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# ABONELİK PLANLARI (LEMON SQUEEZY LİNKLERİ)
# ---------------------------------------------------------
st.markdown("<h3>💳 Abonelik ve Paket Planları (Starter / Pro)</h3>", unsafe_allow_html=True)
col_p1, col_p2 = st.columns(2)

email_param = f"?checkout[email]={user_email}" if user_email else ""
starter_link = "https://shortsai.lemonsqueezy.com/checkout/buy/b9834fd0-be33-4377-85b7-47da685d2df1" + email_param
pro_link = "https://shortsai.lemonsqueezy.com/checkout/buy/39b5d7c7-4b5e-47b1-a29a-248e682ea857" + email_param

with col_p1:
    st.markdown("""
        <div class="pricing-card">
            <h3 style="color: #c084fc; margin-bottom: 5px;">Starter Plan</h3>
            <h2 style="color: #ffffff; margin-bottom: 15px;">$9.99 <span style="font-size: 14px; color: #9ca3af;">/ tek seferlik</span></h2>
            <p style="color: #9ca3af; font-size: 13px;">Temel yapay zeka video üretim özelliklerine erişim.</p>
        </div>
    """, unsafe_allow_html=True)
    st.link_button("👉 Starter Plan Satın Al", starter_link, type="secondary", use_container_width=True)

with col_p2:
    st.markdown("""
        <div class="pricing-card">
            <h3 style="color: #38bdf8; margin-bottom: 5px;">Pro Plan</h3>
            <h2 style="color: #ffffff; margin-bottom: 15px;">$29.99 <span style="font-size: 14px; color: #9ca3af;">/ tek seferlik</span></h2>
            <p style="color: #9ca3af; font-size: 13px;">Tüm AI video araçlarına ve sınırsız özelliklere tam erişim.</p>
        </div>
    """, unsafe_allow_html=True)
    st.link_button("👉 Pro Plan Satın Al", pro_link, type="primary", use_container_width=True)

st.divider()
st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# VİDEO OLUŞTURMA PANELİ
# ---------------------------------------------------------
st.markdown('<div class="main-box">', unsafe_allow_html=True)
st.markdown("### 📝 **Adım 1:** Metninizi veya Senaryonuzu Girin", unsafe_allow_html=True)

text_input = st.text_area(
    "Metin:",
    value="",
    height=130,
    placeholder="Videoda okunmasını istediğiniz metni veya senaryoyu buraya yazın...",
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🎙️ **Adım 2:** Ses ve Görsel Tasarım Ayarları", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    voice = st.selectbox(
        "Ses Modeli:",
        [
            "🇹🇷 Ahmet (Doğal Erkek - Popüler)",
            "🇹🇷 Emel (Dinamik Kadın)",
            "🇹🇷 Cenk (Tok & Ciddi Erkek)"
        ]
    )
with col2:
    font_size = st.slider("Altyazı Boyutu:", 30, 50, 40)

st.markdown("</div>", unsafe_allow_html=True)

if "Ahmet" in voice:
    voice_code = "tr-TR-AhmetNeural"
elif "Cenk" in voice:
    voice_code = "tr-TR-FatihNeural"
else:
    voice_code = "tr-TR-EmelNeural"

async def generate_audio(text, voice_name, output_path):
    communicate = edge_tts.Communicate(text, voice_name, rate="+8%", pitch="+2Hz")
    await communicate.save(output_path)

if st.button("✨ VİDEOYU SİHİRLİ ŞEKİLDE OLUŞTUR"):
    if not user_email or "@" not in user_email:
        st.warning("⚠️ Video üretmeden önce lütfen üst kısıma geçerli bir e-posta adresi girin!")
    elif current_credits <= 0 and not is_pro_user:
        st.error("⚠️ Ücretsiz kullanım hakkınız kalmamıştır! Sınırsız video üretmek için lütfen yukarıdaki paketlerden birini satın alın.")
    elif not text_input.strip():
        st.warning("⚠️ Lütfen boş bırakmayın, bir metin girin!")
    else:
        with st.spinner("🚀 Yapay zeka çalışıyor: Ultra gerçekçi seslendirmeniz hazırlanıyor, altyazılar işleniyor..."):
            audio_file = "temp_audio.mp3"
            output_file = "final_output.mp4"
            
            available_bgs = sorted([f for f in os.listdir(".") if f.endswith(".mp4") and f != "final_output.mp4"])
            
            if not available_bgs:
                st.error("Hata: Sunucuda hiç arka plan videosu bulunamadı! Lütfen GitHub deposuna .mp4 uzantılı videolar yükleyin.")
            else:
                candidates = available_bgs
                if len(available_bgs) > 1 and "last_bg" in st.session_state and st.session_state.last_bg in available_bgs:
                    candidates = [b for b in available_bgs if b != st.session_state.last_bg]
                
                background_video = random.choice(candidates)
                st.session_state.last_bg = background_video
                
                asyncio.run(generate_audio(text_input, voice_code, audio_file))
                
                try:
                    video = VideoFileClip(background_video)
                    audio = AudioFileClip(audio_file)
                    
                    if video.duration > audio.duration:
                        max_start = video.duration - audio.duration
                        import random as r_time
                        start_time = r_time.uniform(0, max_start)
                        end_time = start_time + audio.duration
                        video = video.subclipped(start_time, end_time)
                    else:
                        video = video.subclipped(0, video.duration)
                    
                    words = text_input.split()
                    clips = [video]
                    
                    total_words = len(words)
                    time_per_word = audio.duration / max(total_words, 1)
                    
                    chunk_size = 2
                    for i in range(0, total_words, chunk_size):
                        chunk = " ".join(words[i:i + chunk_size])
                        start_time = i * time_per_word
                        end_time = min((i + chunk_size) * time_per_word, audio.duration)
                        
                        try:
                            txt_clip = (
                                TextClip(
                                    text=chunk,
                                    font="DejaVuSans-Bold",
                                    font_size=font_size,
                                    color="white",
                                    stroke_color="black",
                                    stroke_width=2,
                                    method="caption",
                                    size=(int(video.w * 0.85), None),
                                    margin=(20, 20)
                                )
                                .with_start(start_time)
                                .with_duration(max(0.15, end_time - start_time))
                                .with_position(("center", "center"))
                            )
                            clips.append(txt_clip)
                        except Exception:
                            pass
                    
                    final_video = CompositeVideoClip(clips)
                    final_video = final_video.with_audio(audio)
                    
                    final_video.write_videofile(
                        output_file,
                        fps=24,
                        codec="libx264",
                        audio_codec="aac",
                        preset="ultrafast",
                        logger=None
                    )
                    
                    if not is_pro_user:
                        db[user_email]["credits"] -= 1
                        save_db(db)
                    
                    st.markdown('<div class="main-box">', unsafe_allow_html=True)
                    st.success("🎉 Videonuz başarıyla oluşturuldu!")
                    st.video(output_file)
                    
                    with open(output_file, "rb") as file:
                        st.download_button(
                            label="📥 VİDEOYU İNDİR (1080P)",
                            data=file,
                            file_name="viral_short_pro.mp4",
                            mime="video/mp4"
                        )
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"İşlem sırasında bir hata oluştu: {e}")
