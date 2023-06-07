import random, string
from db import cursor, conn, create_table, table_name
import hashlib

class ApiUser:
    def __init__(self, uid: int, api_key: str=None, call_count: int=0) -> None:
        self._synced = False
        self._uid = uid
        self._api_key = api_key if not None else ApiUser.gen_api_key()
        self._call_count = call_count

    def add_to_db(self) -> None:
        self._api_key: str = ApiUser.gen_api_key()
        
        sql = f"""
            INSERT INTO {table_name}(
                uid,
                api_key
            )
            VALUES (?, ?);
        """
        cursor.execute(sql, (self._uid, self._api_key))
        conn.commit()

    def get_api_key(self) -> str:
        return self._api_key
    
    def get_uid(self) -> str:
        return self._uid
    
    def get_call_count(self) -> int:
        return self._call_count
    
    def getUserFromUid(uid: int):
        try:
            sql = f"""
                SELECT * 
                FROM {table_name}
                WHERE uid = (?)
            """
            result = cursor.execute(sql, (uid,)).fetchone()

            user = ApiUser(result[0], api_key=result[1], call_count=result[2])
            return user
        except Exception as e:
            return None


    # @staticmethod
    # def delete_user_by_api_key(api_key: string):
    #     sql = f"DELETE FROM {table_name} WHERE _api_key = (?)"
    #     cursor.execute(sql, (api_key,))
    #     conn.commit()

    @staticmethod
    def gen_api_key() -> str:
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(50))


    @staticmethod
    def encrypt(key: string) -> str:
        return hashlib.sha256((key).encode('utf-8')).hexdigest()
    
    
    @staticmethod
    def encrypt(key: string) -> str:
        return hashlib.sha256((key).encode('utf-8')).hexdigest()
    
    @staticmethod
    def validate_api_key(key: str) -> bool:
        sql = f"SELECT uid FROM {table_name} WHERE api_key = (?);"
        result = cursor.execute(sql, (key,)).fetchone()

        if (result != None):
            sql = f"UPDATE {table_name} SET call_count = call_count + 1 WHERE uid = (?)"
            cursor.execute(sql, result)
            conn.commit()
            return True
        else:
            return False

# __________________________ USE THESE FUNCTIONS FOR TESTING PURPOSES ONLY ______________________________
    @staticmethod
    def print_db() -> None:
        results = cursor.execute(f"SELECT * FROM {table_name};")

        print("(uid, first_name, last_name, username, email, encrypted_api_key, call_count)")
        for result in results:
            print(result)

    @staticmethod
    def truncate() -> None:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        create_table()
