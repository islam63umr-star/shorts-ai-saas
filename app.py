import streamlit as st
import asyncio
import os
import time
from moviepy.editor import VideoFileClip, AudioFileClip
import edge_tts

# Səhifə Tənzimləmələri və İnterfeys
st.set_page_config(page_title="Shorts AI SaaS", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .main-title {font-size: 32px; font-weight: bold; color: #FF4B4B; text-align: center;}
    .sub-title {font-size: 16px; color: #555; text-align: center; margin-bottom: 25px;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚡ Otomatik Shorts & TikTok Oluşturucu</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Metninizi yazın, saniyeler içinde viral olmaya hazır videonuzu indirin!</div>', unsafe_allow_html=True)

# Mətn və Fon seçimi
script_text = st.text_area(
    "📝 Video Senaryosu (Hikaye / Gizemli Metin):", 
    "Minecraft'ın hiç bilinmeyen karanlık sırrını duydunuz mu? Çoğu oyuncu bu köyü gördüğünde oyunu hemen kapatıyor...",
    height=120
)

bg_option = st.selectbox(
    "🎮 Arka Plan Konsepti Seçin:",
    ["Minecraft Parkour (Aksiyon)", "Satisfying Slime / Cutting", "GTA V Mega Ramp"]
)

# Video Yaratma Düyməsi
if st.button("🚀 Videoyu Otomatik Oluştur", type="primary", use_container_width=True):
    if not script_text.strip():
        st.warning("Lütfen önce bir senaryo metni girin!")
    else:
        status_box = st.info("⚙️ Sistem çalışıyor: Ses sentezleniyor ve video montajlanıyor...")
        
        unique_id = int(time.time())
        audio_file = f"voice_{unique_id}.mp3"
        output_file = f"short_{unique_id}.mp4"
        bg_file = "background.mp4"
        
        if not os.path.exists(bg_file):
            st.error("❌ Hata: Sunucuda 'background.mp4' arka plan videosu bulunamadı! Lütfen repository klasörüne arka plan videosu ekleyin.")
        else:
            try:
                # Canlı Türk Sesi İle Seslendirme
                async def generate_audio():
                    communicate = edge_tts.Communicate(script_text, "tr-TR-AhmetNeural")
                    await communicate.save(audio_file)

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(generate_audio())

                # Video və Səsin Birləşdirilməsi
                audio_clip = AudioFileClip(audio_file)
                video_clip = VideoFileClip(bg_file)

                if video_clip.duration > audio_clip.duration:
                    video_clip = video_clip.subclip(0, audio_clip.duration)

                final_video = video_clip.set_audio(audio_clip)

                # 9:16 Formatına Kırpma
                w, h = final_video.size
                target_width = int(h * (9 / 16))
                if w > target_width:
                    x1 = (w - target_width) // 2
                    final_video = final_video.crop(x1=x1, y1=0, x2=x1 + target_width, y2=h)

                final_video.write_videofile(
                    output_file,
                    fps=24,
                    codec='libx264',
                    audio_codec='aac',
                    bitrate='4M',
                    logger=None
                )

                status_box.empty()
                st.success("🎉 Videonuz başarıyla hazırlandı!")
                
                st.video(output_file)

                with open(output_file, "rb") as file:
                    st.download_button(
                        label="📥 Videoyu Yüksek Kalitede İndir",
                        data=file,
                        file_name=f"shorts_{unique_id}.mp4",
                        mime="video/mp4",
                        use_container_width=True
                    )

            except Exception as e:
                st.error(f"❌ Bir hata oluştu: {e}")
