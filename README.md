# Dynamic Syllabus Management for Higher Studies

**SANTHIRAM ENGINEERING COLLEGE (AUTONOMOUS) : NANDYAL**  
*Approved by AICTE: New Delhi | Permanently Affiliated to JNTUA, Ananthapuramu*  
*Accredited by NAAC (Grade-A), Accredited by NBA (Dept. of CSE & ECE)*  
**DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING**

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
├── run.bat                          # 1-Click launcher (starts backend & opens browser)
├── push_to_github.bat               # 1-Click helper to push project to GitHub
├── README.md                        # Project documentation
│
├── backend/                         # === BACKEND FOLDER ===
│   ├── app.py                       # Main Flask Server & REST APIs
│   ├── database.py                  # SQLite Schema & Data Auto-Indexer
│   ├── syllabus.db                  # Pre-populated Database (Users, Notes, Circulars)
│   ├── requirements.txt             # Python Dependencies
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
    ├── materials/                   # 211+ actual PDF, DOCX, and PPTX study notes
    ├── images/                      # Campus, student, and UI graphics
    ├── css/                         # styles.css & style.css
    └── js/                          # Frontend client scripts
```

---

## 🚀 How to Run the Project

### Method 1: One-Click Startup (Recommended)
Double-click **`run.bat`** in the main project folder.  
It automatically boots the Flask backend in `backend/`, connects the `frontend/`, and opens your default browser at `http://localhost:5000`.

### Method 2: Running from Terminal
```powershell
cd backend
python app.py
```
Then visit: `http://localhost:5000`

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

## 📤 How to Push to GitHub

A Git repository has already been initialized and committed with the complete Frontend and Backend implementation!

To push to your GitHub account:
1. Create a new repository on [GitHub](https://github.com/new) (e.g., `Dynamic-Syllabus-Management-System`).
2. Double-click **`push_to_github.bat`** and paste your GitHub repository URL, **OR** run these commands inside the `Dynamic_Syllabus_Management_System` folder:
   ```powershell
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git branch -M main
   git push -u origin main
   ```

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
