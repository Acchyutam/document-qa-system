import os
import hashlib
from pdf2image import convert_from_path
from modules import embeddings, db_handler
import streamlit as st

def handle_upload(uploaded_file):
    filename = uploaded_file.name
    temp_path = f"temp_{filename}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    doc_hash = get_file_hash(temp_path)
    st.session_state.setdefault('documents', {})[doc_hash] = filename
    st.session_state.document_hash = doc_hash

    if db_handler.document_exists(doc_hash):
        db_handler.update_filename_if_needed(doc_hash, filename)
    else:
        embeddings.vectorize_and_store(temp_path, doc_hash, filename)
        st.success(f"✅ Ingested and stored: {filename}")

    with st.expander(f"👀 Preview {filename}", expanded=False):
        if st.button(f"Show Preview of {filename}", key=f"preview_button_{filename}"):
            preview_pdf(temp_path)

def preview_pdf(file_path):
    img = convert_from_path(file_path, first_page=1, last_page=1)[0]
    img_path = "temp_preview.png"
    img.save(img_path, 'PNG')
    st.image(img_path, caption="Preview of Uploaded PDF", use_column_width=True)
    os.remove(img_path)

def get_file_hash(file_path):
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()
