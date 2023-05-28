import sqlite3


class Cards:
    def __init__(self):
        self.conn = sqlite3.connect('cards.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY,
                readout TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time TIMESTAMP,
                readout TEXT
            )
        ''')

    def close(self):
        self.cursor.close()
        self.conn.close()

    def insert(self, siid: int, readout: str):
        self.cursor.execute("INSERT OR REPLACE INTO cards VALUES (?, ?)", [siid, readout])
        self.cursor.execute("INSERT INTO uploads (time, readout) VALUES (datetime('now'), ?)", [readout])
        self.conn.commit()

    def read(self):
        self.cursor.execute('SELECT * FROM cards')
        cards = self.cursor.fetchall()
        return cards
