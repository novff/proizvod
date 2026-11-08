from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.entities import User, AuditLog
from app.schemas.auth import RegisterIn, LoginIn, TokenOut, UserOut
from app.core.security import hash_password, verify_password, create_access_token
from app.api.deps import get_current_user
router = APIRouter(prefix="/api/auth", tags=["Авторизация"])
@router.post("/register", response_model=UserOut, status_code=201)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=data.email.lower()).first(): raise HTTPException(409, "Email уже зарегистрирован")
    user=User(email=data.email.lower(), full_name=data.full_name, password_hash=hash_password(data.password), role="operator")
    db.add(user); db.commit(); db.refresh(user)
    db.add(AuditLog(user_id=user.id, action="register", entity="user", entity_id=user.id)); db.commit()
    return user
@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, db: Session = Depends(get_db)):
    user=db.query(User).filter_by(email=data.email.lower()).first()
    if not user or not user.is_active or not verify_password(data.password, user.password_hash): raise HTTPException(401, "Неверный email или пароль")
    return {"access_token": create_access_token(str(user.id), user.role)}
@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)): return user
