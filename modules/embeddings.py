from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import streamlit as st

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"device": "cpu"})

def vectorize_and_store(file_path, doc_hash, filename):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = splitter.split_documents(docs)

    for doc in split_docs:
        doc.metadata = {"document_hash": doc_hash, "filename": filename}

    vectors = FAISS.from_documents(split_docs, embedding_model)
    st.session_state.setdefault('vectorstores', {})[doc_hash] = vectors

def embed_question(question):
    return embedding_model.embed_query(question)
