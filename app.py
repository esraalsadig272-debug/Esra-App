import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="صانع الامتحانات التفاعلي", page_icon="📝")

st.title("📝 صانع الامتحانات التفاعلي")

# قراءة المفتاح المحفوظ سرياً في Streamlit أو من القائمة الجانبية
api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else st.sidebar.text_input("أدخلي مفتاح Gemini API:", type="password")

if not api_key:
    st.info("الرجاء إدخال Gemini API Key للبدء.")
else:
    try:
        genai.configure(api_key=api_key)
        # استخدام النسخة الرسمية والمستقرة 
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        st.success("التطبيق متصل وجاهز! 🚀")
        
        uploaded_file = st.file_uploader("ارفعي ملف الشيت (PDF أو صورة)", type=["pdf", "png", "jpg", "jpeg"])
        text_input = st.text_area("أو الصقي نص الشيت هنا مباشرة:", height=150)
        
        if st.button("توليد الامتحان 🚀"):
            with st.spinner("جاري قراءة الشيت وإنشاء الأسئلة..."):
                if uploaded_file is not None:
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
