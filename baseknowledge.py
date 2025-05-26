import os
from flask import request
from db import get_db_connection
import jwt
from model import extract_text_from_file, create_faiss_index, read_faiss_index
from werkzeug.utils import secure_filename

SECRET_KEY = os.getenv("SECRET_KEY")
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'data')

def upload_file_handler():
    # === Validasi token JWT ===
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return {"message": "Unauthorized"}, 401

    token = auth_header.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {"message": "Token expired"}, 401
    except jwt.DecodeError:
        return {"message": "Invalid token"}, 401

    # === Validasi file ===
    if 'file' not in request.files:
        return {"message": "Tidak ada file yang dikirim."}, 400

    file = request.files['file']
    if file.filename == '':
        return {"message": "Nama file kosong."}, 400

    filename = secure_filename(file.filename)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id FROM uploaded_files WHERE filename = %s", (filename,))
    existing = cursor.fetchone()

    if existing:
        conn.close()
        return {"message": f"File '{filename}' sudah ada. Gunakan nama berbeda."}, 409
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        # Ekstrak QA dari file
        qa_pairs = extract_text_from_file(filepath)
        print("✅ Jumlah QA ditemukan:", len(qa_pairs))
        if not qa_pairs:
            return {"message": "File tidak mengandung QA valid."}, 400

        uploaded_by = payload["username"]

        # === Simpan metadata file ===
        cursor.execute("""
            INSERT INTO uploaded_files (filename, uploaded_by)
            VALUES (%s, %s)
        """, (filename, uploaded_by))

        # === Simpan QA pairs ke DB ===
        for qa in qa_pairs:
            cursor.execute("""
                INSERT INTO qa_data (question, answer, filename, created_by)
                VALUES (%s, %s, %s, %s)
            """, (qa["question"], qa["answer"], filename, uploaded_by))

        conn.commit()
        conn.close()

        # === Update FAISS Index ===
        create_faiss_index()
        read_faiss_index()

        return {"message": f"File {filename} berhasil diupload dan QA berhasil ditambahkan."}, 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"message": f"Gagal memproses file: {str(e)}"}, 500
    
def list_uploaded_files_handler():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT uf.filename, uf.uploaded_by, uf.uploaded_at,
               COUNT(q.id) AS total_qa
        FROM uploaded_files uf
        LEFT JOIN qa_data q ON uf.filename = q.filename
        GROUP BY uf.filename, uf.uploaded_by, uf.uploaded_at
        ORDER BY uf.uploaded_at DESC
    """)
    files = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"files": files}

def delete_file_handler(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Hapus dari DB
    cursor.execute("DELETE FROM uploaded_files WHERE filename = %s", (filename,))
    cursor.execute("DELETE FROM qa_data WHERE filename = %s", (filename,))
    conn.commit()
    cursor.close()
    conn.close()

    # Hapus file fisik
    if os.path.exists(file_path):
        os.remove(file_path)

    # Rebuild FAISS index dari data sisa
    create_faiss_index()

    return {"message": f"File {filename} dan seluruh QA terkait berhasil dihapus."}

def get_qa_data():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    offset = (page - 1) * limit

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM qa_data")
    total = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT id, question, answer, filename
        FROM qa_data
        ORDER BY id ASC
        LIMIT %s OFFSET %s
    """, (limit, offset))

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return {
        "qa": results,
        "total": total,
        "page": page,
        "limit": limit
    }