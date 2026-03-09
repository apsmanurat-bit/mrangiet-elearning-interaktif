import streamlit as st

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
    st.title("Materi Kuliah")
    st.info("Bagian ini akan berisi daftar modul yang bisa Anda pelajari.")
    # Nanti kita isi dengan teks atau link video di langkah berikutnya

# Halaman AI
elif menu == "🤖 Tanya Asisten AI":
    st.title("Tanya Asisten AI")
    st.write("Ada yang kurang jelas dari materi? Tanyakan langsung di sini.")
    # Nanti kita hubungkan dengan API Gemini di langkah berikutnya

# Halaman Kuis
elif menu == "📝 Kuis":
    st.title("Kuis Interaktif")
    st.write("Uji pemahamanmu di sini.")
