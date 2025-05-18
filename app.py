# === app.py ===
from flask import Flask, request, jsonify
from flask_session import Session
from flask_cors import CORS
from dotenv import load_dotenv
from faq import get_all_faqs, add_faq, update_faq, delete_faq, get_suggestions, accept_suggestion, get_all_questions, generate_suggestions
from account import login_handler, logout_handler, get_current_user_handler,get_users_handler, create_user_handler,update_user_handler, delete_user_handler,reset_password_handler
from user import submit_question_handler
import os

from db import get_db_connection
from datetime import datetime

load_dotenv()
# === SETUP ===
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
CORS(app, supports_credentials=True)


# === ACCOUNT ===
@app.route('/login', methods=['POST'])
def login_route():
    return login_handler()

@app.route('/me', methods=['GET'])
def get_current_user_route():
    return get_current_user_handler()

@app.route('/logout', methods=['GET'])
def logout_route():
    return logout_handler()

@app.route('/users', methods=['GET'])
def get_users_route():
    return get_users_handler()

@app.route('/users', methods=['POST'])
def create_user_route():
    return create_user_handler()

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user_route(user_id):
    result = update_user_handler(user_id)
    return update_user_handler(user_id)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    return delete_user_handler(user_id)

@app.route('/users/reset-password', methods=['PUT'])
def reset_password_route():
    return reset_password_handler()

# === USER ===
@app.route('/submit-question', methods=['POST'])
def submit_question_route():
    result = submit_question_handler()
    return jsonify(result)


# === Final FAQ ===
@app.route('/faq', methods=['GET'])
def list_faqs():
    return jsonify(get_all_faqs())

@app.route('/faq', methods=['POST'])
def create_faq():
    data = request.json
    return jsonify(add_faq(data))

@app.route('/faq/<int:faq_id>', methods=['PUT'])
def update_faq_route(faq_id):
    data = request.json
    return jsonify(update_faq(faq_id, data))

@app.route('/faq/<int:faq_id>', methods=['DELETE'])
def delete_faq_route(faq_id):
    return jsonify(delete_faq(faq_id))


# === FAQ Suggestion ===
@app.route('/faq-suggestions', methods=['GET'])
def list_suggestions():
    return jsonify(get_suggestions())

@app.route('/faq-suggestions/<int:suggestion_id>/accept', methods=['POST'])
def accept_suggestion_route(suggestion_id):
    data = request.json
    return jsonify(accept_suggestion(suggestion_id, data))

@app.route('/faq-suggestions/generate', methods=['POST'])
def generate_faq_suggestions_route():
    result = generate_suggestions()
    return jsonify(result)


# === Riwayat Pertanyaan User ===
@app.route('/user-questions', methods=['GET'])
def list_questions():
    return jsonify(get_all_questions())


# === Dashboard ===
@app.route("/dashboard-stats", methods=["GET"])
def dashboard_stats():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Total pertanyaan hari ini
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM user_questions
        WHERE DATE(created_at) = %s
    """, (today,))
    total_questions_today = cursor.fetchone()['total'] or 0

    # 2. Jumlah file base knowledge
    cursor.execute("SELECT COUNT(*) AS total FROM uploaded_files")
    total_files_uploaded = cursor.fetchone()['total'] or 0

    # 3. Jumlah QA yang terindeks ke FAISS (dari MySQL)
    cursor.execute("SELECT COUNT(*) AS total FROM qa_data")
    total_qa_indexed = cursor.fetchone()['total'] or 0

    # 4. Grafik: jumlah pertanyaan per hari (7 hari terakhir)
    cursor.execute("""
        SELECT DATE_FORMAT(created_at, '%%Y-%%m-%%d') AS tanggal, COUNT(*) AS jumlah
        FROM user_questions
        WHERE created_at >= CURDATE() - INTERVAL 7 DAY
        GROUP BY DATE_FORMAT(created_at, '%%Y-%%m-%%d')
        ORDER BY tanggal ASC
    """)
    questions_per_day = cursor.fetchall()

    # 5. Grafik: kategori pertanyaan terbanyak
    cursor.execute("""
        SELECT category, COUNT(*) AS value
        FROM faq_final
        WHERE category IS NOT NULL
        GROUP BY category
        ORDER BY value DESC
        LIMIT 5
    """)
    top_categories = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({
        "total_questions_today": total_questions_today,
        "total_files_uploaded": total_files_uploaded,
        "total_qa_indexed": total_qa_indexed,
        "questions_per_day": questions_per_day,
        "top_categories": top_categories
    })



# === MAIN ===
if __name__ == "__main__":
    app.run(debug=True, port=5000)
