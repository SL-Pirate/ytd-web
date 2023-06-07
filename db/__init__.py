import sqlite3

conn = sqlite3.connect("api_users.db", check_same_thread=False)
cursor = conn.cursor()
table_name = "api_users"
table2_name = "users"

def create_table() -> None:
    cursor.execute(
        f"""
            CREATE TABLE IF NOT EXISTS {table_name}(
                uid INTEGER,
                api_key VARCHAR(64) NOT NULL UNIQUE,
                call_count INTEGER DEFAULT 0,

                FOREIGN KEY (uid) REFERENCES {table2_name} (uid)
            );
        """
    )
    cursor.execute(
        f"""
            CREATE TABLE IF NOT EXISTS {table2_name}(
                uid INTEGER PRIMARY KEY,
                first_name VARCHAR(500),
                last_name VARCHAR(500),
                email VARCHAR(200) NOT NULL UNIQUE,
                username VARCHAR(100) NOT NULL,
                password NOT NULL,
                salt NOT NULL UNIQUE
            );
        """
    )

create_table()
