import asyncio
import os
import edge_tts
from moviepy import AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip
import streamlit as st

st.set_page_config(page_title="Shorts AI SaaS", page_icon="🚀")

st.title("🚀 AI Shorts Generator")
st.write("Minecraft fonuna uyğun gecə və motivasiya videoları yaradın!")

text_input = st.text_area(
    "Videoda səsləndiriləcək mətn (Türkcə/Azərbaycanca):",
    (
        "Bilirsinizmi, əsl uğur heç vaxt təsadüfən gəlmir. Gecə yarısı hər"
        " kəs yuxudaykən, otağında təkbaşına nəsə qurmağa çalışırsansa, deməli"
        " sən fərqlisən."
    ),
)

voice = st.selectbox(
    "Səs seçin:", ["tr-TR-AhmetNeural", "tr-TR-EmelNeural", "az-AZ-BabekNeural"]
)


async def generate_audio(text, voice_name, output_path):
  communicate = edge_tts.Communicate(text, voice_name, rate="+0%", pitch="+0Hz")
  await communicate.save(output_path)


if st.button("🎥 Videonu Yarat"):
  if not text_input.strip():
    st.warning("Zəhmət olmasa mətn daxil edin!")
  else:
    with st.spinner("Video hazırlanır, zəhmət olmasa gözləyin..."):
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

          # Sözləri bölürük və şrifti daha səliqəli, kiçik edirik
          words = text_input.split()
          clips = [video]
          duration_per_word = audio.duration / max(len(words), 1)

          chunk_size = 3  # Eyni anda 3 söz çıxsın ki, ekrana rahat sığışsın
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
                      font_size=32,  # Şrift ölçüsü kiçildildi ki, ekrana sığsın
                      color="white",
                      stroke_color="black",
                      stroke_width=1.5,
                      method="caption",
                      size=(int(video.w * 0.8), None),
                  )
                  .with_start(start_time)
                  .with_duration(end_time - start_time)
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

          st.success("🎉 Video hazırdır!")
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
                                     
