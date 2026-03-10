import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI ---
st.set_page_config(page_title="Portal Akademik Mandiri", layout="wide")

# API KEY AI
API_KEY = "AIzaSyC6cVc6kfcMaPu5H25UmB73RMTlbwt1nR0"
genai.configure(api_key=API_KEY)

# Password Rahasia Bapak untuk memberi izin
PASSWORD_DOSEN = "ADMIN123" 

# Inisialisasi Database Sederhana di Memori
if 'db_mahasiswa' not in st.session_state:
    st.session_state.db_mahasiswa = {} # Format: { 'Nama-Matkul': 'Status' }

# --- SIDEBAR ---
st.sidebar.title("🔐 Akses Masuk")
nama_mhs = st.sidebar.text_input("Nama Lengkap (Sesuai Presensi):")
matkul_pilihan = st.sidebar.selectbox("Pilih Mata Kuliah:", [
    "Pancasila", "Pendidikan Kewarganegaraan", "Communicative Grammar I", 
    "Communicative Grammar II", "Filsafat Moral", "Public Speaking", 
    "Metode Penelitian", "Translation I", "Translation II"
])

key_mhs = f"{nama_mhs.lower()}-{matkul_pilihan}"

st.sidebar.markdown("---")
st.sidebar.subheader("🔑 Menu Otoritas Dosen")
pwd = st.sidebar.text_input("Password Dosen:", type="password")

# --- LOGIKA UTAMA ---
if not nama_mhs:
    st.title("👋 Selamat Datang Pak Guru & Mahasiswa")
    st.info("Silakan masukkan nama di samping untuk memulai.")
else:
    # Cek apakah sudah terdaftar
    if key_mhs not in st.session_state.db_mahasiswa:
        st.title("📝 Pendaftaran Kelas")
        st.warning(f"Nama **{nama_mhs}** belum terdaftar di kelas **{matkul_pilihan}**.")
        if st.button("Klik Untuk Mendaftar"):
            st.session_state.db_mahasiswa[key_mhs] = "Menunggu"
            st.success("Pendaftaran berhasil! Silakan lapor ke Bapak Dosen untuk disetujui.")
            st.rerun()

    else:
        status = st.session_state.db_mahasiswa[key_mhs]
        
        if status == "Disetujui":
            st.title(f"📖 Materi: {matkul_pilihan}")
            st.success(f"Selamat datang {nama_mhs}! Akses Anda telah aktif.")
            
            tanya = st.text_input("Tanyakan sesuatu pada Asisten AI:")
            if tanya:
                model = genai.GenerativeModel('gemini-1.5-flash')
                res = model.generate_content(f"Jawab secara akademik untuk mahasiswa bernama {nama_mhs} di matkul {matkul_pilihan}: {tanya}")
                st.write(res.text)
        else:
            st.title("⏳ Menunggu Persetujuan")
            st.info(f"Halo {nama_mhs}, pendaftaran Anda sedang menunggu divalidasi oleh Bapak Dosen.")

# --- HALAMAN KHUSUS DOSEN (Hanya muncul jika password benar) ---
if pwd == PASSWORD_DOSEN:
    st.markdown("---")
    st.header("👨‍🏫 Ruang Kendali Dosen")
    st.write("Daftar Mahasiswa yang Mengantre Akses:")
    
    if not st.session_state.db_mahasiswa:
        st.write("Belum ada mahasiswa yang mendaftar.")
    else:
        for mhs, stat in st.session_state.db_mahasiswa.items():
            col1, col2, col3 = st.columns([3, 2, 2])
            col1.write(f"**{mhs.split('-')[0].upper()}** ({mhs.split('-')[1]})")
            col2.write(f"Status: {stat}")
            if col3.button("Beri Izin", key=mhs):
                st.session_state.db_mahasiswa[mhs] = "Disetujui"
                st.rerun()
