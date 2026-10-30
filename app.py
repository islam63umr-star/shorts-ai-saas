import asyncio
import os
import edge_tts
from moviepy import AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip
import streamlit as st

st.set_page_config(page_title="Shorts AI SaaS", page_icon="🚀")

st.title("🚀 AI Shorts Generator")
st.write("Dinamik altyazılı və real türk səsli video generatoru!")

text_input = st.text_area(
    "Videoda səsləndiriləcək mətn (Türkçe):",
    "1914 yılında iki kardeş, fırtınalı bir gecede denize açıldı. Dalgalar teknelerini alabora ettiğinde herkes onların yok olduğunu sandı.",
)

voice = st.selectbox(
    "Ses seçin:", ["tr-TR-AhmetNeural", "tr-TR-EmelNeural", "az-AZ-BabekNeural"]
)


async def generate_audio(text, voice_name, output_path):
  communicate = edge_tts.Communicate(text, voice_name, rate="+0%", pitch="+0Hz")
  await communicate.save(output_path)


if st.button("🎥 Dinamik Altyazılı Video Oluştur"):
  if not text_input.strip():
    st.warning("Lütfen bir metin girin!")
  else:
    with st.spinner(
        "Səs, dinamik altyazı və video sinxronlaşdırılır, gözləyin..."
    ):
      audio_file = "temp_audio.mp3"
      output_file = "final_output.mp4"
      background_video = "background.mp4"

      if not os.path.exists(background_video):
        st.error(
            "Hata: 'background.mp4' dosyası bulunamadı! Lütfen GitHub'a"
            " background.mp4 yükleyin."
        )
      else:
        # 1. Səsi yarat
        asyncio.run(generate_audio(text_input, voice, audio_file))

        try:
          video = VideoFileClip(background_video)
          audio = AudioFileClip(audio_file)

          if video.duration > audio.duration:
            video = video.subclipped(0, audio.duration)

          # Mətni sözlərə bölüb ardıcıl yerləşdiririk
          words = text_input.split()
          clips = [video]
          duration_per_word = audio.duration / max(len(words), 1)

          chunk_size = 4  # Eyni anda neçə söz görünəcək
          for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i : i + chunk_size])
            start_time = (i / chunk_size) * (
                audio.duration / (len(words) / chunk_size)
            )
            end_time = min(start_time + (duration_per_word * chunk_size), audio.duration)

            try:
              txt_clip = (
                  TextClip(
                      text=chunk,
                      font_size=50,
                      color="white",
                      stroke_color="black",
                      stroke_width=2,
                      method="caption",
                      size=(int(video.w * 0.9), None),
                  )
                  .with_start(start_time)
                  .with_duration(end_time - start_time)
                  .with_position(("center", "center"))
              )
              clips.append(txt_clip)
            except Exception:
              pass

          # Bütün klipləri birləşdiririk
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

          st.success("🎉 Dinamik altyazılı video hazırdır!")
          st.video(output_file)

          with open(output_file, "rb") as file:
            st.download_button(
                label="📥 Videonu İndir",
                data=file,
                file_name="ai_short.mp4",
                mime="video/mp4",
            )

        except Exception as e:
          st.error(f"Hata oluştu: {e}")
