"""
Dynamic Syllabus Management for Higher Studies - Backend Server
Santhiram Engineering College: Nandyal (Autonomous)
Department of Computer Science & Engineering
"""

import os
import sys
import sqlite3
import datetime
from flask import Flask, request, jsonify, session, send_from_directory, redirect, url_for
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import jwt

# Directory paths
BACKEND_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, '..'))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')
MATERIALS_DIR = os.path.join(FRONTEND_DIR, 'materials')
IMAGES_DIR = os.path.join(FRONTEND_DIR, 'images')
CSS_DIR = os.path.join(FRONTEND_DIR, 'css')
JS_DIR = os.path.join(FRONTEND_DIR, 'js')

os.makedirs(MATERIALS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(CSS_DIR, exist_ok=True)
os.makedirs(JS_DIR, exist_ok=True)

sys.path.insert(0, BACKEND_DIR)
from database import get_db_connection, init_db, DB_PATH

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
app.secret_key = 'srec-dynamic-syllabus-secret-key-autonomous-2025'
CORS(app)

JWT_SECRET = 'srec-dynamic-syllabus-jwt-secret-key-autonomous-2025-secure-token'

# Auto-initialize database if not present
if not os.path.exists(DB_PATH):
    init_db()

# ----------------- Helper Functions -----------------
def generate_token(user_dict):
    payload = {
        'id': user_dict['id'],
        'email': user_dict['email'],
        'role': user_dict['role'],
        'name': user_dict['name'],
        'reg_no': user_dict['reg_no'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def get_current_user():
    if 'user_id' in session:
        conn = get_db_connection()
        user = conn.execute("SELECT id, reg_no, name, email, branch, role FROM users WHERE id = ?", (session['user_id'],)).fetchone()
        conn.close()
        if user:
            return dict(user)

    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            conn = get_db_connection()
            user = conn.execute("SELECT id, reg_no, name, email, branch, role FROM users WHERE id = ?", (payload['id'],)).fetchone()
            conn.close()
            if user:
                return dict(user)
        except Exception:
            return None
    return None

# ----------------- Static & Page Routes -----------------
@app.route('/')
def index_route():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/dashboard')
def dashboard_route():
    return send_from_directory(FRONTEND_DIR, 'Main.html')

@app.route('/admin')
def admin_route():
    return send_from_directory(FRONTEND_DIR, 'admin.html')

@app.route('/materials/<path:filename>')
def serve_material(filename):
    if os.path.exists(os.path.join(MATERIALS_DIR, filename)):
        as_attachment = request.args.get('download', 'false').lower() == 'true'
        return send_from_directory(MATERIALS_DIR, filename, as_attachment=as_attachment)
    if os.path.exists(os.path.join(FRONTEND_DIR, filename)):
        return send_from_directory(FRONTEND_DIR, filename)
    return jsonify({"error": "Study material not found"}), 404

@app.route('/images/<path:filename>')
def serve_image(filename):
    if os.path.exists(os.path.join(IMAGES_DIR, filename)):
        return send_from_directory(IMAGES_DIR, filename)
    return send_from_directory(FRONTEND_DIR, filename)

@app.route('/css/<path:filename>')
def serve_css(filename):
    if os.path.exists(os.path.join(CSS_DIR, filename)):
        return send_from_directory(CSS_DIR, filename)
    return send_from_directory(FRONTEND_DIR, filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    if os.path.exists(os.path.join(JS_DIR, filename)):
        return send_from_directory(JS_DIR, filename)
    return send_from_directory(FRONTEND_DIR, filename)

@app.route('/<path:filename>')
def serve_any_file(filename):
    target_frontend = os.path.join(FRONTEND_DIR, filename)
    if os.path.isfile(target_frontend):
        return send_from_directory(FRONTEND_DIR, filename)

    target_mat = os.path.join(MATERIALS_DIR, filename)
    if os.path.isfile(target_mat):
        as_attachment = request.args.get('download', 'false').lower() == 'true'
        return send_from_directory(MATERIALS_DIR, filename, as_attachment=as_attachment)

    target_img = os.path.join(IMAGES_DIR, filename)
    if os.path.isfile(target_img):
        return send_from_directory(IMAGES_DIR, filename)

    target_css = os.path.join(CSS_DIR, filename)
    if os.path.isfile(target_css):
        return send_from_directory(CSS_DIR, filename)

    target_js = os.path.join(JS_DIR, filename)
    if os.path.isfile(target_js):
        return send_from_directory(JS_DIR, filename)

    return jsonify({"error": f"File '{filename}' not found on server"}), 404

# ----------------- Authentication APIs -----------------
@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.get_json(silent=True) or request.form
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required"}), 400

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE LOWER(email) = ?", (email,)).fetchone()
    conn.close()

    if not user:
        return jsonify({"success": False, "message": "Invalid email or password"}), 401

    if not check_password_hash(user['password_hash'], password):
        return jsonify({"success": False, "message": "Invalid email or password"}), 401

    user_dict = {
        'id': user['id'],
        'reg_no': user['reg_no'],
        'name': user['name'],
        'email': user['email'],
        'branch': user['branch'],
        'role': user['role']
    }

    session['user_id'] = user['id']
    token = generate_token(user_dict)

    return jsonify({
        "success": True,
        "message": "Login successful! Welcome to SREC Syllabus Portal.",
        "user": user_dict,
        "token": token
    })

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    data = request.get_json(silent=True) or request.form
    name = data.get('name', '').strip()
    reg_no = data.get('reg_no', '').strip().upper()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()
    branch = data.get('branch', 'CSE').strip().upper()

    if not name or not email or not password:
        return jsonify({"success": False, "message": "Name, email, and password are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE LOWER(email) = ?", (email,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"success": False, "message": "A user with this email already exists"}), 409

    if reg_no:
        cursor.execute("SELECT id FROM users WHERE reg_no = ?", (reg_no,))
        if cursor.fetchone():
            conn.close()
            return jsonify({"success": False, "message": "A student with this Registration Number already exists"}), 409

    p_hash = generate_password_hash(password)
    cursor.execute('''
    INSERT INTO users (name, reg_no, email, password_hash, branch, role)
    VALUES (?, ?, ?, ?, ?, 'student')
    ''', (name, reg_no or f"TEMP-{int(datetime.datetime.utcnow().timestamp())}", email, p_hash, branch))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "success": True,
        "message": f"Student {name} registered successfully! You can now log in."
    })

@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully"})

@app.route('/api/auth/me', methods=['GET'])
def api_me():
    user = get_current_user()
    if not user:
        return jsonify({"authenticated": False}), 401
    return jsonify({"authenticated": True, "user": user})

# ----------------- Syllabus & Subject APIs -----------------
@app.route('/api/departments', methods=['GET'])
def api_departments():
    conn = get_db_connection()
    depts = conn.execute("SELECT * FROM departments ORDER BY id").fetchall()
    conn.close()
    return jsonify([dict(d) for d in depts])

@app.route('/api/regulations', methods=['GET'])
def api_regulations():
    conn = get_db_connection()
    regs = conn.execute("SELECT * FROM regulations ORDER BY year DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in regs])

@app.route('/api/subjects', methods=['GET'])
def api_subjects():
    semester = request.args.get('semester')
    regulation = request.args.get('regulation')
    dept = request.args.get('department')

    query = "SELECT * FROM subjects WHERE 1=1"
    params = []

    if semester:
        query += " AND UPPER(semester) = ?"
        params.append(semester.upper())
    if regulation:
        query += " AND UPPER(regulation) = ?"
        params.append(regulation.upper())
    if dept:
        query += " AND UPPER(department_code) = ?"
        params.append(dept.upper())

    query += " ORDER BY name ASC"
    conn = get_db_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

# ----------------- Study Materials APIs -----------------
@app.route('/api/materials', methods=['GET'])
def api_materials():
    q = request.args.get('q', '').strip().lower()
    semester = request.args.get('semester', '').strip().upper()
    regulation = request.args.get('regulation', '').strip().upper()
    subject_id = request.args.get('subject_id')
    unit = request.args.get('unit')

    query = "SELECT * FROM materials WHERE 1=1"
    params = []

    if q:
        query += " AND (LOWER(subject_name) LIKE ? OR LOWER(unit_label) LIKE ? OR LOWER(file_name) LIKE ?)"
        term = f"%{q}%"
        params.extend([term, term, term])

    if semester:
        query += " AND UPPER(semester) = ?"
        params.append(semester)

    if regulation:
        query += " AND UPPER(regulation) = ?"
        params.append(regulation)

    if subject_id:
        query += " AND subject_id = ?"
        params.append(subject_id)

    if unit:
        query += " AND unit_number = ?"
        params.append(unit)

    query += " ORDER BY id DESC"
    conn = get_db_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/materials/upload', methods=['POST'])
def api_upload_material():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "No file selected"}), 400

    subject_name = request.form.get('subject_name', '').strip()
    unit_number = int(request.form.get('unit_number', 1))
    unit_label = request.form.get('unit_label', f"UNIT-{unit_number}").strip()
    semester = request.form.get('semester', 'SEM-1').strip().upper()
    regulation = request.form.get('regulation', 'R23').strip().upper()
    uploaded_by = request.form.get('uploaded_by', 'Faculty')

    if not subject_name:
        return jsonify({"success": False, "message": "Subject name is required"}), 400

    filename = secure_filename(file.filename)
    if not filename:
        filename = f"upload_{int(datetime.datetime.utcnow().timestamp())}.pdf"

    save_path = os.path.join(MATERIALS_DIR, filename)
    file.save(save_path)
    file_size = os.path.getsize(save_path)
    file_type = os.path.splitext(filename)[1].lower().replace('.', '')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM subjects WHERE UPPER(name) = ? AND UPPER(semester) = ?", (subject_name.upper(), semester))
    sub_row = cursor.fetchone()
    if sub_row:
        subject_id = sub_row['id']
    else:
        cursor.execute("INSERT INTO subjects (name, semester, regulation) VALUES (?, ?, ?)", (subject_name, semester, regulation))
        subject_id = cursor.lastrowid

    cursor.execute('''
    INSERT INTO materials (subject_id, subject_name, unit_number, unit_label, file_name, file_path, file_size, file_type, semester, regulation, uploaded_by)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (subject_id, subject_name, unit_number, unit_label, filename, f'materials/{filename}', file_size, file_type, semester, regulation, uploaded_by))
    conn.commit()
    mat_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "success": True,
        "message": f"Successfully uploaded '{filename}' for {subject_name} ({unit_label})!",
        "material_id": mat_id
    })

@app.route('/api/materials/<int:mat_id>', methods=['DELETE'])
def api_delete_material(mat_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT file_name FROM materials WHERE id = ?", (mat_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return jsonify({"success": False, "message": "Material not found"}), 404

    cursor.execute("DELETE FROM materials WHERE id = ?", (mat_id,))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": f"Material ID {mat_id} deleted successfully"})

# ----------------- Dynamic Syllabus Updates APIs -----------------
@app.route('/api/updates', methods=['GET'])
def api_updates():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM syllabus_updates ORDER BY date_posted DESC LIMIT 10").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/updates', methods=['POST'])
def api_add_update():
    data = request.get_json(silent=True) or request.form
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    category = data.get('category', 'Syllabus Revision').strip()
    dept = data.get('department', 'All').strip()
    sem = data.get('semester', 'All').strip()
    posted_by = data.get('posted_by', 'HOD / Faculty').strip()

    if not title or not description:
        return jsonify({"success": False, "message": "Title and description are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO syllabus_updates (title, description, category, department, semester, posted_by)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, description, category, dept, sem, posted_by))
    conn.commit()
    update_id = cursor.lastrowid
    conn.close()

    return jsonify({"success": True, "message": "Syllabus update broadcasted successfully!", "id": update_id})

# ----------------- Contact & Student Feedback API -----------------
@app.route('/api/contact', methods=['POST'])
def api_contact():
    data = request.get_json(silent=True) or request.form
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    subject = data.get('subject', 'General Inquiry').strip()
    message = data.get('message', '').strip()

    if not name or not email or not message:
        return jsonify({"success": False, "message": "Name, email, and message are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO contact_messages (name, email, phone, subject, message)
    VALUES (?, ?, ?, ?, ?)
    ''', (name, email, phone, subject, message))
    conn.commit()
    msg_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "success": True,
        "message": "Thank you! Your feedback/inquiry has been received by Santhiram Engineering College faculty."
    })

# ----------------- Admin Statistics & Inquiries -----------------
@app.route('/api/admin/stats', methods=['GET'])
def api_admin_stats():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM materials")
    total_materials = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM subjects")
    total_subjects = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM contact_messages")
    total_messages = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM syllabus_updates")
    total_updates = c.fetchone()[0]

    c.execute("SELECT id, subject_name, unit_label, file_name, semester, regulation FROM materials ORDER BY id DESC LIMIT 5")
    recent_materials = [dict(r) for r in c.fetchall()]

    conn.close()
    return jsonify({
        "total_users": total_users,
        "total_materials": total_materials,
        "total_subjects": total_subjects,
        "total_messages": total_messages,
        "total_updates": total_updates,
        "recent_materials": recent_materials
    })

@app.route('/api/admin/messages', methods=['GET'])
def api_admin_messages():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM contact_messages ORDER BY created_at DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/admin/users', methods=['GET'])
def api_admin_users():
    conn = get_db_connection()
    rows = conn.execute("SELECT id, reg_no, name, email, branch, role, created_at FROM users ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"===============================================================")
    print(f"  SANTHIRAM ENGINEERING COLLEGE - NANDYAL (AUTONOMOUS)")
    print(f"  Dynamic Syllabus Management System Backend Server")
    print(f"  Frontend Path: {FRONTEND_DIR}")
    print(f"  Server URL:    http://localhost:{port}")
    print(f"===============================================================")
    app.run(host='0.0.0.0', port=port, debug=False)
