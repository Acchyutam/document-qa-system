import streamlit as st
import pyttsx3
import io

def inject_custom_css():
    st.markdown("""
    <style>
    .main { background-color: #1f2937; color: white; }
    h1, h2, h3 { color: #f9fafb; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def offer_audio(text):
    if st.checkbox("🔊 Listen to answer"):
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        engine.setProperty('voice', engine.getProperty('voices')[1].id)
        engine.save_to_file(text, 'temp_audio.mp3')
        engine.runAndWait()
        with open('temp_audio.mp3', 'rb') as f:
            st.audio(f.read(), format="audio/mp3")

def show_recent_questions():
    
    with st.expander("🕑 Recently Asked Questions on Your Documents", expanded=True):
        uploaded_documents = st.session_state.get('documents', {})

        if uploaded_documents:
            selected_filename = st.selectbox(
                "📄 Select a document to view recent questions:",
                list(uploaded_documents.values()),
                key="recent_doc_select"
            )

            selected_hash = None
            for hash_val, file_name in uploaded_documents.items():
                if file_name == selected_filename:
                    selected_hash = hash_val
                    break

            if selected_hash:
                cursor.execute(
                    "SELECT question, answer FROM qa_table WHERE document_hash = %s ORDER BY id DESC LIMIT 10",
                    (selected_hash,)
                )
                recent_qas = cursor.fetchall()

                if recent_qas:
                    for idx, (q, a) in enumerate(recent_qas):
                        with st.container():
                            st.markdown(f"**🔹 {q}**", unsafe_allow_html=True)

                            if st.button(f"Show Answer {idx+1}", key=f"recent_show_{idx}"):
                                # Save into session state
                                st.session_state['recent_answer'] = a
                                st.session_state['recent_question'] = q
                                st.session_state['recent_filename'] = selected_filename
                                st.session_state['recent_idx'] = idx

                    # 🔥 After buttons loop, check if a recent_answer exists
                    if 'recent_answer' in st.session_state and st.session_state['recent_answer']:
                        st.success("✅ Answer:")
                        st.caption(f"📄 Answer from: {st.session_state.get('recent_filename', 'Unknown Document')}")
                        st.write(st.session_state['recent_answer'])

                        # 🎤 Voice option
                        if st.checkbox(f"🔊 Listen to the Answer", key=f"listen_recent_answer"):
                            audio_clip = generate_audio_clip(st.session_state['recent_answer'])
                            st.audio(audio_clip, format="audio/mp3")

                else:
                    st.info("No recent questions yet for this document. Ask your first question!")
            else:
                st.warning("Selected document not found.")
        else:
            st.info("Upload and ingest a document first to see recent questions.")


