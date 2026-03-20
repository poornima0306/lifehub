import sqlite3
conn = sqlite3.connect("lifehub.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
data = cursor.fetchall()
print(data)
conn.close()