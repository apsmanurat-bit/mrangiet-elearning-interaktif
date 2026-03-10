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

def ambil_data_sheets():
    try:
        import time
        # Memaksa data segar agar perubahan di Sheets cepat terbaca
        url_refresh = f"{SHEET_URL}&cache={int(time.time())}"
        df = pd.read_csv(url_refresh)
        # Bersihkan header kolom
        df.columns = df.columns.str.strip().str.upper()
        # Bersihkan data dari spasi tambahan
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        return df
    except Exception as e:
        st.error(f"Koneksi ke Google Sheets Gagal: {e}")
        return pd.DataFrame()

# --- TAMPILAN SIDEBAR ---
st.sidebar.title("🎓 Portal Akademik")
nama_mhs = st.sidebar.text_input("Masukkan Nama Lengkap:")
list_matkul = [
    "Pancasila", "Pendidikan Kewarganegaraan", "Communicative Grammar I", 
    "Communicative Grammar II", "Filsafat Moral", "Public Speaking", 
    "Metode Penelitian", "Translation I", "Translation II"
]
matkul_pilihan = st.sidebar.selectbox("Pilih Mata Kuliah:", list_matkul)

st.sidebar.markdown("---")

# --- PROSES CEK AKSES ---
df_database = ambil_data_sheets()

if not nama_mhs:
    st.title("👋 Selamat Datang")
    st.info("Silakan masukkan nama lengkap Anda di menu samping untuk memulai.")
else:
    # Cari data di tabel
    match = df_database[
        (df_database['NAMA'].str.lower() == nama_mhs.lower()) & 
        (df_database['MATA_KULIAH'].str.lower() == matkul_pilihan.lower())
    ]
    
    status = "Tidak Ditemukan"
    if not match.empty:
        status = str(match.iloc[0]['STATUS']).strip().lower()

    # Logika Tampilan Berdasarkan Status
    if "setuju" in status:
        st.sidebar.success("✅ Akses Diterima")
        menu = st.sidebar.radio("Navigasi:", ["🏠 Beranda", "🤖 Tanya Asisten AI"])
        
        if menu == "🏠 Beranda":
            st.title(f"Selamat Datang di Kelas {matkul_pilihan}")
            st.subheader(f"Halo, {nama_mhs}!")
            st.success("Anda sudah terdaftar secara resmi.")
            
        elif menu == "🤖 Tanya Asisten AI":
            st.title("🤖 Asisten AI")
            tanya = st.text_input(f"Halo {nama_mhs}, ada yang ingin ditanyakan tentang {matkul_pilihan}?")
            if tanya:
                with st.spinner("Berpikir..."):
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    res = model.generate_content(f"Sapa {nama_mhs} dan jawab secara akademik tentang {matkul_pilihan}: {tanya}")
                    st.write(res.text)
                    
    elif "tunggu" in status:
        st.title("⏳ Akses Tertunda")
        st.warning(f"Halo {nama_mhs}, pendaftaran Anda masih menunggu persetujuan Bapak Dosen.")
    else:
        st.title("📝 Belum Terdaftar")
        st.error(f"Maaf {nama_mhs}, Anda belum memiliki akses untuk kelas {matkul_pilihan}.")
        st.write("Pastikan penulisan Nama dan Mata Kuliah di Google Sheets sudah sesuai.")

# --- BAGIAN MONITOR UNTUK DOSEN (Hanya Muncul di Bawah) ---
st.markdown("---")
with st.expander("🔍 Papan Monitor Dosen (Cek Data Sheets di Sini)"):
    st.write("Berikut adalah data yang terbaca dari Google Sheets Bapak saat ini:")
    st.dataframe(df_database)
    st.info("Tips: Pastikan kolom NAMA, MATA_KULIAH, dan STATUS tertulis dengan benar di baris pertama Sheets.")
