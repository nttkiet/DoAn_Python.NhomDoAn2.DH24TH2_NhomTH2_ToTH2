#db.py

import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",   # thay bằng mật khẩu MySQL của bạn
        database="qlnhansu"
    )


