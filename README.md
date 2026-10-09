# Dynamic Syllabus Management for Higher Studies

**SANTHIRAM ENGINEERING COLLEGE (AUTONOMOUS) : NANDYAL**  
*Approved by AICTE: New Delhi | Permanently Affiliated to JNTUA, Ananthapuramu*  
*Accredited by NAAC (Grade-A), Accredited by NBA (Dept. of CSE & ECE)*  
**DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING**

---

## 🌐 Live Implementation & Project Links

| Resource | Direct Link |
| :--- | :--- |
| 🚀 **Live Interactive Login Page** | **[Open Live Login Portal](https://raw.githack.com/Harika3560123/Dynamic-Syllabus-Management-System/main/frontend/index.html)** |
| 📊 **Live Student Dashboard (`Main.html`)** | **[Open Live Dashboard](https://raw.githack.com/Harika3560123/Dynamic-Syllabus-Management-System/main/frontend/Main.html)** |
| 🛡️ **Live Faculty & Admin Portal (`admin.html`)** | **[Open Faculty Portal](https://raw.githack.com/Harika3560123/Dynamic-Syllabus-Management-System/main/frontend/admin.html)** |
| 💻 **Frontend Source Code Folder** | **[View `frontend/` on GitHub](https://github.com/Harika3560123/Dynamic-Syllabus-Management-System/tree/main/frontend)** |
| ⚙️ **Backend Source Code Folder** | **[View `backend/` on GitHub](https://github.com/Harika3560123/Dynamic-Syllabus-Management-System/tree/main/backend)** |
| 🗄️ **Flask REST API Server (`app.py`)** | **[View `backend/app.py`](https://github.com/Harika3560123/Dynamic-Syllabus-Management-System/blob/main/backend/app.py)** |
| 🗃️ **SQLite Database Module (`database.py`)** | **[View `backend/database.py`](https://github.com/Harika3560123/Dynamic-Syllabus-Management-System/blob/main/backend/database.py)** |

---

## 👥 Project Team & Mentors

### Student Developers:
| Reg. No | Student Name | Role | Email |
| :--- | :--- | :--- | :--- |
| **23X51A0532** | **B. HARIKA** | Project Lead / Full Stack | `23x51a0532@srecnandyal.edu.in` |
| **23X51A0530** | **B. KAVYA** | Full Stack Developer | `23x51a0530@srecnandyal.edu.in` |
| **23X51A0518** | **B. RAJAKUMARI** | Database & UI Design | `23x51a0518@srecnandyal.edu.in` |
| **23X51A0520** | **B. MANISHA** | Material Indexing & Testing | `23x51ao520@srecnandyal.edu.in` |

### Faculty Mentors:
* **Project Guide:** Mr. M. Amareswara Kumar, M.Tech (Assistant Professor, Dept. of CSE)
* **Project Coordinator:** Ms. S. Nazia Banu, M.Sc, M.Tech (Associate Professor, Dept. of CSE)
* **Head of Department (HOD):** Dr. Farooq Sunar Mahammad, M.Tech, Ph.D (Professor & HOD, Dept. of CSE)

---

## 📁 Project Architecture & Folder Breakdown

The project is cleanly separated into **Frontend** and **Backend** folders:

```
Dynamic_Syllabus_Management_System/
│
├── app.py                           # Root WSGI entrypoint for Cloud / Render deployment
├── requirements.txt                 # Python dependencies (Flask, Flask-CORS, PyJWT, gunicorn)
├── Procfile                         # Cloud process configuration
├── render.yaml                      # Render cloud deployment blueprint
├── run.bat                          # 1-Click launcher (starts backend on port 8000 & opens browser)
├── README.md                        # Project documentation
│
├── backend/                         # === BACKEND FOLDER ===
│   ├── app.py                       # Main Flask Server & REST APIs (Port 8000)
│   ├── database.py                  # SQLite Schema & Data Auto-Indexer
│   ├── syllabus.db                  # Pre-populated Database (Users, Notes, Circulars)
│   ├── requirements.txt             # Backend Python Dependencies
│   └── run_backend.bat              # Backend launcher script
│
└── frontend/                        # === FRONTEND FOLDER ===
    ├── index.html                   # Student & Faculty Login / Self-Registration
    ├── Main.html                    # Student Dashboard with Live Search & Updates
    ├── admin.html                   # Faculty & Admin Management Portal
    ├── about.html                   # About SREC, Vision & Mission
    ├── regulation.html              # Autonomous Regulations (R20, R21, R23)
    │
    ├── Sem-1.html ... Sem-7.html    # UG Semester-wise study material pages
    ├── sem--1.html ... sem--4.html  # PG Semester-wise study material pages
    ├── sem---3.html, sem---4.html   # R23 Semester study material pages
    ├── open_in_browser.bat          # Direct offline browser preview launcher
    │
    ├── materials/                   # Study notes (.pdf, .docx, .pptx)
    ├── images/                      # Campus, student, and UI graphics
    ├── css/                         # styles.css & style.css
    └── js/                          # Frontend client scripts
```

---

## 🚀 How to Run the Project Locally

### Method 1: One-Click Startup (Recommended)
Double-click **`run.bat`** in the main project folder.  
It automatically boots the Flask backend in `backend/` on **Port 8000**, connects the `frontend/`, and opens your default browser at `http://localhost:8000`.

### Method 2: Running from Terminal
```powershell
cd backend
python app.py
```
Then visit: `http://localhost:8000`

---

## 🔑 Login Credentials

The SQLite database comes pre-seeded with team members and an administrator account:

| Account | Email | Password | Role |
| :--- | :--- | :--- | :--- |
| **B. Harika** | `23x51a0532@srecnandyal.edu.in` | `srec@1234` | Student Lead |
| **B. Kavya** | `23x51a0530@srecnandyal.edu.in` | `srec@1234` | Student |
| **B. Rajakumari** | `23x51a0518@srecnandyal.edu.in` | `srec@1234` | Student |
| **B. Manisha** | `23x51ao520@srecnandyal.edu.in` | `srec@1234` | Student |
| **Faculty / Admin** | `admin@srecnandyal.edu.in` | `admin123` | Admin / HOD |

---

## 🌐 Backend REST API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/auth/login` | Student & Faculty Authentication |
| `POST` | `/api/auth/register` | Register new student |
| `POST` | `/api/auth/logout` | Terminate session |
| `GET` | `/api/auth/me` | Fetch active user session |
| `GET` | `/api/materials` | Search & filter study materials (supports `?q=...`) |
| `POST` | `/api/materials/upload` | Dynamically upload new PDF/DOCX notes |
| `DELETE` | `/api/materials/<id>` | Delete outdated notes |
| `GET` | `/api/updates` | Fetch latest syllabus circulars |
| `POST` | `/api/updates` | Broadcast new circular (Faculty/Admin) |
| `POST` | `/api/contact` | Submit student queries / feedback |
| `GET` | `/api/admin/stats` | Dashboard statistics & analytics |
| `GET` | `/api/admin/messages` | View student contact messages |
| `GET` | `/api/admin/users` | List registered students |
