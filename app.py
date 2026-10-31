import asyncio
import os
import edge_tts
from moviepy import AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip
import streamlit as st

st.set_page_config(
    page_title="Shorts AI Studio | Pro Creator", page_icon="✨", layout="centered"
)

# --- SİSTEM ÜÇÜN NÖVBƏLİ VİDEO SAYĞACI (DÖVRİ SİSTEM) ---
if "bg_index" not in st.session_state:
  st.session_state.bg_index = 0

# ---------------------------------------------------------
# PROFESSIONAL SAAS & PRICING DİZAYNI (TÜRKÇE)
# ---------------------------------------------------------
st.markdown(
    """
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
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# ANA EKRAN & TEST HƏDİYYƏ BİLDİRİŞİ
# ---------------------------------------------------------
st.markdown(
    '<div><span class="badge">✨ AI-POWERED VIRAL SHORTS ENGINE</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    "<h1"
    " style='font-size:32px; font-weight:800; margin-bottom:5px;'>Saniyeler"
    " İçinde Viral Short'lar Üretin</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color:#9ca3af; font-size:15px;'>İstediğiniz konuyu yazın,"
    " kusursuz altyazı ve yapay zeka seslendirmesi ile videonuz saniyeler içinde"
    " hazırdır.</p>",
    unsafe_allow_html=True,
)

# İstifadəçiyə dərhal hər şeyin işlədiyini göstərmək üçün sınaq məlumatı:
st.info(
    "🎁 **Pro Sınaq Rejimi Aktivdir:** Sistemi yoxlamaq üçün bu gün 1 pulsuz"
    " viral video haqqınız var!"
)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# ABONELİK PLANLARI (LOKALİZASİYA - TÜRKÇE)
# ---------------------------------------------------------
st.markdown("<h3>💳 Abonelik Planları</h3>", unsafe_allow_html=True)
col_p1, col_p2 = st.columns(2)

with col_p1:
  st.markdown(
      """
        <div class="pricing-card">
            <h3 style="color: #c084fc; margin-bottom: 5px;">Pro Creator</h3>
            <h2 style="color: #ffffff; margin-bottom: 15px;">$9.99 <span style="font-size: 14px; color: #9ca3af;">/ ay</span></h2>
            <p style="color: #9ca3af; font-size: 13px;">Ayda 200 viral video, 1080p kalite ve profesyonel altyazı.</p>
        </div>
        """,
      unsafe_allow_html=True,
  )
  st.markdown(
      "[👉 Pro Paket Satın Al (Test"
      " Et)](https://lemonsqueezy.com/buy/your-pro-link)",
      unsafe_allow_html=True,
  )

with col_p2:
  st.markdown(
      """
        <div class="pricing-card">
            <h3 style="color: #38bdf8; margin-bottom: 5px;">Unlimited</h3>
            <h2 style="color: #ffffff; margin-bottom: 15px;">$29.99 <span style="font-size: 14px; color: #9ca3af;">/ ay</span></h2>
            <p style="color: #9ca3af; font-size: 13px;">Sınırsız video üretimi, 7/24 öncelikli yüksek sunucu gücü.</p>
        </div>
        """,
      unsafe_allow_html=True,
  )
  st.markdown(
      "[👉 Sınırsız Paket Satın Al](https://lemonsqueezy.com/buy/your-unlimited-link)",
      unsafe_allow_html=True,
  )

st.divider()
st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# VİDEO OLUŞTURMA PANELİ
# ---------------------------------------------------------
st.markdown('<div class="main-box">', unsafe_allow_html=True)
st.markdown(
    "### 📝 **Adım 1:** Hikayenizi veya Senaryonuzu Yazın",
    unsafe_allow_html=True,
)

default_story = (
    "Dünyanın en zengin insanlarının hayatını değiştiren o tek sırrı biliyor"
    " musun? Çoğu insan sabah uyandığında telefonu eline alır ve saatlerce boş"
    " boş kaydırarak gününü çöpe atar. Ama o çok başarılı olan %1'lik kesim,"
    " uyanır uyanmaz zihnini eğitmeye başlar. Bilim insanları kanıtladı: Her gün"
    " sadece bir dakikanı bile kendi hedeflerine adarsan, bir yılın sonunda"
    " etrafındaki herkesi geride bırakırsın. Şimdi bu videoyu da diğerleri gibi"
    " geçip gidecek misin, yoksa kendi imparatorluğunu kuran o %1'lik cesur"
    " insanlardan biri olacak mısın? Seçim senin. Abone ol ve gücünü herkese"
    " göster!"
)

text_input = st.text_area(
    "Metin:", value=default_story, height=140, label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    "### 🎙️ **Adım 2:** Ses ve Tasarım Ayarları", unsafe_allow_html=True
)

col1, col2 = st.columns(2)
with col1:
  voice = st.selectbox(
      "Ses Modeli:", ["tr-TR-EmelNeural (Canlı Kadın)", "tr-TR-AhmetNeural (Erkek)"]
  )
with col2:
  font_size = st.slider("Altyazı Font Boyutu:", 30, 50, 40)

st.markdown("</div>", unsafe_allow_html=True)

voice_code = (
    "tr-TR-EmelNeural" if "Emel" in voice else "tr-TR-AhmetNeural"
)


async def generate_audio(text, voice_name, output_path):
  communicate = edge_tts.Communicate(
      text, voice_name, rate="+5%", pitch="+0Hz"
  )
  await communicate.save(output_path)


if st.button("✨ VİDEOYU SİHİRLİ ŞEKİLDE OLUŞTUR"):
  if not text_input.strip():
    st.warning("Lütfen bir metin girin!")
  else:
    with st.spinner(
        "🚀 Yapay zeka çalışıyor: Ses senkronize ediliyor, altyazılar"
        " işleniyor..."
    ):
      audio_file = "temp_audio.mp3"
      output_file = "final_output.mp4"

      # --- NÖVBƏLİ (DÖVRİ) VİDEO SEÇİM SİSTEMİ ---
      available_bgs = sorted(
          [
              f
              for f in os.listdir(".")
              if f.endswith(".mp4") and f != "final_output.mp4"
          ]
      )

      if not available_bgs:
        st.error(
            "Hata: Sunucuda hiç fon videosu bulunamadı! Lütfen GitHub'a .mp4"
            " uzantılı videolar yükleyin."
        )
      else:
        # Hər dəfə növbəti videoya keçir (sıra ilə dövr edir)
        background_video = available_bgs[
            st.session_state.bg_index % len(available_bgs)
        ]
        st.session_state.bg_index += 1  # Növbəti dəfə sonrakı video seçiləcək

        st.info(
            f"🎬 Arka Plan (Növbəli Sıra): {background_video} istifadə olundu."
        )

        asyncio.run(generate_audio(text_input, voice_code, audio_file))

        try:
          video = VideoFileClip(background_video)
          audio = AudioFileClip(audio_file)

          if video.duration > audio.duration:
            video = video.subclipped(0, audio.duration)

          words = text_input.split()
          clips = [video]

          total_words = len(words)
          time_per_word = audio.duration / max(total_words, 1)

          chunk_size = 2
          for i in range(0, total_words, chunk_size):
            chunk = " ".join(words[i : i + chunk_size])
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
                      margin=(20, 20),
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
              logger=None,
          )

          st.markdown('<div class="main-box">', unsafe_allow_html=True)
          st.success("🎉 Videonuz başarıyla oluşturuldu!")
          st.video(output_file)

          with open(output_file, "rb") as file:
            st.download_button(
                label="📥 VİDEOYU İNDİR (1080P)",
                data=file,
                file_name="viral_short_pro.mp4",
                mime="video/mp4",
            )
          st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
          st.error(f"Hata oluştu: {e}")
