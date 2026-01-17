import streamlit as st

st.title("⚖️ مستشار قانون العمل (Rules as Code)")

# 1. جمع الحقائق من المستخدم (Inputs)
st.header("أدخل بيانات الموظف")
years_of_service = st.number_input("مدة الخدمة (بالسنوات)", min_value=0, max_value=60, value=1)
age = st.number_input("عمر الموظف", min_value=18, max_value=80, value=25)

# 2. المعالجة القانونية (The Legal Engine)
if st.button("احسب رصيد الأجازات"):
    
    # القاعدة الافتراضية
    vacation_days = 21
    reason = "يستحق الرصيد الاعتيادي (أقل من 10 سنوات خدمة وأقل من 50 سنة)."

    # الشروط الاستثنائية (المادة 47)
    # الشرط الأول: تجاوز سن الخمسين
    if age >= 50:
        vacation_days = 30
        reason = "يستحق 30 يوماً لأنه تجاوز سن الخمسين (طبقاً للمادة 47)."
    
    # الشرط الثاني: تجاوز 10 سنوات خدمة (حتى لو سنه صغير)
    elif years_of_service >= 10:
        vacation_days = 30
        reason = "يستحق 30 يوماً لأنه أمضى أكثر من 10 سنوات في الخدمة."

    # 3. الحكم النهائي (Output)
    st.success(f"رصيد الأجازات المستحق: {vacation_days} يوماً")
    st.info(f"السند القانوني: {reason}")