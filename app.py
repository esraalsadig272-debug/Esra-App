import streamlit as st
import google.generativeai as genai
import json

st.set_page_config(page_title="تطبيق الامتحانات", page_icon="📝")

st.title("📝 صانع الامتحانات التفاعلي")

api_key = st.sidebar.text_input("أدخلي مفتاح Gemini API:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeAIModel('gemini-1.5-flash')

    sheet_text = st.text_area("انصخي نص الشيت هنا:", height=200)

    if st.button("توليد الامتحان 🚀") and sheet_text:
        with st.spinner("جاري إنشاء الأسئلة..."):
            prompt = f"""
            أنت معلم خبير. بناءً على النص المرفق، قم بإنشاء امتحان مكون من 3 أسئلة اختيار من متعدد.
            يجب أن تكون المخرجات بصيغة JSON فقط بهذا الشكل:
            [
                {{
                    "question": "السؤال",
                    "options": ["أ) ...", "ب) ...", "ج) ...", "د) ..."],
                    "correct_answer": "أ",
                    "explanation": "الشرح"
                }}
            ]
            النص: {sheet_text}
            """
            try:
                response = model.generate_content(
                    prompt, 
                    generation_config={"response_mime_type": "application/json"}
                )
                st.session_state.quiz_data = json.loads(response.text)
                st.success("تم إنشاء الامتحان بنجاح!")
            except Exception as e:
                st.error(f"حدث خطأ: {e}")

    if "quiz_data" in st.session_state:
        st.write("---")
        st.subheader("📋 الامتحان")
        
        user_answers = {}
        with st.form("quiz_form"):
            for i, q in enumerate(st.session_state.quiz_data):
                st.write(f"**س{i+1}: {q['question']}**")
                user_answers[i] = st.radio("إجابتك:", q['options'], key=f"q_{i}")
                st.write("---")
            
            submit_button = st.form_submit_button("إنهاء الامتحان وتصحيح الإجابات 🎯")

        if submit_button:
            score = 0
            st.subheader("📊 النتيجة والتحليل")
            for i, q in enumerate(st.session_state.quiz_data):
                selected = user_answers[i]
                selected_letter = selected.split(")")[0].strip()
                correct_letter = q['correct_answer']

                if selected_letter == correct_letter:
                    score += 1
                    st.success(f"س{i+1}: إجابة صحيحة! ({selected})")
                else:
                    st.error(f"س{i+1}: إجابة خاطئة. إجابتك: {selected} | الصحيحة: {correct_letter}")
                    st.info(f"💡 الشرح: {q['explanation']}")
            
            total = len(st.session_state.quiz_data)
            st.metric("الدرجة النهائية", f"{score} / {total}", f"{(score/total)*100:.0f}%")
else:
    st.warning("الرجاء إدخال Gemini API Key في القائمة الجانبية للبدء.")
