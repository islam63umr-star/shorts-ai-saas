import asyncio
import os
import edge_tts
from moviepy import AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip
import streamlit as st

st.set_page_config(page_title="Shorts AI SaaS", page_icon="🚀")

st.title("🚀 AI Shorts Generator")
st.write("Türkçe gerçek ses ve ekranda alt yazı ile otomatik video oluşturun!")

text_input = st.text_area(
    "Videoda seslendirilecek metin (Türkçe):",
    "1914 yılında iki kardeş, fırtınalı bir gecede denize açıldı. Dalgalar teknelerini alabora ettiğinde herkes onların yok olduğunu sandı. Ancak aylar sonra ıssız bir adada sağ bulundular. Unutma; fırtına ne kadar güçlü olursa olsun, vazgeçmeyen insanı yutamaz!",
)

# Türkçe doğal sesler
voice = st.selectbox(
    "Ses seçin:", ["tr-TR-AhmetNeural", "tr-TR-EmelNeural", "az-AZ-BabekNeural"]
)


async def generate_audio(text, voice_name, output_path):
  communicate = edge_tts.Communicate(text, voice_name, rate="+0%", pitch="+0Hz")
  await communicate.save(output_path)


if st.button("🎥 Alt Yazılı Video Oluştur"):
  if not text_input.strip():
    st.warning("Lütfen bir metin girin!")
  else:
    with st.spinner("Yapay zeka sesi, alt yazıyı ve videoyu birleştiriyor..."):
      audio_file = "temp_audio.mp3"
      output_file = "final_output.mp4"
      background_video = "background.mp4"

      if not os.path.exists(background_video):
        st.error(
            "Hata: 'background.mp4' dosyası bulunamadı! Lütfen GitHub'a"
            " background.mp4 yükleyin."
        )
      else:
        # 1. Türkçe Sesi Üret
        asyncio.run(generate_audio(text_input, voice, audio_file))

        try:
          # 2. Video ve Sesi Yükle
          video = VideoFileClip(background_video)
          audio = AudioFileClip(audio_file)

          if video.duration > audio.duration:
            video = video.subclipped(0, audio.duration)

          # 3. Alt Yazı Oluşturma
          try:
            txt_clip = TextClip(
                text=text_input,
                font_size=40,
                color="white",
                bg_color="black",
                size=(int(video.w * 0.85), None),
                method="caption",
            )
            txt_clip = txt_clip.with_duration(audio.duration).with_position(
                ("center", "center")
            )

            # Alt yazıyı videonun üzerine ekle
            video = CompositeVideoClip([video, txt_clip])
          except Exception as txt_err:
            st.warning(f"Alt yazı uyarısı: {txt_err}")

          # 4. Sesi Videoya Bağla ve Kaydet
          final_video = video.with_audio(audio)
          final_video.write_videofile(
              output_file,
              fps=24,
              codec="libx264",
              audio_codec="aac",
              preset="ultrafast",
              logger=None,
          )

          st.success("🎉 Alt yazılı ve Türkçe sesli video hazır!")
          st.video(output_file)

          # İndirme Butonu
          with open(output_file, "rb") as file:
            st.download_button(
                label="📥 Videoyu İndir",
                data=file,
                file_name="ai_short.mp4",
                mime="video/mp4",
            )

        except Exception as e:
          st.error(f"Hata oluştu: {e}")
          
