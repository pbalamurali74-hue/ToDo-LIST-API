# 📝 Secure To-Do List RESTful API (Python FastAPI)

[![Live Demo](https://img.shields.io/badge/Demo-Vercel%20Live-brightgreen?style=for-the-badge&logo=vercel)](https://to-do-list-api-tau.vercel.app)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)

A production-grade, rate-limited, and secure RESTful service built with Python **FastAPI**, **SQLAlchemy ORM**, **Pydantic validation**, and **SQLite**. Features enterprise-grade dual JWT authentication, automated rate-limiting, and serverless deployment on Vercel.

---

## 🌐 Live Deployment & Interactive Docs

- 🖥️ **Live API Base URL:** [https://to-do-list-api-tau.vercel.app](https://to-do-list-api-tau.vercel.app)
- 📖 **Interactive Swagger UI:** [https://to-do-list-api-tau.vercel.app/docs](https://to-do-list-api-tau.vercel.app/docs)
- 📑 **ReDoc Documentation:** [https://to-do-list-api-tau.vercel.app/redoc](https://to-do-list-api-tau.vercel.app/redoc)

---

## 🔒 Key Security & Architectural Features

1. **Dual JWT Token Authentication:**
   - **Access Tokens:** Short-lived 15-minute access tokens for authenticated API requests.
   - **Refresh Tokens:** Long-lived 7-day database-backed refresh tokens enabling secure session renewal and single-click revocation (`/logout`).
2. **Password Security:** Salted and hashed passwords implemented using `bcrypt` via Passlib.
3. **Pydantic Request Validation:** Strict schema validation on all request bodies, producing structured `400 Bad Request` responses on invalid inputs.
4. **Isolated User Access Controls:** Users can only view, modify, and delete their own to-do tasks (`401 Unauthorized` and `403 Forbidden` guards).
5. **Advanced Search & Pagination:** Supports limit/offset pagination (`page`, `limit`), case-insensitive title/description keyword searching, status filtering (`completed`), and flexible sorting (`asc` / `desc`).
6. **DDoS Protection & Rate Limiting:** Powered by `slowapi` (configured at 15 attempts/15 mins on auth endpoints, 100/15 mins globally).
7. **Database Cascading Deletion:** When a user is deleted, all corresponding tasks and active refresh sessions are automatically cascaded and pruned.

---

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **ORM & Database:** SQLAlchemy, SQLite
- **Validation & Settings:** Pydantic, Pydantic-Settings
- **Security:** PyJWT, Passlib (Bcrypt)
- **Rate Limiting:** slowapi
- **Testing & Deployment:** Pytest, Vercel Serverless (`vercel.json`)

---

## 📁 Repository Structure

```
├── app/
│   ├── config.py             # Typed configuration loader (Pydantic Settings)
│   ├── database.py           # SQLite connection & SessionLocal factory
│   ├── main.py               # FastAPI entrypoint, middleware, routers, & exception overrides
│   ├── middleware.py         # SlowAPI Limiter instantiation & rate handlers
│   ├── models.py             # Declarative SQLAlchemy models (User, Todo, RefreshToken)
│   ├── schemas.py            # Input validation & output formatting (Pydantic schemas)
│   ├── security.py           # Hashing and JWT sign/verify utilities
│   └── routers/
│       ├── auth.py           # Authentication endpoints (/register, /login, /refresh, /logout)
│       └── todos.py          # To-do CRUD endpoints (/todos/)
├── tests/
│   ├── conftest.py           # Pytest fixtures & isolated in-memory test DB configuration
│   ├── test_auth.py          # Auth endpoint integration tests
│   └── test_todos.py         # To-do CRUD integration tests
├── requirements.txt          # Python package dependencies
├── vercel.json               # Serverless Vercel configuration
├── verify.sh                 # End-to-end curl verification script
└── README.md                 # Project documentation
```

---

## 🚀 Running Locally

### 1. Prerequisites
Ensure you have **Python 3.9+** and `pip` installed.

### 2. Clone & Install Dependencies
```bash
git clone https://github.com/pbalamurali74-hue/ToDo-LIST-API.git
cd ToDo-LIST-API
python3 -m pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory (or use the preconfigured defaults):
```env
PORT=8000
DATABASE_URL="sqlite:///./todo.db"
JWT_ACCESS_SECRET="super-secret-access-token-key-change-this-in-production"
JWT_REFRESH_SECRET="super-secret-refresh-token-key-change-this-in-production"
APP_ENV="development"
```

### 4. Start Development Server
```bash
python3 -m uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`. Navigate to `http://localhost:8000/docs` to test endpoints via Swagger UI.

---

## 🧪 Running Automated Tests

Run the complete test suite with `pytest`:
```bash
python3 -m pytest
```
*The test suite uses an in-memory SQLite database (`sqlite:///:memory:`) that resets between test cases, keeping your local data clean.*

---

## 📝 API Endpoint Reference

| Endpoint | Method | Authentication | Request Body / Parameters | Description |
|---|---|---|---|---|
| `/register` | `POST` | None | `{ name, email, password }` | Register new user; returns access & refresh tokens. |
| `/login` | `POST` | None | `{ email, password }` | Authenticate credentials; returns access & refresh tokens. |
| `/refresh` | `POST` | None | `{ refreshToken }` | Validates refresh session; returns new access token. |
| `/logout` | `POST` | None | `{ refreshToken }` | Revokes refresh token in database. |
| `/todos/` | `POST` | Bearer Token | `{ title, description }` | Creates a new task. |
| `/todos/` | `GET` | Bearer Token | Query: `page`, `limit`, `completed`, `search`, `sort_by`, `sort_order` | Returns paginated, filtered tasks for user. |
| `/todos/{id}` | `PUT` | Bearer Token | `{ title, description, completed }` | Modifies a task (owner-only guard). |
| `/todos/{id}` | `DELETE` | Bearer Token | None | Deletes a task (owner-only guard). |

---

## 👤 Author

**Purushotham Balamurali**  
- **GitHub:** [@pbalamurali74-hue](https://github.com/pbalamurali74-hue)  
- **LinkedIn:** [purushothambalamurali](https://www.linkedin.com/in/purushothambalamurali/)  
- **Portfolio:** [Purushotham Balamurali Portfolio](https://github.com/pbalamurali74-hue)
