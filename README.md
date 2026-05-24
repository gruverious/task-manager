# Task Manager API

A full-stack Task Manager application built with FastAPI, PostgreSQL, and vanilla JavaScript.

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, PostgreSQL
- **Auth:** JWT Authentication, bcrypt password hashing
- **Frontend:** HTML, CSS, JavaScript (Fetch API)

## Features

- User Registration and Login
- JWT Authentication
- Create, View, Update, Delete Tasks
- Users can only access their own tasks

## Project Structure

```bash
task-manager/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── database.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── register.html
│   ├── dashboard.html
│   ├── style.css
│   └── app.js
└── README.md
```

## Local Setup

### 1. Clone the repository
git clone https://github.com/yourusername/task-manager.git
cd task-manager

### 2. Create virtual environment
python -m venv venv
source venv/Scripts/activate

### 3. Install dependencies
cd backend
pip install -r requirements.txt

### 4. Setup PostgreSQL
CREATE DATABASE taskmanager;

### 5. Create .env file
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/taskmanager
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

### 6. Run the backend
uvicorn main:app --reload

### 7. Open frontend
Open frontend/index.html with Live Server in VS Code

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /register | Register new user |
| POST | /login | Login and get JWT token |
| POST | /tasks | Create a task |
| GET | /tasks | Get all tasks |
| GET | /tasks/{id} | Get single task |
| PUT | /tasks/{id} | Update task |
| DELETE | /tasks/{id} | Delete task |

## Deployment

This app is deployed on Render.
- Backend API: https://your-app.onrender.com
- API Docs: https://your-app.onrender.com/docs

## Author

Sivaraj - Python Developer Internship Assessment