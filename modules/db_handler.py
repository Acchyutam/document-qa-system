import mysql.connector
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from modules.embeddings import embed_question
import os

from dotenv import load_dotenv
load_dotenv()

db = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_DATABASE')
)
cursor = db.cursor()

def document_exists(doc_hash):
    cursor.execute("SELECT filename FROM qa_table WHERE document_hash = %s LIMIT 1", (doc_hash,))
    return cursor.fetchone() is not None

def update_filename_if_needed(doc_hash, new_filename):
    cursor.execute("SELECT filename FROM qa_table WHERE document_hash = %s LIMIT 1", (doc_hash,))
    old_filename = cursor.fetchone()[0]
    if old_filename != new_filename:
        cursor.execute("UPDATE qa_table SET filename = %s WHERE document_hash = %s", (new_filename, doc_hash))
        db.commit()
        st.info(f"🔄 Updated filename in DB from {old_filename} to {new_filename}")

def search_similar_question(doc_hash, question):
    user_emb = embed_question(question)
    cursor.execute("SELECT question, question_embedding, answer FROM qa_table WHERE document_hash = %s", (doc_hash,))
    best_sim = 0
    best_answer = None
    for q, emb_json, a in cursor.fetchall():
        emb = np.array(json.loads(emb_json))
        sim = cosine_similarity([user_emb], [emb])[0][0]
        if sim > best_sim:
            best_sim = sim
            best_answer = a
    return best_answer if best_sim >= 0.8 else None

def save_question(doc_hash, filename, question, answer):
    try:
        q_embed = embed_question(question)
        cursor.execute(
            "INSERT INTO qa_table (document_hash, filename, question, question_embedding, answer) VALUES (%s, %s, %s, %s, %s)",
            (doc_hash, filename, question, json.dumps(q_embed), answer)
        )
        db.commit()
    except Exception as e:
        print(f"DB Save Error: {e}")
