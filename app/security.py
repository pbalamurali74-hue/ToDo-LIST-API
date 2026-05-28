from datetime import datetime, timedelta
import uuid
import bcrypt
import jwt
from app.config import settings

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False


def create_access_token(user_id: str) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": user_id,
        "exp": now + timedelta(minutes=15),
        "iat": now,
    }
    return jwt.encode(payload, settings.JWT_ACCESS_SECRET, algorithm=ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": user_id,
        "jti": str(uuid.uuid4()),
        "exp": now + timedelta(days=7),
        "iat": now,
    }
    return jwt.encode(payload, settings.JWT_REFRESH_SECRET, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str:
    payload = jwt.decode(token, settings.JWT_ACCESS_SECRET, algorithms=[ALGORITHM])
    return payload["sub"]


def decode_refresh_token(token: str) -> str:
    payload = jwt.decode(token, settings.JWT_REFRESH_SECRET, algorithms=[ALGORITHM])
    return payload["sub"]
