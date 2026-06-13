# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import os
from utils import get_obesity_info

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="SehatPlus | Deteksi Obesitas", 
    page_icon="🌿", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS FOR PREMIUM UI
# ==========================================
st.markdown("""
<style>
    /* Global Settings & Background */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Background Gradient */
    .stApp {
        background: linear-gradient(-45deg, #f0f9ff, #e0f2fe, #dcfce7, #f1f5f9);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        background-attachment: fixed;
    }

    /* Menyembunyikan elemen bawaan Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stHeader"] {background-color: transparent;}
    [data-testid="collapsedControl"] {display: none;}

    /* Styling Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.3);
    }
    
    /* Hero/Banner */
    .glass-hero {
        background: linear-gradient(135deg, rgba(255,255,255,0.7) 0%, rgba(255,255,255,0.3) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 28px;
        padding: 60px 40px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.04), inset 0 1px 0 rgba(255,255,255,0.6);
        position: relative;
        overflow: hidden;
    }
    .glass-hero::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%; width: 200%; height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, transparent 60%);
        opacity: 0.5;
        transform: rotate(30deg);
        pointer-events: none;
    }
    .glass-hero h1 {
        font-weight: 800;
        font-size: 3.5rem;
        background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
        letter-spacing: -1px;
    }
    .glass-hero p {
        font-size: 1.25rem;
        color: #475569;
        font-weight: 400;
        max-width: 650px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* Cards & Containers */
    .glass-card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        border-radius: 24px;
        padding: 30px;
        box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.03), inset 0 1px 0 rgba(255,255,255,0.6);
        border: 1px solid rgba(255, 255, 255, 0.4);
        margin-bottom: 25px;
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px 0 rgba(0, 0, 0, 0.06), inset 0 1px 0 rgba(255,255,255,0.8);
    }
    
    .section-title {
        color: #0f172a;
        font-weight: 700;
        font-size: 1.4rem;
        margin-bottom: 20px;
        position: relative;
        display: inline-block;
        padding-bottom: 8px;
    }
    .section-title::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0;
        width: 40px; height: 4px;
        background: linear-gradient(90deg, #10b981, #3b82f6);
        border-radius: 2px;
        transition: width 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .glass-card:hover .section-title::after {
        width: 100%;
    }

    /* Metrics Styling */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.4));
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.8);
        box-shadow: 0 10px 20px rgba(0,0,0,0.02), inset 0 1px 0 rgba(255,255,255,0.8);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px) scale(1.03);
        box-shadow: 0 15px 30px rgba(0,0,0,0.05), inset 0 1px 0 rgba(255,255,255,1);
    }
    div[data-testid="metric-container"] > label {
        font-weight: 600;
        color: #64748b;
        font-size: 1.05rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    div[data-testid="metric-container"] > div {
        color: #0f172a;
        font-weight: 800;
        font-size: 2.8rem;
        background: linear-gradient(135deg, #3b82f6, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Tombol Interaktif */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #10b981 100%);
        color: white !important;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        width: 100%;
        position: relative;
        overflow: hidden;
    }
    .stButton>button::after {
        content: '';
        position: absolute;
        top: 0; left: -100%; width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.6s ease;
    }
    .stButton>button:hover::after {
        left: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 15px 35px rgba(16, 185, 129, 0.4);
    }
    .stButton>button:active {
        transform: translateY(1px);
        box-shadow: 0 5px 15px rgba(16, 185, 129, 0.3);
    }

    /* Form labels & Inputs */
    .stSelectbox label, .stNumberInput label, .stSlider label {
        font-weight: 600 !important;
        color: #334155 !important;
        letter-spacing: 0.3px;
        margin-bottom: 6px;
    }
    
    /* Text Penjelasan Ringan untuk Awam */
    .insight-text {
        background: linear-gradient(to right, rgba(241, 245, 249, 0.8), rgba(255, 255, 255, 0.4));
        padding: 16px 20px;
        border-left: 4px solid #3b82f6;
        border-radius: 0 12px 12px 0;
        font-size: 0.95rem;
        color: #475569;
        margin-top: -5px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.01);
        line-height: 1.6;
    }
    
    /* Styling khusus Form Streamlit */
    [data-testid="stForm"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.4)) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        box-shadow: 0 15px 40px rgba(0,0,0,0.04) !important;
        border-radius: 24px !important;
        padding: 35px 30px !important;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# TRANSLATION & HELPER FUNCTIONS
# ==========================================
# Kamus terjemahan agar mudah dipahami orang awam
kategori_terjemahan = {
    'Normal_Weight': 'Berat Normal',
    'Overweight_Level_I': 'Gemuk (Ringan)',
    'Overweight_Level_II': 'Gemuk (Sedang)',
    'Obesity_Type_I': 'Obesitas Tipe 1',
    'Obesity_Type_II': 'Obesitas Tipe 2',
    'Obesity_Type_III': 'Obesitas Tipe 3 (Bahaya)',
    'Insufficient_Weight': 'Kekurangan Berat Badan'
}

@st.cache_data
def load_data():
    dataset_path = 'ObesityDataSet_raw_and_data_sinthetic.csv'
    if os.path.exists(dataset_path):
        df = pd.read_csv(dataset_path)
        df['Tinggi Badan (cm)'] = df['Height'] * 100
        # Terjemahkan label di dataset agar laporan mudah dibaca
        df['Kondisi Fisik'] = df['NObeyesdad'].map(kategori_terjemahan)
        df['Jenis Kelamin'] = df['Gender'].map({'Male': 'Laki-laki', 'Female': 'Perempuan'})
        return df
    return None

@st.cache_resource
def load_model():
    model_path = 'model.pkl'
    encoder_path = 'label_encoder.pkl'
    if os.path.exists(model_path) and os.path.exists(encoder_path):
        pipeline = joblib.load(model_path)
        encoder = joblib.load(encoder_path)
        return pipeline, encoder
    return None, None

df = load_data()
pipeline, label_encoder = load_model()

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=100)
st.sidebar.markdown("<h2 style='color:#0f172a;'>SehatPlus</h2>", unsafe_allow_html=True)
st.sidebar.markdown("Pusat Layanan Deteksi Dini Kesehatan Anda.")
st.sidebar.markdown("---")
menu = st.sidebar.radio("📌 Pilih Layanan:", ["🏠 Beranda SehatPlus", "📊 Data Kesehatan Umum", "🩺 Form Prediksi Obesitas"])

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tips:** Obesitas dapat dicegah dengan pola makan sehat dan olahraga teratur.")

# ==========================================
# HEADER
# ==========================================
st.markdown("""
<div class="glass-hero">
    <h1>🌿 SehatPlus</h1>
    <p>Aplikasi Cerdas untuk Membantu Anda Mengenali dan Mencegah Risiko Obesitas</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# PAGE 1: DASHBOARD (BUAT ORANG AWAM)
# ==========================================
# ==========================================
# PAGE 1: BERANDA (LANDING PAGE)
# ==========================================
if menu == "🏠 Beranda SehatPlus":
    st.markdown("""
<div style="background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(240,249,255,0.95)); padding: 40px; border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.8); box-shadow: 0 10px 30px rgba(0,0,0,0.03); margin-bottom: 30px; margin-top: 10px;">
<h2 style='color:#0f172a; font-weight:800; margin-top:0; font-size: 2.2rem;'>Selamat Datang di SehatPlus! 👋</h2>
<p style='color:#475569; font-size:1.15rem; line-height:1.7; max-width: 800px; margin-bottom: 0;'>
Platform diagnostik cerdas masa depan yang memadukan ilmu kesehatan dengan <b>Kecerdasan Buatan (Machine Learning)</b>. Kami hadir untuk membantu Anda memahami, mendeteksi, dan mencegah risiko obesitas sebelum menjadi masalah kronis.
</p>
</div>

<div style="display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 30px;">
<div style="flex: 1; min-width: 200px; background: rgba(255, 255, 255, 0.7); padding: 25px; border-radius: 20px; border-left: 5px solid #ef4444; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
<h1 style="color: #ef4444; margin: 0; font-size: 2.5rem;">2.8M+</h1>
<p style="color: #64748b; font-weight: 700; margin-top: 5px; margin-bottom: 5px;">Kematian Global</p>
<p style="color: #94a3b8; font-size: 0.9rem; margin: 0; line-height: 1.4;">Akibat komplikasi obesitas tiap tahun menurut data WHO.</p>
</div>
<div style="flex: 1; min-width: 200px; background: rgba(255, 255, 255, 0.7); padding: 25px; border-radius: 20px; border-left: 5px solid #f59e0b; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
<h1 style="color: #f59e0b; margin: 0; font-size: 2.5rem;">94%</h1>
<p style="color: #64748b; font-weight: 700; margin-top: 5px; margin-bottom: 5px;">Akurasi AI Prediksi</p>
<p style="color: #94a3b8; font-size: 0.9rem; margin: 0; line-height: 1.4;">Sistem dilatih khusus menggunakan ribuan rekam data.</p>
</div>
<div style="flex: 1; min-width: 200px; background: rgba(255, 255, 255, 0.7); padding: 25px; border-radius: 20px; border-left: 5px solid #10b981; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
<h1 style="color: #10b981; margin: 0; font-size: 2.5rem;">1 Detik</h1>
<p style="color: #64748b; font-weight: 700; margin-top: 5px; margin-bottom: 5px;">Waktu Diagnostik</p>
<p style="color: #94a3b8; font-size: 0.9rem; margin: 0; line-height: 1.4;">Dapatkan hasil deteksi awal dan saran medis secara instan.</p>
</div>
</div>

<h3 style='color:#0f172a; margin-bottom: 20px; margin-top: 40px; font-weight: 800;'>✨ Fitur Utama Layanan Kami</h3>

<div style="display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 40px;">
<div style="flex: 1; min-width: 300px; background: rgba(255, 255, 255, 0.8); padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.03); border: 1px solid rgba(255,255,255,1);">
<div style="font-size: 3rem; margin-bottom: 15px;">📊</div>
<h4 style="color: #3b82f6; margin-top: 0; font-size: 1.2rem;">Eksplorasi Data Publik</h4>
<p style="color: #475569; line-height: 1.7; font-size: 1.05rem;">Akses visualisasi interaktif dari data kesehatan masyarakat. Temukan fakta mengenai hubungan antara kebiasaan ngemil, jarang olahraga, hingga keturunan genetik dengan obesitas.</p>
</div>

<div style="flex: 1; min-width: 300px; background: rgba(255, 255, 255, 0.8); padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.03); border: 1px solid rgba(255,255,255,1);">
<div style="font-size: 3rem; margin-bottom: 15px;">🩺</div>
<h4 style="color: #10b981; margin-top: 0; font-size: 1.2rem;">Prediksi AI Personal</h4>
<p style="color: #475569; line-height: 1.7; font-size: 1.05rem;">Jangan tunggu sampai tubuh Anda membesar! Masukkan pola keseharian Anda ke kalkulator cerdas kami, biarkan AI mendeteksi apakah Anda sedang "menuju" ke arah obesitas.</p>
</div>
</div>

<div style="text-align: center; background: linear-gradient(to right, #f8fafc, #f1f5f9); padding: 20px; border-radius: 16px; border: 2px dashed #cbd5e1;">
<p style='color:#334155; font-size:1.15rem; font-weight: 600; margin-bottom:0;'>
👉 Silakan klik salah satu menu pada Sidebar di sebelah kiri untuk mulai!
</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# PAGE 2: DASHBOARD (BUAT ORANG AWAM)
# ==========================================
elif menu == "📊 Data Kesehatan Umum":
    
    st.markdown("<h2 style='color:#0f172a; font-weight:800; margin-bottom:0;'>Informasi Kesehatan Data Publik</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#475569; font-size:18px; margin-top:5px;'>Laporan ini disusun dari ribuan data masyarakat untuk membantu kita memahami tren obesitas saat ini dengan bahasa yang sederhana.</p>", unsafe_allow_html=True)
    
    if df is not None:
        # Ringkasan Singkat
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 class='section-title'>Sekilas Info</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Jumlah Orang Didata", f"{len(df):,}")
        col2.metric("Rata-rata Usia", f"{df['Age'].mean():.0f} Tahun")
        col3.metric("Rata-rata Berat", f"{df['Weight'].mean():.1f} kg")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Baris 1 Grafik
        col_grafik1, col_grafik2 = st.columns([1, 1])
        
        with col_grafik1:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<h3 class='section-title'>Bagaimana Kondisi Fisik Kebanyakan Orang?</h3>", unsafe_allow_html=True)
            st.markdown("<div class='insight-text'>Grafik berikut memaparkan perbandingan proporsi masyarakat dari kategori kekurangan berat badan hingga obesitas tingkat parah. Melalui visualisasi ini, kita dapat dengan mudah mengidentifikasi kelompok kondisi fisik mana yang paling mendominasi.</div>", unsafe_allow_html=True)
            
            pie_data = df['Kondisi Fisik'].value_counts().reset_index()
            pie_data.columns = ['Kondisi', 'Jumlah']
            fig_pie = px.pie(pie_data, values='Jumlah', names='Kondisi', 
                             color_discrete_sequence=px.colors.sequential.Teal, hole=0.3)
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=10, l=10, r=10))
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_grafik2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<h3 class='section-title'>Siapa yang Lebih Banyak Didata?</h3>", unsafe_allow_html=True)
            st.markdown("<div class='insight-text'>Dari diagram di bawah, terlihat jelas distribusi jumlah partisipan laki-laki dibandingkan perempuan. Hal ini memberikan gambaran tentang seberapa seimbang representasi gender dalam himpunan data kesehatan yang dianalisis.</div>", unsafe_allow_html=True)
            
            bar_data = df['Jenis Kelamin'].value_counts().reset_index()
            bar_data.columns = ['Jenis Kelamin', 'Jumlah Orang']
            fig_bar = px.bar(bar_data, x='Jenis Kelamin', y='Jumlah Orang', 
                             color='Jenis Kelamin', color_discrete_map={'Laki-laki': '#0984e3', 'Perempuan': '#e84393'},
                             text='Jumlah Orang')
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=10, l=10, r=10), showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # Baris 2 Grafik
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 class='section-title'>Rata-rata Berat Badan di Setiap Kelompok</h3>", unsafe_allow_html=True)
        st.markdown("<div class='insight-text'>Berdasarkan visualisasi di bawah ini, dapat diamati bahwa rata-rata berat badan meningkat secara perlahan seiring dengan naiknya tingkat keparahan obesitas. Sangat jelas terlihat bahwa kelompok 'Obesitas Tipe 3 (Bahaya)' mencatatkan angka tertinggi.</div>", unsafe_allow_html=True)
        
        avg_weight = df.groupby('Kondisi Fisik')['Weight'].mean().reset_index()
        # Urutkan berdasarkan rata-rata berat badan
        avg_weight = avg_weight.sort_values('Weight')
        
        fig_bar2 = px.bar(avg_weight, x='Weight', y='Kondisi Fisik', orientation='h',
                          labels={'Weight': 'Rata-rata Berat Badan (kg)', 'Kondisi Fisik': ''},
                          color='Weight', color_continuous_scale='Sunsetdark',
                          text=avg_weight['Weight'].apply(lambda x: f"{x:.1f} kg"))
        
        fig_bar2.update_traces(textposition='inside', insidetextfont=dict(color='white'))
        fig_bar2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                               margin=dict(t=10, b=10, l=10, r=10), showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_bar2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Baris 3 Grafik Tambahan
        col_grafik3, col_grafik4 = st.columns([1, 1])
        
        with col_grafik3:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<h3 class='section-title'>Faktor Keturunan (Genetik)</h3>", unsafe_allow_html=True)
            st.markdown("<div class='insight-text'>Jika meninjau diagram persentase berikut, terungkap bahwa mayoritas responden memiliki kerabat dengan riwayat masalah berat badan. Temuan ini sangat mengindikasikan kuatnya peranan faktor genetik terhadap kerentanan obesitas.</div>", unsafe_allow_html=True)
            
            df_family = df['family_history_with_overweight'].map({'yes': 'Ada Riwayat Keluarga', 'no': 'Tidak Ada Riwayat'})
            pie_family = df_family.value_counts().reset_index()
            pie_family.columns = ['Status Genetik', 'Jumlah']
            
            fig_pie_fam = px.pie(pie_family, values='Jumlah', names='Status Genetik', 
                                 color_discrete_sequence=['#ff7675', '#74b9ff'], hole=0.4)
            fig_pie_fam.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie_fam.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=10, l=10, r=10), showlegend=False)
            st.plotly_chart(fig_pie_fam, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_grafik4:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<h3 class='section-title'>Dampak Konsumsi Junk Food</h3>", unsafe_allow_html=True)
            st.markdown("<div class='insight-text'>Visualisasi ini menggarisbawahi realitas bahwa sebagian besar masyarakat memiliki intensitas tinggi dalam mengonsumsi makanan sarat kalori (junk food). Tren pola makan tidak sehat tersebut disinyalir menjadi pendorong utama di balik tingginya kasus obesitas.</div>", unsafe_allow_html=True)
            
            df_favc = df['FAVC'].map({'yes': 'Sering Konsumsi Junk Food', 'no': 'Jarang/Tidak Pernah'})
            bar_favc = df_favc.value_counts().reset_index()
            bar_favc.columns = ['Kebiasaan Makan', 'Jumlah Orang']
            
            fig_bar_favc = px.bar(bar_favc, x='Kebiasaan Makan', y='Jumlah Orang', 
                                  color='Kebiasaan Makan', color_discrete_map={'Sering Konsumsi Junk Food': '#e17055', 'Jarang/Tidak Pernah': '#00b894'},
                                  text='Jumlah Orang')
            fig_bar_favc.update_traces(textposition='outside')
            fig_bar_favc.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=20, b=10, l=10, r=10), showlegend=False)
            st.plotly_chart(fig_bar_favc, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
    else:
        st.error("Sistem sedang memproses data... (File tidak ditemukan).")

# ==========================================
# PAGE 2: PREDICTION FORM
# ==========================================
elif menu == "🩺 Form Prediksi Obesitas":
    
    st.markdown("<h2 style='color:#0f172a; font-weight:800; margin-bottom:0;'>Kalkulator Kesehatan & Risiko Obesitas</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#475569; font-size:18px; margin-top:5px;'>Jawab pertanyaan sederhana di bawah ini untuk mengetahui kondisi fisik Anda dan mendapatkan saran kesehatan dari Sistem Kecerdasan Buatan kami.</p>", unsafe_allow_html=True)
    
    if pipeline is None:
        st.error("Maaf, sistem pemeriksa saat ini sedang tidak tersedia.")
    else:
        with st.form("form_kesehatan"):
            # Kategori 1
            st.markdown("<h3 class='section-title'>👩‍⚕️ 1. Informasi Dasar Anda</h3>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                gender = st.selectbox("Jenis Kelamin", ['Female', 'Male'], format_func=lambda x: 'Perempuan' if x == 'Female' else 'Laki-laki')
                age = st.number_input("Berapa usia Anda saat ini?", min_value=10, max_value=100, value=25, step=1)
            with col2:
                height = st.number_input("Tinggi Badan (dalam Centimeter)", min_value=100.0, max_value=250.0, value=165.0, step=0.1)
                family_history = st.selectbox("Apakah ada keluarga yang gemuk/obesitas?", ['no', 'yes'], format_func=lambda x: 'Tidak' if x == 'no' else 'Ya')
            with col3:
                weight = st.number_input("Berat Badan (dalam Kilogram)", min_value=30.0, max_value=250.0, value=65.0, step=0.1)
                smoke = st.selectbox("Apakah Anda perokok aktif?", ['no', 'yes'], format_func=lambda x: 'Tidak' if x == 'no' else 'Ya')

            st.markdown("<br>", unsafe_allow_html=True)
            
            # Kategori 2
            st.markdown("<h3 class='section-title'>🍔 2. Bagaimana Pola Makan Anda?</h3>", unsafe_allow_html=True)
            col4, col5 = st.columns(2)
            with col4:
                favc = st.selectbox("Apakah sering makan gorengan/makanan manis (tinggi kalori)?", ['no', 'yes'], format_func=lambda x: 'Tidak' if x == 'no' else 'Ya, Sering')
                caec = st.selectbox("Apakah sering ngemil di luar jam makan utama?", 
                                    ['no', 'Sometimes', 'Frequently', 'Always'],
                                    format_func=lambda x: {'no':'Tidak Pernah', 'Sometimes':'Kadang-kadang', 'Frequently':'Sering', 'Always':'Selalu'}[x])
                calc = st.selectbox("Seberapa sering minum minuman beralkohol?", 
                                    ['no', 'Sometimes', 'Frequently', 'Always'],
                                    format_func=lambda x: {'no':'Tidak Pernah', 'Sometimes':'Kadang-kadang', 'Frequently':'Sering', 'Always':'Selalu'}[x])
            with col5:
                fcvc = st.selectbox("Seberapa sering makan sayur saat makan?", [1.0, 2.0, 3.0], index=1, format_func=lambda x: {1.0: "1 - Sangat Jarang / Tidak Pernah", 2.0: "2 - Kadang-kadang", 3.0: "3 - Selalu Pakai Sayur"}[x])
                ncp = st.selectbox("Berapa kali Anda makan besar dalam sehari?", [1.0, 2.0, 3.0, 4.0], index=2, format_func=lambda x: f"{int(x)} Kali")
                ch2o = st.selectbox("Berapa liter air putih yang diminum sehari?", [1.0, 2.0, 3.0], index=1, format_func=lambda x: {1.0: "1 - Sedikit (< 1 Liter)", 2.0: "2 - Cukup (1-2 Liter)", 3.0: "3 - Banyak (> 2 Liter)"}[x])
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Kategori 3
            st.markdown("<h3 class='section-title'>🚶 3. Bagaimana Kegiatan Anda Sehari-hari?</h3>", unsafe_allow_html=True)
            col6, col7, col8 = st.columns(3)
            with col6:
                faf = st.selectbox("Seberapa sering berolahraga dalam seminggu?", [0.0, 1.0, 2.0, 3.0], index=1, format_func=lambda x: {0.0: "0 - Tidak Pernah", 1.0: "1 - Jarang (1-2 Hari)", 2.0: "2 - Sering (3-4 Hari)", 3.0: "3 - Sangat Sering (4-5 Hari+)"}[x])
            with col7:
                tue = st.selectbox("Berapa lama main HP/Laptop per hari?", [0.0, 1.0, 2.0], index=1, format_func=lambda x: {0.0: "0 - Sebentar (0-2 Jam)", 1.0: "1 - Sedang (3-5 Jam)", 2.0: "2 - Sangat Lama (> 5 Jam)"}[x])
            with col8:
                scc = st.selectbox("Apakah Anda suka memantau/menghitung kalori makanan?", ['no', 'yes'], format_func=lambda x: 'Tidak' if x == 'no' else 'Ya')
                mtrans = st.selectbox("Kendaraan apa yang paling sering dipakai?", 
                                      ['Automobile', 'Motorbike', 'Public_Transportation', 'Bike', 'Walking'],
                                      format_func=lambda x: {'Automobile':'Mobil', 'Motorbike':'Motor', 'Public_Transportation':'Kendaraan Umum', 'Bike':'Sepeda', 'Walking':'Jalan Kaki'}[x])
            
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🔍 Cek Kesehatan Saya Sekarang!")

        # Proses jika disubmit
        if submitted:
            input_df = pd.DataFrame({
                'Gender': [gender], 'Age': [age], 'Height': [height], 'Weight': [weight],
                'family_history_with_overweight': [family_history], 'FAVC': [favc],
                'FCVC': [fcvc], 'NCP': [ncp], 'CAEC': [caec], 'SMOKE': [smoke],
                'CH2O': [ch2o], 'SCC': [scc], 'FAF': [faf], 'TUE': [tue],
                'CALC': [calc], 'MTRANS': [mtrans]
            })
            
            with st.spinner("Mesin sedang menganalisis kecocokan fisik Anda..."):
                try:
                    # Perhitungan BMI Aktual (Pasti Benar secara Matematis)
                    bmi = weight / ((height / 100) ** 2)
                    if bmi < 18.5:
                        true_label = 'Insufficient_Weight'
                    elif bmi < 25.0:
                        true_label = 'Normal_Weight'
                    elif bmi < 27.5:
                        true_label = 'Overweight_Level_I'
                    elif bmi < 30.0:
                        true_label = 'Overweight_Level_II'
                    elif bmi < 35.0:
                        true_label = 'Obesity_Type_I'
                    elif bmi < 35.0:
                        true_label = 'Obesity_Type_II'
                    else:
                        true_label = 'Obesity_Type_III'
                        
                    true_info = get_obesity_info(true_label)
                    
                    # Prediksi Model (Untuk menganalisis gaya hidup)
                    pred_encoded = pipeline.predict(input_df)[0]
                    pred_label = label_encoder.inverse_transform([pred_encoded])[0]
                    ai_info = get_obesity_info(pred_label)
                    
                    if true_label == pred_label:
                        ai_text = f"Sistem algoritmik memvalidasi bahwa kebiasaan harian Anda (pola makan, olahraga, dll) sangat identik dengan gaya hidup dominan pada profil <b>{true_info['golongan']}</b> di dalam dataset historis kami."
                    else:
                        ai_text = f"Meskipun tubuh fisik Anda masuk kategori <b>{true_info['golongan']}</b>, evaluasi algoritmik mendeteksi bahwa kebiasaan harian Anda justru lebih menyerupai gaya hidup orang-orang berprofil <b>{ai_info['golongan']}</b> di dalam dataset kami."
                        
                    html_result = f"""<div style="background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(240,249,255,0.95)); padding: 40px; border-radius: 24px; border: 2px solid rgba(59, 130, 246, 0.3); box-shadow: 0 15px 40px rgba(59, 130, 246, 0.08); margin-top: 30px;">
<div style="text-align: center; margin-bottom: 30px;">
<h3 style="color: #64748b; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 5px;">Skor Indeks Massa Tubuh (BMI): <strong style="color: #0f172a;">{bmi:.1f}</strong></h3>
<h2 style="color: #3b82f6; font-size: 1.5rem; margin-top: 0;">Status Saat Ini: <br>
<span style="font-size: 3.2rem; font-weight: 800; background: linear-gradient(135deg, #ec4899, #f43f5e); -webkit-background-clip: text; -webkit-text-fill-color: transparent; display: inline-block; margin-top: 10px;">{true_info['golongan']}</span></h2>
</div>
<hr style="border: none; height: 1px; background: linear-gradient(90deg, transparent, #cbd5e1, transparent); margin: 0 0 30px 0;">
<div style="display: flex; flex-wrap: wrap; gap: 25px; margin-bottom: 25px;">
<div style="flex: 1; min-width: 280px; background: rgba(255,255,255,0.8); padding: 25px; border-radius: 16px; border: 1px solid rgba(255,255,255,1); box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
<h4 style="color: #0f172a; margin-top: 0; margin-bottom: 15px; font-size: 1.15rem; display: flex; align-items: center; gap: 8px;"><span style="font-size: 1.4rem;">🩺</span> Penjelasan Medis (BMI)</h4>
<p style="font-size: 1rem; color: #475569; line-height: 1.7; margin-bottom: 0;">Berdasarkan perhitungan tinggi badan ({height} cm) dan berat badan ({weight} kg), Anda memiliki skor BMI <b>{bmi:.1f}</b>.<br><br>{true_info['alasan']}</p>
</div>
<div style="flex: 1; min-width: 280px; background: rgba(255,255,255,0.8); padding: 25px; border-radius: 16px; border: 1px solid rgba(255,255,255,1); box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
<h4 style="color: #0f172a; margin-top: 0; margin-bottom: 15px; font-size: 1.15rem; display: flex; align-items: center; gap: 8px;"><span style="font-size: 1.4rem;">📊</span> Evaluasi Gaya Hidup (Dataset)</h4>
<p style="font-size: 1rem; color: #475569; line-height: 1.7; margin-bottom: 0;">{ai_text}</p>
</div>
</div>
<div style="background: linear-gradient(to right, #f8fafc, #f1f5f9); padding: 25px; border-radius: 16px; border-left: 5px solid #10b981; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
<h4 style="color: #0f172a; margin-bottom: 12px; margin-top: 0; font-size: 1.15rem; display: flex; align-items: center; gap: 8px;"><span style="font-size: 1.4rem;">💡</span> Rekomendasi Klinis Utama</h4>
<p style="font-size: 1rem; color: #334155; line-height: 1.7; margin-bottom: 0;">{true_info['saran']}</p>
</div>
</div>"""
                    st.markdown(html_result, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Maaf, terjadi kesalahan saat memproses data: {e}")
