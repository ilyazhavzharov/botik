import sqlite3

conn = sqlite3.connect('registration_codes.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users
               (user_id INTEGER PRIMARY KEY, code TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS codes
               (code TEXT PRIMARY KEY)''')

def add_code(code):
    cursor.execute('INSERT OR IGNORE INTO codes (code) VALUES (?)', (code,))
    conn.commit()

def is_code_valid(code):
    cursor.execute('SELECT code FROM codes WHERE code = ?', (code,))
    return cursor.fetchone() is not None


def add_user(user_id, code):
    cursor.execute('INSERT OR REPLACE INTO users (user_id, code) VALUES (?, ?)', (user_id, code))
    conn.commit()

def check_user_code(user_id):
    cursor.execute('SELECT code FROM users WHERE user_id = ?', (user_id,))
    data = cursor.fetchone()
    return data[0] if data else None


