import streamlit as st
import pandas as pd
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="Portal Akademik Bapak", layout="wide")

# --- KONEKSI DATABASE ---
ID_SHEET = "10AY2akSXfTdG2hoNpqh65YTCgWZ9ZZIzC82POnVvyf8"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/export?format=csv&gid=0"

# API KEY AI
API_KEY = "AIzaSyC6cVc6kfcMaPu5H25UmB73RMTlbwt1nR0"
genai.configure(api_key=API_KEY)

def cek_status_mahasiswa(nama_cari, matkul_cari):
    try:
        import time
        # Menambahkan angka acak agar data selalu terbaru
        url_refresh = f"{SHEET_URL}&cache={int(time.time())}"
        df = pd.read_csv(url_refresh)
        
        # Bersihkan nama kolom
        df.columns = df.columns.str.strip().str.upper()
        
        # Bersihkan data dari spasi tambahan
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        # Cari mahasiswa (tidak peka huruf besar/kecil)
        match = df[
            (df['NAMA'].str.lower() == nama_cari.lower()) & 
            (df['MATA_KULIAH'].str.lower() == matkul_cari.lower())
        ]
        
        if not match.empty:
            return str(match.iloc[0]['STATUS']).strip()
        return "Tidak Ditemukan"
    except Exception as e:
        return f"Error: {e}"

# --- TAMPILAN SIDEBAR ---
st.sidebar.title("🎓 Portal Akademik")
nama_mhs = st.sidebar.text_input("Masukkan Nama Lengkap:")
matkul_pilihan = st.sidebar.selectbox("Pilih Mata Kuliah:", [
    "Pancasila", "Pendidikan Kewarganegaraan", "Communicative Grammar I", 
    "Communicative Grammar II", "Filsafat Moral", "Public Speaking", 
    "Metode Penelitian", "Translation I", "Translation II"
])

st.sidebar.markdown("---")

# --- LOGIKA UTAMA ---
if not nama_mhs:
    st.title("👋 Selamat Datang")
    st.info("Silakan masukkan nama lengkap Anda di menu samping untuk memulai.")
else:
    status = cek_status_mahasiswa(nama_mhs, matkul_pilihan)
    
    # Cek apakah statusnya mengandung kata 'Setuju' (biar lebih fleksibel)
    if "setuju" in str(status).lower():
        st.sidebar.success("✅ Akses Diterima")
        menu = st.sidebar.radio("Navigasi:", ["🏠 Beranda", "🤖 Tanya Asisten AI"])
        
        if menu == "🏠 Beranda":
            st.title(f"Selamat Datang di Kelas {matkul_pilihan}")
            st.subheader(f"Halo, {nama_mhs}!")
            st.write("Anda sudah terdaftar secara resmi di portal ini.")
            
        elif menu == "🤖 Tanya Asisten AI":
            st.title("🤖 Asisten AI")
            tanya = st.text_input(f"Halo {nama_mhs}, ada yang ingin ditanyakan tentang {matkul_pilihan}?")
            if tanya:
                with st.spinner("Berpikir..."):
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    res = model.generate_content(f"Sapa {nama_mhs} dan jawab secara akademik tentang {matkul_pilihan}: {tanya}")
                    st.write(res.text)
                    
    elif "tunggu" in str(status).lower():
        st.title("⏳ Akses Tertunda")
        st.warning(f"Halo {nama_mhs}, pendaftaran Anda masih menunggu persetujuan Bapak Dosen.")
    else:
        st.title("📝 Belum Terdaftar")
        st.error(f"Maaf {nama_mhs}, Anda belum memiliki akses untuk kelas {matkul_pilihan}.")
        st.write("Silakan hubungi Bapak Dosen untuk didaftarkan ke sistem.")
