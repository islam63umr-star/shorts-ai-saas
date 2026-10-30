import asyncio
import os
import streamlit as st
import edge_tts
from moviepy import AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip
from moviepy.config import change_settings

# Streamlit Cloud-da altyazıların görünməsi üçün ImageMagick yolunu tənzimləyirik
try:
  change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})
except:
  pass

st.set_page_config(page_title="Shorts AI SaaS", page_icon="🚀")

st.title("🚀 AI Shorts Generator (Subway Surfers)")
st.write("Türkcə real səs və ekranda altyazı ilə avtomatik video yaradın!")

text_input = st.text_area(
    "Videoda səsləndiriləcək mətn (Türkcə):",
    "Hayatta her zaman ileri bakın, çünkü arkaya bakarsanız kaybedersiniz.",
)

# Türk səsləri ilk sırada və seçilmiş olsun
voice = st.selectbox(
    "Səs seçin:", ["tr-TR-AhmetNeural", "tr-TR-EmelNeural", "az-AZ-BabekNeural"]
)


async def generate_audio(text, voice_name, output_path):
  communicate = edge_tts.Communicate(text, voice_name, rate="+0%", pitch="+0Hz")
  await communicate.save(output_path)


if st.button("🎥 Altyazılı Video Yarat"):
  if not text_input.strip():
    st.warning("Zəhmət olmasa mətn daxil edin!")
  else:
    with st.spinner(
        "Süni intellekt real türk səsini, altyazını və videonu birləşdirir..."
    ):
      audio_file = "temp_audio.mp3"
      output_file = "final_output.mp4"
      background_video = "background.mp4"

      if not os.path.exists(background_video):
        st.error(
            "Xəta: 'background.mp4' faylı tapılmadı! Zəhmət olmasa GitHub-a"
            " background.mp4 yükləyin."
        )
      else:
        # 1. Real səsi yarat
        asyncio.run(generate_audio(text_input, voice, audio_file))

        try:
          # 2. Videonu və səsi yüklə
          video = VideoFileClip(background_video)
          audio = AudioFileClip(audio_file)

          if video.duration > audio.duration:
            video = video.subclipped(0, audio.duration)

          # 3. Ekrana altyazı əlavə etmək
          try:
            txt_clip = TextClip(
                text=text_input,
                font_size=45,
                color="white",
                bg_color="rgba(0,0,0,0.6)",
                size=(video.w * 0.9, None),
                method="caption",
            )
            txt_clip = txt_clip.with_duration(audio.duration).with_position(
                ("center", "center")
            )

            # Videonu altyazı ilə birləşdir
            video = CompositeVideoClip([video, txt_clip])
          except Exception as txt_err:
            st.warning(f"Altyazı xəbərdarlığı: {txt_err}")

          # 4. Səsi videoya ver
          final_video = video.with_audio(audio)
          final_video.write_videofile(
              output_file,
              fps=24,
              codec="libx264",
              audio_codec="aac",
              preset="ultrafast",
              logger=None,
          )

          st.success("🎉 Altyazılı və türk səslü video uğurla hazırdır!")
          st.video(output_file)

          # Endirmə düyməsi
          with open(output_file, "rb") as file:
            st.download_button(
                label="📥 Videonu yüklə",
                data=file,
                file_name="ai_short.mp4",
                mime="video/mp4",
            )

        except Exception as e:
          st.error(f"Xəta baş verdi: {e}")
