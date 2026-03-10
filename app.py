import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="E-Learning Interaktif", layout="wide")

# API KEY (Langsung pakai milik Anda)
API_KEY = "AIzaSyC6cVc6kfcMaPu5H25UmB73RMTlbwt1nR0"
genai.configure(api_key=API_KEY)

# Sidebar
st.sidebar.title("📚 Menu Belajar")
menu = st.sidebar.radio("Pilih Halaman:", ["🏠 Beranda", "📖 Materi Kuliah", "🤖 Tanya Asisten AI", "📝 Kuis"])

# --- HALAMAN BERANDA ---
if menu == "🏠 Beranda":
    st.title("🌟 Selamat Datang di Platform E-Learning")
    nama = st.text_input("Masukkan Nama Anda:")
    if nama:
        st.success(f"Selamat belajar, {nama}!")

# --- HALAMAN MATERI ---
elif menu == "📖 Materi Kuliah":
    st.title("📖 Materi: Pendidikan Kewarganegaraan")
    st.write("Identitas nasional adalah jati diri bangsa.")

# --- HALAMAN ASISTEN AI ---
elif menu == "🤖 Tanya Asisten AI":
    st.title("🤖 Asisten AI Pintar")
    pertanyaan = st.text_input("Ketik pertanyaan Anda di sini:")
    
    if pertanyaan:
        with st.spinner("Sedang mencari jawaban..."):
            # STRATEGI 3 TAHAP: Mencoba model satu per satu sampai berhasil
            success = False
            # Daftar model yang akan dicoba (dari yang tercanggih ke yang paling stabil)
            model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
            
            for name in model_names:
                if not success:
                    try:
                        model = genai.GenerativeModel(name)
                        response = model.generate_content(pertanyaan)
                        st.markdown(f"### Jawaban (Model: {name}):")
                        st.write(response.text)
                        success = True
                    except Exception:
                        continue # Jika gagal, coba model berikutnya
            
            if not success:
                st.error("Semua model AI sedang sibuk atau API Key belum aktif. Mohon tunggu 5-10 menit lalu coba lagi, atau pastikan 'Generative AI' sudah diaktifkan di Google AI Studio Anda.")

# --- HALAMAN KUIS ---
elif menu == "📝 Kuis":
    st.title("📝 Kuis")
    jawaban = st.radio("Semboyan Indonesia?", ["Bhinneka Tunggal Ika", "Merdeka"])
    if st.button("Cek"):
        if jawaban == "Bhinneka Tunggal Ika":
            st.success("Benar!")
