import sqlite3
from contextlib import closing

DATABASE = '/tmp/lmt.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def init_db():
    with closing(connect_db()) as db:
        with open('schema.sql', 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()

#init_db()
