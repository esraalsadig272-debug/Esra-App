import streamlit as st
import google.generativeai as genai

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
        
        uploaded_file = st.file_uploader("ارفعي ملف الشيت (PDF أو صورة)", type=["pdf", "png", "jpg", "jpeg"])
        text_input = st.text_area("أو الصقي نص الشيت هنا مباشرة:", height=150)
        
        if st.button("توليد الامتحان 🚀"):
            with st.spinner("جاري قراءة الشيت وإنشاء الأسئلة..."):
                if uploaded_file is not None:
                    # قراءة الملف مباشرة عبر نموذج Gemini الذكي
                    file_bytes = uploaded_file.read()
                    mime_type = uploaded_file.type
                    
                    prompt = "قم بإنشاء امتحان تفاعلي شامل من أسئلة اختيار من متعدد مع الإجابات النموذجية والشرح بناءً على هذا الملف:"
                    
                    response = model.generate_content([
                        {"mime_type": mime_type, "data": file_bytes},
                        prompt
                    ])
                    st.markdown("### 📋 الامتحان الناتِج:")
                    st.write(response.text)
                elif text_input.strip():
                    prompt = f"قم بإنشاء امتحان تفاعلي مكون من أسئلة اختيار من متعدد مع الإجابات النموذجية بناءً على النص التالي:\n\n{text_input}"
                    response = model.generate_content(prompt)
                    st.markdown("### 📋 الامتحان الناتِج:")
                    st.write(response.text)
                else:
                    st.warning("الرجاء رفع ملف أو كتابة نص الشيت أولاً.")
                    
    except Exception as e:
        st.error(f"حدث خطأ أثناء الاتصال: {e}")
