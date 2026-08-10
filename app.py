import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

st.set_page_config(page_title="صانع الامتحانات التفاعلي", page_icon="📝")

st.title("📝 صانع الامتحانات التفاعلي")

st.sidebar.header("الإعدادات")
api_key = st.sidebar.text_input("أدخلي مفتاح Gemini API:", type="password")

if not api_key:
    st.info("الرجاء إدخال Gemini API Key في القائمة الجانبية للبدء.")
else:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.success("تم الاتصال بنجاح! جاهز لتوليد الامتحان.")
        
        # خيار رفع ملف PDF أو كتابة نص
        uploaded_file = st.file_uploader("ارفعي ملف الشيت (PDF)", type=["pdf"])
        text_input = st.text_area("أو الصقي نص الشيت هنا مباشرة:", height=150)
        
        extracted_text = ""
        
        if uploaded_file is not None:
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                extracted_text += page.extract_text() or ""
        elif text_input.strip():
            extracted_text = text_input.strip()
            
        if st.button("توليد الامتحان 🚀"):
            if extracted_text:
                with st.spinner("جاري قراءة الشيت وإنشاء الأسئلة..."):
                    prompt = f"قم بإنشاء امتحان تفاعلي مكون من أسئلة اختيار من متعدد مع الإجابات النموذجية بناءً على المحتوى التالي:\n\n{extracted_text}"
                    response = model.generate_content(prompt)
                    st.markdown("### 📋 الامتحان الناتِج:")
                    st.write(response.text)
            else:
                st.warning("الرجاء رفع ملف PDF أو كتابة نص الشيت أولاً.")
                
    except Exception as e:
        st.error(f"حدث خطأ أثناء الاتصال: {e}")
