import asyncio
import os
import edge_tts
from moviepy import AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip
import streamlit as st

st.set_page_config(page_title="Shorts AI SaaS", page_icon="🚀")

st.title("🚀 AI Shorts Generator (Türkiye Pazarı İçin)")
st.write(
    "Tamamen doğal Türkiye Türkçesi ləhcəsi və boşluksuz, səliqəli altyazı"
    " sistemi!"
)

text_input = st.text_area(
    "Videoda səsləndiriləcək mətn (Türkiye Türkçesi):",
    (
        "Köyün ortasında, herkesin uyuduğu gece saatlerinde odasında çalışan bir"
        " genç vardı. Kimseye kulak asmadan kendi geleceğini inşa ediyordu."
        " Çünkü gerçek başarı sabırla kazanılır!"
    ),
)

# Sırf Türkiye Türkçəsi üçün ən təbii neural səslər
voice = st.selectbox(
    "Türkiye Türkçesi Ses Seçin:", ["tr-TR-AhmetNeural", "tr-TR-EmelNeural"]
)


async def generate_audio(text, voice_name, output_path):
  communicate = edge_tts.Communicate(text, voice_name, rate="+0%", pitch="+0Hz")
  await communicate.save(output_path)


if st.button("🎥 Profesyonel Video Oluştur"):
  if not text_input.strip():
    st.warning("Lütfen bir metin girin!")
  else:
    with st.spinner("Türkiye Türkçesi ses, altyazı ve video işleniyor..."):
      audio_file = "temp_audio.mp3"
      output_file = "final_output.mp4"
      background_video = "background.mp4"

      if not os.path.exists(background_video):
        st.error("Hata: 'background.mp4' dosyası bulunamadı!")
      else:
        # 1. Səsi təmiz Türkiyə türkcəsində yaradırıq
        asyncio.run(generate_audio(text_input, voice, audio_file))

        try:
          video = VideoFileClip(background_video)
          audio = AudioFileClip(audio_file)

          if video.duration > audio.duration:
            video = video.subclipped(0, audio.duration)

          # Mətni sözlərə ayırırıq
          words = text_input.split()
          clips = [video]

          # Sözlərin arasında boşluq qalmaması üçün hər sözün sürətini səsə görə hesablayırıq
          total_words = len(words)
          time_per_word = audio.duration / max(total_words, 1)

          # Hər dəfə 2-3 söz ekranda axıcı şəkildə, boşluqsuz dəyişəcək
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
                      font_size=40,
                      color="yellow",  # Diqqət çəkən profesyonel sarı rəng
                      stroke_color="black",
                      stroke_width=2,
                      method="caption",
                      size=(int(video.w * 0.85), None),
                  )
                  .with_start(start_time)
                  .with_duration(
                      max(0.1, end_time - start_time)
                  )  # Boşluq qalmaması üçün minimum müddət
                  .with_position(("center", "center"))
              )
              clips.append(txt_clip)
            except Exception as t_err:
              st.write(f"Altyazı hatası: {t_err}")

          final_video = CompositeVideoClip(clips)
          final_video = final_video.with_audio(audio)

          final_video.write_videofile(
              output_file,
          )

          st.success("🎉 Video hazır! Türkiyə bazarı üçün tam uyğundur.")
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
