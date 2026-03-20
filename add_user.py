import sqlite3
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "lifehub.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "1234"))
conn.commit()
conn.close()
print("Users added")