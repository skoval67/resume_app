from fastapi import APIRouter, Response, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas import UserCreate, Token
import crud
from auth import get_password_hash, verify_password, create_access_token
from database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    password_hash = get_password_hash(user.password)
    new_user = crud.create_user(db, email=user.email, password_hash=password_hash)
    token = create_access_token({"sub": str(new_user.id)})
    return Token(access_token=token)

@router.post("/token")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    # Устанавливаем токен в cookie
    response.set_cookie(
        key="access_token",
        value=create_access_token({"sub": str(user.id)}),
        httponly=False,
        secure=False,         # только HTTPS
        samesite="lax",       # нужно для работы с фронтом на другом домене
        max_age=60*60         # срок действия cookie
    )

    return {"message": "Login successful"}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}
