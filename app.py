import asyncio
import os
import edge_tts
from moviepy import AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip
import streamlit as st

st.set_page_config(
    page_title="Shorts AI Studio | Pro Creator", page_icon="✨", layout="centered"
)

# ---------------------------------------------------------
# CAPCUT / OPUS CLIIP İLHAMLI MİNİMALİST & PRO DİZAYN (CSS)
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
        font-family: 'Inter', sans-serif;
    }
    
    /* Əsas Konteyner Kartı */
    .main-box {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 30px;
        backdrop-filter: blur(10px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
        margin-bottom: 25px;
    }
    
    /* Nəhəng AI Generator Düyməsi */
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
    
    /* Nişanlar (Badges) */
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
# SIDEBAR - ABUNƏLİK VƏ QİYMƏTLƏR (Stripe Entegrasyonu)
# ---------------------------------------------------------
with st.sidebar:
  st.markdown("### ⚡ Shorts AI Studio")
  st.caption("Next-Gen Video Generation Engine")
  st.divider()

  st.markdown("#### 💳 Abonelik Planları")
  plan = st.selectbox(
      "Seçim:", ["Pro Creator ($9.99 / 200 Video)", "Unlimited Empire ($29.99 / Sonsuz)"]
  )

  if "Pro" in plan:
    st.info(
        "✨ **Pro Paket:** Ayda 200 viral video, 1080p render, təmiz"
        " altyazı."
    )
    st.markdown(
        "[👉 Pro Abone Ol ($9.99)](https://buy.stripe.com/test_pro_plan)"
    )
  else:
    st.success(
        "🔥 **Unlimited:** Sınırsız video, 7/24 öncelikli server gücü."
    )
    st.markdown(
        "[👉 Sınırsız Al ($29.99)](https://buy.stripe.com/test_unlimited_plan)"
    )

  st.divider()
  st.caption("🔒 256-Bit SSL Secured by Stripe")

# ---------------------------------------------------------
# ANA EKRAN (CAPCUT / OPUS ÜSLUBU)
# ---------------------------------------------------------
st.markdown(
    '<div><span class="badge">✨ AI-POWERED SHORTS ENGINE v3.0</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    "<h1"
    " style='font-size:32px; font-weight:800; margin-bottom:5px;'>Saniyeler"
    " İçinde Viral Short'lar Üretin</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color:#9ca3af; font-size:15px;'>Minecraft fonu, kusursuz"
    " senkronize altyazı ve insan doğallığında yapay zeka sesi ile kitleni"
    " büyüt.</p>",
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# Əsas Giriş Kartı
st.markdown('<div class="main-box">', unsafe_allow_html=True)
st.markdown(
    "### 📝 **Adım 1:** Hikayeni veya Senaryonu Gir",
    unsafe_allow_html=True,
)

text_input = st.text_area(
    "Metin (Türkiye Türkçesi):",
    value=(
        "Biliyor musun? Gece yarısı odasında tek başına oturup hayalleri için"
        " savaşan insanları asla küçümseme. Onlar dışarıdan yalnız görünürler"
        " ama aslında kendi imparatorluklarını kuruyorlar..."
    ),
    height=120,
    label_visibility="collapsed",
)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🎙️ **Adım 2:** Ses ve Tasarım Ayarları", unsafe_allow_html=True)

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


# Render Düğməsi
if st.button("✨ VİDEOYU SİHİRLİ ŞEKİLDE OLUŞTUR"):
  if not text_input.strip():
    st.warning("Lütfen bir metin girin!")
  else:
    with st.spinner(
        "🚀 AI motoru çalışıyor: Ses senkronize ediliyor, altyazılar işleniyor..."
    ):
      audio_file = "temp_audio.mp3"
      output_file = "final_output.mp4"
      background_video = "background.mp4"

      if not os.path.exists(background_video):
        st.error(
            "Hata: 'background.mp4' dosyası sunucuda bulunamadı! Lütfen"
            " yükleyin."
        )
      else:
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
    
