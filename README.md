# 🔐 Secure To-Do REST API

A production-oriented **FastAPI REST API** demonstrating authentication, authorization, validation, database persistence, automated testing and rate limiting.

## Features
- JWT access and refresh tokens.
- bcrypt password hashing.
- Registration, login, refresh and logout.
- Authenticated To-Do CRUD.
- Pagination, search, filtering and sorting.
- Pydantic validation.
- SlowAPI rate limiting.
- SQLAlchemy ORM with SQLite.
- Cascade cleanup of user-owned records.
- Automated integration tests.

## Architecture
```
Client
  ↓
FastAPI
  ↓
Authentication / Validation / Rate Limiting
  ↓
API Routers
  ↓
SQLAlchemy ORM
  ↓
SQLite
```

## Tech Stack
Python • FastAPI • SQLAlchemy • Pydantic • JWT • bcrypt • SQLite • Pytest

## Run locally
```bash
python3 -m pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload
```

API documentation:
```
http://localhost:8000/docs
```

Run tests:
```bash
python3 -m pytest
```

## Live API
[Open deployed API](https://to-do-list-api-tau.vercel.app/)

## What this demonstrates
Backend API design • Authentication • Authorization • Database design • Automated testing • Secure application practices

**Author:** Purushotham Balamurali