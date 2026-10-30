import asyncio
import os
import edge_tts
from moviepy import AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip
import streamlit as st

st.set_page_config(
    page_title="Shorts AI Studio | Viral Video Creation",
    page_icon="⚡",
    layout="wide",
)

# ---------------------------------------------------------
# CSS DİZAYNI (DARK NEON STYLE)
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0d0f12;
        color: #e6e8ec;
    }
    [data-testid="stSidebar"] {
        background-color: #13171f;
        border-right: 1px solid #222733;
    }
    .pro-card {
        background: linear-gradient(145deg, #181d28, #10141d);
        border: 1px solid #2a3142;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    }
    .stButton>button {
        background: linear-gradient(90deg, #f59e0b, #d97706);
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 28px !important;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #fbbf24, #f59e0b);
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.5);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# SIDEBAR - ABUNƏLİK PLANLARI
# ---------------------------------------------------------
with st.sidebar:
  st.title("⚡ Shorts AI Studio")
  st.caption("Otomatik Viral Video Platformu")
  st.divider()

  plan = st.radio(
      "Plan Seçin:",
      [
          "Ücretsiz Deneme",
          "Pro Creator ($9.99/ay)",
          "Unlimited Empire ($29.99/ay)",
      ],
      index=1,
  )

  if "Pro Creator" in plan:
    st.info("✅ Aylık 200 Video Oluşturma Hakkı")
    st.markdown(
        "[👉 Pro Pakete Geç ($9.99)](https://buy.stripe.com/test_pro_plan)"
    )
  elif "Unlimited" in plan:
    st.warning("🔥 Sınırsız Video Üretimi")
    st.markdown(
        "[👉 Sınırsız Pakete Geç"
        " ($29.99)](https://buy.stripe.com/test_unlimited_plan)"
    )

  st.divider()
  st.caption("🔒 Güvenli Ödeme Altyapısı")

# ---------------------------------------------------------
# ANA EKRAN
# ---------------------------------------------------------
st.title("🚀 Shorts AI - Viral Video Generatorü")
st.write(
    "Saniyeler içinde Minecraft fonlu, kusursuz altyazılı ve profesyonel"
    " sesli videolar üretin."
)

st.divider()

st.markdown('<div class="pro-card">', unsafe_allow_html=True)
st.subheader("📝 Senaryo ve Ses Ayarları")

text_input = st.text_area(
    "Videoda Seslendirilecek Hikaye (Türkiye Türkçesi):",
    value=(
        "Biliyor musun? Gece yarısı odasında tek başına oturup hayalleri için"
        " savaşan insanları asla küçümseme. Onlar dışarıdan yalnız görünürler"
        " ama aslında kendi imparatorluklarını kuruyorlar..."
    ),
    height=130,
)

col1, col2 = st.columns(2)
with col1:
  voice = st.selectbox(
      "🎙️ Türkçe Ses Seçimi:",
      ["tr-TR-EmelNeural (Kadın)", "tr-TR-AhmetNeural (Erkek)"],
  )
with col2:
  font_size = st.slider("🔤 Altyazı Boyutu:", 30, 55, 42)

st.markdown("</div>", unsafe_allow_html=True)

voice_code = (
    "tr-TR-EmelNeural" if "Emel" in voice else "tr-TR-AhmetNeural"
)


async def generate_audio(text, voice_name, output_path):
  communicate = edge_tts.Communicate(
      text, voice_name, rate="+5%", pitch="+0Hz"
  )
  await communicate.save(output_path)


if st.button("🚀 PROFESYONEL VİDEOYU OLUŞTUR", type="primary"):
  if not text_input.strip():
    st.warning("Lütfen bir metin girin!")
  else:
    with st.spinner("Video işleniyor, lütfen bekleyin..."):
      audio_file = "temp_audio.mp3"
      output_file = "final_output.mp4"
      background_video = "background.mp4"

      if not os.path.exists(background_video):
        st.error("Hata: 'background.mp4' dosyası bulunamadı!")
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

          st.success("🎉 Video başarıyla oluşturuldu!")
          st.video(output_file)

          with open(output_file, "rb") as file:
            st.download_button(
                label="📥 VİDEOYU İNDİR",
                data=file,
                file_name="viral_short.mp4",
                mime="video/mp4",
            )

        except Exception as e:
          st.error(f"Bir hata oluştu: {e}")
    
