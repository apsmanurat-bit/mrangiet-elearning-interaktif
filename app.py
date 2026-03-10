import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="E-Learning Interaktif", layout="wide")

# API KEY ANDA
API_KEY = "AIzaSyC6cVc6kfcMaPu5H25UmB73RMTlbwt1nR0"
genai.configure(api_key=API_KEY)

st.sidebar.title("📚 Menu Belajar")
menu = st.sidebar.radio("Pilih Halaman:", ["🏠 Beranda", "🤖 Tanya Asisten AI", "📖 Materi", "📝 Kuis"])

if menu == "🏠 Beranda":
    st.title("🌟 Selamat Datang")
    st.write("Aplikasi E-Learning sudah aktif. Silakan pilih menu di samping.")

elif menu == "🤖 Tanya Asisten AI":
    st.title("🤖 Asisten AI")
    pertanyaan = st.text_input("Ketik pertanyaan Anda:")
    
    if pertanyaan:
        with st.spinner("Mencari jawaban..."):
            try:
                # JURUS PAMUNGKAS: Cari model apa saja yang ada di akun Anda
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                if available_models:
                    # Ambil model pertama yang tersedia (biasanya gemini-pro atau gemini-1.5-flash)
                    selected_model = available_models[0]
                    model = genai.GenerativeModel(selected_model)
                    response = model.generate_content(pertanyaan)
                    
                    st.write(f"**Jawaban (via {selected_model}):**")
                    st.write(response.text)
                else:
                    st.error("Tidak ada model AI yang ditemukan di akun Anda.")
            except Exception as e:
                st.error(f"Kesalahan: {e}")

elif menu == "📖 Materi":
    st.title("📖 Materi Kuliah")
    st.write("Identitas Nasional adalah ciri khas suatu bangsa.")

elif menu == "📝 Kuis":
    st.title("📝 Kuis")
    st.write("Apa warna bendera Indonesia?")
    st.button("Merah Putih")
