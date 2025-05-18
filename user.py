from flask import request
from db import get_db_connection


def submit_question_handler():
    data = request.get_json()
    question = data.get('question')
    answer = data.get('answer')

    if not question:
        return {'error': 'Pertanyaan wajib diisi'}, 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO user_questions (question, answer, finalized)
            VALUES (%s, %s, %s)
        """, (question, answer, 0))  # finalized = 0 by default
        conn.commit()
        return {'message': 'Pertanyaan berhasil disimpan'}
    except Exception as e:
        print("❌ Gagal simpan pertanyaan:", e)
        conn.rollback()
        return {'error': 'Gagal menyimpan ke database'}, 500
    finally:
        cursor.close()
        conn.close()
