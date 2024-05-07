import mysql
import mysql.connector
from mysql.connector import Error
import bcrypt


# Функция для подключения к базе данных MySQL
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            database='atgex',
            user='root',
            password=''
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Ошибка при подключении к базе данных:", e)
        return None

# Функция для аутентификации пользователя
def authenticate_user(login, password):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT paswd FROM user_list WHERE usr = %s", (login,))
            record = cursor.fetchone()
            if record:
                hashed_password = record[0] # Преобразование строки в байтовую строки
                if bcrypt.checkpw(password.encode('utf-8'), str(hashed_password).encode('utf-8')):
                    return True
        except Error as e:
            print("Ошибка при выполнении запроса:", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return False



def is_key_valid(login, uuid):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT have_key FROM user_list WHERE usr = %s AND uuid = %s", (login, uuid,))
            record = cursor.fetchone()
            if record:
                have_key = record[0]
                if have_key == 1:
                    return True
        except Error as e:
            print("Ошибка при выполнении запроса:", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return False

