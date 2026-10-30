import os
import streamlit as st
import asyncio
import edge_tts
from moviepy import VideoFileClip, AudioFileClip

st.set_page_config(page_title="Shorts AI SaaS", page_icon="🚀")

st.title("🚀 AI Shorts Generator (Subway Surfers)")
st.write("Mətni daxil edin, süni intellekt səsləndirib avtomatik videoya çevirsin!")

text_input = st.text_area("Videoda səsləndiriləcək mətn:", "Salam dostlar, bu gün süni intellektlə necə video düzəltməyi öyrənirik!")

voice = st.selectbox("Səs seçin:", ["az-AZ-BabekNeural", "az-AZ-AidanNeural", "en-US-AriaNeural"])

async def generate_audio(text, voice_name, output_path):
    communicate = edge_tts.Communicate(text, voice_name)
    await communicate.save(output_path)

if st.button("🎥 Video yarat"):
    if not text_input.strip():
        st.warning("Zəhmət olmasa mətn daxil edin!")
    else:
        with st.spinner("Süni intellekt səsi və videonu birləşdirir..."):
            audio_file = "temp_audio.mp3"
            output_file = "final_output.mp4"
            background_video = "background.mp4"
            
            if not os.path.exists(background_video):
                st.error("Xəta: 'background.mp4' faylı tapılmadı! Zəhmət olmasa GitHub-a background.mp4 yükləyin.")
            else:
                # 1. Səsi yarat
                asyncio.run(generate_audio(text_input, voice, audio_file))
                
                # 2. Videonu və səsi birləşdir
                try:
                    video = VideoFileClip(background_video)
                    audio = AudioFileClip(audio_file)
                    
                    # Videonun uzunluğunu səsə uyğun qısalt
                    if video.duration > audio.duration:
                        video = video.subclipped(0, audio.duration)
                    
                    final_video = video.with_audio(audio)
                    final_video.write_videofile(
                        output_file, 
                        fps=24, 
                        codec="libx264", 
                        audio_codec="aac",
                        preset="ultrafast",
                        logger=None
                    )
                    
                    st.success("🎉 Video uğurla hazırdır!")
                    st.video(output_file)
                    
                    # Endirmə düyməsi
                    with open(output_file, "rb") as file:
                        st.download_button(
                            label="📥 Videonu yüklə",
                            data=file,
                            file_name="ai_short.mp4",
                            mime="video/mp4"
                        )
                        
                except Exception as e:
                    st.error(f"Xəta baş verdi: {e}")
