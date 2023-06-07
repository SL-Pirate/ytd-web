import sqlite3

conn = sqlite3.connect("api_users.db", check_same_thread=False)
cursor = conn.cursor()
table_name = "api_users"

def create_table() -> None:
    cursor.execute(
        f"""
            CREATE TABLE IF NOT EXISTS {table_name}(
                uid INTEGER PRIMARY KEY,
                first_name VARCHAR(500),
                last_name VARCHAR(500),
                username VARCHAR(100) NOT NULL,
                api_key VARCHAR(64) NOT NULL UNIQUE,
                call_count INTEGER NOT NULL
            )
        """
    )

create_table()
