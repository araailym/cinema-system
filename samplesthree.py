import sqlite3
import hashlib

conn = sqlite3.connect("ticketsdata.db")
cur=conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS ticketsdata (
    id INTEGER NOT NULL PRIMARY KEY,
    movie_id INTEGER NOT NULL ,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES moviesdata(movie_id),
    FOREIGN KEY (user_id) REFERENCES userdata(user_id)
    UNIQUE(movie_id, user_id)
)
""")

mid1, uid1=1, 1
mid2, uid2=1, 2
mid3, uid3=2, 2
cur.execute("INSERT INTO ticketsdata (movie_id, user_id) VALUES(?,?)",(mid1, uid1))
cur.execute("INSERT INTO ticketsdata (movie_id, user_id) VALUES(?,?)",(mid2, uid2))
cur.execute("INSERT INTO ticketsdata (movie_id, user_id) VALUES(?,?)",(mid3, uid3))


conn.commit()