import os
import sqlite3 as sql

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sql.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Do we need to seed this database?
        self.cursor.execute('SELECT name FROM sqlite_master WHERE type=\'table\';')
        tables = self.cursor.fetchall()
        if len(tables) == 0:
            self.seed()

    def seed(self):
        file = os.open('database.sql', os.O_RDONLY)
        
        with open(file, 'r') as f:
            self.cursor.executescript(f.read())
            self.conn.commit()
        
        os.close(file)

    def query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_aggregate_rat_count(self):
        query = 'SELECT SUM(count) FROM rats;'
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    def get_aggregate_rat_count_by_server(self, server_id):
        query = f'SELECT SUM(count) FROM rats WHERE server_id = \'{server_id}\';'
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    def get_rat_count_for_user(self, user_id, server_id):
        query = f'SELECT SUM(count) FROM rats WHERE user_id = \'{user_id}\' AND server_id = \'{server_id}\';'
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    def upsert_rat_count(self, user_id, server_id, count):
        query = f'INSERT OR REPLACE INTO rats (user_id, server_id, count) VALUES (\'{user_id}\', \'{server_id}\', {count});'
        self.cursor.execute(query)
        self.conn.commit()
    
    def __del__(self):
        self.conn.close()
