import streamlit as st
import json
import datetime
from datetime import timedelta
import os
import pandas as pd
import plotly.express as px
import base64  # <--- INI YANG TADI LUPA DIMASUKKAN

# ==========================================
# 1. KONFIGURASI & CSS
# ==========================================
st.set_page_config(
    page_title="SleepFlow Ultimate",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed" 
)

# CSS AGAR TAMPILAN SEPERTI APLIKASI ASLI
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Tab Menu Style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        flex: 1;
    }
    .stTabs [aria-selected="true"] {
        background-color: #6C63FF;
        color: white;
    }

    /* Tombol */
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 3.5em;
        font-weight: bold;
        border: none;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SISTEM DATABASE & LOGIC
# ==========================================
DB_FILE = 'riwayat_tidur.csv'

def init_db():
    if not os.path.exists(DB_FILE):
        df = pd.DataFrame(columns=['Tanggal', 'Skor', 'Status'])
        df.to_csv(DB_FILE, index=False)

def save_to_history(skor, status):
    init_db()
    df = pd.read_csv(DB_FILE)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    new_data = pd.DataFrame({'Tanggal': [now], 'Skor': [skor], 'Status': [status]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

def load_history():
    init_db()
    return pd.read_csv(DB_FILE)

def load_knowledge_base():
    if not os.path.exists('sleep_data.json'):
        return []
    # Encoding utf-8 biar emoji aman
    with open('sleep_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['questions']

# ==========================================
# 3. HALAMAN: DASHBOARD
# ==========================================
def show_dashboard():
    st.header("📊 Statistik")
    df = load_history()
    
    if df.empty:
        st.info("Data masih kosong. Yuk cek tidurmu dulu!")
    else:
        avg = df['Skor'].mean()
        last = df.iloc[-1]['Status']
        col1, col2 = st.columns(2)
        col1.metric("Rata-rata", f"{avg:.1f}")
        col2.metric("Terakhir", last)
        
        fig = px.line(df, x='Tanggal', y='Skor', markers=True)
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 4. HALAMAN: DIAGNOSA
# ==========================================
def show_diagnosa():
    st.header("🩺 Cek Tidur")
    questions = load_knowledge_base()
    
    if not questions:
        st.error("Database sleep_data.json tidak ditemukan!")
        return

    with st.form("cek_tidur"):
        answers = {}
        for q in questions:
            st.write(f"**{q['text']}**")
            answers[q['id']] = st.radio("Label", ["Tidak", "Ya"], horizontal=True, key=q['id'], label_visibility="collapsed")
            st.write("---")
        
        if st.form_submit_button("Analisis"):
            score = sum([q['bobot'] for q in questions if answers[q['id']] == "Ya"])
            saran = [q['saran'] for q in questions if answers[q['id']] == "Ya"]
            
            if score < 10: status = "Sehat"
            elif score < 25: status = "Warning"
            else: status = "Bahaya"
            
            save_to_history(score, status)
            
            st.success(f"Skor: {score} ({status})")
            for s in saran:
                st.info(s)

# ==========================================
# 5. HALAMAN: TOOLS (DENGAN LOOPING)
# ==========================================
def show_tools():
    st.header("🛠️ Alat Bantu")
    
    subtab1, subtab2 = st.tabs(["🧮 Kalkulator", "🎧 Musik (Loop)"])
    
    with subtab1:
        bangun = st.time_input("Mau bangun jam?", datetime.time(5,0))
        if st.button("Hitung"):
            tgl = datetime.datetime.combine(datetime.date.today() + timedelta(days=1), bangun)
            ideal = tgl - timedelta(hours=7.5)
            st.success(f"Tidur jam: **{ideal.strftime('%H:%M')}**")
            
    with subtab2:
        st.write("Suara relaksasi (Akan berputar terus/Looping).")
        
        # FUNGSI AUDIO LOOPING
        def putar_audio_loop(label, nama_file):
            file_path = f"audio/{nama_file}"
            
            st.markdown(f"**{label}**")
            
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    data = f.read()
                b64 = base64.b64encode(data).decode()
                
                # HTML Player dengan atribut 'loop'
                md = f"""
                    <audio controls loop style="width:100%;">
                        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    </audio>
                """
                st.markdown(md, unsafe_allow_html=True)
            else:
                st.error(f"File '{nama_file}' tidak ada di folder audio!")

        # Tampilan Grid
        c1, c2 = st.columns(2)
        
        with c1:
            putar_audio_loop("🌧️ Hujan", "hujan.mp3")
            st.write("---") 
            putar_audio_loop("🔥 Api", "api.mp3")
            
        with c2:
            putar_audio_loop("🦗 Jangkrik", "jangkrik.mp3")
            st.write("---")
            putar_audio_loop("🌊 Sungai", "sungai.mp3")

# ==========================================
# 6. NAVIGASI UTAMA
# ==========================================
def main():
    st.caption("SleepFlow Pro v3.1")

    # MENU TABS UTAMA (SELALU DI ATAS)
    tab1, tab2, tab3 = st.tabs(["🏠 DASHBOARD", "🩺 CEK TIDUR", "🛠️ TOOLS"])

    with tab1:
        show_dashboard()
    
    with tab2:
        show_diagnosa()
        
    with tab3:
        show_tools()

if __name__ == "__main__":
    main()