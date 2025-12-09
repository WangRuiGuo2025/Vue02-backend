import sqlite3
from sqlite3 import Error
from datetime import datetime

DB_PATH = "message_board.db"

def create_db_and_table():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        create_table_sql = """
        CREATE TABLE IF NOT EXISTS message_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mid INTEGER NOT NULL,
            email TEXT,
            message TEXT NOT NULL,
            good INTEGER DEFAULT 0,
            bad INTEGER DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_sql)
        conn.commit()

    except Error as e:
        print(f"操作失败：{e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_db_and_table()