import sqlite3
DATABASE_NAME = "history.db"
def connect():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS execution_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        line INTEGER,
        variable TEXT,
        value TEXT
    )
    """)
    conn.commit()
    return conn, cursor
def save(line, variable, value):
    conn, cursor = connect()
    cursor.execute("""
        INSERT INTO execution_log (line, variable, value)
        VALUES (?, ?, ?)
    """, (line, variable, str(value)))
    conn.commit()
    conn.close()
def show_records():
    conn, cursor = connect()
    cursor.execute("""
        SELECT id, line, variable, value
        FROM execution_log
    """)
    rows = cursor.fetchall()
    print("\nDatabase Records:\n")
    for row in rows:
        print(row)
    print(f"\nTotal Records: {len(rows)}")
    conn.close()
def clear():
    conn, cursor = connect()
    cursor.execute("DELETE FROM execution_log")
    conn.commit()
    conn.close()