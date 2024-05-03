import mysql
import mysql.connector
import bcrypt


# Функция для подключения к базе данных MySQL
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            database='adam_project_keys',
            user='admin',
            password='Tytyber13112007'
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
                hashed_password = record[0].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    return True
        except Error as e:
            print("Ошибка при выполнении запроса:", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return False

def is_key_valid(uuid):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT have_key FROM user_list WHERE uuid = %s", (uuid,))
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


connect_to_database()

# def main():
#     login = "admin"
#     password = "admin"
#     key = "adam-k1mbdHE5zqSaVNZpIJ9u"

#     if authenticate_user(login, password):
#         print("Пользователь аутентифицирован успешно.")
#     else:
#         print("Ошибка аутентификации пользователя.")

#     if is_key_valid(key):
#         print("Ключ действителен.")
#     else:
#         print("Недействительный ключ.")

# if __name__ == "__main__":
#     main()

