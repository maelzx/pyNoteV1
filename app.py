from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
import os
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATABASE = 'database.db'

def get_db():
  db = getattr(g, '_database', None)
  if db is None:
      db = g._database = sqlite3.connect(DATABASE)
  return db

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
      db.close()

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      db = get_db()
      db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
      db.commit()
      return redirect(url_for('login'))
  return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      db = get_db()
      user = db.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
      if user:
          session['user_id'] = user[0]
          return redirect(url_for('index'))
  return render_template('login.html')

@app.route('/create_note', methods=['GET', 'POST'])
def create_note():
  if request.method == 'POST':
      content = request.form['content']
      note_id = str(uuid.uuid4())
      user_id = session.get('user_id')
      db = get_db()
      db.execute('INSERT INTO notes (note_id, content, user_id) VALUES (?, ?, ?)', (note_id, content, user_id))
      db.commit()
      return redirect(url_for('view_note', note_id=note_id))
  return render_template('create_note.html')

@app.route('/note/<note_id>')
def view_note(note_id):
  db = get_db()
  note = db.execute('SELECT * FROM notes WHERE note_id = ?', (note_id,)).fetchone()
  return render_template('view_note.html', note=note)

@app.route('/my_notes')
def my_notes():
  user_id = session.get('user_id')
  if not user_id:
      return redirect(url_for('login'))
  
  db = get_db()
  notes = db.execute('SELECT * FROM notes WHERE user_id = ?', (user_id,)).fetchall()
  return render_template('my_notes.html', notes=notes)

if __name__ == '__main__':
  app.run(debug=True)