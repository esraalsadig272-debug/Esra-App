import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="صانع الامتحانات التفاعلي", page_icon="📝")

st.title("📝 صانع الامتحانات التفاعلي")

# جلب المفتاح المحفوظ سرياً تلقائياً
api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else None

if not api_key:
    st.error("لم يتم العثور على API Key في Secrets! الرجاء التأكد من إضافته في إعدادات Streamlit.")
else:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.success("التطبيق متصل ومحفوظ تلقائياً! 🚀")
        
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
