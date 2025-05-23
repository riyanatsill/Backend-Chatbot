from db import get_db_connection
from flask import request

def get_all_faqs():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM faq ORDER BY id DESC")
    result = cursor.fetchall()
    conn.close()
    return result

def add_faq(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO faq (question, answer, category)
        VALUES (%s, %s, %s)
    """, (data['question'], data['answer'], data['category']))
    conn.commit()
    conn.close()
    return {'message': 'FAQ berhasil ditambahkan'}

def update_faq(faq_id, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE faq
        SET question=%s, answer=%s, category=%s
        WHERE id=%s
    """, (data['question'], data['answer'], data['category'], faq_id))
    conn.commit()
    conn.close()
    return {'message': 'FAQ berhasil diperbarui'}

def delete_faq(faq_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM faq WHERE id=%s", (faq_id,))
    conn.commit()
    conn.close()
    return {'message': 'FAQ berhasil dihapus'}


# === HISTORY ===

def get_all_questions():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    offset = (page - 1) * limit
    category = request.args.get("category")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if category and category.lower() != "semua":
        cursor.execute("SELECT COUNT(*) AS total FROM history WHERE category = %s", (category,))
        total = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT id, question, answer, category
            FROM history
            WHERE category = %s
            ORDER BY id ASC
            LIMIT %s OFFSET %s
        """, (category, limit, offset))
    else:
        cursor.execute("SELECT COUNT(*) AS total FROM history")
        total = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT id, question, answer, category
            FROM history
            ORDER BY id ASC
            LIMIT %s OFFSET %s
        """, (limit, offset))

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return {
        "questions": results,
        "total": total,
        "page": page,
        "limit": limit
    }