from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.schemas import UserIn, Token, UserProfile
from app.core.security import authenticate_user, create_access_token, get_current_user
from app.db.mongo import get_user_by_email, get_user_by_username, create_user
from app.utils.emailer import send_email
import uuid

router = APIRouter()

@router.post("/signup", status_code=201)
def signup(user: UserIn):
    if get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Generate unique username (e.g., short UUID)
    username = f"user-{uuid.uuid4().hex[:8]}"
    create_user(user.email, user.password, username)
    
    # Send the username to the user's email
    send_email(
        recipient=user.email,
        subject="Welcome to MultiLang RAG",
        body=f"Hi! Your username is: {username}. Please use this to log in."
    )

    return {"msg": "User created. Username has been sent to your email."}

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/user", response_model=UserProfile)
def get_user(username: str = Depends(get_current_user)):
    user = get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user