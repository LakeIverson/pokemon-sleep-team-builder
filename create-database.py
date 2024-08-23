import sys
import os
import sqlite3

DB_FILE = "sleep.db"

def create():
    print('Deleting {0} if it exists.'.format(DB_FILE))
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    print('Creating {0} and turning foreign_keys on.'.format(DB_FILE))
    con = sqlite3.connect(DB_FILE)
    con.execute("PRAGMA foreign_keys = ON")
    con.close()
    database_file = open("database.schema", "r")
    creating = True
    print('Creating tables:\n')
    while(creating):
        query = ""
        generating_query = True
        while(generating_query):
            line = database_file.readline()
            if line == "":
                creating = False
                break
            query += line
            if ';' in line:
                generating_query = False
        if not creating:
            break
        con = sqlite3.connect(DB_FILE)
        print(query)
        con.execute(query)
        con.close()
    database_file.close()
    con.close()
    return

create()
