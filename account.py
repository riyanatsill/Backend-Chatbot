import bcrypt
from flask import request, session
from db import get_db_connection

def login_handler():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return {'error': 'Username dan password wajib diisi'}, 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return {'error': 'Username atau password salah'}, 401

    session['user'] = {
        'id': user['id'],
        'username': user['username'],
        'email': user['email'],
        'role': user['role']
    }

    return {'message': 'Login berhasil', 'role': user['role']}, 200  # tambahkan status 200 eksplisit


def get_current_user_handler():
    user = session.get('user')
    if not user:
        return {'error': 'Unauthorized'}, 401
    return user


def logout_handler():
    session.pop('user', None)
    return {'message': 'Logout berhasil'}


def get_users_handler():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, email, role, created_at FROM users ORDER BY id ASC")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users


def create_user_handler():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'admin')

    if not username or not email or not password:
        return {'error': 'Semua field wajib diisi'}, 400

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
    if cursor.fetchone():
        return {'error': 'Username atau email sudah terdaftar'}, 409

    cursor.execute("INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
                   (username, email, hashed, role))
    conn.commit()
    cursor.close()
    conn.close()
    return {'message': 'Admin berhasil ditambahkan'}


def update_user_handler(user_id):
    data = request.get_json()
    role = data.get('role')

    if role not in ['admin', 'superadmin']:
        return {'error': 'Role tidak valid'}, 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role = %s WHERE id = %s", (role, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {'message': 'Role berhasil diperbarui'}


def delete_user_handler(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {'message': 'Admin berhasil dihapus'}


def reset_password_handler():
    user = session.get('user')
    if not user:
        return {'error': 'Unauthorized'}, 401

    data = request.get_json()
    new_password = data.get('password')
    if not new_password:
        return {'error': 'Password tidak boleh kosong'}, 400

    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed, user['id']))
    conn.commit()
    cursor.close()
    conn.close()

    return {'message': 'Password berhasil diubah'}
