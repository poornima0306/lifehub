import sqlite3

def init_db():
    conn = sqlite3.connect("/tmp/lifehub.db")
    cursor = conn.cursor()

    # -------- USERS TABLE --------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # -------- TASKS TABLE (CLEAN + COMPLETE) --------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            task TEXT,
            due_date TEXT,
            category TEXT DEFAULT 'Personal',
            priority TEXT DEFAULT 'Medium',
            progress INTEGER DEFAULT 0,
            complete INTEGER DEFAULT 0,
            reminder_time TEXT DEFAULT NULL
        )
    """)

    conn.commit()
    conn.close()

    print("✅ Database initialized successfully (clean version)")


# -------- RUN DIRECTLY --------
if __name__ == "__main__":
    init_db()
