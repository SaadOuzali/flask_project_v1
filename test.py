from mysql.connector import Error
from db import MysqlConnector
from helpers import db_config

try:
    connector = MysqlConnector(**db_config)
    conn = connector.connection()

    print("Before:", conn.is_connected())

    if conn.is_connected():
        print("Connected!")
        cursor = conn.cursor()
        cursor.execute("SELECT NOW()")
        print("DB time:", cursor.fetchone())

    print("After:", conn.is_connected())

except Error as e:
    print("Error:", e)



