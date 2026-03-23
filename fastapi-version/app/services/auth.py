from sqlmodel import Session, select
from app.models import User
from app.schemas.auth import UserCreate
from app.core.auth import create_access_token

def register_user(session: Session, user_data: UserCreate):
    statement = select(User).where(User.username == user_data.username)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise ValueError("Username already exists")
    
    new_user = User(username=user_data.username)
    new_user.set_password(user_data.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user

def login(session: Session, username: str, password: str):
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()

    if not user or not user.verify_password(password):
        raise ValueError("Invalid username or password")
    
    access_token = create_access_token(username=user.username)
    return access_token