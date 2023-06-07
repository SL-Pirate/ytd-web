import random, string
from db import cursor, conn, create_table, table_name
from ytd_helper import encryption_salt
import hashlib

class ApiUser:
    def __init__(self, username: str, first_name: str = None, last_name: str = None) -> None:
        self._username: str = username
        self._first_name: str = first_name
        self._last_name: str = last_name
        self._call_count: int = 0
        self._api_key: str = ApiUser.gen_api_key()

        self._encrypted_api_key: str = ApiUser.encrypt(self._api_key)
        
        self.add_to_db()

    def add_to_db(self) -> None:
        sql = f"""
            INSERT INTO {table_name}(
                first_name, 
                last_name, 
                username, 
                api_key, 
                call_count
            )
            VALUES (?, ?, ?, ?, ?);
        """
        cursor.execute(sql, self._to_tuple())
        conn.commit()

    def get_api_key(self) -> str:
        return self._api_key

    def _to_tuple(self) -> tuple[any]:
        return (self._first_name, self._last_name, self._username, self._encrypted_api_key, self._call_count)

    @staticmethod
    def delete_user_by_api_key(api_key: string):
        sql = f"DELETE FROM {table_name} WHERE _api_key = (?)"
        cursor.execute(sql, (api_key,))
        conn.commit()

    @staticmethod
    def gen_api_key() -> str:
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(50))

    @staticmethod
    def encrypt(key: string) -> str:
        return hashlib.sha256((key + encryption_salt).encode('utf-8')).hexdigest()
    
    @staticmethod
    def validate_api_key(key: str) -> bool:
        sql = f"SELECT uid FROM {table_name} WHERE api_key = (?);"
        encrypted_key = ApiUser.encrypt(key)
        result = cursor.execute(sql, (encrypted_key,))

        if (result):
            sql = f"UPDATE {table_name} SET call_count = call_count + 1 WHERE uid = (?)"
            cursor.execute(sql, result.fetchone())
            conn.commit()
            return True
        else:
            return False

# __________________________ USE THESE FUNCTIONS FOR TESTING PURPOSES ONLY ______________________________
    @staticmethod
    def print_db() -> None:
        results = cursor.execute(f"SELECT * FROM {table_name};")

        print("(uid, first_name, last_name, username, encrypted_api_key, call_count)")
        for result in results:
            print(result)

    @staticmethod
    def truncate() -> None:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        create_table()


