import sqlite3

class DBclass:
    def __init__(self, database_file):

        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def create_user(self, chat_id):
        with self.connection:
            self.cursor.execute('INSERT INTO user (chat_id) VALUES (?)', (chat_id,))
