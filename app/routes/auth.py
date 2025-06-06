import os
from dotenv import load_dotenv
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, LoginRequest, LoginResponse
from app.services.auth_service import get_current_user, get_password_hash, authenticate_user, create_access_token
from app.config.database import get_db
from ..models.user import User, UserType

load_dotenv()

#ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verify if Username already registered
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Buscar o UserType correspondente ao user_type fornecido
    user_type = db.query(UserType).filter(UserType.name == user.user_type).first()
    if not user_type:
        raise HTTPException(status_code=400, detail=f"Invalid user type: {user.user_type}")

    # Create user
    db_user = User(
        username=user.username,
        name=user.name,
        email=user.email,
        document=user.document,
        phone_number=user.phone_number,
        password=get_password_hash(user.password),
        user_type_id=user.user_type
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Rota para login e obtenção de token
@router.post("/token", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    auth_result = authenticate_user(db, request.username, request.password)
    user = auth_result["user"]
    user_type = auth_result["type"]
    role = auth_result["role"]
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "type": user_type, "role": role}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "name": user.name,
        "email": user.email,
        "document": user.document,
        "phone_number": user.phone_number,
        "user_type": user_type,
        "role": role
    }

# Rota protegida de exemplo (obter dados do usuário atual)
@router.get("/users/me/", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user