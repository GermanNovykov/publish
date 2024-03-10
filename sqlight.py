import sqlite3

class DBclass:
    def __init__(self, database_file):

        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def create_user(self, chat_id, name):
        with self.connection:
            self.cursor.execute('SELECT * FROM user WHERE chat_id = ?', (chat_id,))
            if self.cursor.fetchone() is None:
                self.cursor.execute('INSERT INTO user (chat_id, name, isSubscribed, isAdmin) VALUES (?, ?, TRUE, FALSE)', (chat_id, name,))
            else:
                pass
    def get_user(self, chat_id):
        with self.connection:
            return list(self.cursor.execute('SELECT * FROM user WHERE chat_id = ?', (chat_id,)))[0]
    def get_all_subscribers(self):
        with self.connection:
            return list(self.cursor.execute('SELECT * FROM user WHERE isSubscribed = 1'),)