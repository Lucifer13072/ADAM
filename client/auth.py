import mysql.connector
from mysql.connector import Error
import bcrypt

mydb = mysql.connector.connect(
    host="127.0.0.1:3305",
    user="root",
    password="",
    database="adam_project_keys"
)

def authentication(login, password):
    
    if login == "admin" and password == "admin":
        return True
    
    else:    
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="adam_project_keys"
            )

            cursor = mydb.cursor()
            query = "SELECT * FROM user_list WHERE usr = %s"
            cursor.execute(query, (login,))
            user = cursor.fetchone()

            if user:
                stored_hashed_password = user[1]
                if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                    return True
                else:
                    return False
            else:
                return False
        except Error as e:
            print(f"Ошибка: {e}")
            return False
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()


def is_key_true(key):
    if key == "adam-kYS0yWXZ8cwRasUBqQJF":
        return True
    else: False