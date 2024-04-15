import mysql.connector
from mysql.connector import Error


a = {"login":"admin", "password":"admin"}


def authatification(login, password):
    if login == a["login"] and password == a["password"]:
        return True
    else:
        return False