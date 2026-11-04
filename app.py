import asyncio
import json
import os
import random
import uuid
import streamlit as st
import edge_tts
from moviepy import AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip

st.set_page_config(
    page_title="Nexen AI | Autonomous Short Video Engine", page_icon="⚡", layout="centered"
)

# --- VERİTABANI YÖNETİMİ ---
DB_FILE = "users_db.json"
DEVICE_DB_FILE = "devices_db.json"

def load_db(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_db(db, file_path):
    with open(file_path, "w") as f:
        json.dump(db, f, indent=4)

# --- URL QUERY PARAMETERS İLƏ DAİMİ CİHAZ TANIMA ---
query_params = st.query_params
if "device" not in query_params or not query_params["device"]:
    new_device_id = str(uuid.uuid4())
    st.query_params["device"] = new_device_id
    current_device = new_device_id
else:
    current_device = query_params["device"]

def process_successful_payment(email, plan_type):
    db = load_db(DB_FILE)
    if email in db:
        if plan_type == "monthly":
            db[email]["credits"] = 200  
            db[email]["plan"] = "Aylık Plan (200 Video)"
            db[email]["is_pro"] = True
        elif plan_type == "yearly_unlimited":
            db[email]["credits"] = 99999  
            db[email]["plan"] = "Sonsuz Plan (1 Yıl)"
            db[email]["is_pro"] = True
        save_db(db, DB_FILE)
        return True
    return False

# ---------------------------------------------------------
# NEXEN - STİL AYARLARI
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
    @keyframes nexen-continuous-spin {
        0% { transform: rotate(0deg) scale(1); filter: drop-shadow(0 0 10px rgba(139, 92, 246, 0.8)); }
        50% { transform: rotate(180deg) scale(1.08); filter: drop-shadow(0 0 20px rgba(56, 189, 248, 1)); }
        100% { transform: rotate(360deg) scale(1); filter: drop-shadow(0 0 10px rgba(139, 92, 246, 0.8)); }
    }
    .spinning-ai-logo-small {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 45px;
        height: 45px;
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 50%, #06b6d4 100%);
        border-radius: 12px;
        animation: nexen-continuous-spin 2s linear infinite;
        box-shadow: 0 0 20px rgba(147, 51, 234, 0.7);
    }
    .loader-box-compact {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 18px 24px;
        background: rgba(11, 16, 27, 0.95);
        border-radius: 16px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        margin: 1.5rem 0;
        box-shadow: 0 15px 30px rgba(0,0,0,0.6);
    }
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
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ÜST BÖLÜM: AI LOQO
# ---------------------------------------------------------
st.markdown('<div class="nexen-logo-wrapper"><div class="nexen-svg-box"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 17L12 22L22 17" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 12L12 17L22 12" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></div><div><div style="font-size: 28px; font-weight: 900; background: linear-gradient(90deg, #ffffff, #c4b5fd, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.5px;">NEXEN AI</div><div style="font-size: 11px; color: #94a3b8; font-weight: 600; letter-spacing: 2.5px; text-transform: uppercase;">Autonomous Short Video Engine</div></div></div>', unsafe_allow_html=True)

st.markdown("<h1 style='font-size:26px; font-weight:800; margin-bottom:8px; letter-spacing:-0.5px;'>Saniyeler İçinde Viral Short'lar Üretin</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8; font-size:14px;'>Senaryonuzu girin; yapay zeka altyazıları, profesyonel insan seslerini ve görüntüleri otomatik birleştirsin.</p>", unsafe_allow_html=True)

st.markdown('<div class="trust-banner">🔒 URL Tabanlı Cihaz Kilidi • Haklar Asla Sıfırlanmaz • Sınırsız Stüdyo Gücü</div>', unsafe_allow_html=True)

# --- VERİTABANI & CİHAZ YÖNETİMİ ---
db = load_db(DB_FILE)
device_db = load_db(DEVICE_DB_FILE)

if "user_email" not in st.session_state:
    st.session_state.user_email = None

auto_recognized_email = None
for saved_email, dev_id in device_db.items():
    if dev_id == current_device:
        auto_recognized_email = saved_email
        break

if auto_recognized_email and not st.session_state.user_email:
    st.session_state.user_email = auto_recognized_email

col_stat1, col_stat2 = st.columns([2, 1])

with col_stat1:
    if not st.session_state.user_email:
        st.markdown("### Platforma Giriş / Kayıt")
        st.write("E-posta adresinizi girin (Cihazınız URL üzerinden kilitlenir ve haklarınız korunur).")
        
        with st.form("clean_login_form"):
            email_input = st.text_input("E-posta Adresi:", placeholder="ornek@gmail.com")
            login_submit = st.form_submit_button("Giriş Yap ve Haklarımı Getir")
            
            if login_submit:
                clean_email = email_input.strip().lower()
                valid_domains = ["gmail.com", "mail.ru", "outlook.com", "yahoo.com", "hotmail.com"]
                is_valid_domain = any(clean_email.endswith("@" + domain) for domain in valid_domains)
                
                if is_valid_domain:
                    existing_email_for_device = None
                    for semail, did in device_db.items():
                        if did == current_device:
                            existing_email_for_device = semail
                            break
                    
                    if existing_email_for_device and existing_email_for_device != clean_email:
                        st.error(f"Bu cihaz zaten '{existing_email_for_device}' hesabına bağlıdır! Ücretsiz hak hakkınızı bu cihazdan zaten kullandınız.")
                    else:
                        st.session_state.user_email = clean_email
                        if clean_email not in db:
                            db[clean_email] = {"credits": 1, "is_pro": False, "plan": "Ücretsiz Deneme"}
                            save_db(db, DB_FILE)
                        
                        device_db[clean_email] = current_device
                        save_db(device_db, DEVICE_DB_FILE)
                        st.success("Cihazınız başarıyla doğrulandı!")
                        st.rerun()
                else:
                    st.error("Lütfen geçerli bir e-posta uzantısı girin (@gmail.com, @mail.ru vb.).")
    else:
        st.success(f"Tanınan Hesap: {st.session_state.user_email} (Kilitli 🔒)")
        if st.button("Çıkış Yap"):
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
        st.markdown("<div style='background:#0f1523; color:#94a3b8; padding:12px; border-radius:12px; text-align:center; font-size:13px; border:1px solid #1e293b;'>Cihaz Bekleniyor</div>", unsafe_allow_html=True)
    elif is_pro_user:
        st.markdown("<div style='background:rgba(16, 185, 129, 0.15); color:#34d399; border:1px solid rgba(16,185,129,0.3); padding:12px; border-radius:12px; text-align:center; font-weight:700;'>PRO AKTİF ⚡</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background:#0f1523; color:#fbbf24; border:1px solid rgba(251,191,36,0.3); padding:12px; border-radius:12px; text-align:center; font-weight:700;'>Kalan Hak: {current_credits}</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# ABONELİK PLANLARI
# ---------------------------------------------------------
st.markdown("<h3>Abonelik ve Paket Planları</h3>", unsafe_allow_html=True)
col_p1, col_p2 = st.columns(2)

with col_p1:
    st.markdown("""
        <div class="pricing-card">
            <h3 style="color: #c4b5fd; margin-bottom: 5px; font-size: 18px;">Aylık Plan</h3>
            <h2 style="color: #ffffff; margin-bottom: 12px; font-size: 24px;">$9.99 <span style="font-size: 13px; color: #94a3b8; font-weight: 400;">/ ay (200 Video)</span></h2>
            <p style="color: #94a3b8; font-size: 13px;">Ödeme onaylandığı an 200 video hakkı hesabınıza kalıcı olarak yüklenir.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Ödemeyi Yap ve Aylık Planı Al", key="btn_monthly"):
        if st.session_state.user_email:
            success = process_successful_payment(st.session_state.user_email, "monthly")
            if success:
                st.success("Ödeme başarıyla onaylandı! 200 video hakkı hesabınıza eklendi.")
                st.rerun()
        else:
            st.warning("Önce giriş yapmalısınız.")

with col_p2:
    st.markdown("""
        <div class="pricing-card">
            <h3 style="color: #38bdf8; margin-bottom: 5px; font-size: 18px;">Sonsuz Plan</h3>
            <h2 style="color: #ffffff; margin-bottom: 12px; font-size: 24px;">$29.99 <span style="font-size: 13px; color: #94a3b8; font-weight: 400;">/ 1 Yıl Sınırsız</span></h2>
            <p style="color: #94a3b8; font-size: 13px;">Ödeme onaylandığı an sınırsız mod kalıcı olarak aktifleşir.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Ödemeyi Yap ve Sonsuz Planı Al", key="btn_yearly"):
        if st.session_state.user_email:
            success = process_successful_payment(st.session_state.user_email, "yearly_unlimited")
            if success:
                st.success("Ödeme başarıyla onaylandı! 1 yıllık sınırsız hak tanımlandı.")
                st.rerun()
        else:
            st.warning("Önce giriş yapmalısınız.")

st.divider()
st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# VİDEO ÜRETİM PANELİ
# ---------------------------------------------------------
st.markdown('<div class="main-box">', unsafe_allow_html=True)
st.markdown("### **Adım 1:** Metninizi veya Senaryonuzu Girin", unsafe_allow_html=True)

text_input = st.text_area(
    "Metin:",
    value="",
    height=130,
    placeholder="Videoda seslendirilmesini istediğiniz metni buraya yazın...",
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### **Adım 2:** Profesyonel İnsan Sesi ve Altyazı Ayarları", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    voice = st.selectbox(
        "Profesyonel İnsan Sesi:",
        [
            "Murat (Ağırbaşlı ve Derin Erkek Sesi - Çok Popüler)",
            "Deniz (Profesyonel Canlı Kadın Sesi)",
            "Ahmet (Dinamik Genç Podkast Sesi)"
        ]
    )
with col2:
    font_size = st.slider("Altyazı Boyutu:", 30, 50, 40)

st.markdown("</div>", unsafe_allow_html=True)

if "Murat" in voice:
    voice_code = "tr-TR-MuratNeural"
elif "Deniz" in voice:
    voice_code = "tr-TR-DenizNeural"
else:
    voice_code = "tr-TR-AhmetNeural"

async def generate_audio(text, voice_name, output_path):
    communicate = edge_tts.Communicate(text, voice_name, rate="-6%", pitch="+0Hz")
    await communicate.save(output_path)

async def process_video_generation(text, voice_code, font_size, current_email, is_pro_user, db):
    audio_file = "temp_audio.mp3"
    output_file = "final_output.mp4"
    
    available_bgs = sorted([f for f in os.listdir(".") if f.endswith(".mp4") and f != "final_output.mp4"])
    
    if not available_bgs:
        st.error("Hata: Sunucuda hiçbir arka plan videosu bulunamadı. Lütfen .mp4 formatında arka plan videoları ekleyin.")
        return
        
    candidates = available_bgs
    if len(available_bgs) > 1 and "last_bg" in st.session_state and st.session_state.last_bg in available_bgs:
        candidates = [b for b in available_bgs if b != st.session_state.last_bg]
    
    background_video = random.choice(candidates)
    st.session_state.last_bg = background_video
    
    try:
        await generate_audio(text, voice_code, audio_file)
    except Exception as e:
        raise RuntimeError(f"Ses sintezi sırasında Microsoft sunucu hatası: {e}")
    
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
        save_db(db, DB_FILE)
    
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.success("Videomuz karaoke efekti ve profesyonel insan sesiyle başarıyla oluşturuldu!")
    st.video(output_file)
    
    with open(output_file, "rb") as file:
        st.download_button(
            label="VİDEOYU İNDİR (1080P)",
            data=file,
            file_name="nexen_viral_short.mp4",
            mime="video/mp4"
        )
    st.markdown("</div>", unsafe_allow_html=True)

if st.button("VİDEOYU ÜRET"):
    if not st.session_state.user_email:
        st.warning("Video üretmeden önce lütfen yukarıdaki alana e-postanızı girerek giriş yapın.")
    elif current_credits <= 0 and not is_pro_user:
        st.error("Ücretsiz kullanım hakkınız kalmamıştır. Sınırsız video üretmek için lütfen yukarıdaki paketlerden birini seçin.")
    elif not text_input.strip():
        st.warning("Lütfen boş bırakmayın, bir metin girin.")
    else:
        loader_placeholder = st.empty()
        with loader_placeholder.container():
            st.markdown(
                '<div class="loader-box-compact"><div class="spinning-ai-logo-small"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 17L12 22L22 17" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 12L12 17L22 12" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></div><div><div style="font-size: 15px; font-weight: 800; color: #38bdf8; letter-spacing: 1px;">NEXEN AI ENGINE</div><div style="color: #94a3b8; font-size: 12px; margin-top: 2px;">Video profesyonel ses ve altyazı ile sentezleniyor...</div></div></div>',
                unsafe_allow_html=True
            )

        try:
            asyncio.run(process_video_generation(text_input, voice_code, font_size, st.session_state.user_email, is_pro_user, db))
            loader_placeholder.empty()
        except Exception as err:
            loader_placeholder.empty()
            st.error(f"İşlem sırasında hata oluştu: {err}")

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: #64748b; font-size: 13px;'>
        <p>Nexen Engine — Tüm hakları saklıdır. © 2026</p>
        <p>Destek: <a href='mailto:shortaipro@gmail.com' style='color: #a78bfa; text-decoration: none;'>shortaipro@gmail.com</a></p>
    </div>
""", unsafe_allow_html=True)
