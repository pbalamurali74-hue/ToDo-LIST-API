from datetime import datetime, timedelta, timezone
import jwt
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, RefreshToken
from app.schemas import (
    UserRegister,
    UserLogin,
    TokenResponse,
    RefreshRequest,
    TokenRefreshResponse,
)
from app.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from app.middleware import limiter

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("15/minute")
async def register(request: Request, user_data: UserRegister, db: Session = Depends(get_db)):
    # Check if email is unique
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )

    # Hash password
    pwd_hash = hash_password(user_data.password)

    # Create user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=pwd_hash,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate tokens
    access_token = create_access_token(new_user.id)
    refresh_token = create_refresh_token(new_user.id)

    # Save refresh token to db
    expires_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=7)
    db_refresh_token = RefreshToken(
        token=refresh_token,
        user_id=new_user.id,
        expires_at=expires_at,
    )
    db.add(db_refresh_token)
    db.commit()

    return TokenResponse(token=access_token, refreshToken=refresh_token)


@router.post("/login", response_model=TokenResponse)
@limiter.limit("15/minute")
async def login(request: Request, credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Generate tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    # Save refresh token
    expires_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=7)
    db_refresh_token = RefreshToken(
        token=refresh_token,
        user_id=user.id,
        expires_at=expires_at,
    )
    db.add(db_refresh_token)
    db.commit()

    return TokenResponse(token=access_token, refreshToken=refresh_token)


@router.post("/refresh", response_model=TokenRefreshResponse)
async def refresh(refresh_data: RefreshRequest, db: Session = Depends(get_db)):
    try:
        user_id = decode_refresh_token(refresh_data.refreshToken)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    # Check if token exists in db and is not expired
    db_token = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == refresh_data.refreshToken)
        .first()
    )
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not recognized",
        )

    if db_token.expires_at < datetime.now(timezone.utc).replace(tzinfo=None):
        db.delete(db_token)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
        )

    # Generate new access token
    new_access_token = create_access_token(user_id)
    return TokenRefreshResponse(token=new_access_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(refresh_data: RefreshRequest, db: Session = Depends(get_db)):
    db_token = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == refresh_data.refreshToken)
        .first()
    )
    if db_token:
        db.delete(db_token)
        db.commit()
    return
