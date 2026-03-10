import streamlit as st
import pandas as pd
import google.generativeai as genai
from datetime import datetime

# --- 1. KONFIGURASI HALAMAN & API ---
st.set_page_config(page_title="LMS Interaktif Pak Guru", layout="wide")

# API KEY AI (Gemini)
API_KEY = "AIzaSyC6cVc6kfcMaPu5H25UmB73RMTlbwt1nR0"
genai.configure(api_key=API_KEY)

# ID Google Sheets Bapak (Diambil dari link yang Bapak berikan)
ID_SHEET = "10AY2akSXfTdG2hoNpqh65YTCgWZ9ZZIzC82POnVvyf8"
# URL untuk menarik data sebagai CSV (Anti-Error 401)
URL_DATA = f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/export?format=csv&gid=0"

# Password Rahasia Dosen
PASSWORD_DOSEN = "ADMIN123"

# --- 2. FUNGSI AMBIL DATA SHEETS ---
def ambil_data_mahasiswa():
    try:
        # Tambahkan timestamp agar data selalu yang paling baru dari Sheets
        url_refresh = f"{URL_DATA}&refresh={datetime.now().timestamp()}"
        df = pd.read_csv(url_refresh)
        # Bersihkan header kolom
        df.columns = df.columns.str.strip().str.upper()
        # Bersihkan data dari spasi tambahan
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        return df
    except Exception as e:
        st.error(f"⚠️ Gagal terhubung ke Google Sheets: {e}")
        return pd.DataFrame(columns=['NAMA', 'MATA_KULIAH', 'STATUS'])

# Inisialisasi Database Nilai di Memori (Bisa di-download Dosen)
if 'rekap_nilai' not in st.session_state:
    st.session_state.rekap_nilai = []

# --- 3. SIDEBAR (LOGIN & MATKUL) ---
st.sidebar.title("🎓 Portal Akademik")
nama_input = st.sidebar.text_input("Nama Lengkap Mahasiswa:")
list_matkul = [
    "Pancasila", "Pendidikan Kewarganegaraan", "Communicative Grammar I", 
    "Communicative Grammar II", "Filsafat Moral", "Public Speaking", 
    "Metode Penelitian", "Translation I", "Translation II"
]
matkul_pilihan = st.sidebar.selectbox("Pilih Mata Kuliah:", list_matkul)

st.sidebar.markdown("---")
pwd_dosen = st.sidebar.text_input("Menu Dosen (Password):", type="password")

# --- 4. LOGIKA UTAMA ---
df_db = ambil_data_mahasiswa()

if not nama_input:
    st.title("👋 Selamat Datang di Portal E-Learning")
    st.info("Silakan mahasiswa masukkan Nama Lengkap di menu samping.")
    st.image("https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&q=80&w=1000", use_column_width=True)
else:
    # Cari Mahasiswa di Database Sheets
    mhs_data = df_db[
        (df_db['NAMA'].str.lower() == nama_input.strip().lower()) & 
        (df_db['MATA_KULIAH'].str.lower() == matkul_pilihan.lower())
    ]

    if mhs_data.empty:
        st.title("📝 Belum Terdaftar")
        st.error(f"Maaf {nama_input}, Anda belum memiliki akses untuk kelas {matkul_pilihan}.")
        st.write("Silakan hubungi Bapak Dosen untuk didaftarkan ke Google Sheets.")
    
    elif "setuju" not in str(mhs_data.iloc[0]['STATUS']).lower():
        st.title("⏳ Akses Tertunda")
        st.warning(f"Halo {nama_input}, status Anda di Google Sheets masih 'Menunggu'.")
        
    else:
        # --- AKSES DITERIMA ---
        st.sidebar.success(f"✅ Akses: {nama_input.upper()}")
        
        # Pilihan Menu (Tanya AI disembunyikan jika masuk menu Ujian)
        nav = st.sidebar.radio("Navigasi:", ["🏠 Beranda", "📖 Baca Materi", "📝 Menu Ujian", "🤖 Tanya Asisten AI"])
        
        # --- A. MENU BERANDA ---
        if nav == "🏠 Beranda":
            st.title(f"Selamat Datang, {nama_input}!")
            st.subheader(f"Anda terdaftar di kelas: {matkul_pilihan}")
            st.write("Gunakan menu di samping untuk membaca materi atau mengerjakan ujian.")

        # --- B. MENU MATERI ---
        elif nav == "📖 Baca Materi":
            st.title(f"📚 Materi: {matkul_pilihan}")
            st.info(f"Modul belajar untuk {matkul_pilihan} akan segera tersedia di sini.")
            st.write("---")
            st.write("*(Bapak bisa mengedit bagian ini untuk menaruh link PDF)*")

        # --- C. MENU UJIAN (PROTEKSI AI) ---
        elif nav == "📝 Menu Ujian":
            st.title("✍️ Pusat Ujian")
            st.warning("⚠️ Fitur 'Tanya Asisten AI' dinonaktifkan di halaman ini.")
            
            jenis_tes = st.selectbox("Pilih Sesi Ujian:", [
                "--- Pilih Sesi ---", "QUIZ 1", "QUIZ 2", "QUIZ 3", "QUIZ 4", 
                "MID TEST", "FINAL TEST", "FINAL PROJECT"
            ])
            
            if jenis_tes != "--- Pilih Sesi ---":
                st.subheader(f"Mengerjakan: {jenis_tes}")
                st.write(f"Silakan jawab pertanyaan untuk {matkul_pilihan} di bawah ini.")
                jawaban_mhs = st.text_area("Lembar Jawaban:", height=250)
                
                if st.button("Kirim & Nilai Otomatis"):
                    with st.spinner("AI sedang mengoreksi jawaban Anda..."):
                        # Koreksi Otomatis Angka Saja 0-100
                        model_ai = genai.GenerativeModel('gemini-1.5-flash')
                        prompt = f"Berikan nilai angka saja (0-100) untuk jawaban mahasiswa ini di matkul {matkul_pilihan}: {jawaban_mhs}. JANGAN BERI TEKS APAPUN, HANYA ANGKA."
                        response = model_ai.generate_content(prompt)
                        skor = response.text.strip()
                        
                        # Simpan ke Rekap Dosen
                        st.session_state.rekap_nilai.append({
                            "Nama": nama_input,
                            "Matkul": matkul_pilihan,
                            "Ujian": jenis_tes,
                            "Nilai": skor,
                            "Waktu": datetime.now().strftime("%H:%M:%S")
                        })
                        st.success(f"Ujian Selesai! Skor Anda: **{skor}**")

        # --- D. MENU TANYA AI ---
        elif nav == "🤖 Tanya Asisten AI":
            st.title("🤖 Asisten AI Akademik")
            st.write("Fitur ini tersedia selama Anda tidak berada di halaman Ujian.")
            tanya = st.text_input(f"Halo {nama_input}, ada yang ingin ditanyakan seputar {matkul_pilihan}?")
            if tanya:
                with st.spinner("Berpikir..."):
                    model_ai = genai.GenerativeModel('gemini-1.5-flash')
                    res = model_ai.generate_content(f"Jawab pertanyaan mahasiswa {nama_input} tentang {matkul_pilihan}: {tanya}")
                    st.write(res.text)

# --- 5. PANEL REKAP NILAI (UNTUK DOSEN) ---
if pwd_dosen == PASSWORD_DOSEN:
    st.markdown("---")
    st.header("👨‍🏫 Panel Kontrol Dosen")
    st.subheader("📊 Rekap Nilai Ujian (Real-time)")
    
    if st.session_state.rekap_nilai:
        df_nilai = pd.DataFrame(st.session_state.rekap_nilai)
        st.table(df_nilai)
        
        # Tombol Download agar Nilai Tidak Hilang
        st.download_button(
            label="📥 Download Nilai ke Excel (CSV)",
            data=df_nilai.to_csv(index=False),
            file_name=f"Nilai_{matkul_pilihan}_{datetime.now().strftime('%d%m%Y')}.csv",
            mime="text/csv"
        )
