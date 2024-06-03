import bcrypt
import requests
import json

def authenticate_user(username, password):
    url = 'https://atgex.ru/script/php/API.php'
    data = {
        'usr': username,
        'paswd': password
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # Проверка на HTTP ошибки
        
        if response.text.strip() == "true":
            return True
        else:
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False  # Возвращаем False в случае ошибки запроса


def is_key_valid(login, uuid):
    pass
