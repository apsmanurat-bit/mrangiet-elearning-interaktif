import streamlit as st
import google.generativeai as genai

# Konfigurasi API Gemini (Ganti dengan API Key Anda nanti atau gunakan Secrets)
# Untuk keamanan, kita akan meminta input API Key di aplikasi atau lewat Secrets
api_key = st.sidebar.text_input("Masukkan Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
# Pengaturan Halaman
st.set_page_config(page_title="E-Learning Interaktif", layout="wide")

# Sidebar untuk Navigasi
st.sidebar.title("Menu Belajar")
menu = st.sidebar.radio("Pilih Halaman:", ["🏠 Beranda", "📖 Materi Kuliah", "🤖 Tanya Asisten AI", "📝 Kuis"])

# Halaman Beranda
if menu == "🏠 Beranda":
    st.title("Selamat Datang di Platform E-Learning")
    st.write("Halo! Silakan pilih materi di menu samping untuk mulai belajar.")
    nama = st.text_input("Masukkan Nama Anda:")
    if nama:
        st.success(f"Selamat belajar, {nama}! Mari buat hari ini produktif.")

# Halaman Materi
elif menu == "📖 Materi Kuliah":
    st.title("📖 Materi Kuliah: Dasar Kewarganegaraan")
    st.write("Silakan baca materi di bawah ini:")
    st.markdown("""
    ### Apa itu Warga Negara?
    Warga negara adalah penduduk sebuah negara atau bangsa berdasarkan keturunan, tempat kelahiran, dan sebagainya yang mempunyai kewajiban dan hak penuh sebagai seorang warga dari negara itu.
    """)

# Halaman AI
elif menu == "🤖 Tanya Asisten AI":
    st.title("🤖 Tanya Asisten AI")
    if not api_key:
        st.warning("Silakan masukkan API Key di menu samping untuk mengaktifkan AI.")
    else:
        pertanyaan = st.text_input("Apa yang ingin Anda tanyakan tentang materi hari ini?")
        if pertanyaan:
            with st.spinner("Sedang berpikir..."):
                response = model.generate_content(pertanyaan)
                st.write("### Jawaban AI:")
                st.write(response.text)

# Halaman Kuis
elif menu == "📝 Kuis":
    st.title("📝 Kuis Singkat")
    st.write("Siapa yang disebut sebagai warga negara?")
    jawaban = st.radio("Pilih jawaban:", ["Orang asing", "Penduduk asli/terdaftar", "Turis"])
    if st.button("Cek Jawaban"):
        if jawaban == "Penduduk asli/terdaftar":
            st.success("Benar sekali!")
        else:
            st.error("Salah, coba lagi ya.")
