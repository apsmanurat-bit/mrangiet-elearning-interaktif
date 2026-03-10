import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Portal Akademik & Ujian", layout="wide")

# API KEY AI
API_KEY = "AIzaSyC6cVc6kfcMaPu5H25UmB73RMTlbwt1nR0"
genai.configure(api_key=API_KEY)

# Password Rahasia Bapak
PASSWORD_DOSEN = "ADMIN123" 

# Inisialisasi Database Internal
if 'db_mahasiswa' not in st.session_state:
    st.session_state.db_mahasiswa = {} 

# --- DATA MATERI KULIAH ---
MATERI_KULIAH = {
    "Pancasila": "📖 **Modul Pancasila:** Dasar Negara dan Ideologi.",
    "Pendidikan Kewarganegaraan": "📖 **Modul PKn:** Hak dan Kewajiban Warga Negara.",
    "Communicative Grammar I": "📖 **Modul Grammar I:** Dasar-dasar Tenses.",
    "Communicative Grammar II": "📖 **Modul Grammar II:** Advanced Grammar.",
    "Filsafat Moral": "📖 **Modul Filsafat Moral:** Etika dan Kebajikan.",
    "Public Speaking": "📖 **Modul Public Speaking:** Teknik Berbicara di Depan Umum.",
    "Metode Penelitian": "📖 **Modul Metopel:** Teknik Menyusun Skripsi.",
    "Translation I": "📖 **Modul Translation I:** Dasar Penerjemahan.",
    "Translation II": "📖 **Modul Translation II:** Penerjemahan Akademik."
}

# --- SIDEBAR ---
st.sidebar.title("🔐 Portal Akademik")
nama_mhs = st.sidebar.text_input("Nama Lengkap Anda:")
matkul_pilihan = st.sidebar.selectbox("Pilih Mata Kuliah:", list(MATERI_KULIAH.keys()))

st.sidebar.markdown("---")
st.sidebar.subheader("👨‍🏫 Otoritas Dosen")
pwd = st.sidebar.text_input("Password Rahasia:", type="password")

key_mhs = f"{nama_mhs.lower()}-{matkul_pilihan}"

# --- LOGIKA UTAMA ---
if not nama_mhs:
    st.title("👋 Selamat Datang")
    st.info("Silakan isi Nama dan pilih Mata Kuliah di samping.")
else:
    if key_mhs not in st.session_state.db_mahasiswa:
        st.title("📝 Form Pendaftaran")
        st.warning(f"Halo {nama_mhs}, Anda belum terdaftar di kelas **{matkul_pilihan}**.")
        if st.button("Daftar ke Kelas"):
            st.session_state.db_mahasiswa[key_mhs] = "Menunggu"
            st.success("Pendaftaran Terkirim! Mohon tunggu persetujuan Bapak Dosen.")
            st.rerun()
    else:
        status = st.session_state.db_mahasiswa[key_mhs]
        
        if status == "Disetujui":
            st.sidebar.success("✅ Akses Diterima")
            
            # --- LOGIKA MENU DINAMIS ---
            # Default menu
            pilihan_menu = ["🏠 Beranda", "📖 Baca Materi", "📝 Menu Ujian", "🤖 Tanya Asisten AI"]
            
            # Pilih Menu Utama
            menu_utama = st.sidebar.radio("Navigasi:", pilihan_menu)
            
            # LOGIKA PROTEKSI: Jika memilih Ujian, sembunyikan fitur AI
            if menu_utama == "📝 Menu Ujian":
                st.title("✍️ Pusat Ujian & Tes")
                st.warning("⚠️ Perhatian: Fitur Asisten AI dinonaktifkan selama sesi ujian berlangsung.")
                
                sub_ujian = st.selectbox("Pilih Jenis Ujian:", [
                    "--- Pilih Ujian ---", "QUIZ 1", "QUIZ 2", "QUIZ 3", "QUIZ 4", 
                    "MID TEST", "FINAL TEST", "FINAL PROJECT"
                ])
                
                if sub_ujian != "--- Pilih Ujian ---":
                    st.subheader(f"Sesi: {sub_ujian}")
                    st.write(f"Silakan kerjakan {sub_ujian} untuk mata kuliah {matkul_pilihan}.")
                    st.info("Soal ujian akan tampil di sini sesuai instruksi Bapak Dosen.")
                    # Mahasiswa tidak bisa melihat "Tanya Asisten AI" karena radio button pindah ke sini
                
            elif menu_utama == "🏠 Beranda":
                st.title(f"Selamat Datang, {nama_mhs}!")
                st.write(f"Anda masuk di kelas **{matkul_pilihan}**.")
                
            elif menu_utama == "📖 Baca Materi":
                st.title(f"📚 Materi: {matkul_pilihan}")
                st.info(MATERI_KULIAH[matkul_pilihan])
                
            elif menu_utama == "🤖 Tanya Asisten AI":
                st.title("🤖 Asisten AI Akademik")
                st.write("Silakan bertanya apa saja seputar materi kuliah.")
                tanya = st.text_input("Ketik pertanyaan Anda:")
                if tanya:
                    with st.spinner("Mencari jawaban..."):
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        res = model.generate_content(f"Jawab pertanyaan mahasiswa bernama {nama_mhs} tentang {matkul_pilihan}: {tanya}")
                        st.write(res.text)
        
        else:
            st.title("⏳ Menunggu Otoritas")
            st.warning(f"Pendaftaran {nama_mhs} sedang diproses oleh Bapak Dosen.")

# --- RUANG KENDALI DOSEN ---
if pwd == PASSWORD_DOSEN:
    st.markdown("---")
    st.header("👨‍🏫 Panel Otoritas Dosen")
    if not st.session_state.db_mahasiswa:
        st.write("Belum ada antrean pendaftaran.")
    else:
        for mhs, stat in st.session_state.db_mahasiswa.items():
            if stat == "Menunggu":
                col1, col2, col3 = st.columns([3, 2, 2])
                col1.write(f"👤 **{mhs.split('-')[0].upper()}**")
                col2.write(f"📘 {mhs.split('-')[1]}")
                if col3.button("SETUJUI", key=mhs):
                    st.session_state.db_mahasiswa[mhs] = "Disetujui"
                    st.rerun()
