"""
Database Module for Dynamic Syllabus Management System
Santhiram Engineering College (SREC) - Autonomous, Nandyal
Department of Computer Science & Engineering
"""

import os
import sqlite3
import glob
from werkzeug.security import generate_password_hash, check_password_hash
from bs4 import BeautifulSoup

BACKEND_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BACKEND_DIR, 'syllabus.db')
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, '..'))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reg_no TEXT UNIQUE,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        branch TEXT DEFAULT 'CSE',
        role TEXT DEFAULT 'student',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 2. Departments Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        program_type TEXT DEFAULT 'UG'
    )
    ''')

    # 3. Regulations Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS regulations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        year INTEGER NOT NULL,
        status TEXT DEFAULT 'Active'
    )
    ''')

    # 4. Subjects Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT,
        name TEXT NOT NULL,
        department_code TEXT DEFAULT 'CSE',
        semester TEXT NOT NULL,
        regulation TEXT DEFAULT 'R20'
    )
    ''')

    # 5. Study Materials Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS materials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER,
        subject_name TEXT NOT NULL,
        unit_number INTEGER,
        unit_label TEXT,
        file_name TEXT NOT NULL,
        file_path TEXT NOT NULL,
        file_size INTEGER DEFAULT 0,
        file_type TEXT,
        semester TEXT NOT NULL,
        regulation TEXT DEFAULT 'R20',
        uploaded_by TEXT DEFAULT 'System',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (subject_id) REFERENCES subjects(id)
    )
    ''')

    # 6. Syllabus Updates / Announcements Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS syllabus_updates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        category TEXT DEFAULT 'Syllabus Revision',
        department TEXT DEFAULT 'All',
        semester TEXT DEFAULT 'All',
        posted_by TEXT DEFAULT 'HOD - Dr. Farooq Sunar Mahammad',
        date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 7. Contact / Student Feedback Messages Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contact_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        subject TEXT,
        message TEXT NOT NULL,
        status TEXT DEFAULT 'Pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()

    # Seed Default Data
    seed_users(cursor)
    seed_departments(cursor)
    seed_regulations(cursor)
    seed_syllabus_updates(cursor)
    index_existing_materials(cursor, conn)

    conn.commit()
    conn.close()
    print("Database initialized and verified successfully.")

def seed_users(cursor):
    default_users = [
        ("23X51A0532", "B. HARIKA", "23x51a0532@srecnandyal.edu.in", "srec@1234", "CSE", "student"),
        ("23X51A0530", "B. KAVYA", "23x51a0530@srecnandyal.edu.in", "srec@1234", "CSE", "student"),
        ("23X51A0518", "B. RAJAKUMARI", "23x51a0518@srecnandyal.edu.in", "srec@1234", "CSE", "student"),
        ("23X51A0520", "B. MANISHA", "23x51ao520@srecnandyal.edu.in", "srec@1234", "CSE", "student"),
        ("23X51A0520A", "B. MANISHA (Alt)", "23x51a0520@srecnandyal.edu.in", "srec@1234", "CSE", "student"),
        ("ADMIN01", "Dr. Farooq Sunar Mahammad (HOD/Admin)", "admin@srecnandyal.edu.in", "admin123", "CSE", "admin"),
        ("FAC01", "Mr. M. Amareswara Kumar (Project Guide)", "faculty@srecnandyal.edu.in", "faculty123", "CSE", "faculty")
    ]

    for reg_no, name, email, password, branch, role in default_users:
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if not cursor.fetchone():
            p_hash = generate_password_hash(password)
            cursor.execute('''
            INSERT INTO users (reg_no, name, email, password_hash, branch, role)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (reg_no, name, email, p_hash, branch, role))

def seed_departments(cursor):
    departments = [
        ("CSE", "Computer Science & Engineering", "UG"),
        ("AIML", "Artificial Intelligence & Machine Learning", "UG"),
        ("CSE_DS", "CSE - Data Structures & Data Science", "UG"),
        ("ECE", "Electronics & Communication Engineering", "UG"),
        ("EEE", "Electrical & Electronics Engineering", "UG"),
        ("CIVIL", "Civil Engineering", "UG"),
        ("CSE_DESIGN", "CSE - Design", "UG"),
        ("MBA", "Master of Business Administration", "PG"),
        ("MCA", "Master of Computer Applications", "PG"),
        ("MTECH", "Master of Technology (CSE/VLSI)", "PG")
    ]
    for code, name, ptype in departments:
        cursor.execute("SELECT id FROM departments WHERE code = ?", (code,))
        if not cursor.fetchone():
            cursor.execute('''
            INSERT INTO departments (code, name, program_type)
            VALUES (?, ?, ?)
            ''', (code, name, ptype))

def seed_regulations(cursor):
    regs = [
        ("R20", 2020, "Active"),
        ("R21", 2021, "Active"),
        ("R23", 2023, "Current/Latest")
    ]
    for code, yr, stat in regs:
        cursor.execute("SELECT id FROM regulations WHERE code = ?", (code,))
        if not cursor.fetchone():
            cursor.execute('''
            INSERT INTO regulations (code, year, status)
            VALUES (?, ?, ?)
            ''', (code, yr, stat))

def seed_syllabus_updates(cursor):
    cursor.execute("SELECT COUNT(*) FROM syllabus_updates")
    if cursor.fetchone()[0] == 0:
        updates = [
            ("R23 Curriculum Update for B.Tech CSE", 
             "Unit-4 AI & Machine Learning references updated according to JNTUA revised syllabus guidelines.",
             "Syllabus Revision", "CSE", "SEM-3", "Dr. Farooq Sunar Mahammad (HOD)"),
            ("Semester Mid-Term Study Materials Available", 
             "All units (1 to 5) for Database Management Systems (DBMS), Operating Systems (OS), and Software Engineering (SE) have been uploaded and verified.",
             "Study Material", "All", "SEM-3 & SEM-4", "Ms. S. Nazia Banu (Co-ordinator)"),
            ("Dynamic Syllabus Feedback Notice", 
             "Students can request topic revisions and reference books using the feedback contact form.",
             "Notification", "All", "All", "Mr. M. Amareswara Kumar (Guide)")
        ]
        for title, desc, cat, dept, sem, poster in updates:
            cursor.execute('''
            INSERT INTO syllabus_updates (title, description, category, department, semester, posted_by)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, desc, cat, dept, sem, poster))

def index_existing_materials(cursor, conn):
    cursor.execute("SELECT COUNT(*) FROM materials")
    if cursor.fetchone()[0] > 0:
        return

    materials_dir = os.path.join(FRONTEND_DIR, 'materials')
    html_files = glob.glob(os.path.join(FRONTEND_DIR, '*.html'))

    for hf in html_files:
        fname = os.path.basename(hf)
        if fname in ['index.html', 'Main.html', 'Main-harika.html', 'about.html', 'regulation.html', 'admin.html']:
            continue
        
        sem_name = fname.replace('.html', '').upper()
        reg = "R20"
        if "---" in fname:
            reg = "R23"
        elif "--" in fname:
            reg = "R21"

        with open(hf, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        h2s = soup.find_all('h2')
        for h2 in h2s:
            subject_name = h2.text.strip().replace('___', '').strip()
            if not subject_name:
                continue

            cursor.execute('''
            SELECT id FROM subjects WHERE name = ? AND semester = ? AND regulation = ?
            ''', (subject_name, sem_name, reg))
            sub_row = cursor.fetchone()
            if sub_row:
                subject_id = sub_row[0]
            else:
                cursor.execute('''
                INSERT INTO subjects (name, department_code, semester, regulation)
                VALUES (?, 'CSE', ?, ?)
                ''', (subject_name, sem_name, reg))
                subject_id = cursor.lastrowid

            div = h2.find_next_sibling('div', class_='contact-icon')
            if div:
                links = div.find_all('a')
                for a in links:
                    unit_label = a.text.strip()
                    href = a.get('href', '').strip()
                    if not href or href == '#' or href.startswith('Main.html'):
                        continue

                    unit_num = 0
                    if '1' in unit_label: unit_num = 1
                    elif '2' in unit_label: unit_num = 2
                    elif '3' in unit_label: unit_num = 3
                    elif '4' in unit_label: unit_num = 4
                    elif '5' in unit_label: unit_num = 5

                    file_path = os.path.join(materials_dir, href)
                    file_size = 0
                    if os.path.exists(file_path):
                        file_size = os.path.getsize(file_path)

                    ext = os.path.splitext(href)[1].lower().replace('.', '')

                    cursor.execute('''
                    INSERT INTO materials (subject_id, subject_name, unit_number, unit_label, file_name, file_path, file_size, file_type, semester, regulation, uploaded_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'System')
                    ''', (subject_id, subject_name, unit_num, unit_label, href, f'materials/{href}', file_size, ext, sem_name, reg))

    if os.path.exists(materials_dir):
        for f in os.listdir(materials_dir):
            if f.endswith(('.pdf', '.docx', '.pptx')):
                cursor.execute("SELECT id FROM materials WHERE file_name = ?", (f,))
                if not cursor.fetchone():
                    file_path = os.path.join(materials_dir, f)
                    file_size = os.path.getsize(file_path)
                    ext = os.path.splitext(f)[1].lower().replace('.', '')
                    cursor.execute('''
                    INSERT INTO materials (subject_id, subject_name, unit_number, unit_label, file_name, file_path, file_size, file_type, semester, regulation, uploaded_by)
                    VALUES (NULL, 'General Reference', 0, 'Document', ?, ?, ?, ?, 'General', 'R20', 'Faculty')
                    ''', (f, f'materials/{f}', file_size, ext))

if __name__ == '__main__':
    init_db()
