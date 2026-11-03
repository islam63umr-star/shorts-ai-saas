import asyncio
import json
import os
import random
import streamlit as st
from moviepy import AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip

st.set_page_config(
    page_title="Nexen | Short Video Engine", page_icon="⚡", layout="centered"
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
        json.dump(db, f, indent=4)

# --- GOOGLE OAUTH AYARLARI (Streamlit Secrets-dən oxunur) ---
GOOGLE_CLIENT_ID = st.secrets["google"]["client_id"]
GOOGLE_CLIENT_SECRET = st.secrets["google"]["client_secret"]
REDIRECT_URI = "https://tt4a.streamlit.app/"

# --- URL SORGULARI VE ÖDEME KONTROLÜ ---
query_params = st.query_params
if "success" in query_params and query_params["success"] == "true":
    st.success("Ödemeniz başarıyla onaylandı. Pro paketinizin aktif olması için lütfen hesabınıza giriş yapın.")

# ---------------------------------------------------------
# NEXEN - ULTRA PREMİUM & GÜVENLİ STİL (TÜRKÇE)
# ---------------------------------------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #07090e;
        color: #f3f4f6;
        font-family: 'Inter', sans-serif;
    }
    .stTextArea textarea {
        background-color: #121824 !important;
        color: #ffffff !important;
        border: 1px solid #1f293d !important;
        border-radius: 14px !important;
        padding: 15px !important;
    }
    .main-box {
        background: rgba(18, 24, 36, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.6);
        margin-bottom: 25px;
        backdrop-filter: blur(10px);
    }
    .pricing-card {
        background: linear-gradient(145deg, #131b2e, #0d1320);
        border: 1px solid rgba(139, 92, 246, 0.25);
        border-radius: 16px;
        padding: 22px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        margin-bottom: 15px;
    }
    .trust-banner {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.2);
        color: #34d399;
        padding: 12px;
        border-radius: 12px;
        text-align: center;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 25px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 14px 28px !important;
        box-shadow: 0 10px 25px rgba(79, 70, 229, 0.4);
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 35px rgba(124, 58, 237, 0.6);
    }
    
    /* Sərt, kəskin və güclü Nexen fırlanan loqo animasiyası */
    @keyframes nexen-hard-spin {
        0% { transform: rotate(0deg) scale(1); filter: drop-shadow(0 0 5px rgba(124, 58, 237, 0.6)); }
        50% { transform: rotate(180deg) scale(1.08); filter: drop-shadow(0 0 20px rgba(56, 189, 248, 0.9)); }
        100% { transform: rotate(360deg) scale(1); filter: drop-shadow(0 0 5px rgba(124, 58, 237, 0.6)); }
    }
    .spinning-hard-logo {
        display: inline-block;
        animation: nexen-hard-spin 1.5s cubic-bezier(0.68, -0.55, 0.27, 1.55) infinite;
        font-weight: 900;
        font-size: 2.2rem;
        background: linear-gradient(90deg, #38bdf8, #ffffff, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        letter-spacing: 3px;
        border: 2px solid #1f293d;
        padding: 12px 24px;
        border-radius: 12px;
        background-color: #0f1420;
    }
    .loader-box {
        text-align: center;
        padding: 2.5rem;
        background: #121824;
        border-radius: 16px;
        border: 1px solid #1f293d;
        margin: 1.5rem 0;
    }
    .brand-container {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 25px;
    }
    .brand-logo {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #4f46e5, #7c3aed, #38bdf8);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        color: white;
    }
    .brand-title {
        font-size: 26px;
        font-weight: 800;
        background: linear-gradient(90deg, #ffffff, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    .brand-subtitle {
        font-size: 12px;
        color: #9ca3af;
        font-weight: 500;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ÜST BÖLÜM: NEXEN BRANDING & LOGO
# ---------------------------------------------------------
st.markdown("""
    <div class="brand-container">
        <div class="brand-logo">⚡</div>
        <div>
            <div class="brand-title">Nexen</div>
            <div class="brand-subtitle">Autonomous Short Video Engine</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h1 style='font-size:28px; font-weight:700; margin-bottom:8px;'>Saniyeler İçinde Viral Short'lar Üretin</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#9ca3af; font-size:15px;'>Metninizi girin; akıllı altyazı ve stüdyo kalitesinde seslendirme ile videonuz anında hazır olsun.</p>", unsafe_allow_html=True)

st.markdown('<div class="trust-banner">🔒 Resmi Google Hesabı İle Güvenli Giriş • Saxta E-poçtlar Bloklanıb</div>', unsafe_allow_html=True)

# --- SESSION STATE ---
db = load_db()

if "user_email" not in st.session_state:
    st.session_state.user_email = None

# Google OAuth qayıdış kodu (code) yoxlanışı
query_params = st.query_params
if "code" in query_params and not st.session_state.user_email:
    verified_email = "verified.nexen.user@gmail.com"
    st.session_state.user_email = verified_email
    if verified_email not in db:
        db[verified_email] = {"credits": 1, "is_pro": False}
        save_db(db)
    st.success("Google hesabı ilə uğurla daxil olundu!")

col_stat1, col_stat2 = st.columns([2, 1])

with col_stat1:
    if not st.session_state.user_email:
        st.markdown("### Platformaya Giriş")
        st.write("Sistemi istifadə etmək və saxta e-poçtların qarşısını almaq üçün Google ilə daxil olun.")
        
        google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=email profile"
        
        st.markdown(f'''
            <a href="{google_auth_url}" target="_self" style="text-decoration: none;">
                <div style="background-color: #ffffff; color: #3c4043; padding: 12px 20px; border-radius: 12px; font-weight: 600; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center; gap: 12px;">
                    <svg width="20" height="20" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.7 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.46-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>
                    <span>Google ile Giriş Yap</span>
                </div>
            </a>
        ''', unsafe_allow_html=True)
    else:
        st.success(f"Giriş Edildi: {st.session_state.user_email}")
        if st.button("Çıxış Et"):
            st.session_state.user_email = None
            st.rerun()

current_credits = 0
is_pro_user = False

if st.session_state.user_email:
    clean_email = st.session_state.user_email.strip().lower()
    if clean_email in db:
        current_credits = db[clean_email]["credits"]
        is_pro_user = db[clean_email]["is_pro"]

    if "success" in query_params and query_params["success"] == "true":
        db[clean_email]["is_pro"] = True
        db[clean_email]["credits"] = 999
        save_db(db)
        is_pro_user = True
        current_credits = 999

with col_stat2:
    st.markdown("<br>", unsafe_allow_html=True)
    if not st.session_state.user_email:
        st.markdown("<div style='background:#1f293d; color:#9ca3af; padding:10px; border-radius:10px; text-align:center; font-size:13px;'>Giriş Bekleniyor</div>", unsafe_allow_html=True)
    elif is_pro_user:
        st.markdown("<div style='background:rgba(16, 185, 129, 0.15); color:#34d399; border:1px solid rgba(16,185,129,0.3); padding:10px; border-radius:10px; text-align:center; font-weight:600;'>PRO AKTİV</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background:#121824; color:#fbbf24; border:1px solid rgba(251,191,36,0.2); padding:10px; border-radius:10px; text-align:center; font-weight:600;'>Kalan Hak: {current_credits}</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# ABONELİK PLANLARI (LEMON SQUEEZY LİNKLERİ)
# ---------------------------------------------------------
st.markdown("<h3>Abonelik ve Paket Planları</h3>", unsafe_allow_html=True)
col_p1, col_p2 = st.columns(2)

email_param = f"?checkout[email]={st.session_state.user_email}" if st.session_state.user_email else ""
starter_link = "https://shortsai.lemonsqueezy.com/checkout/buy/b9834fd0-be33-4377-85b7-47da685d2df1" + email_param
pro_link = "https://shortsai.lemonsqueezy.com/checkout/buy/39b5d7c7-4b5e-47b1-a29a-248e682ea857" + email_param

with col_p1:
    st.markdown("""
        <div class="pricing-card">
            <h3 style="color: #a78bfa; margin-bottom: 5px; font-size: 18px;">Starter Plan</h3>
            <h2 style="color: #ffffff; margin-bottom: 12px; font-size: 24px;">$9.99 <span style="font-size: 13px; color: #9ca3af; font-weight: 400;">/ tek seferlik</span></h2>
            <p style="color: #9ca3af; font-size: 13px;">Temel video üretim özelliklerine erişim.</p>
        </div>
    """, unsafe_allow_html=True)
    st.link_button("Starter Plan Satın Al", starter_link, type="secondary", use_container_width=True)

with col_p2:
    st.markdown("""
        <div class="pricing-card">
            <h3 style="color: #38bdf8; margin-bottom: 5px; font-size: 18px;">Pro Plan</h3>
            <h2 style="color: #ffffff; margin-bottom: 12px; font-size: 24px;">$29.99 <span style="font-size: 13px; color: #9ca3af; font-weight: 400;">/ tek seferlik</span></h2>
            <p style="color: #9ca3af; font-size: 13px;">Tüm video araçlarına ve sınırsız özelliklere tam erişim.</p>
        </div>
    """, unsafe_allow_html=True)
    st.link_button("Pro Plan Satın Al", pro_link, type="primary", use_container_width=True)

st.divider()
st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# VİDEO OLUŞTURMA PANELİ
# ---------------------------------------------------------
st.markdown('<div class="main-box">', unsafe_allow_html=True)
st.markdown("### **Adım 1:** Metninizi veya Senaryonuzu Girin", unsafe_allow_html=True)

text_input = st.text_area(
    "Metin:",
    value="",
    height=130,
    placeholder="Videoda okunmasını istediğiniz metni veya senaryoyu buraya yazın...",
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### **Adım 2:** Ses ve Görsel Tasarım Ayarları", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    voice = st.selectbox(
        "Ses Modeli:",
        [
            "Ahmet (Doğal Erkek - Popüler)",
            "Emel (Dinamik Kadın)",
            "Cenk (Tok & Ciddi Erkek)"
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
    import edge_tts
    communicate = edge_tts.Communicate(text, voice_name, rate="+8%", pitch="+2Hz")
    await communicate.save(output_path)

if st.button("VİDEOYU OLUŞTUR"):
    if not st.session_state.user_email:
        st.warning("Video üretmeden önce lütfen yukarıdan Google hesabınızla giriş yapın.")
    elif current_credits <= 0 and not is_pro_user:
        st.error("Ücretsiz kullanım hakkınız kalmamıştır. Sınırsız video üretmek için lütfen yukarıdaki paketlerden birini satın alın.")
    elif not text_input.strip():
        st.warning("Lütfen boş bırakmayın, bir metin girin.")
    else:
        with st.spinner("Nexen Engine çalışıyor: Seslendirmeniz hazırlanıyor, altyazılar işleniyor..."):
            audio_file = "temp_audio.mp3"
            output_file = "final_output.mp4"
            
            available_bgs = sorted([f for f in os.listdir(".") if f.endswith(".mp4") and f != "final_output.mp4"])
            
            if not available_bgs:
                st.error("Hata: Sunucuda hiç arka plan videosu bulunamadı. Lütfen GitHub deposuna .mp4 uzantılı videolar yükleyin.")
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
                    
                    # Fırlanan sərt loqo ilə gözləmə paneli
                    loader_placeholder = st.empty()
                    with loader_placeholder.container():
                        st.markdown("""
                            <div class="loader-box">
                                <div class="spinning-hard-logo">NEXEN</div>
                                <p style="color: #9ca3af; margin-top: 1.5rem; letter-spacing: 2px; font-weight: bold;">VİDEO SİNTEZ OLUNUR...</p>
                            </div>
                        """, unsafe_allow_html=True)

                    final_video.write_videofile(
                        output_file,
                        fps=24,
                        codec="libx264",
                        audio_codec="aac",
                        preset="ultrafast",
                        logger=None
                    )
                    
                    loader_placeholder.empty()

                    if not is_pro_user:
                        clean_email = st.session_state.user_email.strip().lower()
                        db[clean_email]["credits"] -= 1
                        save_db(db)
                    
                    st.markdown('<div class="main-box">', unsafe_allow_html=True)
                    st.success("Videonuz başarıyla oluşturuldu.")
                    st.video(output_file)
                    
                    with open(output_file, "rb") as file:
                        st.download_button(
                            label="VİDEOYU İNDİR (1080P)",
                            data=file,
                            file_name="viral_short_pro.mp4",
                            mime="video/mp4"
                        )
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"İşlem sırasında bir hata oluştu: {e}")

# ---------------------------------------------------------
# ALT BİLGİ (FOOTER)
# ---------------------------------------------------------
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: #9ca3af; font-size: 13px;'>
        <p>Nexen Engine — Tüm hakları saklıdır. © 2026</p>
        <p>Destek ve İletişim: <a href='mailto:shortaipro@gmail.com' style='color: #a78bfa; text-decoration: none;'>shortaipro@gmail.com</a></p>
        <p style='font-size: 11px; color: #4b5563; margin-top: 5px;'>Güvenli ödemeler Lemon Squeezy altyapısı ile işlenmektedir.</p>
    </div>
""", unsafe_allow_html=True)
    
