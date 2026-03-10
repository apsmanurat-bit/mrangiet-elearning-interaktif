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
ID_SHEET = "10AY2akSXfTdG2hoNpqh65YTCgWZ9ZZIzC82POnVvyf8"
URL_DATA = f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/export?format=csv&gid=0"

# Password Rahasia Dosen
PASSWORD_DOSEN = "ADMIN123"

# --- 2. FUNGSI DINAMIS MENCARI MODEL (ANTI-404) ---
def panggil_ai(perintah):
    try:
        # Cari daftar model yang benar-benar aktif di akun Bapak saat ini
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                model_aktif = m.name
                model = genai.GenerativeModel(model_aktif)
                response = model.generate_content(perintah)
                return response.text
        return "Gagal: Tidak ada model aktif."
    except Exception as e:
        return f"Error Sistem: {str(e)}"

# --- 3. AMBIL DATA SHEETS ---
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

# --- 4. SIDEBAR ---
st.sidebar.title("🎓 Portal Akademik")
nama_input = st.sidebar.text_input("Nama Lengkap Mahasiswa:")
list_matkul = [
    "Pancasila", "Pendidikan Kewarganegaraan", "Communicative Grammar I", 
    "Communicative Grammar II", "Filsafat Moral", "Public Speaking", 
    "Metode Penelitian", "Translation I", "Translation II"
]
matkul_pilihan = st.sidebar.selectbox("Pilih Mata Kuliah:", list_matkul)
pwd_dosen = st.sidebar.text_input("Menu Dosen (Password):", type="password")

# --- 5. LOGIKA UTAMA ---
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
                        prompt = f"Beri nilai angka 0-100 saja untuk jawaban mahasiswa di matkul {matkul_pilihan}: {jawaban_mhs}. HANYA ANGKA SAJA."
                        hasil_ai = panggil_ai(prompt)
                        
                        # Ambil angka saja dari jawaban AI
                        skor = ''.join(filter(str.isdigit, hasil_ai))
                        
                        if skor:
                            st.session_state.rekap_nilai.append({
                                "Nama": nama_input, "Matkul": matkul_pilihan, 
                                "Ujian": jenis_tes, "Nilai": skor, "Waktu": datetime.now().strftime("%H:%M")
                            })
                            st.success(f"Ujian Terkirim! Skor Anda: {skor}")
                        else:
                            st.error(f"Koreksi Gagal: {hasil_ai}")

        elif nav == "🤖 Tanya AI":
            st.title("🤖 Asisten AI")
            tanya = st.text_input("Ketik pertanyaan Anda:")
            if tanya:
                with st.spinner("Berpikir..."):
                    jawaban = panggil_ai(tanya)
                    st.write(jawaban)

# --- PANEL DOSEN ---
if pwd_dosen == PASSWORD_DOSEN:
    st.markdown("---")
    st.header("👨‍🏫 Rekap Nilai Dosen")
    if st.session_state.rekap_nilai:
        df_nilai = pd.DataFrame(st.session_state.rekap_nilai)
        st.table(df_nilai)
        st.download_button("📥 Download Nilai (CSV)", df_nilai.to_csv(index=False), "nilai.csv")
    else:
        st.write("Belum ada data nilai masuk.")
