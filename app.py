import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="Portal Akademik Bapak", layout="wide")

# --- ID SPREADSHEET BAPAK YANG SUDAH SAYA CEK ---
ID_SHEET = "10AY2akSXfTdG2hoNpqh65YTCgWZ9ZZIzC82POnVvyf8" 
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/pub?output=csv"

# API KEY AI
API_KEY = "AIzaSyC6cVc6kfcMaPu5H25UmB73RMTlbwt1nR0"
genai.configure(api_key=API_KEY)

def cek_status_mahasiswa(nama_cari, matkul_cari):
    try:
        import time
        # Memaksa data segar setiap 10 detik agar persetujuan Bapak langsung terbaca
        url = f"{SHEET_URL}&refresh={int(time.time() / 10)}"
        df = pd.read_csv(url)
        
        # Membersihkan teks agar tidak error karena spasi
        df.columns = df.columns.str.strip()
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        # Pencarian (tidak peka huruf besar/kecil)
        hasil = df[(df['NAMA'].str.lower() == nama_cari.lower()) & 
                   (df['MATA_KULIAH'] == matkul_cari)]
        
        if not hasil.empty:
            return hasil.iloc[0]['STATUS']
        return "Tidak Ditemukan"
    except Exception:
        return "Error: Pastikan File Sudah Di-Publikasikan ke Web"

# --- Tampilan Utama ---
st.sidebar.title("🎓 Portal Akademik")
nama_mhs = st.sidebar.text_input("Masukkan Nama Lengkap:")
matkul_pilihan = st.sidebar.selectbox("Pilih Mata Kuliah:", [
    "Pancasila", "Pendidikan Kewarganegaraan", "Communicative Grammar I", 
    "Communicative Grammar II", "Filsafat Moral", "Public Speaking", 
    "Metode Penelitian", "Translation I", "Translation II"
])

if not nama_mhs:
    st.title("👋 Selamat Datang")
    st.info("Silakan masukkan nama lengkap Anda di samping untuk masuk.")
else:
    status = cek_status_mahasiswa(nama_mhs, matkul_pilihan)
    
    if status == "Disetujui":
        st.sidebar.success("✅ Akses Diterima")
        menu = st.sidebar.radio("Navigasi:", ["🏠 Beranda", "🤖 Tanya Asisten AI"])
        
        if menu == "🏠 Beranda":
            st.title(f"Selamat Datang di Kelas {matkul_pilihan}")
            st.write(f"Halo **{nama_mhs}**, senang melihat Anda kembali!")
        elif menu == "🤖 Tanya Asisten AI":
            st.title("🤖 Asisten AI")
            pertanyaan = st.text_input(f"Halo {nama_mhs}, ada yang ingin ditanyakan?")
            if pertanyaan:
                model = genai.GenerativeModel('gemini-1.5-flash')
                res = model.generate_content(f"Sapa {nama_mhs} dan jawab pertanyaan ini: {pertanyaan}")
                st.write(res.text)
                
    elif status == "Menunggu":
        st.title("⏳ Akses Tertunda")
        st.warning(f"Halo {nama_mhs}, pendaftaran Anda sedang menunggu persetujuan Dosen.")
    else:
        st.title("📝 Belum Terdaftar")
        st.error(f"Maaf {nama_mhs}, Anda belum memiliki akses untuk kelas {matkul_pilihan}.")
        st.write("Silakan hubungi Bapak Dosen untuk didaftarkan.")
