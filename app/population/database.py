from flask import g
import sqlite3
import os.path

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# db_path = os.path.join(BASE_DIR, "PupilPremiumTable.db")
# with sqlite3.connect(db_path) as db:

def connect_db_popu():
    #print("==>app/population/database.py::connect_db_popu enter")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "NSW_POPULATION.sqlite")
    sql = sqlite3.connect(db_path)
    #sql = sqlite3.connect('NSW_POPULATION.sqlite')
    #print ("Opened database successfully")
    print("==>app/population/database.py::connect_db")
    print(db_path)
    sql.row_factory = sqlite3.Row
    return sql

def get_db_popu():
    #print("==>app/population/database.py::get_db_popu enter")
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db_popu()
    return g.sqlite_db
