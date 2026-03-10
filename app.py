import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="Portal E-Learning Bapak", layout="wide")

# API KEY ANDA
API_KEY = "AIzaSyC6cVc6kfcMaPu5H25UmB73RMTlbwt1nR0"
genai.configure(api_key=API_KEY)

# --- SIDEBAR (MENU SAMPING) ---
st.sidebar.title("🎓 Portal Akademik")

# 1. Pilih Mata Kuliah
list_matkul = [
    "Pancasila", 
    "Pendidikan Kewarganegaraan", 
    "Communicative Grammar I", 
    "Communicative Grammar II", 
    "Filsafat Moral", 
    "Public Speaking", 
    "Metode Penelitian", 
    "Translation I", 
    "Translation II"
]
matkul_pilihan = st.sidebar.selectbox("Pilih Mata Kuliah:", list_matkul)

st.sidebar.markdown("---")

# 2. Pilih Menu Aktivitas
menu = st.sidebar.radio("Pilih Aktivitas:", ["🏠 Beranda", "📖 Materi Kuliah", "🤖 Tanya Asisten AI", "📝 Kuis"])

# --- FUNGSI AI ---
def tanya_ai(pertanyaan, konteks_matkul):
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if available_models:
            model = genai.GenerativeModel(available_models[0])
            # Memberikan instruksi agar AI menjawab sesuai mata kuliah
            prompt = f"Anda adalah asisten dosen untuk mata kuliah {konteks_matkul}. Jawablah pertanyaan mahasiswa berikut: {pertanyaan}"
            response = model.generate_content(prompt)
            return response.text
        return "Model AI tidak tersedia."
    except Exception as e:
        return f"Kesalahan: {e}"

# --- ISI HALAMAN ---

if menu == "🏠 Beranda":
    st.title(f"🌟 Selamat Datang di Kelas {matkul_pilihan}")
    st.write(f"Selamat datang di platform pembelajaran digital untuk mata kuliah **{matkul_pilihan}**.")
    nama = st.text_input("Masukkan Nama Anda:")
    if nama:
        st.success(f"Halo {nama}, selamat bergabung di kelas {matkul_pilihan}!")

elif menu == "📖 Materi Kuliah":
    st.title(f"📖 Materi: {matkul_pilihan}")
    st.info(f"Halaman ini berisi ringkasan materi untuk {matkul_pilihan}.")
    # Contoh isi otomatis berdasarkan pilihan
    st.write(f"Sekarang kita akan mempelajari konsep dasar dari **{matkul_pilihan}**.")
    st.markdown("*(Bapak bisa mengganti teks ini dengan materi asli Bapak di file app.py)*")

elif menu == "🤖 Tanya Asisten AI":
    st.title(f"🤖 Asisten AI: {matkul_pilihan}")
    st.write(f"Tanyakan apa saja khusus mengenai materi **{matkul_pilihan}**.")
    
    pertanyaan = st.text_input("Ketik pertanyaan Anda:")
    if pertanyaan:
        with st.spinner("Mencari jawaban cerdas..."):
            jawaban = tanya_ai(pertanyaan, matkul_pilihan)
            st.markdown("### Jawaban Asisten:")
            st.write(jawaban)

elif menu == "📝 Kuis":
    st.title(f"📝 Kuis: {matkul_pilihan}")
    st.write(f"Mari uji pemahaman Anda tentang **{matkul_pilihan}**.")
    
    # Kuis sederhana yang menyesuaikan nama matkul
    st.write(f"Apakah Anda sudah menguasai materi **{matkul_pilihan}** minggu ini?")
    pilihan = st.radio("Pilih progres Anda:", ["Sangat Paham", "Cukup Paham", "Masih Bingung"])
    if st.button("Kirim Respon"):
        st.success(f"Terima kasih! Dosen akan melihat progres Anda di kelas {matkul_pilihan}.")
