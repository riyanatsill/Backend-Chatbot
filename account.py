import bcrypt
from flask import request, jsonify
import jwt
import datetime
import os
from extensions import mail
from flask_mail import Message
from db import get_db_connection

SECRET_KEY = os.getenv("SECRET_KEY")
RESET_SECRET_KEY = os.getenv("RESET_SECRET_KEY", "reset-secret")

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

    if not user:
        return {'error': 'Username atau password salah'}, 401

    # ❌ Cek dulu kalau sudah diblokir
    if user.get("is_blocked"):
        return {'error': 'Akun ini terblokir. Silakan reset password melalui email.'}, 403

    # ❌ Cek password
    if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        new_failed = user.get("failed_attempts", 0) + 1
        is_blocked = new_failed >= 3

        # Update failed_attempts dan is_blocked
        cursor.execute(
            "UPDATE users SET failed_attempts = %s, is_blocked = %s WHERE id = %s",
            (new_failed, is_blocked, user['id'])
        )
        conn.commit()

        if is_blocked:
            if not user.get("reset_token"):
                # Generate token reset password
                reset_token = generate_reset_token(user['email'])
                reset_link = f"https://pmb-productions.vercel.app/reset-password?token={reset_token}"

                # Simpan reset_token di DB
                cursor.execute("UPDATE users SET reset_token = %s WHERE id = %s", (reset_token, user['id']))
                conn.commit()

                # Kirim email reset password
                send_reset_email(user['email'], reset_link)

            return {'error': 'Akun ini terblokir. Link reset sudah dikirim ke email.'}, 403

        return {'error': 'Username atau password salah'}, 401

    # ✅ Password benar: reset failed_attempts
    cursor.execute("UPDATE users SET failed_attempts = 0 WHERE id = %s", (user['id'],))
    conn.commit()
    cursor.close()
    conn.close()

    # ✅ Login token (biasa)
    token = jwt.encode(
        {"id": user['id'], "username": user['username'], "email": user['email'], "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)},
        os.getenv("SECRET_KEY", "secret"),
        algorithm="HS256"
    )
    return {'token': token}, 200



def get_current_user_handler():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return {'error': 'Unauthorized'}, 401

    token = auth.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {
            "id": payload["id"],
            "username": payload["username"],
            "email": payload["email"]
        }, 200
    except jwt.ExpiredSignatureError:
        return {'error': 'Token expired'}, 401
    except jwt.DecodeError:
        return {'error': 'Token tidak valid'}, 401


def logout_handler():
    # Untuk JWT, logout bersifat client-side (hapus token dari localStorage)
    return {'message': 'Logout berhasil (hapus token di sisi frontend)'}, 200


def get_users_handler():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, email, created_at, is_blocked FROM users ORDER BY id ASC")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users


def create_user_handler():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return {'error': 'Semua field wajib diisi'}, 400

    # Hash password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Cek apakah username atau email sudah terdaftar
    cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return {'error': 'Username atau email sudah terdaftar'}, 409

    # Tambahkan user baru dengan kolom tambahan is_blocked dan failed_attempts
    cursor.execute("""
        INSERT INTO users (username, email, password, failed_attempts, is_blocked)
        VALUES (%s, %s, %s, %s, %s)
    """, (username, email, hashed, 0, False))

    conn.commit()
    cursor.close()
    conn.close()
    return {'message': 'Admin berhasil ditambahkan'}, 201



def delete_user_handler(user_id):
    # Ambil token dari header
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return {'error': 'Unauthorized'}, 401

    token = auth_header.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {'error': 'Token expired'}, 401
    except jwt.DecodeError:
        return {'error': 'Invalid token'}, 401

    # Cegah user menghapus dirinya sendiri
    if payload["id"] == user_id:
        return {'error': 'Tidak dapat menghapus akun sendiri'}, 403

    # Lanjutkan penghapusan
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return {'message': 'Admin berhasil dihapus'}, 200

def generate_reset_token(user_email):
    payload = {
        'email': user_email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    return jwt.encode(payload, RESET_SECRET_KEY, algorithm="HS256")


def send_reset_email(to_email, reset_link):
    msg = Message('Reset Password Akun Anda',
                  sender=os.getenv('MAIL_USERNAME'),
                  recipients=[to_email])
    msg.body = f"""
    Hai,

    Akun Anda telah diblokir karena terlalu banyak percobaan login yang gagal.
    Silakan reset password Anda melalui link berikut (berlaku 30 menit):

    {reset_link}

    Terima kasih.
    """
    mail.send(msg)
    print(f"✅ Email reset password berhasil dikirim ke {to_email}")



def reset_password_handler():
    # Ambil token dari header Authorization
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return {'error': 'Unauthorized'}, 401

    token = auth_header.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {'error': 'Token expired'}, 401
    except jwt.DecodeError:
        return {'error': 'Invalid token'}, 401

    # Ambil password baru dari body
    data = request.get_json()
    new_password = data.get('password')
    if not new_password:
        return {'error': 'Password tidak boleh kosong'}, 400

    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Update password ke database berdasarkan ID dari token
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed, payload['id']))
    conn.commit()
    cursor.close()
    conn.close()

    return {'message': 'Password berhasil diubah'}, 200

def reset_password_email_handler():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('password')

    if not token or not new_password:
        return {'error': 'Token dan password baru wajib diisi'}, 400

    try:
        payload = jwt.decode(token, RESET_SECRET_KEY, algorithms=["HS256"])
        email = payload.get('email')
    except jwt.ExpiredSignatureError:
        return {'error': 'Link reset sudah expired.'}, 400
    except jwt.DecodeError:
        return {'error': 'Link reset tidak valid.'}, 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if not user:
        return {'error': 'User tidak ditemukan.'}, 404

    # Cek token di DB
    if user.get('reset_token') != token:
        return {'error': 'Token sudah tidak berlaku atau sudah digunakan.'}, 400

    # Reset password dan hapus reset_token
    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cursor.execute("UPDATE users SET password = %s, failed_attempts = 0, is_blocked = 0, reset_token = NULL WHERE id = %s", (hashed, user['id']))
    conn.commit()
    cursor.close()
    conn.close()

    return {'message': 'Password berhasil direset. Silakan login kembali.'}, 200
