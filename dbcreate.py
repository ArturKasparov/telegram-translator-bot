import sqlite3

def create_db():
    connection = sqlite3.connect('tasks.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            done BOOLEAN NOT NULL CHECK (done IN (0, 1)) DEFAULT 0
        )
    ''')
    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_db()