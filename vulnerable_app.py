"""
vulnerable_app.py
CCT College Dublin — Week 5 Practical
DO NOT deploy this code. It is intentionally insecure.
"""

import sqlite3
import hashlib
import pickle
import bcrypt
from flask import Flask, request

app = Flask(__name__)
# ── FLAW 1: Hardcoded credentials (B105) ─────────────────
DB_PASSWORD = "admin123"
SECRET_KEY  = "hardcoded_secret_key_12345"


def get_user(username):
    """Look up a user — FLAW 2: SQL Injection (B608)"""
    conn   = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # BAD: string concatenation opens SQL injection
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))   # Note the tuple

    return cursor.fetchone()

def hash_password(password: str) -> bytes:
    """bcrypt handles salting automatically."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed)


def run_expression(user_input):
    """Evaluate input — FLAW 4: eval() injection (B307)"""
    return eval(user_input)


def load_session(data: bytes):
    """Load session — FLAW 5: insecure pickle (B301)"""
    return pickle.loads(data)


@app.route('/user')
def user():
    username = request.args.get('username', '')
    return str(get_user(username))

if __name__ == '__main__':
    app.run(debug=True)   # FLAW 1b: debug mode in production
