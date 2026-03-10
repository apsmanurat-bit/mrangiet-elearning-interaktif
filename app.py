import streamlit as st
import pandas as pd
import google.generativeai as genai
from datetime import datetime

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="LMS Akademik Pak Guru", layout="wide")

# API KEY AI (Gemini)
API_KEY = "AIzaSyC6cVc6kfcMaPu5H25UmB73RMTlbwt1nR0"
genai.configure(api_key=API_KEY)

# --- ID SHEET (SUDAH DIPERBAIKI - TANPA KOMA/SPASI) ---
ID_SHEET = "10AY2akSXfTdG2hoNpqh65YTCgWZ9ZZIzC82POnVvyf8"
URL_DATA = f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/export?format=csv&gid=0"

# Password Rahasia Dosen
PASSWORD_DOSEN = "ADMIN123"

# --- 2. AMBIL DATA SHEETS ---
def ambil_data_mahasiswa():
    try:
        # Menghindari cache agar data selalu update
        url_refresh = f"{URL_DATA}&refresh={datetime.now().timestamp()}"
        df = pd.read_csv(url_refresh)
        df.columns = df.columns.str.strip().str.upper()
        # Bersihkan data dari spasi di depan/belakang
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].str.strip()
        return df
    except Exception as e:
        return pd.DataFrame(columns=['NAMA', 'MATA_KULIAH', 'STATUS'])

# Simpan Nilai di Memori Sesi
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
    st.info("Mahasiswa: Masukkan Nama Lengkap di samping.")
else:
    # Cari Mahasiswa (Case Insensitive)
    mhs_data = df_db[
        (df_db['NAMA'].str.lower() == nama_input.strip().lower()) & 
        (df_db['MATA_KULIAH'].str.lower() == matkul_pilihan.lower())
    ]

    if mhs_data.empty:
        st.title("📝 Belum Terdaftar")
        st.error(f"Maaf {nama_input}, Anda belum terdaftar di kelas {matkul_pilihan}.")
        st.write("Hubungi Dosen untuk didaftarkan di Google Sheets.")
        
    elif "setuju" not in str(mhs_data.iloc[0]['STATUS']).lower():
        st.title("⏳ Akses Tertunda")
        st.warning(f"Halo {nama_input}, status Anda masih 'Menunggu'.")
        
    else:
        # --- AKSES DITERIMA ---
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
                            model = genai.GenerativeModel('gemini-1.5-flash')
                            prompt = f"Beri nilai angka 0-100 untuk jawaban mahasiswa di matkul {matkul_pilihan}: {jawaban_mhs}. Balas HANYA dengan angka saja."
                            response = model.generate_content(prompt)
                            
                            skor_raw = response.text.strip()
                            # Ambil angka saja, pastikan bukan kode error 403
                            skor = ''.join(filter(str.isdigit, skor_raw))
                            
                            if not skor or int(skor) > 100:
                                skor = "Nilai Manual"

                            st.session_state.rekap_nilai.append({
                                "Nama": nama_input, "Matkul": matkul_pilihan, 
                                "Ujian": jenis_tes, "Nilai": skor, "Waktu": datetime.now().strftime("%H:%M")
                            })
                            st.success(f"Ujian Terkirim! Skor Anda: {skor}")
                        except:
                            st.error("Koneksi AI Sibuk. Nilai akan diinput manual.")

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
                        st.error("AI sedang istirahat.")

# --- 5. PANEL DOSEN ---
if pwd_dosen == PASSWORD_DOSEN:
    st.markdown("---")
    st.header("👨‍🏫 Panel Kontrol Dosen")
    if st.session_state.rekap_nilai:
        df_nilai = pd.DataFrame(st.session_state.rekap_nilai)
        st.table(df_nilai)
        st.download_button("📥 Download Nilai (CSV)", df_nilai.to_csv(index=False), "nilai_mahasiswa.csv")
    else:
        st.write("Belum ada data nilai masuk.")
