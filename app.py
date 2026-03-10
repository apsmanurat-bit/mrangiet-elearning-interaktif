import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="E-Learning Interaktif", layout="wide")

# API KEY MILIK ANDA
API_KEY = "AIzaSyC6cVc6kfcMaPu5H25UmB73RMTlbwt1nR0"
genai.configure(api_key=API_KEY)

st.sidebar.title("📚 Menu Belajar")
menu = st.sidebar.radio("Pilih Halaman:", ["🏠 Beranda", "🤖 Tanya Asisten AI"])

if menu == "🏠 Beranda":
    st.title("Selamat Datang")
    st.write("Silakan buka menu Tanya Asisten AI untuk mengetes.")

elif menu == "🤖 Tanya Asisten AI":
    st.title("🤖 Debug Mode AI")
    pertanyaan = st.text_input("Ketik pertanyaan tes:")
    
    if pertanyaan:
        with st.spinner("Mencoba menghubungi Google AI..."):
            try:
                # Kita pakai model yang paling dasar dan pasti ada
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(pertanyaan)
                st.write("### Jawaban AI:")
                st.write(response.text)
            except Exception as e:
                st.error("Terjadi Kesalahan Teknis!")
                st.info(f"Pesan Error dari Google: {str(e)}")
                st.warning("Jika errornya 'API_KEY_INVALID', berarti kuncinya salah salin. Jika 'Location not supported', berarti butuh sedikit setting tambahan.")
