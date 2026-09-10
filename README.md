# Flask Discussion Board

A lightweight, feature-rich web discussion forum built with **Python**, **Flask**, **SQLAlchemy**, and **SQLite**. Users can register, log in, create discussion threads, reply to existing threads, and edit or delete their own posts.

---

## Features

- **User Authentication**: Registration and login using hashed passwords (`werkzeug.security` / `Flask-Login`).
- **Discussion Threads**: Create, view, and read community discussion topics.
- **Replies**: Comment and participate in ongoing thread discussions.
- **Author Controls**: Thread and reply authors can edit or delete their own content with built-in permission checks.
- **ORM & Database**: Clean database mapping using SQLAlchemy with SQLite.

---

## Project Structure

```text
flask_discussion_board/
├── app.py              # Application factory and main entry point
├── routes.py           # Route handlers for auth, threads, and replies
├── models.py           # SQLAlchemy database models (User, Post, Reply)
├── templates/          # Jinja2 HTML templates
│   ├── base.html       # Global base layout
│   ├── index.html      # Home feed / thread list
│   ├── login.html      # Login page
│   ├── register.html   # Registration page
│   ├── create_post.html# New thread creation page
│   ├── thread.html     # Single thread view & reply form
│   ├── edit_post.html  # Thread editing form
│   └── edit_reply.html # Reply editing form
└── instance/
    └── app.db          # SQLite database file (generated)
```

---

## Quick Start

### 1. Prerequisites 
Ensure you have Python 3.10+ installed on your machine.

---

### 2. Set Up Virtual Environment
```bash
# Clone or navigate into the project folder
cd flask_discussion_board

# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run the Application

```bash
python app.py
```

Open your browser and navigate to `http://127.0.0.1:5000`.

---

## Database Initialization

If starting with a fresh environment, run Python interactive shell to initialize the SQLite database tables:

```python
from app import app
from models import db

with app.app_context():
    db.create_all()
```

### License

Distributed under the MIT License. See `LICENSE` for more information.