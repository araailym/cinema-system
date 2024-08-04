import sqlite3
import hashlib

conn = sqlite3.connect("moviesdata.db")
cur=conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS moviesdata (
    id INTEGER NOT NULL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    year INTEGER NOT NULL,
    UNIQUE(title, year)
)
""")

title1, year1="Inception", 2010
title2, year2="Pulp Fiction", 1994
title3, year3="Forrest Gump", 1994
cur.execute("INSERT INTO moviesdata (title, year) VALUES(?,?)",(title1,year1))
cur.execute("INSERT INTO moviesdata (title, year) VALUES(?,?)",(title2,year2))
cur.execute("INSERT INTO moviesdata (title, year) VALUES(?,?)",(title3,year3))


conn.commit()