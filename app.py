import streamlit as st
import pandas as pd
from collections import Counter
from nltk import ngrams
import io

# === إعدادات الصفحة ===
st.set_page_config(page_title="المحلل القانوني", layout="wide")

st.title("⚖️ منصة التحليل القانوني الذكي")
st.markdown("---")

# === القائمة الجانبية (Sidebar) ===
with st.sidebar:
    st.header("إعدادات التحليل")
    uploaded_file = st.file_uploader("ارفع ملف النص القانوني (TXT)", type=['txt'])
    min_percentage = st.slider("حساسية التحليل (%)", 0.1, 2.0, 0.1)
    st.info("كل ما الرقم يقل، كل ما النتائج تزيد.")

# === منطق التحليل (الماكينة) ===
def analyze_text(raw_text):
    # 1. التنظيف
    text = raw_text.replace("،", " ").replace("(", " ").replace(")", " ")
    text = text.replace("-", " ").replace(".", " ").replace(":", " ").replace("\n", " ").replace('"', " ")
    
    stop_words = ["في", "من", "على", "أن", "أو", "هذا", "هذه", "تم", "التي", "الذي", "عن", "كان", "لها", "ذلك", "فى", "و", "بها", "لا", "إلى", "ما", "مع", "كل", "أنه", "هو", "هي"]
    
    all_words = text.split()
    total_count = len(all_words)
    clean_words = [w for w in all_words if w not in stop_words]
    
    results = []
    
    # 2. الكلمات الفردية
    word_counts = Counter(clean_words)
    for word, freq in word_counts.most_common():
        pct = (freq / total_count) * 100
        if pct >= min_percentage:
            results.append({"العبارة": word, "التكرار": freq, "النوع": "كلمة فردية", "النسبة": round(pct, 2)})
            
    # 3. العبارات المركبة
    grams = ngrams(clean_words, 2)
    phrases = [" ".join(g) for g in grams]
    phrase_counts = Counter(phrases)
    for phrase, freq in phrase_counts.most_common():
        if freq >= 2:
            pct = (freq / total_count) * 100
            if pct >= (min_percentage / 2): # تساهل في العبارات المركبة
                 results.append({"العبارة": phrase, "التكرار": freq, "النوع": "عبارة مركبة", "النسبة": round(pct, 2)})
                 
    return results, total_count

# === العرض (Frontend) ===
if uploaded_file is not None:
    # قراءة الملف المرفوع
    string_data = uploaded_file.read().decode("utf-8")
    
    if st.button("ابدأ التحليل 🚀"):
        with st.spinner('جاري تحليل النصوص...'):
            data, total = analyze_text(string_data)
            
            # عرض إحصائيات سريعة
            col1, col2 = st.columns(2)
            col1.metric("إجمالي الكلمات", total)
            col2.metric("النتائج المستخرجة", len(data))
            
            # تحويل لداتا فريم وعرض الجدول
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
            
            # زرار تحميل الإكسل
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Report')
                
            st.download_button(
                label="📥 تحميل التقرير (Excel)",
                data=buffer,
                file_name="legal_analysis_report.xlsx",
                mime="application/vnd.ms-excel"
            )
else:
    st.warning("من فضلك قم برفع ملف نصي للبدء.")