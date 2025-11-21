import streamlit as st

# ==========================================
# KONFIGURASI HALAMAN WEB
# ==========================================
st.set_page_config(
    page_title="Cek Kualitas Tidur",
    page_icon="🛌",
    layout="centered"
)

# ==========================================
# 1. DATABASE KNOWLEDGE BASE (BAHASA AWAM)
# ==========================================
def load_knowledge_base():
    return {
        "basis_pengetahuan": [
            {
                "kategori": "🤔 BAGIAN 1: SUSAH MULAI TIDUR?",
                "pertanyaan": [
                    {
                        "id": "Q01", 
                        "teks": "Setelah rebahan dan memejamkan mata, apakah Anda butuh waktu lebih dari 30 menit sampai benar-benar terlelap?", 
                        "bobot": 5, 
                        "saran": "Cobalah teknik napas santai 4-7-8 (Tarik napas 4 detik, tahan 7 detik, buang 8 detik) agar badan rileks."
                    },
                    {
                        "id": "Q02", 
                        "teks": "Apakah pikiran Anda sering 'muter-muter' (overthinking) atau cemas justru saat mau tidur?", 
                        "bobot": 4, 
                        "saran": "Coba tuliskan semua pikiran itu di kertas (Jurnal) 1 jam sebelum tidur, supaya kepala jadi enteng."
                    }
                ]
            },
            {
                "kategori": "⏰ BAGIAN 2: JADWAL & KEBIASAAN",
                "pertanyaan": [
                    {
                        "id": "Q03", 
                        "teks": "Apakah total jam tidur Anda kurang dari 6 jam sehari?", 
                        "bobot": 5, 
                        "saran": "Tubuh butuh minimal 7 jam untuk 'servis' sel rusak. Coba majukan jam tidur Anda malam ini."
                    },
                    {
                        "id": "Q04", 
                        "teks": "Apakah jam tidur Anda berantakan? (Misal: Senin tidur jam 9, Sabtu tidur jam 2 pagi)", 
                        "bobot": 4, 
                        "saran": "Badan bingung kalau jamnya ganti-ganti. Usahakan bangun di jam yang sama setiap hari, bahkan saat libur."
                    },
                    {
                        "id": "Q05", 
                        "teks": "Apakah Anda sering memakai kasur untuk kerja, makan, atau nonton TV?", 
                        "bobot": 3, 
                        "saran": "Otak jadi bingung membedakan 'tempat kerja' dan 'tempat tidur'. Gunakan kasur HANYA untuk tidur."
                    }
                ]
            },
            {
                "kategori": "🛌 BAGIAN 3: GANGGUAN SAAT TIDUR",
                "pertanyaan": [
                    {
                        "id": "Q06", 
                        "teks": "Apakah sering terbangun tengah malam lalu susah tidur lagi?", 
                        "bobot": 5, 
                        "saran": "Pastikan kamar gelap total dan sejuk (sekitar 20°C). Jangan nyalakan lampu/HP saat terbangun."
                    },
                    {
                        "id": "Q07", 
                        "teks": "Apakah orang rumah bilang kalau Anda ngoroknya kencang banget atau sampai seperti tersedak?", 
                        "bobot": 10, 
                        "saran": "HATI-HATI: Ini tanda napas terhenti sejenak (Sleep Apnea). Bahaya buat jantung. Segera cek ke Dokter."
                    },
                    {
                        "id": "Q08", 
                        "teks": "Apakah kaki rasanya pegal/geli/tidak nyaman kalau didiamkan saat mau tidur?", 
                        "bobot": 5, 
                        "saran": "Mungkin Anda kurang Zat Besi atau Magnesium. Coba pijat kaki dengan air hangat sebelum tidur."
                    }
                ]
            },
            {
                "kategori": "📱 BAGIAN 4: GAYA HIDUP SEBELUM TIDUR",
                "pertanyaan": [
                    {
                        "id": "Q11", 
                        "teks": "Apakah Anda main HP (Scroll sosmed/Chat) sambil tiduran sampai ketiduran?", 
                        "bobot": 4, 
                        "saran": "Cahaya layar HP bikin otak mengira hari masih siang. Letakkan HP jauh dari kasur 1 jam sebelum tidur."
                    },
                    {
                        "id": "Q12", 
                        "teks": "Apakah Anda minum kopi, teh, atau minuman berenergi di sore/malam hari?", 
                        "bobot": 4, 
                        "saran": "Efek kopi bisa tahan 8 jam di darah. Kalau mau ngopi, usahakan sebelum jam 2 siang."
                    },
                    {
                        "id": "Q13", 
                        "teks": "Apakah Anda makan berat (Nasi padang/Gorengan) tepat sebelum tidur?", 
                        "bobot": 3, 
                        "saran": "Perut yang sibuk mencerna bikin suhu badan naik, jadinya tidur tidak nyenyak. Beri jeda 3 jam setelah makan."
                    }
                ]
            },
            {
                "kategori": "😫 BAGIAN 5: EFEK SETELAH BANGUN",
                "pertanyaan": [
                    {
                        "id": "Q17", 
                        "teks": "Apakah siang-siang Anda mengantuk berat sampai susah konsentrasi?", 
                        "bobot": 5, 
                        "saran": "Ini tandanya Anda punya 'Hutang Tidur'. Jangan diabaikan, tubuh minta istirahat."
                    },
                    {
                        "id": "Q18", 
                        "teks": "Apakah Anda jadi gampang marah atau baperan tanpa alasan jelas?", 
                        "bobot": 4, 
                        "saran": "Kurang tidur bikin emosi tidak stabil. Tidur yang cukup bisa bikin perasaan lebih tenang."
                    }
                ]
            }
        ],
        "klasifikasi": [
            {"max": 15, "label": "🌟 TIDUR ANDA JUARA! (Sehat)", "desc": "Pola tidur Anda sudah mantap. Badan pasti terasa segar. Pertahankan kebiasaan ini!", "color": "success"},
            {"max": 35, "label": "⚠️ KURANG OKE (Butuh Perbaikan)", "desc": "Ada beberapa kebiasaan yang bikin tidur Anda kurang berkualitas. Coba cek saran di bawah.", "color": "warning"},
            {"max": 60, "label": "🚑 BURUK (Lampu Merah)", "desc": "Pola tidur ini bisa bikin gampang sakit dan stress. Harus segera diperbaiki mulai malam ini.", "color": "error"},
            {"max": 100, "label": "💀 SANGAT BAHAYA (Segera ke Dokter)", "desc": "Ini bukan masalah biasa lagi. Ada tanda gangguan serius. Sebaiknya konsultasi ke Dokter/Klinik Tidur.", "color": "error"}
        ]
    }

# ==========================================
# 2. LOGIKA UTAMA WEB APP
# ==========================================
def main():
    st.title("🛌 Cek Kualitas Tidur")
    st.markdown("""
    Selamat datang! Sistem ini akan membantu Anda mengecek apakah tidur Anda sudah sehat atau belum.
    **Jawab pertanyaan di bawah ini dengan jujur ya!**
    """)
    
    st.divider()

    data = load_knowledge_base()
    user_answers = {} 
    
    # --- FORM INPUT ---
    with st.form("form_diagnosa"):
        for kategori in data['basis_pengetahuan']:
            # Menggunakan expander agar tidak kepanjangan
            with st.expander(kategori['kategori'], expanded=True):
                for p in kategori['pertanyaan']:
                    jawaban = st.radio(
                        f"{p['teks']}",
                        ('Tidak', 'Ya'),
                        index=0,
                        key=p['id'],
                        horizontal=True
                    )
                    user_answers[p['id']] = jawaban

        submit_button = st.form_submit_button("🔍 Cek Hasil Saya Sekarang", type="primary")

    # --- PROSES (Saat Tombol Ditekan) ---
    if submit_button:
        total_skor = 0
        list_saran = []
        detail_skor_dimensi = {}

        # Hitung Skor
        for kategori in data['basis_pengetahuan']:
            skor_dimensi = 0
            for p in kategori['pertanyaan']:
                if user_answers[p['id']] == 'Ya':
                    total_skor += p['bobot']
                    skor_dimensi += p['bobot']
                    # Format saran lebih ramah
                    list_saran.append(f"💡 **Masalah:** {p['teks']}\n   👉 **Solusi:** {p['saran']}")
            
            detail_skor_dimensi[kategori['kategori']] = skor_dimensi

        # Hasil Klasifikasi
        hasil_label = "Unknown"
        hasil_desc = ""
        hasil_color = "info"
        
        sorted_rules = sorted(data['klasifikasi'], key=lambda x: x['max'])
        for rule in sorted_rules:
            if total_skor <= rule['max']:
                hasil_label = rule['label']
                hasil_desc = rule['desc']
                hasil_color = rule['color']
                break

        # Tampilan Output
        st.divider()
        st.subheader("📊 Hasil Analisis Anda")
        
        if hasil_color == "success":
            st.success(f"### {hasil_label}\n{hasil_desc}")
        elif hasil_color == "warning":
            st.warning(f"### {hasil_label}\n{hasil_desc}")
        else:
            st.error(f"### {hasil_label}\n{hasil_desc}")

        # Kolom Skor
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Skor Masalah", f"{total_skor} / 85")
            st.caption("Semakin RENDAH skor, tidur makin BAGUS.")
        with col2:
            st.write("**Sumber Masalah Terbesar:**")
            # Mencari dimensi dengan masalah terbanyak
            sorted_dimensi = sorted(detail_skor_dimensi.items(), key=lambda x: x[1], reverse=True)
            top_problem = sorted_dimensi[0]
            if top_problem[1] > 0:
                st.error(f"{top_problem[0]} (Poin: {top_problem[1]})")
            else:
                st.success("Tidak ada masalah spesifik.")

        st.subheader("📝 Saran Dokter/Pakar Untuk Anda")
        if len(list_saran) > 0:
            for saran in list_saran:
                st.info(saran)
        else:
            st.balloons()
            st.success("Wah hebat! Tidak ada saran perbaikan karena tidur Anda sudah sempurna.")

if __name__ == "__main__":
    main()