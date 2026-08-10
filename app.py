                    import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="صانع الامتحانات التفاعلي", page_icon="📝")

st.title("📝 صانع الامتحانات التفاعلي")

# الشريط الجانبي لإدخال API Key
st.sidebar.header("الإعدادات")
api_key = st.sidebar.text_input("أدخلي مفتاح Gemini API:", type="password")

if not api_key:
    st.info("الرجاء إدخال Gemini API Key في القائمة الجانبية للبدء.")
else:
    try:
        genai.configure(api_key=api_key)
        # اسم الكلاس الصحيح
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.success("تم الاتصال بنجاح! جاهز لتوليد الامتحان.")
        
        text_input = st.text_area("أدخلي نص المادة أو الشيت هنا:", height=200)
        
        if st.button("توليد الامتحان 🚀"):
            if text_input.strip():
                with st.spinner("جاري إنشاء الأسئلة..."):
                    prompt = f"قم بإنشاء امتحان تفاعلي مكون من أسئلة اختيار من متعدد مع الإجابات النموذجية بناءً على النص التالي:\n\n{text_input}"
                    response = model.generate_content(prompt)
                    st.markdown("### 📋 الامتحان الناتِج:")
                    st.write(response.text)
            else:
                st.warning("الرجاء كتابة أو لصق نص المادة أولاً.")
                
    except Exception as e:
        st.error(f"حدث خطأ أثناء الاتصال: {e}")
