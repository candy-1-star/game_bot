import sqlite3


class Database:
    def __init__(self, db_name='data_users.db'):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

    def creating_table(self):
        self.cur.execute('''
CREATE TABLE IF NOT EXISTS Users (
ids INTEGER PRIMARY KEY,
many INTEGER NOT NULL,
common INTEGER NOT NULL,
rare INTEGER NOT NULL, 
epic INTEGER NOT NULL
)
''')
        self.con.commit()


class Database1:
    def __init__(self, db_name1='data_promo.db'):
        self.con1 = sqlite3.connect(db_name1)
        self.cur1 = self.con1.cursor()

    def creating_table1(self):
        self.cur1.execute('''
CREATE TABLE IF NOT EXISTS Promo (
id_us INTEGER PRIMARY KEY,
promo1 INTEGER NOT NULL,
promo2 INTEGER NOT NULL, 
promo3 INTEGER NOT NULL
)
''')
        self.con1.commit()
