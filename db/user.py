import random, string
from db import cursor, conn, create_table
from db import table2_name as table_name
from ytd_helper import pepper
import hashlib
from sqlite3 import IntegrityError

class User:
    def __init__(
        self, 
        username: str, 
        password: str, 
        email: str, 
        first_name: str = None, 
        last_name: str = None, 
        uid: int = None
    ) -> None:
        self._username: str = username
        self._password: str = password
        self._first_name: str = first_name
        self._last_name: str = last_name
        self._email = email
        self._uid = uid
        self._salt = User.gen_salt()
        self._encrypted_pw: str = User.encrypt(self._password, self._salt)

    @staticmethod
    def login(email, password):
        sql = f"""
            SELECT *
            FROM {table_name}
            WHERE email = (?)
        """
        result = cursor.execute(sql, (email,)).fetchone()

        if (result != None):
            if result[5] == User.encrypt(password, result[6]):
                print(result)
                return User(result[4], result[5], result[3], first_name=result[1], last_name=result[2], uid=result[0])
            else:
                return None
        else:
            return None

    def register(self) -> tuple[any]:
        try:
            sql = f"""
                INSERT INTO {table_name}(
                    first_name, 
                    last_name, 
                    username, 
                    password,
                    email,
                    salt
                )
                VALUES (?, ?, ?, ?, ?, ?);
            """
            cursor.execute(sql, self._to_tuple())
            conn.commit()
            return True, "success"
        except IntegrityError:
            return False, f"{self._email} is already in use!"
        except Exception as e:
            return False, str(e)

    def _to_tuple(self) -> tuple[any]:
        return (self._first_name, self._last_name, self._username, self._encrypted_pw, self._email, self._salt)
    
    def get_name(self) -> tuple[str]:
        return (self._first_name, self._last_name)
    
    def get_uid(self) -> int:
        return self._uid
    
    def get_email(self) -> str:
        return self._email
    
    def get_username(self) -> str:
        return self._username

    # @staticmethod
    # def delete_user_by_api_key(api_key: string):
    #     sql = f"DELETE FROM {table_name} WHERE _api_key = (?)"
    #     cursor.execute(sql, (api_key,))
    #     conn.commit()

    @staticmethod
    def gen_salt() -> str:
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(10))

    @staticmethod
    def encrypt(pw: str, salt: str) -> str:
        encrypted_key = pw
        for i in range(6):
            encrypted_key = hashlib.sha256((salt + encrypted_key + pepper).encode('utf-8')).hexdigest()
        return encrypted_key
    
    # @staticmethod
    # def validate_api_key(key: str) -> bool:
    #     sql = f"SELECT uid FROM {table_name} WHERE api_key = (?);"
    #     encrypted_key = User.encrypt(key)
    #     result = cursor.execute(sql, (encrypted_key,)).fetchone()

    #     if (result != None):
    #         sql = f"UPDATE {table_name} SET call_count = call_count + 1 WHERE uid = (?)"
    #         cursor.execute(sql, result)
    #         conn.commit()
    #         return True
    #     else:
    #         return False

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
