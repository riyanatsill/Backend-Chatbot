from flask import request
from db import get_db_connection
import joblib


model = joblib.load("faq_classifier.joblib")

def classify_question(text):
    if model:
        return model.predict([text])[0]
    return "Umum"



def submit_question_handler():
    data = request.get_json()
    question = data.get('question')
    answer = data.get('answer')

    if not question:
        return {'error': 'Pertanyaan wajib diisi'}, 400
    category = classify_question(question)

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO history (question, answer, category)
            VALUES (%s, %s, %s)
        """, (question, answer, category))
        conn.commit()
        return {'message': 'Pertanyaan berhasil disimpan'}
    except Exception as e:
        print("❌ Gagal simpan pertanyaan:", e)
        conn.rollback()
        return {'error': 'Gagal menyimpan ke database'}, 500
    finally:
        cursor.close()
        conn.close()
