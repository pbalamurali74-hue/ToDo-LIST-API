# 🔐 Secure To-Do REST API

A production-oriented **REST API built with Python and FastAPI**, focused on authentication, authorization, database persistence, validation, testing and API security.

## 🚀 What it does

This project provides a secure backend for managing user accounts and personal To-Do tasks.

### Core features

- JWT access and refresh-token authentication
- Password hashing with bcrypt
- User registration, login, refresh and logout
- Authenticated To-Do CRUD operations
- Search, filtering, pagination and sorting
- Task ownership and authorization checks
- API rate limiting with SlowAPI
- SQLAlchemy ORM + SQLite
- Cascade deletion for user-owned data
- Automated API integration tests
- Automatic Swagger/OpenAPI documentation

## 🏗️ Architecture

```
Client
  ↓
FastAPI
  ↓
Authentication + Validation + Rate Limiting
  ↓
API Routers
  ↓
SQLAlchemy ORM
  ↓
SQLite
```

## 🧰 Tech Stack

**Python • FastAPI • SQLAlchemy • Pydantic • JWT • bcrypt • SQLite • SlowAPI • Uvicorn • Pytest**

## 📁 Project Structure

```
ToDo-LIST-API/
├── app/
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── middleware.py
│   └── routers/
│       ├── auth.py
│       └── todos.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_todos.py
├── requirements.txt
├── verify.sh
└── README.md
```

## ⚙️ Run locally

```bash
git clone https://github.com/pbalamurali74-hue/ToDo-LIST-API.git
cd ToDo-LIST-API
python3 -m pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload
```

Swagger API documentation:

```
http://localhost:8000/docs
```

## 🔐 Environment variables

Create a `.env` file:

```env
PORT=8000
DATABASE_URL=sqlite:///./todo.db
JWT_ACCESS_SECRET=change-this-secret
JWT_REFRESH_SECRET=change-this-refresh-secret
APP_ENV=development
```

Use your own production secrets and never commit real credentials.

## 🧪 Testing

```bash
python3 -m pytest
```

Manual verification:

```bash
./verify.sh
```

## 📡 API

| Endpoint | Method | Authentication | Purpose |
|---|---|---|---|
| `/register` | POST | None | Create user |
| `/login` | POST | None | Authenticate user |
| `/refresh` | POST | None | Refresh access token |
| `/logout` | POST | None | Revoke refresh session |
| `/todos/` | POST | Bearer | Create task |
| `/todos/` | GET | Bearer | List/search/filter tasks |
| `/todos/{id}` | PUT | Bearer | Update task |
| `/todos/{id}` | DELETE | Bearer | Delete task |

## 🛡️ Security

The project demonstrates:

- Password hashing
- JWT authentication
- Refresh-token session management
- Authorization based on task ownership
- Input validation
- Rate limiting
- Environment-based secret configuration

## 💼 Skills demonstrated

**Backend Development • REST API Design • Authentication • Authorization • Database Design • API Security • Automated Testing • Python**

Relevant for **Python Developer, Backend Developer and Software Engineer** internship/fresher roles.

## 👨‍💻 Author

**Purushotham Balamurali**

[GitHub](https://github.com/pbalamurali74-hue) • [LinkedIn](https://www.linkedin.com/in/purushothambalamurali/)