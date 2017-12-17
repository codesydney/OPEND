from flask import g
import sqlite3
import os.path


def connect_db_birth():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "NSW_BIRTH_RATE.sqlite")
    sql = sqlite3.connect(db_path)
    #sql = sqlite3.connect('NSW_BIRTH_RATE.sqlite')
    sql.row_factory = sqlite3.Row
    return sql

def get_db_birth():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db_birth()
    return g.sqlite_db
