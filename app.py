import streamlit as st
import json
import re
import os
import uuid
from datetime import datetime

# --- Ayarlar ---
DB_FILE = "users_db.json"
DEVICE_ID_COOKIE = "nexen_device_id"
COOKIE_ENCRYPTION_KEY = "nexen_super_secret_key" 

# --- Səhifə Ayarları ---
st.set_page_config(
    page_title="Nexen Platform",
    page_icon="🤖",
    layout="wide",
)

# --- Database Funksiyaları ---
def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- Ödənişdən Sonra Limit Artırma Funksiyası ---
def update_user_plan(email, plan_type):
    db = load_db()
    if email in db:
        if plan_type == "monthly":
            db[email]["credits"] = 200  # Ayda 200 video
            db[email]["plan"] = "Aylıq Plan (200 Video)"
            db[email]["is_pro"] = True
        elif plan_type == "yearly_unlimited":
            db[email]["credits"] = 99999  # 1 il sonsuz limit
            db[email]["plan"] = "Limitsiz 1 İl"
            db[email]["is_pro"] = True
        save_db(db)

# --- CSS Stil Tənzimləmələri ---
st.markdown("""
<style>
    .stApp {
        background-color: #f9fafb;
        color: #111827;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e7eb;
    }
    .pricing-card {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .pricing-card .price {
        font-size: 36px;
        font-weight: bold;
        color: #1f2937;
        margin: 10px 0 15px 0;
    }
    .pricing-card .period {
        font-size: 16px;
        color: #6b7280;
    }
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        background-color: #ffffff;
        border-radius: 12px;
        padding: 40px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

db = load_db()

# --- Səhifənin Əsas Məntiqi ---
if "user_email" not in st.session_state:
    st.session_state.user_email = None

if not st.session_state.user_email:
    # --- Giriş Səhifəsi ---
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown("<h2>Giriş / Qeydiyyat</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6b7280; text-align:center; font-size:14px; margin-bottom:20px;'>Davam etmək üçün e-poçt ünvanınızı daxil edin. Hər cihaz üçün ilk girişdə 1 video haqqı verilir.</p>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        email_input = st.text_input("E-poçt ünvanı:", placeholder="məsələn: adiniz@gmail.com")
        submit_login = st.form_submit_button("Daxil Ol")
        
        if submit_login:
            clean_email = email_input.strip().lower()
            email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            
            if clean_email and re.match(email_pattern, clean_email):
                if clean_email not in db:
                    db[clean_email] = {
                        "credits": 1, 
                        "is_pro": False,
                        "plan": "Pulsuz Sınaq"
                    }
                    save_db(db)
                
                st.session_state.user_email = clean_email
                st.success("Uğurla daxil olundu!")
                st.rerun()
            else:
                st.error("Zəhmət olmasa düzgün e-poçt formatı daxil edin.")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- Panel Səhifəsi ---
    current_email = st.session_state.user_email
    user_data = db.get(current_email, {"credits": 0, "plan": "Pulsuz"})
    credits = user_data.get("credits", 0)
    
    with st.sidebar:
        st.markdown(f"### Xoş Gəldiniz!")
        st.markdown(f"**E-poçt:** `{current_email}`")
        st.markdown(f"**Haklarınız:** `{credits}` Video")
        st.markdown(f"**Plan:** `{user_data.get('plan')}`")
        
        # Test məqsədi ilə ödəniş simulyasiyası düymələri (Pulu ödədikdən sonra işləyəcək hissə)
        st.markdown("---")
        st.markdown("### Ödəniş Testi (Simulyasiya)")
        if st.button("9.99₺ Aylıq Paket Al (200 Video)"):
            update_user_plan(current_email, "monthly")
            st.success("Ödəniş uğurlu oldu! 200 video haqqı yükləndi.")
            st.rerun()
            
        if st.button("29.99₺ Sonsuz Paket Al (1 İl)"):
            update_user_plan(current_email, "yearly_unlimited")
            st.success("Ödəniş uğurlu oldu! 1 illik limitsiz plan aktivləşdi.")
            st.rerun()

        if st.button("Çıxış Ol"):
            st.session_state.user_email = None
            st.rerun()

    st.markdown("## Nexen Video Paneli")
    
    # --- Qiymət Paketləri ---
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="pricing-card">
            <h3>AYLIK PLAN</h3>
            <div class="price">9.99₺ <span class="period">/ ay</span></div>
            <ul>
                <li>Ayda 200 Video</li>
                <li>Öncelikli Destek</li>
                <li>HD Dışa Aktarım</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="pricing-card" style="border-color: #1f2937;">
            <h3>SONSUZ PLAN</h3>
            <div class="price">29.99₺ <span class="period">1 İl</span></div>
            <ul>
                <li>Sonsuza Kadar Limitsiz Video</li>
                <li>1 Yıl Boyunca Kullanım</li>
                <li>4K Dışa Aktarım</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Video Yaratma və Söz Effekti")
    st.info("Videoda səslənən cümlələr oxunduqca həmin söz **sarı rəngə** boyanır, oxunub qurtardıqdan sonra isə yenidən **ağ rəngə** qayıdır.")
    
    if credits > 0:
        if st.button("Video Yarat və Hak İşlət"):
            db[current_email]["credits"] -= 1
            save_db(db)
            st.success("Video uğurla yaradıldı! Sözlərin saralma effekti tətbiq edildi.")
            st.rerun()
    else:
        st.error("Haklarınız qurtarıb! Zəhmət olmasa yuxarıdakı paketlərdən birini seçərək davam edin.")
        
