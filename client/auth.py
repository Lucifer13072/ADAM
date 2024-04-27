import bcrypt

def authentication(login, password):
    
    if login == "admin" and password == "admin":
        return True
    
    else:    
        return False


def is_key_true(key):
    if key == "adam-kYS0yWXZ8cwRasUBqQJF":
        return True
    else: 
        False