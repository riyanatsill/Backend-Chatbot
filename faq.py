from db import get_db_connection
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_all_faqs():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM faq_final ORDER BY id DESC")
    result = cursor.fetchall()
    conn.close()
    return result

def add_faq(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO faq_final (question, answer, category)
        VALUES (%s, %s, %s)
    """, (data['question'], data['answer'], data['category']))
    conn.commit()
    conn.close()
    return {'message': 'FAQ berhasil ditambahkan'}

def update_faq(faq_id, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE faq_final
        SET question=%s, answer=%s, category=%s
        WHERE id=%s
    """, (data['question'], data['answer'], data['category'], faq_id))
    conn.commit()
    conn.close()
    return {'message': 'FAQ berhasil diperbarui'}

def delete_faq(faq_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM faq_final WHERE id=%s", (faq_id,))
    conn.commit()
    conn.close()
    return {'message': 'FAQ berhasil dihapus'}

# === SUGGESTION ===

def get_suggestions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM faq_suggestions WHERE status = 'pending'")
    suggestions = cursor.fetchall()

    for s in suggestions:
        cursor.execute("SELECT question FROM faq_suggestion_variants WHERE suggestion_id = %s", (s["id"],))
        variants = cursor.fetchall()
        s["variations"] = [v["question"] for v in variants]

    conn.close()
    return suggestions


def accept_suggestion(suggestion_id, data):
    answer = data.get("answer")
    if not answer:
        return {"error": "Jawaban wajib diisi."}, 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil main_question dan kategori
    cursor.execute("SELECT main_question, category FROM faq_suggestions WHERE id = %s", (suggestion_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return {"error": "Suggestion tidak ditemukan."}, 404

    question = row["main_question"]
    category = row["category"]

    # Masukkan ke Final FAQ
    cursor.execute(
        "INSERT INTO faq_final (question, answer, category) VALUES (%s, %s, %s)",
        (question, answer, category)
    )

    # Update status dan isi jawaban di suggestion
    cursor.execute(
        "UPDATE faq_suggestions SET status = 'accepted', answer = %s WHERE id = %s",
        (answer, suggestion_id)
    )

    # Tandai semua pertanyaan terkait sebagai finalized
    cursor.execute(
        "SELECT question FROM faq_suggestion_variants WHERE suggestion_id = %s",
        (suggestion_id,)
    )
    variants = cursor.fetchall()

    for v in variants:
        cursor.execute(
            "UPDATE user_questions SET finalized = TRUE WHERE question = %s",
            (v["question"],)
        )

    # Juga tandai main_question
    cursor.execute(
        "UPDATE user_questions SET finalized = TRUE WHERE question = %s",
        (question,)
    )

    conn.commit()
    conn.close()
    return {"message": "FAQ Suggestion berhasil dipindahkan ke Final FAQ"}

def classify_question(text):
    text = text.lower()
    if any(keyword in text for keyword in ['kapan', 'tanggal', 'jadwal', 'mulai']):
        return 'Jadwal'
    if any(keyword in text for keyword in ['biaya', 'bayar', 'uang']):
        return 'Biaya'
    if any(keyword in text for keyword in ['syarat', 'persyaratan']):
        return 'Syarat'
    if any(keyword in text for keyword in ['jalur', 'snbp', 'snbt', 'mandiri']):
        return 'Jalur'
    return 'Umum'

def generate_suggestions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Bersihkan data lama
    cursor.execute("DELETE FROM faq_suggestion_variants")
    cursor.execute("DELETE FROM faq_suggestions")
    conn.commit()

    # Ambil pertanyaan yang belum difinalkan
    cursor.execute("SELECT id, question FROM user_questions WHERE finalized = FALSE")
    rows = cursor.fetchall()
    questions = [row["question"] for row in rows]
    ids = [row["id"] for row in rows]

    if len(questions) < 2:
        return {"message": "Tidak cukup pertanyaan untuk clustering."}

    vectorizer = TfidfVectorizer().fit_transform(questions)
    similarity_matrix = cosine_similarity(vectorizer)

    threshold = 0.6
    used_indexes = set()
    count = 0

    for i in range(len(questions)):
        if i in used_indexes:
            continue

        group = [i]
        for j in range(i + 1, len(questions)):
            if j not in used_indexes and similarity_matrix[i][j] > threshold:
                group.append(j)

        if len(group) > 1:
            main_q = questions[i]
            category = classify_question(main_q)

            cursor.execute(
                "INSERT INTO faq_suggestions (main_question, category, status) VALUES (%s, %s, %s)",
                (main_q, category, 'pending')
            )
            conn.commit()
            suggestion_id = cursor.lastrowid

            for idx in group:
                cursor.execute(
                    "INSERT INTO faq_suggestion_variants (suggestion_id, question, similarity_score) VALUES (%s, %s, %s)",
                    (suggestion_id, questions[idx], float(similarity_matrix[i][idx]))
                )
                used_indexes.add(idx)

            count += 1

    conn.commit()
    conn.close()
    return {"message": f"{count} saran FAQ berhasil dibuat."}

# === HISTORY ===

def get_all_questions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, question, answer FROM user_questions ORDER BY id DESC")
    result = cursor.fetchall()
    conn.close()
    return result