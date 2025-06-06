import sqlite3

def retrieve_all_users():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        for row in rows:
            print('ID:', row[0])
            print('Username:', row[1])
            print('Password Hash:', row[2])
            print('------------------------')

retrieve_all_users()