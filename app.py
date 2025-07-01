import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from datetime import datetime
import folium
from streamlit_folium import st_folium

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Investasi",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .section-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #4a5568;
        margin-bottom: 1rem;
        padding: 0.5rem 0;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #4299e1;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .metric-title {
        font-weight: bold;
        color: #4A4A4A;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-weight: 600;
        font-weight: bold;
        color: #2E7D32;
    }
    .metric-delta {
        font-size: 1rem;
        color: #888;
    }
    
    .tab-container {
        margin: 2rem 0;
    }
    
    .flowchart-container {
        background: #f7fafc;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .info-box {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .highlight-green { color: #38a169; font-weight: bold; }
    .highlight-red { color: #e53e3e; font-weight: bold; }
    .highlight-blue { color: #3182ce; font-weight: bold; }
    
    .kpi-card {
        text-align: center;
        background: #f7fafc;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .kpi-value {
        font-size: 1.8rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .kpi-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .insight-box {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
    }
            
        
    }
</style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<h1 class="main-header">Welcome to Dashboard</h1>', unsafe_allow_html=True)
with col2:
    search_query = st.text_input("", placeholder="🔍 Search...")

# Data untuk statistik utama
stats_data = {
    'Laju Pertumbuhan Ekonomi': {'value': 4.95, 'change': -0.40, 'target': '5.30 - 6.60'},
    'Tingkat Kemiskinan': {'value': 10.47, 'change': -2.79, 'target': '9.50 - 10.00'},
    'Indeks Pembangunan Manusia': {'value': 73.88, 'change': 2.79, 'target': 'Target RKP 2024'},
    'Tingkat Pengangguran Terbuka': {'value': 5.57, 'change': -2.79, 'target': '4.60 - 5.30'},
    'Rasio Gini': {'value': 0.369, 'change': -2.79, 'target': 'Target RKP 2024'}
}

# Menampilkan kartu statistik
st.subheader("📈 Indikator Utama")
cols = st.columns(5)
for i, (label, data) in enumerate(stats_data.items()):
    with cols[i]:
        delta_color = "normal" if data['change'] > 0 else "inverse"
        st.metric(
            label=label,
            value=f"{data['value']:.2f}" if data['value'] < 100 else f"{data['value']:.1f}",
            delta=f"{data['change']:.2f}%",
            delta_color=delta_color
        )
        st.caption(f"Target: {data['target']}")

# Tabs untuk kategori
st.markdown('<div class="tab-container">', unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(["📚 Investasi", "🏥 Kesehatan", "🚌 Transportasi", "🏗️ Infrastruktur"])

with tab1:
    # Layout utama dengan 3 kolom
    col1, col2, col3 = st.columns([2, 2, 1.5])

    # ============= KOLOM 1: PETA SEBARAN INVESTASI =============
    with col1:
        st.markdown('<div class="section-title">📍 Peta Sebaran Investasi</div>', unsafe_allow_html=True)
        
        # Data simulasi untuk peta Jawa Tengah
        jateng_data = pd.DataFrame({
            'Kabupaten/Kota': ['Semarang', 'Kendal', 'Batang', 'Pekalongan', 'Pemalang', 'Tegal', 'Brebes'],
            'Status': ['Realisasi', 'Realisasi', 'Realisasi', 'Nasional Imajiner', 'Imajiner', 'Nasional Imajiner', 'Imajiner'],
            'Investasi': [97.5, 96.3, 94.3, 87.2, 82.1, 78.5, 75.3],
            'Lat': [-6.9667, -6.9167, -6.9042, -6.8889, -6.8917, -6.8694, -6.8717],
            'Lon': [110.4167, 110.2042, 109.7292, 109.6753, 109.3842, 109.1403, 109.0428]
        })
        
        # Buat peta dengan plotly
        color_map = {
            'Realisasi': '#38a169',      # Hijau
            'Nasional Imajiner': '#e53e3e',  # Merah  
            'Imajiner': '#3182ce'        # Biru
        }
        
        fig_map = px.scatter_mapbox(
            jateng_data,
            lat="Lat",
            lon="Lon",
            color="Status",
            size="Investasi",
            hover_name="Kabupaten/Kota",
            hover_data={"Investasi": ":.1f", "Status": True},
            color_discrete_map=color_map,
            size_max=20,
            zoom=8,
            center={"lat": -6.9, "lon": 110.0},
            height=400,
            mapbox_style="open-street-map"
        )
        
        fig_map.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            legend=dict(
                title="Legenda",
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(255,255,255,0.8)"
            )
        )
        st.plotly_chart(fig_map, use_container_width=True)
        
        # ============= TREN REALISASI INVESTASI 2016-2024 =============
        st.markdown('<div class="section-title">📈 Tren Realisasi Investasi 2016-2024</div>', unsafe_allow_html=True)
        
        years = list(range(2016, 2025))
        trend_data = pd.DataFrame({
            'Tahun': years,
            'DK Jakarta': [8, 20, 18, 20, 18, 25, 15, 16, 25],
            'Jabar': [15, 9, 8, 9, 10, 6, 4, 3, 18],
            'Jateng': [20, 19, 19, 18, 6, 5, 5, 2, 8],
            'DIY': [28, 28, 26, 25, 22, 20, 18, 16, 15]
        })
        
        fig_trend = go.Figure()
        colors = ['#38a169', '#3182ce', '#e53e3e', '#ed8936']
        
        for i, col in enumerate(['DK Jakarta', 'Jabar', 'Jateng', 'DIY']):
            fig_trend.add_trace(go.Scatter(
                x=trend_data['Tahun'],
                y=trend_data[col],
                mode='lines+markers',
                name=col,
                line=dict(color=colors[i], width=3),
                marker=dict(size=6)
            ))
        
        fig_trend.update_layout(
            height=300,
            xaxis_title="Tahun",
            yaxis_title="Nilai (Triliun)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=40)
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        # Tambahan: Summary Stats
        st.markdown('<div class="section-title">📈 Ringkasan Bulan Ini</div>', unsafe_allow_html=True)
        
        summary_cols = st.columns(2)
        with summary_cols[0]:
            st.markdown("""
            <div class="info-box">
                <div class="metric-title">Proyek Baru</div>
                <div class="metric-value">47</div>
                <div class="metric-delta">+12</div>
            </div>
            """, unsafe_allow_html=True)
        with summary_cols[1]:
            st.markdown("""
            <div class="info-box">
                <div class="metric-title">Investasi Baru</div>
                <div class="metric-value">2.3T</div>
                <div class="metric-delta">+0.8T</div>
            </div>
            """, unsafe_allow_html=True)
        

    # ============= KOLOM 2: DIAGRAM ALUR & TABEL =============
    with col2:
        # Diagram Alur Investasi
        st.markdown('<div class="section-title">🔄 Diagram Alur Investasi</div>', unsafe_allow_html=True)
        
        # Membuat flowchart sederhana dengan plotly
        fig_flow = go.Figure()
        
        # Kotak-kotak flowchart
        boxes = [
            {"text": "Identifikasi<br>Potensi", "x": 1, "y": 3, "color": "#38a169"},
            {"text": "Realisasi<br>Proyek", "x": 3, "y": 3, "color": "#e53e3e"},
            {"text": "Promosi", "x": 5, "y": 4, "color": "#38a169"},
            {"text": "Redisasi<br>Proyek", "x": 5, "y": 3, "color": "#38a169"},
            {"text": "Monitoring", "x": 5, "y": 2, "color": "#38a169"}
        ]
        
        # Tambahkan shapes untuk kotak
        shapes = []
        annotations = []
        
        for box in boxes:
            shapes.append(
                dict(
                    type="rect",
                    x0=box["x"]-0.4, y0=box["y"]-0.3,
                    x1=box["x"]+0.4, y1=box["y"]+0.3,
                    fillcolor=box["color"],
                    line=dict(color=box["color"], width=2),
                    opacity=0.8
                )
            )
            annotations.append(
                dict(
                    x=box["x"], y=box["y"],
                    text=box["text"],
                    showarrow=False,
                    font=dict(color="white", size=10),
                    align="center"
                )
            )
        
        # Tambahkan panah
        shapes.extend([
            # Panah dari Identifikasi ke Realisasi
            dict(type="line", x0=1.4, y0=3, x1=2.6, y1=3, 
                line=dict(color="gray", width=2)),
            # Panah dari Realisasi ke Promosi/Redisasi/Monitoring
            dict(type="line", x0=3.4, y0=3, x1=4.6, y1=3, 
                line=dict(color="gray", width=2)),
            # Panah vertikal ke Promosi dan Monitoring
            dict(type="line", x0=4.6, y0=3, x1=4.6, y1=4, 
                line=dict(color="gray", width=2)),
            dict(type="line", x0=4.6, y0=3, x1=4.6, y1=2, 
                line=dict(color="gray", width=2)),
        ])
        
        fig_flow.update_layout(
            shapes=shapes,
            annotations=annotations,
            xaxis=dict(range=[0, 6], showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(range=[1, 5], showgrid=False, zeroline=False, showticklabels=False),
            height=200,
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=20, b=20, l=20, r=20)
        )
        
        st.plotly_chart(fig_flow, use_container_width=True)
        
        # ============= DAFTAR INDIKASI PROYEK INVESTASI =============
        st.markdown('<div class="section-title">📋 Daftar Indikasi Proyek Investasi</div>', unsafe_allow_html=True)
        
        project_table = pd.DataFrame({
            'Kabupaten/Kota': ['Semarang', 'Kendal', 'Batang'],
            'Nilai Indikator': [97.5, 96.3, 94.3],
            'Ranking': [1, 2, 3],
            'Realisasi (T)': ['85.5 T', '47.2 T', '38.4 T']
        })
        
        # Style the dataframe
        st.dataframe(
            project_table,
            use_container_width=True,
            height=150,
            hide_index=True
        )
        

        # ============= KETERANGAN =============
        
        st.markdown("""
        <div class="insight-box">
            <h4>📈 Capaian Realisasi Investasi</h4>
            <ul>
                <li>Capaian realisasi investasi mengalami sedikit penurunan dibanding target, terutama dari sektor PMDN</li>
                <li>Namun, proyek strategis nasional di <strong>Batang</strong> dan <strong>kendal</strong> menunjukkan peningkatan signifikan</li>
                <li>Perlu fokus pada penyederhanaan proses perizinan, perbaikan sistem OSS, serta penguatan promosi sektor unggulan di kawasan</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Indikator Performa
        st.markdown('<div class="section-title">📊 Indikator Performa</div>', unsafe_allow_html=True)
        
        perf_cols = st.columns(4)
        indicators = [
            {"label": "M63 T", "value": "3.5%", "trend": "down", "color": "red"},
            {"label": "PMO T", "value": "1.2%", "trend": "up", "color": "green"},
            {"label": "PMDN", "value": "3.1%", "trend": "up", "color": "green"},
            {"label": "OSS", "value": "0.8%", "trend": "down", "color": "red"}
        ]
        
        for i, ind in enumerate(indicators):
            with perf_cols[i]:
                trend_symbol = "↗" if ind["trend"] == "up" else "↘"
                color_class = "highlight-green" if ind["color"] == "green" else "highlight-red"
                st.markdown(f"""
                <div style="text-align: center; padding: 0.5rem; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 0.25rem;">{ind['label']}</div>
                    <div class="{color_class}">{trend_symbol} {ind['value']}</div>
                </div>
                """, unsafe_allow_html=True)

    # ============= KOLOM 3: NILAI INVESTASI & KETERANGAN =============
    with col3:

        # KPI Cards
        st.markdown('<div class="section-title">💰 Nilai Investasi Masuk</div>', unsafe_allow_html=True)
        
        kpi_data = [
            {"label": "Nilai Investasi Masuk", "value": "85,0 T", "suffix": "85,6 T*"},
            {"label": "Realisasi PMA", "value": "47,2 T", "suffix": ""},
            {"label": "Jumlah Proyek", "value": "1,250", "suffix": "1,24 T"},
            {"label": "Rasio Investasi terhadap", "value": "29,9 %", "suffix": "29,8 %"},
            {"label": "Tingkat Kepatuhan OSS", "value": "81,2 %", "suffix": ""}
        ]
        
        for kpi in kpi_data:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{kpi['label']}</div>
                <div class="kpi-value">{kpi['value']}</div>
                {f'<div style="font-size: 0.8rem; opacity: 0.8;">{kpi["suffix"]}</div>' if kpi['suffix'] else ''}
            </div>
            """, unsafe_allow_html=True)
        

# Tab Kesehatan
with tab2:
    st.info("🏥 Dashboard Kesehatan - Dalam Pengembangan")
    
    # Contoh chart untuk kesehatan
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏥 Fasilitas Kesehatan")
        health_facilities = pd.DataFrame({
            'Jenis Fasilitas': ['RS Pemerintah', 'RS Swasta', 'Puskesmas', 'Klinik'],
            'Jumlah': [1200, 2800, 9500, 15000]
        })
        
        fig_bar = px.bar(
            health_facilities,
            x='Jenis Fasilitas',
            y='Jumlah',
            color='Jumlah',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.subheader("💉 Cakupan Vaksinasi")
        vaccination_data = pd.DataFrame({
            'Provinsi': ['DKI Jakarta', 'Jawa Barat', 'Jawa Tengah', 'Jawa Timur', 'Sumatera Utara'],
            'Cakupan (%)': [95.2, 87.3, 91.8, 89.4, 84.7]
        })
        
        fig_horizontal = px.bar(
            vaccination_data,
            x='Cakupan (%)',
            y='Provinsi',
            orientation='h',
            color='Cakupan (%)',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig_horizontal, use_container_width=True)

# Tab Transportasi
with tab3:
    st.info("🚌 Dashboard Transportasi - Dalam Pengembangan")
    
    # Contoh untuk transportasi
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🚊 Transportasi Publik")
        transport_data = pd.DataFrame({
            'Moda': ['Bus', 'KRL', 'MRT', 'LRT', 'Angkot'],
            'Penumpang/Hari': [150000, 800000, 120000, 80000, 200000]
        })
        
        fig_donut = px.pie(
            transport_data,
            values='Penumpang/Hari',
            names='Moda',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    
    with col2:
        st.subheader("🛣️ Kondisi Jalan")
        road_condition = pd.DataFrame({
            'Kondisi': ['Baik', 'Sedang', 'Rusak Ringan', 'Rusak Berat'],
            'Persentase': [45, 30, 20, 5]
        })
        
        fig_funnel = px.funnel(
            road_condition,
            x='Persentase',
            y='Kondisi',
            color='Kondisi',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_funnel, use_container_width=True)

# Tab Infrastruktur
with tab4:
    st.info("🏗️ Dashboard Infrastruktur - Dalam Pengembangan")
    
    # Contoh untuk infrastruktur
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏗️ Proyek Infrastruktur")
        infra_projects = pd.DataFrame({
            'Sektor': ['Jalan Tol', 'Bandara', 'Pelabuhan', 'Bendungan', 'Pembangkit Listrik'],
            'Anggaran (Triliun)': [85.5, 45.2, 32.8, 28.6, 67.9],
            'Progress (%)': [78, 65, 82, 91, 55]
        })
        
        fig_scatter = px.scatter(
            infra_projects,
            x='Anggaran (Triliun)',
            y='Progress (%)',
            size='Anggaran (Triliun)',
            color='Sektor',
            hover_name='Sektor',
            size_max=20
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        st.subheader("⚡ Konsumsi Energi")
        energy_data = pd.DataFrame({
            'Bulan': pd.date_range('2024-01-01', periods=12, freq='M'),
            'Konsumsi (TWh)': np.random.uniform(15, 25, 12)
        })
        
        fig_area = px.area(
            energy_data,
            x='Bulan',
            y='Konsumsi (TWh)',
            color_discrete_sequence=['#ff6b6b']
        )
        st.plotly_chart(fig_area, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #718096; font-size: 12px; margin-top: 1rem;">
    📊 Dashboard Investasi Daerah | Data per {date} | Sumber: BKPM & Dinas PMPTSP
</div>
""".format(date=datetime.now().strftime("%B %Y")), unsafe_allow_html=True)

# Sidebar untuk kontrol tambahan
with st.sidebar:
    st.header("🎛️ Kontrol Dashboard")
    
    # Filter periode
    periode = st.selectbox(
        "Periode Data",
        ["Bulanan", "Triwulanan", "Tahunan"],
        index=2
    )
    
    # Filter wilayah
    wilayah_focus = st.multiselect(
        "Fokus Wilayah",
        ["Semarang", "Kendal", "Batang", "Pekalongan", "Pemalang"],
        default=["Semarang", "Kendal", "Batang"]
    )
    
    # Toggle advanced view
    advanced_view = st.checkbox("Mode Lanjutan", value=False)
    
    if advanced_view:
        st.subheader("⚙️ Pengaturan Lanjutan")
        
        # Threshold settings
        investment_threshold = st.slider(
            "Ambang Batas Investasi (T)",
            min_value=1.0,
            max_value=100.0,
            value=50.0,
            step=5.0
        )
        
        # Export options
        st.subheader("📤 Export Data")
        export_format = st.radio(
            "Format Export",
            ["CSV", "Excel", "PDF Report"]
        )
        
        if st.button("📥 Download Data"):
            if export_format == "CSV":
                csv_data = jateng_data.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    csv_data,
                    f"investasi_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    "text/csv"
                )
    
    # Status sistem
    st.markdown("---")
    st.markdown("**🔄 Status Sistem:**")
    st.success("✅ Koneksi Database: Normal")
    st.success("✅ Update Data: Real-time")
    st.info(f"🕐 Terakhir refresh: {datetime.now().strftime('%H:%M:%S')}")
    
    # Quick actions
    st.markdown("**⚡ Quick Actions:**")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔄 Refresh"):
            st.rerun()
    with col_b:
        if st.button("📊 Report"):
            st.info("Generating report...")