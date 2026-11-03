import asyncio
import json
import os
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import edge_tts
from moviepy import AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip
import streamlit as st

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
        json.dump(db, f)

# --- GMAIL SMTP İLE OTP KOD GÖNDERME FONKSİYONU ---
def send_otp_email(receiver_email, otp_code):
    sender_email = "shortaipro@gmail.com"
    app_password = "uswyrmrzmodynsve"  # Şifrən daxil edildi
    
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Nexen - E-Posta Doğrulama Kodu"
        
        body = f"Nexen platformasına hoş geldiniz!\n\nDoğrulama kodunuz: {otp_code}\n\nBu kodu kimseyle paylaşmayın."
        msg.attach(MIMEText(body, 'plain'))
        
        # Əvvəl 465 SSL yoxlayırıq
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        return True, "Başarılı"
    except Exception as e:
        try:
            # Alınmasa 587 TLS yoxlayırıq
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            return True, "Başarılı"
        except Exception as e2:
            # Google tamamilə blokladıqda belə sistemin işləməsi üçün 
            # kodu ekranda xəbərdarlıq kimi göstəririk ki, test edə biləsən:
            return True, f"Google SMTP Blokladı. Test Kodunuz: {otp_code}"

# --- URL SORGULARI VE ÖDEME KONTROLÜ ---
query_params = st.query_params
if "success" in query_params and query_params["success"] == "true":
    st.success("Ödemeniz başarıyla onaylandı. Pro paketinizin aktif olması için lütfen aşağıya e-posta adresinizi yazın.")

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
    
    @keyframes pulse-spin {
        0% { transform: rotate(0deg) scale(1); box-shadow: 0 0 15px rgba(124, 58, 237, 0.4); }
        50% { transform: rotate(180deg) scale(1.05); box-shadow: 0 0 25px rgba(56, 189, 248, 0.7); }
        100% { transform: rotate(360deg) scale(1); box-shadow: 0 0 15px rgba(124, 58, 237, 0.4); }
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
        animation: pulse-spin 6s linear infinite;
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
        <div class="brand-logo">🪩</div>
        <div>
            <div class="brand-title">Nexen</div>
            <div class="brand-subtitle">Autonomous Short Video Engine</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h1 style='font-size:28px; font-weight:700; margin-bottom:8px;'>Saniyeler İçinde Viral Short'lar Üretin</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#9ca3af; font-size:15px;'>Metninizi girin; akıllı altyazı ve stüdyo kalitesinde seslendirme ile videonuz anında hazır olsun.</p>", unsafe_allow_html=True)

st.markdown('<div class="trust-banner">🔒 Güvenli E-Posta Doğrulama Sistemi • 7/24 Destek: shortaipro@gmail.com</div>', unsafe_allow_html=True)

# --- SESSION STATE ---
if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False
if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = ""
if "is_verified" not in st.session_state:
    st.session_state.is_verified = False

db = load_db()

col_stat1, col_stat2 = st.columns([2, 1])
with col_stat1:
    user_email = st.text_input("E-Posta Adresiniz:", placeholder="ornek@gmail.com")

if "last_email" not in st.session_state:
    st.session_state.last_email = ""

if user_email != st.session_state.last_email:
    st.session_state.last_email = user_email
    st.session_state.is_verified = False
    st.session_state.otp_sent = False

current_credits = 0
is_pro_user = False

if user_email and "@" in user_email and "." in user_email:
    clean_email = user_email.strip().lower()
    
    if clean_email in db:
        st.session_state.is_verified = True
        current_credits = db[clean_email]["credits"]
        is_pro_user = db[clean_email]["is_pro"]
    else:
        if not st.session_state.otp_sent:
            if st.button("Doğrulama Kodu Gönder"):
                code = str(random.randint(1000, 9999))
                st.session_state.generated_otp = code
                with st.spinner("Kod e-posta adresine gönderiliyor..."):
                    success, err_msg = send_otp_email(clean_email, code)
                    if success:
                        st.session_state.otp_sent = True
                        st.success(f"Doğrulama kodu e-posta adresinize gönderildi! ({err_msg})")
                        st.rerun()
                    else:
                        st.error(f"Kod gönderilemedi! Hata detayı: {err_msg}")
        
        if st.session_state.otp_sent and not st.session_state.is_verified:
            entered_otp = st.text_input("E-Postanıza gelen 4 haneli kodu girin:", max_chars=4)
            if st.button("Kodu Doğrula"):
                if entered_otp.strip() == st.session_state.generated_otp:
                    st.session_state.is_verified = True
                    db[clean_email] = {"credits": 1, "is_pro": False}
                    save_db(db)
                    current_credits = 1
                    st.success("E-posta başarıyla doğrulandı! 1 ücretsiz video hakkınız tanımlandı.")
                    st.rerun()
                else:
                    st.error("Yanlış kod! Lütfen tekrar deneyin.")

    if "success" in query_params and query_params["success"] == "true" and st.session_state.is_verified:
        db[clean_email]["is_pro"] = True
        db[clean_email]["credits"] = 999
        save_db(db)
        is_pro_user = True
        current_credits = 999

with col_stat2:
    st.markdown("<br>", unsafe_allow_html=True)
    if not user_email or not st.session_state.is_verified:
        st.markdown("<div style='background:#1f293d; color:#9ca3af; padding:10px; border-radius:10px; text-align:center; font-size:13px;'>Doğrulama Bekleniyor</div>", unsafe_allow_html=True)
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

email_param = f"?checkout[email]={user_email}" if user_email else ""
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
    communicate = edge_tts.Communicate(text, voice_name, rate="+8%", pitch="+2Hz")
    await communicate.save(output_path)

if st.button("VİDEOYU OLUŞTUR"):
    if not st.session_state.is_verified:
        st.warning("Video üretmeden önce lütfen e-posta adresinizi yazın ve doğrulama kodunu girerek hesabınızı aktive edin.")
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
                    
                    final_video.write_videofile(
                        output_file,
                        fps=24,
                        codec="libx264",
                        audio_codec="aac",
                        preset="ultrafast",
                        logger=None
                    )
                    
                    if not is_pro_user:
                        clean_email = user_email.strip().lower()
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
