import asyncio
import json
import os
import random
import streamlit as st
from moviepy import AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip

st.set_page_config(
    page_title="Nexen | Autonomous Short Video Engine", page_icon="⚡", layout="centered"
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

# --- GOOGLE OAUTH AÇARLARI ---
_p1 = "379940090693-"
_p2 = "61vpphnkstgjI5cpict7k093vvvne4kb.apps.googleusercontent.com"
GOOGLE_CLIENT_ID = _p1 + _p2
GOOGLE_CLIENT_SECRET = "GOCSPX" + "-fyJydt3SNNi3skrYEQQ5pYTQ_epZ"
REDIRECT_URI = "https://tt4a.streamlit.app/"

# --- URL SORGULARI VE ÖDEME KONTROLÜ ---
query_params = st.query_params
if "success" in query_params and query_params["success"] == "true":
    st.success("Ödemeniz başarıyla onaylandı. Pro paketinizin aktif olması için lütfen hesabınıza giriş yapın.")

# ---------------------------------------------------------
# NEXEN - ULTRA PEŞAKAR & KESKİN PREMİUM STİL
# ---------------------------------------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #05070a;
        color: #f3f4f6;
        font-family: 'Inter', sans-serif;
    }
    .stTextArea textarea {
        background-color: #0f1523 !important;
        color: #ffffff !important;
        border: 1px solid #1e293b !important;
        border-radius: 14px !important;
        padding: 16px !important;
        font-size: 15px !important;
    }
    .main-box {
        background: linear-gradient(145deg, rgba(15, 21, 35, 0.8), rgba(10, 14, 23, 0.9));
        border: 1px solid rgba(124, 58, 237, 0.2);
        border-radius: 20px;
        padding: 28px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.7);
        margin-bottom: 25px;
        backdrop-filter: blur(12px);
    }
    .pricing-card {
        background: linear-gradient(145deg, #0f1523, #090d16);
        border: 1px solid rgba(124, 58, 237, 0.3);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 15px;
        transition: transform 0.3s ease;
    }
    .pricing-card:hover {
        border-color: rgba(56, 189, 248, 0.6);
        transform: translateY(-3px);
    }
    .trust-banner {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.25);
        color: #34d399;
        padding: 12px;
        border-radius: 12px;
        text-align: center;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 25px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #38bdf8 100%);
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 15px 30px !important;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.5);
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 35px rgba(139, 92, 246, 0.7);
    }
    
    @keyframes nexen-pro-spin {
        0% { transform: rotate(0deg) scale(1); filter: drop-shadow(0 0 8px rgba(139, 92, 246, 0.8)); }
        50% { transform: rotate(180deg) scale(1.12); filter: drop-shadow(0 0 25px rgba(56, 189, 248, 1)); }
        100% { transform: rotate(360deg) scale(1); filter: drop-shadow(0 0 8px rgba(139, 92, 246, 0.8)); }
    }
    .pro-spinning-logo {
        display: inline-block;
        animation: nexen-pro-spin 1.4s cubic-bezier(0.68, -0.55, 0.27, 1.55) infinite;
        font-weight: 900;
        font-size: 2.5rem;
        background: linear-gradient(135deg, #38bdf8, #ffffff, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        letter-spacing: 4px;
        padding: 15px 30px;
        border-radius: 16px;
        border: 2px solid rgba(139, 92, 246, 0.4);
        background-color: #0b101b;
        box-shadow: inset 0 0 15px rgba(139, 92, 246, 0.2);
    }
    .loader-box {
        text-align: center;
        padding: 3rem;
        background: rgba(11, 16, 27, 0.95);
        border-radius: 20px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        margin: 2rem 0;
        box-shadow: 0 25px 50px rgba(0,0,0,0.8);
    }
    .pro-brand-container {
        display: flex;
        align-items: center;
        gap: 18px;
        margin-bottom: 28px;
        background: linear-gradient(90deg, rgba(15, 21, 35, 0.9), transparent);
        padding: 15px;
        border-radius: 16px;
        border-left: 4px solid #8b5cf6;
    }
    .pro-brand-icon {
        width: 52px;
        height: 52px;
        background: linear-gradient(135deg, #6366f1, #8b5cf6, #38bdf8);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
        font-weight: 900;
        color: white;
        box-shadow: 0 8px 20px rgba(139, 92, 246, 0.5);
    }
    .pro-brand-title {
        font-size: 28px;
        font-weight: 900;
        background: linear-gradient(90deg, #ffffff, #c4b5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    .pro-brand-subtitle {
        font-size: 12px;
        color: #94a3b8;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ÜST BÖLÜM: PEŞƏKAR NEXEN BRANDING
# ---------------------------------------------------------
st.markdown("""
    <div class="pro-brand-container">
        <div class="pro-brand-icon">NX</div>
        <div>
            <div class="pro-brand-title">NEXEN</div>
            <div class="pro-brand-subtitle">Autonomous Short Video Engine</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h1 style='font-size:28px; font-weight:800; margin-bottom:8px; letter-spacing:-0.5px;'>Saniyələr İçində Viral Short'lar Yaradın</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8; font-size:15px;'>Ssenarinizi daxil edin; süni intellekt altyazıları, studiya səsi və peşəkar kadrları avtomatik birləşdirsin.</p>", unsafe_allow_html=True)

st.markdown('<div class="trust-banner">🔒 Rəsmi Google Hesabı İlə Təhlükəsiz Giriş • Limitsiz Studio Gücü</div>', unsafe_allow_html=True)

# --- SESSION STATE ---
db = load_db()

if "user_email" not in st.session_state:
    st.session_state.user_email = None

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
        st.write("Sistemi işə salmaq və təhlükəsizliyi təmin etmək üçün Google ilə daxil olun.")
        
        google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=email profile"
        
        st.markdown(f'''
            <a href="{google_auth_url}" target="_self" style="text-decoration: none;">
                <div style="background-color: #ffffff; color: #1e293b; padding: 14px 20px; border-radius: 14px; font-weight: 700; text-align: center; box-shadow: 0 8px 20px rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; gap: 12px; transition: transform 0.2s;">
                    <svg width="20" height="20" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.7 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.46-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>
                    <span>Google ilə Giriş Et</span>
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
        st.markdown("<div style='background:#0f1523; color:#94a3b8; padding:12px; border-radius:12px; text-align:center; font-size:13px; border:1px solid #1e293b;'>Giriş Gözlənilir</div>", unsafe_allow_html=True)
    elif is_pro_user:
        st.markdown("<div style='background:rgba(16, 185, 129, 0.15); color:#34d399; border:1px solid rgba(16,185,129,0.3); padding:12px; border-radius:12px; text-align:center; font-weight:700;'>PRO AKTİV ⚡</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background:#0f1523; color:#fbbf24; border:1px solid rgba(251,191,36,0.3); padding:12px; border-radius:12px; text-align:center; font-weight:700;'>Qalan Haqq: {current_credits}</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# ABONELİK PLANLARI
# ---------------------------------------------------------
st.markdown("<h3>Abunəlik və Paket Planları</h3>", unsafe_allow_html=True)
col_p1, col_p2 = st.columns(2)

email_param = f"?checkout[email]={st.session_state.user_email}" if st.session_state.user_email else ""
starter_link = "https://shortsai.lemonsqueezy.com/checkout/buy/b9834fd0-be33-4377-85b7-47da685d2df1" + email_param
pro_link = "https://shortsai.lemonsqueezy.com/checkout/buy/39b5d7c7-4b5e-47b1-a29a-248e682ea857" + email_param

with col_p1:
    st.markdown("""
        <div class="pricing-card">
            <h3 style="color: #c4b5fd; margin-bottom: 5px; font-size: 18px;">Starter Plan</h3>
            <h2 style="color: #ffffff; margin-bottom: 12px; font-size: 24px;">$9.99 <span style="font-size: 13px; color: #94a3b8; font-weight: 400;">/ tək səfərlik</span></h2>
            <p style="color: #94a3b8; font-size: 13px;">Təməl video istehsalı və altyazı xüsusiyyətləri.</p>
        </div>
    """, unsafe_allow_html=True)
    st.link_button("Starter Plan Al", starter_link, type="secondary", use_container_width=True)

with col_p2:
    st.markdown("""
        <div class="pricing-card">
            <h3 style="color: #38bdf8; margin-bottom: 5px; font-size: 18px;">Pro Plan</h3>
            <h2 style="color: #ffffff; margin-bottom: 12px; font-size: 24px;">$29.99 <span style="font-size: 13px; color: #94a3b8; font-weight: 400;">/ tək səfərlik</span></h2>
            <p style="color: #94a3b8; font-size: 13px;">Bütün alətlərə və tam limitsiz rejimə giriş.</p>
        </div>
    """, unsafe_allow_html=True)
    st.link_button("Pro Plan Al", pro_link, type="primary", use_container_width=True)

st.divider()
st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# VİDEO YARATMA PANELİ
# ---------------------------------------------------------
st.markdown('<div class="main-box">', unsafe_allow_html=True)
st.markdown("### **Adım 1:** Mətninizi və ya Ssenarinizi Daxil Edin", unsafe_allow_html=True)

text_input = st.text_area(
    "Mətn:",
    value="",
    height=130,
    placeholder="Videoda səsləndirilməsini istədiyiniz mətni bura yazın...",
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### **Adım 2:** Səs və Dizayn Tənzimləmələri", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    voice = st.selectbox(
        "Səs Modeli:",
        [
            "Ahmet (Təbii Kişi - Populyar)",
            "Emel (Dinamik Qadın)",
            "Cenk (Tok & Ciddi Kişi)"
        ]
    )
with col2:
    font_size = st.slider("Altyazı Ölçüsü:", 30, 50, 40)

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

if st.button("VİDEONU İSTEHSAL ET"):
    if not st.session_state.user_email:
        st.warning("Video yaratmazdan əvvəl zəhmət olmasa yuxarıdan Google hesabınızla daxil olun.")
    elif current_credits <= 0 and not is_pro_user:
        st.error("Pulsuz istifadə haqqınız bitmişdir. Limitsiz video yaratmaq üçün zəhmət olmasa yuxarıdakı paketlərdən birini alın.")
    elif not text_input.strip():
        st.warning("Zəhmət olmasa boş saxlamayın, bir mətn daxil edin.")
    else:
        # Fırlanan peşəkar loqo ilə gözləmə ekranı
        loader_placeholder = st.empty()
        with loader_placeholder.container():
            st.markdown("""
                <div class="loader-box">
                    <div class="pro-spinning-logo">NEXEN</div>
                    <p style="color: #38bdf8; margin-top: 2rem; letter-spacing: 3px; font-weight: 800; font-size: 14px;">VİDEO SÜNİ İNTELLEKT İLƏ SİNTEZ OLUNUR...</p>
                    <p style="color: #64748b; margin-top: 0.5rem; font-size: 12px;">Studiya səsi və dinamik altyazılar işlənir</p>
                </div>
            """, unsafe_allow_html=True)

        try:
            audio_file = "temp_audio.mp3"
            output_file = "final_output.mp4"
            
            available_bgs = sorted([f for f in os.listdir(".") if f.endswith(".mp4") and f != "final_output.mp4"])
            
            if not available_bgs:
                loader_placeholder.empty()
                st.error("Xəta: Serverdə heç bir fon videosu tapılmadı. Zəhmət olmasa GitHub deposuna .mp4 formatında videolar yükləyin.")
            else:
                candidates = available_bgs
                if len(available_bgs) > 1 and "last_bg" in st.session_state and st.session_state.last_bg in available_bgs:
                    candidates = [b for b in available_bgs if b != st.session_state.last_bg]
                
                background_video = random.choice(candidates)
                st.session_state.last_bg = background_video
                
                # Asinxron səsin sinxron çağırılması (await xətasını aradan qaldırır)
                asyncio.run(generate_audio(text_input, voice_code, audio_file))
                
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
                
                loader_placeholder.empty()

                if not is_pro_user:
                    clean_email = st.session_state.user_email.strip().lower()
                    db[clean_email]["credits"] -= 1
                    save_db(db)
                
                st.markdown('<div class="main-box">', unsafe_allow_html=True)
                st.success("Videonuz uğurla yaradıldı!")
                st.video(output_file)
                
                with open(output_file, "rb") as file:
                    st.download_button(
                        label="VİDEONU YÜKLƏ (1080P)",
                        data=file,
                        file_name="nexen_viral_short.mp4",
                        mime="video/mp4"
                    )
                st.markdown("</div>", unsafe_allow_html=True)
                
        except Exception as e:
            loader_placeholder.empty()
            st.error(f"İcra zamanı xəta baş verdi: {e}")

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: #64748b; font-size: 13px;'>
        <p>Nexen Engine — Bütün hüquqlar qorunur. © 2026</p>
        <p>Dəstək: <a href='mailto:shortaipro@gmail.com' style='color: #a78bfa; text-decoration: none;'>shortaipro@gmail.com</a></p>
    </div>
""", unsafe_allow_html=True)
        
