import uuid
import bcrypt
import sqlite3
import random
import string


# Password-specifikt
def hash_password(password):
    """Hash kodeord."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def check_password(password, hashed):
    """Check hashed kodeord"""
    return bcrypt.checkpw(password.encode(), hashed)


# Database hjælpefunktioner
def db_setup():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Opret brugere tabel
    c.execute(
        '''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL UNIQUE)''')
    # Opret licens tabel
    c.execute(
        '''CREATE TABLE IF NOT EXISTS licenses (id INTEGER PRIMARY KEY, license TEXT, user_id INTEGER UNIQUE)''')
    conn.commit()
    conn.close()


def get_user(username):
    """Få bruger fra database"""
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user


def add_user(username, password):
    """Tilføj bruger til database"""
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
              (username, hash_password(password)))
    conn.commit()
    conn.close()


def check_user(username, password):
    """Check om bruger eksisterer i database"""
    user = get_user(username)
    if user:
        return check_password(password, user[2])
    return False


def generate_license(username):
    """Generer licens for bruger"""
    user = get_user(username)

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Generer licens
    license_ = str(uuid.uuid4())

    # Tilføj licens til database
    c.execute("INSERT INTO licenses (license, user_id) VALUES (?, ?)",
              (license_, user[0]))

    conn.commit()
    conn.close()
    print(license_)
    return license_


def get_license(username):
    """Få licens for bruger"""
    user = get_user(username)

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM licenses WHERE user_id = ?", (user[0],))
    license_ = c.fetchone()
    conn.close()

    if not license_:
        license_ = generate_license(username)
    else:
        license_ = license_[1]

    return license_
