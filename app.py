import asyncio
import os
import edge_tts
from moviepy import AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip
import streamlit as st

# Səhifə konfiqurasiyası
st.set_page_config(
    page_title="Shorts AI Studio | Viral Video Creation",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# PSİXOLOJİ VƏ PEŞƏKAR SAAS CSS DİZAYNI (DARK NEON STYLE)
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    /* Ümumi Arxa Fon və Şriftlər */
    .stApp {
        background-color: #0d0f12;
        color: #e6e8ec;
    }
    
    /* Yan Menyu (Sidebar) Stylinq */
    [data-testid="stSidebar"] {
        background-color: #13171f;
        border-right: 1px solid #222733;
    }
    
    /* Peşəkar Kartlar (Pricing & Feature Cards) */
    .pro-card {
        background: linear-gradient(145deg, #181d28, #10141d);
        border: 1px solid #2a3142;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        transition: transform 0.3s ease;
    }
    .pro-card:hover {
        border-color: #f59e0b;
        transform: translateY(-2px);
    }
    
    .pricing-card-featured {
        background: linear-gradient(145deg, #1e1b4b, #0f172a);
        border: 2px solid #8b5cf6;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 0 25px rgba(139, 92, 246, 0.25);
    }
    
    /* Düyələr (Buttons) - Psixoloji İmpulsiv Rənglər */
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
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #fbbf24, #f59e0b);
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.5);
        transform: scale(1.01);
    }
    
    /* Vurğulanan Mətnlər */
    .badge-viral {
        background-color: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 700;
        border: 1px solid rgba(245, 158, 11, 0.3);
        display: inline-block;
        margin-bottom: 12px;
    }
    .badge-pro {
        background-color: rgba(139, 92, 246, 0.2);
        color: #c084fc;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# SIDEBAR - PEŞƏKAR YAN MENYU VƏ ABUNƏLİK PAKETLƏRİ
# ---------------------------------------------------------
with st.sidebar:
  st.markdown(
      '<div><span class="badge-pro">PRO SAAS STUDIO</span></div>',
      unsafe_allow_html=True,
  )
  st.title("⚡ Shorts AI Studio")
  st.caption("Otomatik Viral Video Üretim Platformu")

  st.divider()

  st.subheader("💳 Abonelik Planları")

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
    st.markdown(
        """
        <div class="pricing-card-featured">
            <span class="badge-viral">ÇOK SATAN</span>
            <h3 style="margin:0; color:#fff;">Pro Creator</h3>
            <h2 style="margin:5px 0; color:#f59e0b;">$9.99 <span style="font-size:14px; color:#a1a1aa;">/ ay</span></h2>
            <ul style="font-size:13px; padding-left:18px; color:#d4d4d8;">
                <li><b>200 Viral Video</b> / ay</li>
                <li>Ultra HD Render Hızı</li>
                <li>Filigransız & Yüksek Kalite</li>
                <li>Türkiye Lider Ses Motoru</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "[👉 Pro Pakete Geç ($9.99)](https://buy.stripe.com/test_pro_plan)"
    )

  elif "Unlimited" in plan:
    st.markdown(
        """
        <div class="pro-card">
            <span class="badge-pro">SINIRSIZ EŞİSİZ POWER</span>
            <h3 style="margin:0; color:#fff;">Unlimited Empire</h3>
            <h2 style="margin:5px 0; color:#c084fc;">$29.99 <span style="font-size:14px; color:#a1a1aa;">/ ay</span></h2>
            <ul style="font-size:13px; padding-left:18px; color:#d4d4d8;">
                <li><b>Sınırsız Video Üretimi</b></li>
                <li>7/24 Öncelikli Sunucu Gücü</li>
                <li>Özel Altyazı & Font Şablonları</li>
                <li>Sınırsız Ticari Kullanım Haktan</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "[👉 Sınırsız Pakete Geç"
        " ($29.99)](https://buy.stripe.com/test_unlimited_plan)"
    )

  st.divider()
  st.caption("🔒 256-Bit SSL ile Güvenli Ödeme - Stripe Infrastructure")


# ---------------------------------------------------------
# ANA EKRAN DİZAYNI & VİDEO GENERATOR
# ---------------------------------------------------------
st.markdown(
    '<div><span class="badge-viral">🔥 VİRAL VİDEO MOTORU v2.4</span></div>',
    unsafe_allow_html=True,
)
st.title("Saniyeler İçinde Keşfet Etkili Short'lar Üretin")
st.markdown(
    "<p style='font-size:16
    
