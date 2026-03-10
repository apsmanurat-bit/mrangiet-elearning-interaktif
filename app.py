import streamlit as st
import pandas as pd
import google.generativeai as genai
from datetime import datetime

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="LMS Akademik Pak Guru", layout="wide")

# API KEY AI (Gemini)
API_KEY = "AIzaSyC6cVc6kfcMaPu5H25UmB73RMTlbwt1nR0"
genai.configure(api_key=API_KEY)

# ID Google Sheets Bapak
ID_SHEET = "10AY2akSXfTdG2hoNpqh65, YTCgWZ9ZZIzC82POnVvyf8"
URL_DATA = f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/export?format=csv&gid=0"

# Password Rahasia Dosen
PASSWORD_DOSEN = "ADMIN123"

# --- 2. AMBIL DATA SHEETS ---
def ambil_data_mahasiswa():
    try:
        url_refresh = f"{URL_DATA}&refresh={datetime.now().timestamp()}"
        df = pd.read_csv(url_refresh)
        df.columns = df.columns.str.strip().str.upper()
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        return df
    except:
        return pd.DataFrame(columns=['NAMA', 'MATA_KULIAH', 'STATUS'])

if 'rekap_nilai' not in st.session_state:
    st.session_state.rekap_nilai = []

# --- 3. SIDEBAR ---
st.sidebar.title("🎓 Portal Akademik")
nama_input = st.sidebar.text_input("Nama Lengkap Mahasiswa:")
list_matkul = [
    "Pancasila", "Pendidikan Kewarganegaraan", "Communicative Grammar I", 
    "Communicative Grammar II", "Filsafat Moral", "Public Speaking", 
    "Metode Penelitian", "Translation I", "Translation II"
]
matkul_pilihan = st.sidebar.selectbox("Pilih Mata Kuliah:", list_matkul)
pwd_dosen = st.sidebar.text_input("Menu Dosen (Password):", type="password")

# --- 4. LOGIKA UTAMA ---
df_db = ambil_data_mahasiswa()

if not nama_input:
    st.title("👋 Selamat Datang")
    st.info("Silakan masukkan Nama Lengkap Anda di menu samping.")
else:
    mhs_data = df_db[
        (df_db['NAMA'].str.lower() == nama_input.strip().lower()) & 
        (df_db['MATA_KULIAH'].str.lower() == matkul_pilihan.lower())
    ]

    if mhs_data.empty:
        st.title("📝 Belum Terdaftar")
        st.error(f"Maaf {nama_input}, Anda belum terdaftar di kelas {matkul_pilihan}.")
    elif "setuju" not in str(mhs_data.iloc[0]['STATUS']).lower():
        st.title("⏳ Akses Tertunda")
        st.warning(f"Halo {nama_input}, status Anda masih 'Menunggu' di Google Sheets.")
    else:
        st.sidebar.success(f"✅ AKTIF: {nama_input.upper()}")
        nav = st.sidebar.radio("Navigasi:", ["🏠 Beranda", "📖 Materi", "📝 Ujian", "🤖 Tanya AI"])
        
        if nav == "🏠 Beranda":
            st.title(f"Selamat Datang, {nama_input}!")
            st.write(f"Anda masuk di kelas: **{matkul_pilihan}**")

        elif nav == "📝 Ujian":
            st.title("✍️ Sesi Ujian")
            st.warning("⚠️ Fitur Tanya AI dimatikan selama ujian.")
            jenis_tes = st.selectbox("Pilih Jenis Ujian:", ["--- Pilih ---", "QUIZ 1", "QUIZ 2", "MID TEST", "FINAL TEST"])
            
            if jenis_tes != "--- Pilih ---":
                jawaban_mhs = st.text_area("Tulis Jawaban Anda:", height=200)
                if st.button("Kirim Jawaban"):
                    with st.spinner("Sistem sedang mengoreksi otomatis..."):
                        try:
                            # MENGGUNAKAN NAMA MODEL YANG PALING UMUM (GEMINI-1.5-FLASH)
                            model = genai.GenerativeModel('gemini-1.5-flash')
                            prompt = f"Berikan skor angka antara 0 sampai 100 berdasarkan kualitas jawaban mahasiswa berikut untuk mata kuliah {matkul_pilihan}: '{jawaban_mhs}'. Balas HANYA dengan angka saja."
                            
                            response = model.generate_content(prompt)
                            # Membersihkan hasil agar hanya angka yang tersisa
                            skor_raw = response.text.strip()
                            skor = ''.join(filter(str.isdigit, skor_raw))
                            
                            # Validasi: Jika skor yang keluar aneh (seperti 403 atau kosong)
                            if not skor or int(skor) > 100:
                                skor = "Cek Manual"

                            st.session_state.rekap_nilai.append({
                                "Nama": nama_input, "Matkul": matkul_pilihan, 
                                "Ujian": jenis_tes, "Nilai": skor, "Waktu": datetime.now().strftime("%H:%M")
                            })
                            st.success(f"Ujian Terkirim! Skor Anda: {skor}")
                        except Exception as e:
                            st.error(f"Koneksi AI Terputus. Nilai akan diinput manual oleh Bapak Dosen.")

        elif nav == "🤖 Tanya AI":
            st.title("🤖 Asisten AI")
            tanya = st.text_input("Ketik pertanyaan Anda:")
            if tanya:
                with st.spinner("Berpikir..."):
                    try:
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        res = model.generate_content(tanya)
                        st.write(res.text)
                    except:
                        st.error("Layanan AI sedang sibuk.")

# --- 5. PANEL DOSEN ---
if pwd_dosen == PASSWORD_DOSEN:
    st.markdown("---")
    st.header("👨‍🏫 Rekap Nilai Dosen")
    if st.session_state.rekap_nilai:
        df_nilai = pd.DataFrame(st.session_state.rekap_nilai)
        st.table(df_nilai)
        st.download_button("📥 Download Nilai (CSV)", df_nilai.to_csv(index=False), "nilai.csv")
    else:
        st.write("Belum ada data nilai masuk.")
