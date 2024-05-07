import bcrypt

# Хеш пароля из базы данных
stored_hash = "$2y$10$6Kw5sqPoMTGSMKVgo63pyuafDcwHxAKZLT6RVGAOLGQjVeme2JyHe"

# Пароль, который пользователь вводит для аутентификации
entered_password = "admin"

# Проверка соответствия введенного пароля хешу из базы данных
if bcrypt.checkpw(entered_password.encode('utf-8'), stored_hash.encode('utf-8')):
    print("Пароль верный. Аутентификация успешна.")
else:
    print("Неверный пароль. Аутентификация не удалась.")
