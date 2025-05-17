import streamlit as st
import time
from langchain.chains import create_retrieval_chain, create_stuff_documents_chain
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from modules import db_handler, ui_components
from modules.embeddings import embedding_model

llm = ChatGroq(groq_api_key=st.secrets["API_KEY"], model_name="Llama3-8b-8192")
prompt = ChatPromptTemplate.from_template("""
You are an intelligent assistant. Based on the following context, answer the user's question.

Context:
{context}

Question:
{input}

If the answer is not in the context or not a valid question, just say "I don't know."
""")

def ask_question_interface():
    filenames = list(st.session_state.get('documents', {}).values())
    selected_filename = st.selectbox("📄 Choose document:", filenames)
    selected_hash = [h for h, f in st.session_state['documents'].items() if f == selected_filename][0]
    question = st.text_input("Ask your question:")

    if st.button("📨 Submit Question"):
        if not question.strip():
            st.error("Please enter a valid question.")
            return

        cached = db_handler.search_similar_question(selected_hash, question)
        if cached:
            st.success("✅ Retrieved from cache")
            answer = cached
        else:
            retriever = st.session_state['vectorstores'][selected_hash].as_retriever()
            docs = retriever.get_relevant_documents(question)
            chain = create_stuff_documents_chain(llm, prompt)
            result = chain.invoke({"input": question, "context": docs})
            answer = result.strip()
            if answer.lower().startswith("i don't know"):
                st.warning("Answer not found.")
                return
            db_handler.save_question(selected_hash, selected_filename, question, answer)

        st.write("📝 **Answer:**")
        st.write(answer)
        ui_components.offer_audio(answer)
