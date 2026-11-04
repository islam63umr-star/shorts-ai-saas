import asyncio
import json
import os
import random
import streamlit as st
import edge_tts
from moviepy import AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip

st.set_page_config(
    page_title="Nexen AI | Autonomous Short Video Engine", page_icon="⚡", layout="centered"
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

# --- LİMİT VƏ PLAN YENİLƏMƏ ---
def update_user_plan(email, plan_type):
    db = load_db()
    if email in db:
        if plan_type == "monthly":
            db[email]["credits"] = 200  
            db[email]["plan"] = "Aylıq Plan (200 Video)"
            db[email]["is_pro"] = True
        elif plan_type == "yearly_unlimited":
            db[email]["credits"] = 99999  
            db[email]["plan"] = "Sonsuz Plan (1 İl)"
            db[email]["is_pro"] = True
        save_db(db)

# ---------------------------------------------------------
# NEXEN - ULTRA PEŞAKAR & KESKİN PREMİUM STİL (YENİ PEŞƏKAR SVG LOQO)
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
    
    /* ChatGPT / Claude Stili Peşəkar Yanıb-sönən Neon Loqo */
    .nexen-logo-wrapper {
        display: flex;
        align-items: center;
        gap: 18px;
        padding: 10px 0;
        margin-bottom: 25px;
    }
    .nexen-svg-box {
        width: 54px;
        height: 54px;
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 50%, #06b6d4 100%);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 30px rgba(147, 51, 234, 0.7);
        animation: ai-glow 2.5s infinite ease-in-out;
    }
    @keyframes ai-glow {
        0%, 100% { transform: scale(1); box-shadow: 0 0 20px rgba(147, 51, 234, 0.6); }
        50% { transform: scale(1.06); box-shadow: 0 0 40px rgba(6, 182, 212, 0.9); }
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
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ÜST BÖLÜM: YENİ PEŞƏKAR AI LOQO (SVG)
# ---------------------------------------------------------
st.markdown("""
    <div class="nexen-logo-wrapper">
        <div class="nexen-svg-box">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 17L12 22L22 17" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 12L12 17L22 12" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div>
            <div style="font-size: 28px; font-weight: 900; background: linear-gradient(90deg, #ffffff, #c4b5fd, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.5px;">NEXEN AI</div>
            <div style="font-size: 11px; color: #94a3b8; font-weight: 600; letter-spacing: 2.5px; text-transform: uppercase;">Autonomous Short Video Engine</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h1 style='font-size:26px; font-weight:800; margin-bottom:8px; letter-spacing:-0.5px;'>Saniyələr İçində Viral Short'lar Yaradın</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8; font-size:14px;'>Ssenarinizi daxil edin; süni intellekt altyazıları, insan səslərini və peşəkar kadrları avtomatik birləşdirsin.</p>", unsafe_allow_html=True)

st.markdown('<div class="trust-banner">🔒 Təhlükəsiz E-poçt Qeydiyyatı • Hər Hesaba 1 Pulsuz Hak • Limitsiz Studio Gücü</div>', unsafe_allow_html=True)

# --- SESSION STATE & DATABASE ---
db = load_db()

if "user_email" not in st.session_state:
    st.session_state.user_email = None

col_stat1, col_stat2 = st.columns([2, 1])

with col_stat1:
    if not st.session_state.user_email:
        st.markdown("### Platformaya Giriş / Qeydiyyat")
        st.write("Davam etmək üçün e-poçt ünvanınızı daxil edin (İlk girişdə avtomatik 1 pulsuz hak verilir).")
        
        with st.form("clean_login_form"):
            email_input = st.text_input("E-poçt Ünvanı:", placeholder="ornek@gmail.com")
            login_submit = st.form_submit_button("Daxil Ol və Başla")
            
            if login_submit:
                clean_email = email_input.strip().lower()
                if "@" in clean_email and "." in clean_email and len(clean_email) > 5:
                    st.session_state.user_email = clean_email
                    if clean_email not in db:
                        db[clean_email] = {"credits": 1, "is_pro": False, "plan": "Pulsuz Sınaq"}
                        save_db(db)
                    st.success("Uğurla daxil olundu!")
                    st.rerun()
                else:
                    st.error("Zəhmət olmasa düzgün e-poçt ünvanı daxil edin (məsələn: ad@gmail.com).")
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

with col_stat2:
    st.markdown("<br>", unsafe_allow_html=True)
    if not st.session_state.user_email:
        st.markdown("<div style='background:#0f1523; color:#94a3b8; padding:12px; border-radius:12px; text-align:center; font-size:13px; border:1px solid #1e293b;'>Giriş Gözlənilir</div>", unsafe_allow_html=True)
    elif is_pro_user:
        st.markdown("<div style='background:rgba(16, 185, 129, 0.15); color:#34d399; border:1px solid rgba(16,185,129,0.3); padding:12px; border-radius:12px; text-align:center; font-weight:700;'>PRO AKTİV ⚡</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background:#0f1523; color:#fbbf24; border:1px solid rgba(251,191,36,0.3); padding:12px; border-radius:12px; text-align:center; font-weight:700;'>Qalan Hak: {current_credits}</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# ABONELİK PLANLARI ($9.99 və $29.99)
# ---------------------------------------------------------
st.markdown("<h3>Abunəlik və Paket Planları</h3>", unsafe_allow_html=True)
col_p1, col_p2 = st.columns(2)

with col_p1:
    st.markdown("""
        <div class="pricing-card">
            <h3 style="color: #c4b5fd; margin-bottom: 5px; font-size: 18px;">Aylıq Plan</h3>
            <h2 style="color: #ffffff; margin-bottom: 12px; font-size: 24px;">$9.99 <span style="font-size: 13px; color: #94a3b8; font-weight: 400;">/ ay (200 Video)</span></h2>
            <p style="color: #94a3b8; font-size: 13px;">Təməl video istehsalı və insan səsləri.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Aylıq Plan Al (Test)", key="btn_monthly"):
        if st.session_state.user_email:
            update_user_plan(st.session_state.user_email, "monthly")
            st.success("Aylıq plan aktivləşdi! 200 video əlavə olundu.")
            st.rerun()
        else:
            st.warning("Öncə giriş edin.")

with col_p2:
    st.markdown("""
        <div class="pricing-card">
            <h3 style="color: #38bdf8; margin-bottom: 5px; font-size: 18px;">Sonsuz Plan</h3>
            <h2 style="color: #ffffff; margin-bottom: 12px; font-size: 24px;">$29.99 <span style="font-size: 13px; color: #94a3b8; font-weight: 400;">/ 1 İl Limitsiz</span></h2>
            <p style="color: #94a3b8; font-size: 13px;">Bütün alətlərə və tam limitsiz rejimə giriş.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Sonsuz Plan Al (Test)", key="btn_yearly"):
        if st.session_state.user_email:
            update_user_plan(st.session_state.user_email, "yearly_unlimited")
            st.success("Sonsuz plan aktivləşdi! 1 illik limitsiz hüquq verildi.")
            st.rerun()
        else:
            st.warning("Öncə giriş edin.")

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
st.markdown("### **Adım 2:** Təbii İnsan Səsi və Karaoke Tənzimləmələri", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    voice = st.selectbox(
        "Təbii İnsan Səsi:",
        [
            "Ahmet (Təbii Kişi Səsi - Populyar)",
            "Emel (Dinamik Qadın Səsi)"
        ]
    )
with col2:
    font_size = st.slider("Altyazı Ölçüsü:", 30, 50, 40)

st.markdown("</div>", unsafe_allow_html=True)

if "Ahmet" in voice:
    voice_code = "tr-TR-AhmetNeural"
else:
    voice_code = "tr-TR-EmelNeural"

async def generate_audio(text, voice_name, output_path):
    communicate = edge_tts.Communicate(text, voice_name, rate="+8%", pitch="+2Hz")
    await communicate.save(output_path)

async def process_video_generation(text, voice_code, font_size, current_email, is_pro_user, db):
    audio_file = "temp_audio.mp3"
    output_file = "final_output.mp4"
    
    available_bgs = sorted([f for f in os.listdir(".") if f.endswith(".mp4") and f != "final_output.mp4"])
    
    if not available_bgs:
        st.error("Xəta: Serverdə heç bir fon videosu tapılmadı. Zəhmət olmasa .mp4 formatında fon videoları əlavə edin.")
        return
        
    candidates = available_bgs
    if len(available_bgs) > 1 and "last_bg" in st.session_state and st.session_state.last_bg in available_bgs:
        candidates = [b for b in available_bgs if b != st.session_state.last_bg]
    
    background_video = random.choice(candidates)
    st.session_state.last_bg = background_video
    
    await generate_audio(text, voice_code, audio_file)
    
    video = VideoFileClip(background_video)
    audio = AudioFileClip(audio_file)
    
    if video.duration > audio.duration:
        max_start = video.duration - audio.duration
        start_time = random.uniform(0, max_start)
        end_time = start_time + audio.duration
        video = video.subclipped(start_time, end_time)
    else:
        video = video.subclipped(0, video.duration)
    
    words = text.split()
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
                    color="yellow",
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
        clean_email = current_email.strip().lower()
        db[clean_email]["credits"] -= 1
        save_db(db)
    
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.success("Videonuz karaoke effekti və insan səsi ilə uğurla yaradıldı!")
    st.video(output_file)
    
    with open(output_file, "rb") as file:
        st.download_button(
            label="VİDEONU YÜKLƏ (1080P)",
            data=file,
            file_name="nexen_viral_short.mp4",
            mime="video/mp4"
        )
    st.markdown("</div>", unsafe_allow_html=True)

if st.button("VİDEONU İSTEHSAL ET"):
    if not st.session_state.user_email:
        st.warning("Video yaratmazdan əvvəl zəhmət olmasa yuxarıdakı xanaya e-poçtunuzu daxil edərək daxil olun.")
    elif current_credits <= 0 and not is_pro_user:
        st.error("Pulsuz istifadə hakqınız bitmişdir. Limitsiz video yaratmaq üçün zəhmət olmasa yuxarıdakı paketlərdən birini seçin.")
    elif not text_input.strip():
        st.warning("Zəhmət olmasa boş saxlamayın, bir mətn daxil edin.")
    else:
        loader_placeholder = st.empty()
        with loader_placeholder.container():
            st.markdown("""
                <div class="loader-box">
                    <div style="font-size: 24px; font-weight: 900; color: #38bdf8; margin-bottom: 10px;">NEXEN AI</div>
                    <p style="color: #38bdf8; letter-spacing: 2px; font-weight: 800; font-size: 14px;">VİDEO İNSAN SƏSİ VƏ KARAOKE İLƏ SİNTEZ OLUNUR...</p>
                    <p style="color: #64748b; margin-top: 0.5rem; font-size: 12px;">Sözlər saralır, fon kadrlara uyğunlaşdırılır</p>
                </div>
            """, unsafe_allow_html=True)

        try:
            asyncio.run(process_video_generation(text_input, voice_code, font_size, st.session_state.user_email, is_pro_user, db))
            loader_placeholder.empty()
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
        
