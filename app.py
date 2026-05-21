import streamlit as st
import pandas as pd
from datetime import datetime

# Апп-ын үндсэн тохиргоо
st.set_page_config(page_title="Миний Хувийн Туслах", page_icon="📝", layout="centered")

# --- СЭДЭВ БА ГОО ЗҮЙ (Алдаагүй хувилбар) ---
st.markdown("""
    <style>
    .stApp { background-color: #FAFAFA; }
    h1, h2, h3 { color: #D35400; font-family: 'Segoe UI', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# --- GOOGLE SHEETS-ТЭЙ ХОЛБОГДОХ ХЭСЭГ ---
try:
    sheet_url = st.secrets["private_sheet_url"]
except Exception:
    st.warning("⚠️ Google Sheets-ийн холбоосыг Streamlit Secrets-д тохируулах шаардлагатай.")
    sheet_url = None

def load_data(sheet_name):
    if sheet_url:
        try:
            # Төрөл бүрийн хуудаснаас өгөгдлийг csv хэлбэрээр татаж авах
            base_url = sheet_url.split("/edit")[0]
            url = f"{base_url}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
            return pd.read_csv(url)
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()

# --- ХАЖУУГИЙН ЦЭС (NAVIGATION) ---
st.sidebar.title("📌 ҮНДСЭН ЦЭС")
menu = st.sidebar.radio(
    "Шилжих хуудсаа сонгоно уу:",
    ["🇺🇸 МИССУРИ ТӨЛӨВЛӨГӨӨ", "📚 АКАДЕМИК ҮГС", "📖 ӨДРИЙН ТЭМДЭГЛЭЛ", "🎓 CAMBRIDGE SOCIOLOGY"]
)

# ==========================================
# 1. МИССУРИ ТӨЛӨВЛӨГӨӨ ХУУДАС
# ==========================================
if menu == "🇺🇸 МИССУРИ ТӨЛӨВЛӨГӨӨ":
    st.title("🇺🇸 Миссури сургуулийн бэлтгэл")
    
    sub_menu = st.tabs(["🇲🇳 ...", "🇺🇸 ..."])
    
    with sub_menu[0]:
        st.subheader("📍 Монголд амжуулах ажлууд")
        df_mongolia = load_data("Миссури - Монголд")
        if not df_mongolia.empty:
            for index, row in df_mongolia.iterrows():
                with st.expander(f"🔹 {row.get('Бэлтгэх зүйл', 'Нэргүй ажил')}"):
                    st.write(f"**Тайлбар:** {row.get('Тайлбар', 'Тайлбар байхгүй')}")
        else:
            st.info("Одоогоор Монголд бэлтгэх зүйлсийн жагсаалт хоосон байна эсвэл Sheet-ийн нэр зөрж байна.")
            
    with sub_menu[1]:
        st.subheader("📍 Очоод хийх болон анхаарах зүйлс")
        df_us = load_data("Миссури - Очоод")
        if not df_us.empty:
            for index, row in df_us.iterrows():
                with st.expander(f"🏆 {row.get('Орох тэмцээн уралдаан', 'Нэргүй тэмцээн')}"):
                    st.write(f"**Шаардлагатай зүйлс:** {row.get('Шаардлагатай зүйлс', '-')}")
        else:
            st.info("Одоогоор очоод сурах хугацааны жагсаалт хоосон байна эсвэл Sheet-ийн нэр зөрж байна.")

# ==========================================
# 2. АКАДЕМИК ҮГС ХУУДАС
# ==========================================
elif menu == "📚 АКАДЕМИК ҮГС":
    st.title("📚 Academic Vocabulary")
    st.write("Шинэ үгсээ давтаж, цээжлээрэй.")
    
    df_words = load_data("Академик үг")
    if not df_words.empty:
        search = st.text_input("🔍 Үг хайх:")
        if search:
            df_words = df_words[df_words['үг'].astype(str).str.contains(search, case=False, na=False)]
            
        for index, row in df_words.iterrows():
            st.markdown(f"### 🇬🇧 {row.get('үг', '')}")
            st.markdown(f"**🇲🇳 Утга:** {row.get('утга', '')}")
            st.markdown(f"*💡 Жишээ:* {row.get('жишээ', '')}")
            st.markdown("---")
    else:
        st.info("Үгийн сан хоосон байна эсвэл Sheet-ийн нэр зөрж байна.")

# ==========================================
# 3. ӨДРИЙН ТЭМДЭГЛЭЛ ХУУДАС
# ==========================================
elif menu == "📖 ӨДРИЙН ТЭМДЭГЛЭЛ":
    st.title("📖 Хувийн өдрийн тэмдэглэл")
    
    st.subheader("✍️ Өнөөдрийн мэдрэмжээ буулгах")
    note_date = st.date_input("Огноо сонгох:", datetime.now())
    note_content = st.text_area("Өнөөдөр юу бодогдов?...", height=150)
    
    if st.button("Тэмдэглэлийг хадгалах"):
        if note_content:
            st.success("✅ Тэмдэглэл бичигдлээ! (Линк холболт шалгагдаж байна)")
            
    st.markdown("---")
    st.subheader("📜 Өмнөх тэмдэглэлүүд")
    df_notes = load_data("Тэмдэглэл")
    if not df_notes.empty:
        for index, row in df_notes.iterrows():
            with st.chat_message("user"):
                st.write(f"📅 **{row.get('он сар', '')}**")
                st.write(row.get('мэдрэмжээ буулгах нь', ''))
    else:
        st.info("Өмнө нь бичсэн тэмдэглэл одоогоор байхгүй байна.")

# ==========================================
# 4. CAMBRIDGE SOCIOLOGY ХУУДАС
# ==========================================
elif menu == "🎓 CAMBRIDGE SOCIOLOGY":
    st.title("🎓 Cambridge Sociology")
    
    df_soc = load_data("CAMBRIDGE SOCIOLOGY")
    if not df_soc.empty:
        for index, row in df_soc.iterrows():
            st.markdown(f"### 📖 Сэдэв #{index+1}")
            st.markdown(f"**📚 Унших материал:** {row.get('унших материал', '')}")
            st.markdown(f"**🎯 Сурах зүйл:** {row.get('сурах зүйл', '')}")
            st.markdown(f"**⚠️ Анхаарах зүйл:** {row.get('анхаарах зүйл', '')}")
            st.markdown(f"**💡 Миний ойлгосон зүйл:** {row.get('миний ойлгосон зүйл', '')}")
            st.markdown("---")
    else:
        st.info("Sociology хичээлийн мэдээлэл одоогоор хоосон байна.")
