import sqlite3

def connect_db():
    return sqlite3.connect('DATABASE.db')

atd = connect_db()
atd.execute('DROP TABLE IF EXISTS ACCOUNTS')
atd.execute('CREATE TABLE ACCOUNTS(Username TEXT NOT NULL, Password TEXT NOT NULL, Email TEXT NOT NULL, Mobile_number TEXT NOT NULL)')
atd.commit()
atd.close()