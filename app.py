import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Portal E-Learning Interaktif", layout="wide")

# API KEY AI
API_KEY = "AIzaSyC6cVc6kfcMaPu5H25UmB73RMTlbwt1nR0"
genai.configure(api_key=API_KEY)

# Password Rahasia Bapak (Silakan ganti sesuai keinginan)
PASSWORD_DOSEN = "ADMIN123" 

# Inisialisasi Database Internal (Disimpan di memori aplikasi)
if 'db_mahasiswa' not in st.session_state:
    st.session_state.db_mahasiswa = {} 

# --- DATA MATERI KULIAH ---
# Bapak bisa mengedit isi teks materi di bawah ini nanti
MATERI_KULIAH = {
    "Pancasila": "📖 **Modul Pancasila:** Fokus pada sejarah kelahiran Pancasila dan fungsinya sebagai dasar negara.",
    "Pendidikan Kewarganegaraan": "📖 **Modul PKn:** Membahas tentang identitas nasional dan hak-kewajiban warga negara.",
    "Communicative Grammar I": "📖 **Modul Grammar I:** Penguatan Tenses (Present, Past, Future) dalam percakapan sehari-hari.",
    "Communicative Grammar II": "📖 **Modul Grammar II:** Fokus pada Clause, Passive Voice, dan Conditional Sentences.",
    "Filsafat Moral": "📖 **Modul Filsafat Moral:** Meninjau etika Deontologi, Utilitarianisme, dan Kebajikan.",
    "Public Speaking": "📖 **Modul Public Speaking:** Teknik mengatasi demam panggung dan struktur pidato yang efektif.",
    "Metode Penelitian": "📖 **Modul Metopel:** Langkah-langkah menyusun proposal penelitian dan teknik pengumpulan data.",
    "Translation I": "📖 **Modul Translation I:** Teknik dasar penerjemahan teks umum dari Bahasa Inggris ke Indonesia.",
    "Translation II": "📖 **Modul Translation II:** Penerjemahan teks akademik dan teknik 'equivalence' dalam penerjemahan."
}

# --- SIDEBAR ---
st.sidebar.title("🔐 Akses Portal")
nama_mhs = st.sidebar.text_input("Nama Lengkap Anda:")
matkul_pilihan = st.sidebar.selectbox("Pilih Mata Kuliah:", list(MATERI_KULIAH.keys()))

st.sidebar.markdown("---")
st.sidebar.subheader("👨‍🏫 Otoritas Dosen")
pwd = st.sidebar.text_input("Password Rahasia:", type="password")

key_mhs = f"{nama_mhs.lower()}-{matkul_pilihan}"

# --- LOGIKA UTAMA ---
if not nama_mhs:
    st.title("👋 Selamat Datang di Portal E-Learning")
    st.info("Mahasiswa: Silakan isi Nama dan pilih Mata Kuliah di menu samping.")
    st.image("https://images.unsplash.com/photo-1501504905252-473c47e087f8?auto=format&fit=crop&q=80&w=1000", use_column_width=True)
else:
    # 1. CEK APAKAH SUDAH TERDAFTAR
    if key_mhs not in st.session_state.db_mahasiswa:
        st.title("📝 Form Pendaftaran")
        st.warning(f"Halo {nama_mhs}, Anda belum terdaftar untuk kelas **{matkul_pilihan}**.")
        if st.button("Daftar ke Kelas Ini"):
            st.session_state.db_mahasiswa[key_mhs] = "Menunggu"
            st.success("Pendaftaran Terkirim! Mohon tunggu persetujuan Bapak Dosen.")
            st.rerun()

    else:
        status = st.session_state.db_mahasiswa[key_mhs]
        
        # 2. JIKA SUDAH DISETUJUI
        if status == "Disetujui":
            st.sidebar.success("✅ Akses Diterima")
            menu = st.sidebar.radio("Navigasi:", ["📖 Baca Materi", "🤖 Tanya Asisten AI"])
            
            if menu == "📖 Baca Materi":
                st.title(f"📚 Materi: {matkul_pilihan}")
                st.markdown(f"### Selamat Belajar, {nama_mhs}!")
                st.info(MATERI_KULIAH[matkul_pilihan])
                st.write("---")
                st.write("*(Bapak bisa menambahkan link PDF atau video di sini nantinya)*")
                
            elif menu == "🤖 Tanya Asisten AI":
                st.title("🤖 Asisten AI Akademik")
                tanya = st.text_input(f"Ada yang sulit dari materi {matkul_pilihan}?")
                if tanya:
                    with st.spinner("Sedang mencari jawaban..."):
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        res = model.generate_content(f"Jawab secara mendalam untuk mahasiswa bernama {nama_mhs} tentang topik {matkul_pilihan}: {tanya}")
                        st.write(res.text)
        
        # 3. JIKA MASIH MENUNGGU
        else:
            st.title("⏳ Menunggu Otoritas")
            st.warning(f"Halo {nama_mhs}, pendaftaran Anda sedang diproses oleh Bapak Dosen.")
            st.write("Silakan hubungi Bapak agar akses segera dibuka.")

# --- RUANG KENDALI DOSEN (Muncul jika password benar) ---
if pwd == PASSWORD_DOSEN:
    st.markdown("---")
    st.header("👨‍🏫 Panel Otoritas Dosen")
    
    if not st.session_state.db_mahasiswa:
        st.write("Belum ada antrean pendaftaran.")
    else:
        st.write("Daftar Mahasiswa yang Menunggu Izin:")
        for mhs, stat in st.session_state.db_mahasiswa.items():
            if stat == "Menunggu":
                col1, col2, col3 = st.columns([3, 2, 2])
                nama_display = mhs.split('-')[0].upper()
                matkul_display = mhs.split('-')[1]
                
                col1.write(f"👤 **{nama_display}**")
                col2.write(f"📘 {matkul_display}")
                if col3.button("SETUJUI", key=mhs):
                    st.session_state.db_mahasiswa[mhs] = "Disetujui"
                    st.rerun()

        st.markdown("---")
        st.write("Mahasiswa Terdaftar:")
        for mhs, stat in st.session_state.db_mahasiswa.items():
            if stat == "Disetujui":
                st.write(f"✅ {mhs.split('-')[0].upper()} ({mhs.split('-')[1]})")
