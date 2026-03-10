import streamlit as st
import google.generativeai as genai

# Pengaturan Halaman
st.set_page_config(page_title="E-Learning Interaktif", layout="wide")

# Sidebar untuk Navigasi
st.sidebar.title("Menu Belajar")
api_key = st.sidebar.text_input("Masukkan Gemini API Key:", type="password")
menu = st.sidebar.radio("Pilih Halaman:", ["🏠 Beranda", "📖 Materi Kuliah", "🤖 Tanya Asisten AI", "📝 Kuis"])

# Inisialisasi AI dengan Penanganan Error
model = None
if api_key:
    try:
        genai.configure(api_key=api_key)
        # Mencoba menggunakan model terbaru yang paling umum
        model = genai.GenerativeModel('gemini-1.5-flash-latest') 
    except Exception as e:
        st.error(f"Gagal memuat AI: {e}")

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
    st.markdown("""
    ### Apa itu Warga Negara?
    Warga negara adalah penduduk sebuah negara berdasarkan keturunan, tempat kelahiran, dan sebagainya yang mempunyai kewajiban dan hak penuh.
    """)

# Halaman AI
elif menu == "🤖 Tanya Asisten AI":
    st.title("🤖 Tanya Asisten AI")
    if not api_key:
        st.warning("Silakan masukkan API Key di menu samping (password) untuk mengaktifkan AI.")
    else:
        pertanyaan = st.text_input("Apa yang ingin Anda tanyakan?")
        if pertanyaan:
            with st.spinner("Sedang berpikir..."):
                try:
                    # Jika model pertama gagal, kita pakai cadangan 'gemini-pro'
                    response = model.generate_content(pertanyaan)
                    st.write("### Jawaban AI:")
                    st.write(response.text)
                except Exception:
                    try:
                        # Cadangan otomatis jika model flash tidak ditemukan
                        model_alt = genai.GenerativeModel('gemini-pro')
                        response = model_alt.generate_content(pertanyaan)
                        st.write("### Jawaban AI (Mode Cadangan):")
                        st.write(response.text)
                    except Exception as e:
                        st.error("Model AI tidak ditemukan. Pastikan API Key Anda benar dan sudah aktif di Google AI Studio.")

# Halaman Kuis
elif menu == "📝 Kuis":
    st.title("📝 Kuis Singkat")
    jawaban = st.radio("Siapa warga negara?", ["Orang asing", "Penduduk asli/terdaftar", "Turis"])
    if st.button("Cek Jawaban"):
        if jawaban == "Penduduk asli/terdaftar":
            st.success("Benar sekali!")
        else:
            st.error("Salah, coba lagi ya.")
