import streamlit as st
from dotenv import load_dotenv
from modules import document_processor, embeddings, qa_engine, db_handler, ui_components

load_dotenv()
st.set_page_config(page_title="📄 Document QA System", layout="wide")
ui_components.inject_custom_css()

st.title("📄 Document Question Answering System")
st.caption("Upload your PDF ➔ Ingest ➔ Ask your questions!")

uploaded_files = st.file_uploader("📤 Upload your PDF files", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        document_processor.handle_upload(uploaded_file)

if st.session_state.get('vectorstores'):
    qa_engine.ask_question_interface()

ui_components.show_recent_questions()
