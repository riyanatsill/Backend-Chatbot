# === app.py ===
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
from dotenv import load_dotenv
from faq import get_all_faqs, add_faq, update_faq, delete_faq, get_all_questions
from account import login_handler, logout_handler, get_current_user_handler,get_users_handler, create_user_handler, delete_user_handler,reset_password_handler
from user import submit_question_handler
from model import read_faiss_index, ask_handler
from baseknowledge import upload_file_handler, delete_file_handler, list_uploaded_files_handler, get_qa_data
import os
import io

from db import get_db_connection

load_dotenv()
# === SETUP ===
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
CORS(app, origins=["https://pmb-productions.vercel.app", "http://localhost:5173"], expose_headers=["Content-Disposition"])

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'data')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# === Load FAISS saat startup ===
read_faiss_index()


# === USER ===
@app.route("/ask", methods=["POST"])
def ask_route():
    result = ask_handler()
    return jsonify(result)

# === BASE KNOWLEDGE ===
@app.route('/upload', methods=['POST'])
def upload_file():
    return upload_file_handler()

@app.route('/uploaded-files', methods=['GET'])
def list_uploaded_files():
    result = list_uploaded_files_handler()
    return jsonify(result)

@app.route('/delete-file/<filename>', methods=['DELETE'])
def delete_file(filename):
    result = delete_file_handler(filename)
    return jsonify(result)

@app.route('/qa-data', methods=['GET'])
def qa_data():
    result = get_qa_data()
    return jsonify(result)



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


# === FAQ ===
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


# === Riwayat Pertanyaan User ===
@app.route('/history', methods=['GET'])
def list_questions():
    result = get_all_questions()
    return jsonify(result)


@app.route("/export-history-excel", methods=["GET"])
def export_history_excel():
    category = request.args.get("category")
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if category and category.lower() != "semua":
        cursor.execute("""
            SELECT id, question, answer, category 
            FROM history 
            WHERE category = %s 
            ORDER BY id
        """, (category,))
    else:
        cursor.execute("SELECT id, question, answer, category FROM history ORDER BY id")
    
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return {"message": "Tidak ada data untuk diekspor."}, 404

    df = pd.DataFrame(rows)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="ChatHistory")
    output.seek(0)

    file_safe_category = (category or 'semua').strip().lower().replace(" ", "_")
    filename = f"chat_history_{file_safe_category}.xlsx"

    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )



# === Dashboard ===
@app.route("/dashboard-stats", methods=["GET"])
def dashboard_stats():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Total pertanyaan hari ini
    cursor.execute("""
    SELECT COUNT(*) AS total
    FROM history
    """)
    total_questions = cursor.fetchone()['total'] or 0

    # 2. Jumlah file base knowledge
    cursor.execute("SELECT COUNT(*) AS total FROM uploaded_files")
    total_files_uploaded = cursor.fetchone()['total'] or 0

    # 3. Jumlah QA yang terindeks ke FAISS (dari MySQL)
    cursor.execute("SELECT COUNT(*) AS total FROM qa_data")
    total_qa_indexed = cursor.fetchone()['total'] or 0

    # 4. Grafik: jumlah pertanyaan per hari (7 hari terakhir)
    cursor.execute("""
        SELECT DATE_FORMAT(created_at, '%Y-%m-%d') AS tanggal, COUNT(*) AS jumlah
        FROM history
        WHERE created_at >= CURDATE() - INTERVAL 7 DAY
        GROUP BY DATE_FORMAT(created_at, '%Y-%m-%d')
        ORDER BY tanggal ASC
    """)
    questions_per_day = cursor.fetchall()

    # 5. Grafik: kategori pertanyaan terbanyak
    cursor.execute("""
        SELECT category, COUNT(*) AS value
        FROM history
        WHERE category IS NOT NULL
        GROUP BY category
        ORDER BY value DESC
        LIMIT 5
    """)
    top_categories = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({
        "total_questions_today": total_questions,
        "total_files_uploaded": total_files_uploaded,
        "total_qa_indexed": total_qa_indexed,
        "questions_per_day": questions_per_day,
        "top_categories": top_categories
    })



# === MAIN ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
