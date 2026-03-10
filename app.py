import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="E-Learning Interaktif", layout="wide")

# KONFIGURASI API KEY (Sudah Tertanam)
API_KEY = "AIzaSyC6cVc6kfcMaPu5H25UmB73RMTlbwt1nR0"
genai.configure(api_key=API_KEY)

# Inisialisasi Model AI (Menggunakan versi paling stabil)
model = genai.GenerativeModel('gemini-1.5-flash')

# Sidebar untuk Navigasi
st.sidebar.title("📚 Menu Belajar")
st.sidebar.info("Aplikasi ini terhubung dengan Gemini AI")
menu = st.sidebar.radio("Pilih Halaman:", ["🏠 Beranda", "📖 Materi Kuliah", "🤖 Tanya Asisten AI", "📝 Kuis"])

# --- HALAMAN BERANDA ---
if menu == "🏠 Beranda":
    st.title("🌟 Selamat Datang di Platform E-Learning")
    st.write("Halo! Selamat datang di ruang belajar digital. Silakan gunakan menu di samping untuk memulai.")
    nama = st.text_input("Masukkan Nama Anda:")
    if nama:
        st.success(f"Selamat belajar, {nama}! Semoga sukses dengan studinya hari ini.")

# --- HALAMAN MATERI ---
elif menu == "📖 Materi Kuliah":
    st.title("📖 Materi: Pendidikan Kewarganegaraan")
    st.markdown("""
    ### Topik: Identitas Nasional
    Identitas nasional adalah jati diri yang tata nilai, budaya, dan wataknya menjadi ciri khas suatu bangsa. 
    Contoh identitas nasional Indonesia:
    1. **Bahasa Nasional:** Bahasa Indonesia.
    2. **Bendera Negara:** Sang Merah Putih.
    3. **Lagu Kebangsaan:** Indonesia Raya.
    4. **Semboyan Negara:** Bhinneka Tunggal Ika.
    """)

# --- HALAMAN ASISTEN AI ---
elif menu == "🤖 Tanya Asisten AI":
    st.title("🤖 Asisten AI Pintar")
    st.write("Silakan tanyakan apa saja terkait materi kuliah Anda.")
    
    pertanyaan = st.text_input("Ketik pertanyaan Anda di sini:")
    
    if pertanyaan:
        with st.spinner("Asisten sedang mencari jawaban terbaik..."):
            try:
                # Proses tanya jawab AI
                response = model.generate_content(pertanyaan)
                st.markdown("### Jawaban:")
                st.write(response.text)
            except Exception as e:
                st.error("Waduh, ada kendala koneksi ke otak AI. Coba ulangi sebentar lagi ya.")

# --- HALAMAN KUIS ---
elif menu == "📝 Kuis":
    st.title("📝 Kuis Pemahaman")
    st.write("Uji pemahaman Anda dengan soal di bawah ini:")
    
    soal = "Apa semboyan negara Indonesia?"
    pilihan = ["Bhinneka Tunggal Ika", "Tut Wuri Handayani", "Merdeka atau Mati"]
    
    jawaban = st.radio(soal, pilihan)
    
    if st.button("Kirim Jawaban"):
        if jawaban == "Bhinneka Tunggal Ika":
            st.success("Tepat sekali! Anda luar biasa.")
            st.balloons()
        else:
            st.error("Masih kurang tepat, silakan baca lagi menu Materi.")
