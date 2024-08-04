import sqlite3
import hashlib

conn = sqlite3.connect("userdata.db")
cur=conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS userdata (
    id INTEGER NOT NULL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    UNIQUE(username)
)
""")

username1, password1 = "admin", hashlib.sha256("1111".encode()).hexdigest()
username2, password2 = "arailym", hashlib.sha256("qwerty123".encode()).hexdigest()
username3, password3 = "jane123", hashlib.sha256("janepass".encode()).hexdigest()

cur.execute("INSERT INTO userdata (username, password) VALUES(?,?)",(username1,password1))
cur.execute("INSERT INTO userdata (username, password) VALUES(?,?)",(username2,password2))
cur.execute("INSERT INTO userdata (username, password) VALUES(?,?)",(username3,password3))


conn.commit()