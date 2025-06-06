import sqlite3
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY,
                      username TEXT UNIQUE NOT NULL,
                      password_hash TEXT NOT NULL)''')

def create_user(username, password):
    try:
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        with sqlite3.connect('database.db') as conn:
            conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                        (username, hashed))
        return True
    except sqlite3.IntegrityError:
        return False

def verify_user(username, password):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
    return result and bcrypt.check_password_hash(result[0], password)