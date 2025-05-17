# Document Question Answering System

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.24.0-red)
![LangChain](https://img.shields.io/badge/langchain-0.0.235-green)

An interactive AI-powered Document Question Answering (QA) System that allows users to upload PDF documents and ask natural language questions about their contents.

## 🌟 Features

- **Document Upload**: Support for single or multiple PDF documents
- **Natural Language Queries**: Ask questions in plain English about your documents
- **Semantic Search**: Utilizes vector embeddings to find the most relevant content
- **Context-Aware Answers**: Generates accurate responses based on document context
- **Source Verification**: Highlights the exact portions of the document used to generate answers
- **MySQL Caching**: Automatically stores and retrieves previous Q&A pairs for faster responses
- **Text-to-Speech**: Listen to answers with built-in audio playback
- **User-Friendly Interface**: Clean Streamlit UI for easy interaction

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Language Model**: Llama3-8B (via Groq)
- **Embeddings**: HuggingFaceEmbeddings
- **Vector Store**: FAISS
- **Document Processing**: LangChain
- **Database**: MySQL
- **Text-to-Speech**: Streamlit native TTS

## 📋 Requirements

```
see requirement.txt
```

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/Acchyutam/document-qa-system.git
cd document-qa-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
```bash
# Create a .env file in the project root
echo "GROQ_API_KEY=your_groq_api_key" > .env
echo "MYSQL_HOST=localhost" >> .env
echo "MYSQL_USER=youruser" >> .env
echo "MYSQL_PASSWORD=yourpassword" >> .env
echo "MYSQL_DATABASE=document_qa" >> .env
```

5. Set up the MySQL database:
```bash
# Run the included script to create the necessary tables
python setup_database.py
```

## 🖥️ Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to `http://localhost:8501`

3. Upload your PDF document(s) using the file uploader

4. Wait for the document processing to complete

5. Type your question in the text input field and press Enter

6. View the answer along with highlighted source sections

7. Optionally, click the audio button to listen to the answer

## 🔍 How It Works

1. **Document Ingestion**:
   - The PDF is split into manageable chunks
   - Each chunk is vectorized using HuggingFaceEmbeddings
   - The vectors are stored in a FAISS index for efficient retrieval

2. **Question Processing**:
   - The system checks if a similar question was asked before
   - If found in cache, returns the stored answer immediately
   - Otherwise, the question is vectorized and matched against document chunks

3. **Answer Generation**:
   - The most relevant document chunks are retrieved
   - These chunks are sent to Llama3-8B via Groq API as context
   - The LLM generates a comprehensive answer based on the provided context

4. **Result Presentation**:
   - The answer is displayed to the user
   - Source texts are highlighted in the document viewer
   - The Q&A pair is stored in MySQL for future reference

## 🗂️ Project Structure

```
document-qa-system/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Project dependencies
├── setup_database.py       # Database setup script
├── .env                    # Environment variables (not tracked by git)
├── modules/
│   ├── __init__.py
│   ├── document_processor.py  # PDF processing functions
│   ├── embeddings.py       # Vector embedding utilities
│   ├── qa_engine.py        # Q&A generation logic
│   ├── db_handler.py       # MySQL database operations
│   └── ui_components.py    # Streamlit UI elements
└── data/
    └── .gitkeep            # Folder for temporary data storage
```



## 🙏 Acknowledgements

- [LangChain](https://github.com/hwchase17/langchain) for the document processing framework
- [Streamlit](https://streamlit.io/) for the web interface
- [FAISS](https://github.com/facebookresearch/faiss) for efficient similarity search
- [Llama3](https://ai.meta.com/llama/) and [Groq](https://groq.com/) for the language model

