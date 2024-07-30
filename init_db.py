import sqlite3

DATABASE = 'database.db'

def init_db():
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  
  # Create users table
  cursor.execute('''
  CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT NOT NULL,
      password TEXT NOT NULL
  )
  ''')
  
  # Create notes table
  cursor.execute('''
  CREATE TABLE IF NOT EXISTS notes (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      note_id TEXT NOT NULL,
      content TEXT NOT NULL,
      user_id INTEGER,
      FOREIGN KEY (user_id) REFERENCES users (id)
  )
  ''')
  
  conn.commit()
  conn.close()

if __name__ == '__main__':
  init_db()
  print("Database initialized and tables created.")