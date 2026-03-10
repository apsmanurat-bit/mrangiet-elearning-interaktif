import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="Portal E-Learning Interaktif", layout="wide")

# API KEY ANDA
API_KEY = "AIzaSyC6cVc6kfcMaPu5H25UmB73RMTlbwt1nR0"
genai.configure(api_key=API_KEY)

# --- SIDEBAR (MENU SAMPING) ---
st.sidebar.title("🎓 Portal Akademik")

# 1. Input Nama Mahasiswa (Disimpan di Sidebar agar AI tahu siapa yang bertanya)
nama_mhs = st.sidebar.text_input("Masukkan Nama Anda:", placeholder="Contoh: Budi Santoso")

st.sidebar.markdown("---")

# 2. Pilih Mata Kuliah
list_matkul = [
    "Pancasila", "Pendidikan Kewarganegaraan", "Communicative Grammar I", 
    "Communicative Grammar II", "Filsafat Moral", "Public Speaking", 
    "Metode Penelitian", "Translation I", "Translation II"
]
matkul_pilihan = st.sidebar.selectbox("Pilih Mata Kuliah:", list_matkul)

st.sidebar.markdown("---")

# 3. Pilih Menu Aktivitas
menu = st.sidebar.radio("Pilih Aktivitas:", ["🏠 Beranda", "📖 Materi Kuliah", "🤖 Tanya Asisten AI", "📝 Kuis"])

# --- FUNGSI AI DENGAN PENYAPAAN NAMA ---
def tanya_ai(pertanyaan, konteks_matkul, nama):
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if available_models:
            model = genai.GenerativeModel(available_models[0])
            
            # Instruksi Khusus agar AI Menyapa Nama Mahasiswa
            if nama:
                instruksi = f"Anda adalah asisten dosen yang ramah untuk mata kuliah {konteks_matkul}. Mahasiswa yang bertanya bernama {nama}. Awali jawaban Anda dengan menyapa {nama} secara sopan, lalu jawab pertanyaannya."
            else:
                instruksi = f"Anda adalah asisten dosen untuk mata kuliah {konteks_matkul}."
                
            prompt = f"{instruksi}\n\nPertanyaan: {pertanyaan}"
            response = model.generate_content(prompt)
            return response.text
        return "Model AI tidak tersedia."
    except Exception as e:
        return f"Kesalahan: {e}"

# --- ISI HALAMAN ---

if menu == "🏠 Beranda":
    st.title(f"🌟 Selamat Datang di Kelas {matkul_pilihan}")
    if nama_mhs:
        st.subheader(f"Halo, {nama_mhs}!")
        st.write(f"Senang melihat Anda bergabung di kelas **{matkul_pilihan}** hari ini. Silakan pilih materi atau tanya asisten AI jika ada kesulitan.")
    else:
        st.warning("Silakan isi nama Anda di menu samping agar asisten AI dapat mengenali Anda.")
        st.write(f"Selamat datang di platform pembelajaran digital untuk mata kuliah **{matkul_pilihan}**.")

elif menu == "📖 Materi Kuliah":
    st.title(f"📖 Materi: {matkul_pilihan}")
    st.info(f"Topik minggu ini: Pendalaman materi dasar {matkul_pilihan}.")
    st.write("Silakan pelajari modul yang telah disediakan atau diskusikan dengan asisten AI jika ada bagian yang kurang jelas.")

elif menu == "🤖 Tanya Asisten AI":
    st.title(f"🤖 Asisten AI: {matkul_pilihan}")
    
    if not nama_mhs:
        st.error("⚠️ Mohon isi nama Anda di menu samping terlebih dahulu agar Asisten AI bisa menjawab dengan sopan.")
    else:
        st.write(f"Halo **{nama_mhs}**, ada yang bisa saya bantu terkait mata kuliah **{matkul_pilihan}**?")
        pertanyaan = st.text_input("Ketik pertanyaan Anda di sini:")
        
        if pertanyaan:
            with st.spinner(f"Sabar ya {nama_mhs}, saya sedang mencari jawaban..."):
                jawaban = tanya_ai(pertanyaan, matkul_pilihan, nama_mhs)
                st.markdown("### Jawaban Asisten:")
                st.write(jawaban)

elif menu == "📝 Kuis":
    st.title(f"📝 Kuis: {matkul_pilihan}")
    st.write(f"Halo {nama_mhs if nama_mhs else 'Mahasiswa'}, mari uji pemahaman Anda.")
    # (Logika kuis tetap seperti sebelumnya)
    st.radio("Apakah materi hari ini sudah jelas?", ["Sangat Jelas", "Perlu Penjelasan Lagi"])
    if st.button("Kirim Respon"):
        st.balloons()
