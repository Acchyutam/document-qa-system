import mysql.connector

db = mysql.connector.connect(
    host=,
    user=,
    password=
)

cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS qa")
cursor.execute("""
CREATE TABLE IF NOT EXISTS qa.qa_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_hash TEXT,
    filename TEXT,
    question TEXT,
    question_embedding TEXT,
    answer TEXT
)
""")

print("✅ Database and table setup complete.")
