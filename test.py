import sqlite3

def test_database():
    conn = sqlite3.connect("lifehub.db")
    cursor = conn.cursor()

    print("🔍 Checking tables...\n")

    # Check users
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print("👤 USERS:")
    if users:
        for u in users:
            print(u)
    else:
        print("No users found")

    print("\n------------------\n")

    # Check tasks
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    print("📝 TASKS:")
    if tasks:
        for t in tasks:
            print(t)
    else:
        print("No tasks found")

    print("\n------------------\n")

    # Check structure
    print("📊 TABLE STRUCTURE:")
    cursor.execute("PRAGMA table_info(tasks)")
    columns = cursor.fetchall()
    for col in columns:
        print(col)

    conn.close()
    print("\n✅ Test completed")


if __name__ == "__main__":
    test_database()