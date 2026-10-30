import asyncio
import os
import edge_tts
from moviepy import AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip
import streamlit as st

st.set_page_config(page_title="Shorts AI SaaS", page_icon="🚀")

st.title("🚀 AI Shorts Generator (Pro Versiya)")
st.write("Hərf kəsilməsi düzəldilmiş və daha canlı səs sistemi!")

text_input = st.text_area(
    "Videoda səsləndiriləcək mətn (Türkiye Türkçesi):",
    (
        "Biliyor musun? Gece yarısı odasında tek başına oturup hayalleri için"
        " savaşan insanları asla küçümseme..."
    ),
)

# Səs seçimi (Emel və ya Ahmet - tonlama ilə daha təbii çıxır)
voice = st.selectbox(
    "Səs Seçin:", ["tr-TR-EmelNeural", "tr-TR-AhmetNeural"]
)


async def generate_audio(text, voice_name, output_path):
  # Səsin robotikliyini azaltmaq üçün təbii sürət və ton tənzimləməsi
  communicate = edge_tts.Communicate(
      text, voice_name, rate="+5%", pitch="+0Hz"
  )
  await communicate.save(output_path)


if st.button("🎥 Qüsursuz Video Yarat"):
  if not text_input.strip():
    st.warning("Zəhmət olmasa mətn daxil edin!")
  else:
    with st.spinner("Video və səs tənzimlənir, gözləyin..."):
      audio_file = "temp_audio.mp3"
      output_file = "final_output.mp4"
      background_video = "background.mp4"

      if not os.path.exists(background_video):
        st.error("Xəta: 'background.mp4' faylı tapılmadı!")
      else:
        asyncio.run(generate_audio(text_input, voice, audio_file))

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
                      font_size=42,
                      color="yellow",
                      stroke_color="black",
                      stroke_width=2,
                      method="caption",
                      size=(int(video.w * 0.85), None),
                      margin=(
                          15,
                          15,
                      ),  # Hərflərin quyruqlarının kəsilməməsi üçün kənar boşluğu!
                  )
                  .with_start(start_time)
                  .with_duration(max(0.15, end_time - start_time))
                  .with_position(("center", "center"))
              )
              clips.append(txt_clip)
            except Exception as t_err:
              st.write(f"Xəta: {t_err}")

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

          st.success("🎉 Video hazırdır! Hərflər və səs tənzimləndi.")
          st.video(output_file)

          with open(output_file, "rb") as file:
            st.download_button(
                label="📥 Videonu İndir",
                data=file,
                file_name="ai_short.mp4",
                mime="video/mp4",
            )

        except Exception as e:
          st.error(f"Xəta baş verdi: {e}")
              
